#!/usr/bin/env python3
"""Rebuild the offline corpus from pinned Git objects, never working-tree files.

Python 3.10+, Git. No network, upstream checkout changes, or third-party packages.
All sources are staged before replacing docs/. Existing docs/ must be unmodified.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.parse import quote

SKILL = Path(__file__).resolve().parents[1]
DOC_EXT = {".md", ".rst", ".adoc", ".asciidoc", ".dox", ".inc"}
CODE_EXT = {".h", ".hpp", ".hxx", ".cpp", ".cc", ".c", ".f90", ".py", ".cmake", ".sh", ".yaml", ".yml", ".in"}
SKIP_PARTS = {".git", "_build", "__pycache__", "node_modules", "third_party", "third-party", "dalapi"}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def under(path, roots):
    return any(path == root or path.startswith(root + "/") for root in roots)


def classify(path, source):
    p = PurePosixPath(path)
    if p.name in {"AGENTS.md", "CLAUDE.md"} or SKIP_PARTS.intersection(p.parts):
        return None
    notice = re.match(r"(?i)^(license|copying|notice|copyright|third.party)", p.name)
    selected_scope = under(path, source["docs"] + source["api"] + source["examples"])
    if (notice and (len(p.parts) == 1 or selected_scope)) or p.parts[0] in {"LICENSES", "licensing", ".reuse"}:
        return "license"
    if path in source["extra"]:
        return "license" if "LICENSE" in p.name else "doc"
    if source["project"] == "SYCLomatic" and path.startswith("docs/dev_guide/api-mapping-status/") and p.suffix == ".csv":
        return "doc"
    if under(path, source["api"]) and p.suffix in {".h", ".hpp", ".hxx", ".in"} and not {"backend", "detail", "test"}.intersection(p.parts):
        return "api"
    if under(path, source["examples"]) and (p.suffix in CODE_EXT | DOC_EXT or p.name in {"CMakeLists.txt", "Makefile"}):
        return "doc" if p.suffix in {".md", ".rst", ".adoc"} else "example"
    if under(path, source["docs"]):
        if p.suffix in DOC_EXT:
            return "doc"
        # RST literalinclude files, API specs and examples accompanying docs.
        if p.suffix in CODE_EXT:
            # Do not vendor all PTI tool implementation simply because its docs
            # live beside the code. Nor oneAPI-samples outside selected examples.
            if source["project"] in {"oneAPI-samples", "level-zero"} or (source["project"] == "pti-gpu" and path.startswith("tools/")):
                return None
            return "api" if p.suffix in {".yml", ".yaml", ".h", ".hpp"} else "support"
    return None


def title_of(data, fallback):
    lines = data.decode("utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines[:100]):
        s = line.strip()
        if s.startswith("# "):
            return re.sub(r"<[^>]+>", "", s[2:]).strip()[:160]
        if i + 1 < len(lines) and s and not s.startswith(".."):
            bar = lines[i + 1].strip()
            if len(bar) >= 3 and len(set(bar)) == 1 and bar[0] in "=-~^":
                return s[:160]
    return fallback


def verify_tree(docs):
    """Verify raw files plus generated metadata against the bundle inventory."""
    expected = json.loads((docs / "inventory.json").read_text())
    actual = {p.relative_to(docs).as_posix(): digest(p.read_bytes())
              for p in docs.rglob("*") if p.is_file() and p.name != "inventory.json"}
    if actual != expected:
        differences = sorted(k for k in expected.keys() | actual.keys() if expected.get(k) != actual.get(k))
        raise ValueError("Bundle differs from inventory: " + ", ".join(differences[:8]))
    catalog = json.loads((docs / "catalog.json").read_text())
    for entry in catalog:
        if actual.get(entry["path"]) != entry["sha256"]:
            raise ValueError("Catalog hash mismatch: " + entry["path"])
    return len(catalog)


def build(sources_root, destination, lock):
    catalog = []
    summary = []
    for source in lock["sources"]:
        name, rev = source["project"], source["commit"]
        root = sources_root / name
        if not re.fullmatch(r"[0-9a-f]{40}", rev):
            raise ValueError("Expected full commit SHA for " + name)
        tree = {}
        for record in git(root, "ls-tree", "-rz", rev).split(b"\0"):
            if record:
                metadata, path = record.split(b"\t", 1)
                mode, object_type, object_id = metadata.decode().split()
                tree[path.decode()] = (mode, object_type, object_id)
        selected = {p: classify(p, source) for p in tree if classify(p, source)}
        if not any(kind == "doc" for kind in selected.values()):
            raise ValueError("No documentation selected for " + name)
        if not any(kind == "license" for kind in selected.values()):
            raise ValueError("No license selected for " + name)
        paths = sorted(selected)
        for path in paths:
            if tree[path][0] not in {"100644", "100755"} or tree[path][1] != "blob":
                raise ValueError("Selected source is not a regular file: " + path)
        # Read raw blobs: git archive can apply export-subst/export-ignore, and
        # working-tree reads can apply filters or include uncommitted changes.
        request = "".join(tree[p][2] + "\n" for p in paths).encode()
        batch = subprocess.run(["git", "-C", str(root), "cat-file", "--batch"],
                               input=request, stdout=subprocess.PIPE, check=True).stdout
        stream = io.BytesIO(batch)
        for path in paths:
            relative = PurePosixPath(path)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("Unsafe upstream path: " + path)
            object_id, object_type, size = stream.readline().decode().split()
            if object_id != tree[path][2] or object_type != "blob":
                raise ValueError("Unexpected Git object for " + path)
            data = stream.read(int(size))
            if len(data) != int(size) or stream.read(1) != b"\n":
                raise ValueError("Truncated Git blob for " + path)
            output = Path("upstream") / name / path
            target = destination / output
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            catalog.append(dict(project=name, path=output.as_posix(), source_path=path,
                                title=title_of(data, relative.stem), kind=selected[path],
                                bytes=len(data), sha256=digest(data)))
        entries = [e for e in catalog if e["project"] == name]
        summary.append((source, entries))
        print(f"{name}: {len(entries)} files", flush=True)
    catalog.sort(key=lambda e: e["path"])
    (destination / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")
    (destination / "sources.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    toc = ["# Documentation index", "", "Pinned upstream source text; choose a project, then one or two pages. See [SOURCE.md](SOURCE.md) for scope and provenance.", "", "| Project | Files | Contents |", "|---|---:|---|"]
    provenance = ["# Documentation sources", "", "This bundle contains unmodified source files from the commits below. It is a selected documentation corpus, not a complete toolkit manual or an installed toolkit. Local working-tree edits are not copied. Sources are not asserted to be mutually release-compatible.", "", "## Coverage and limitations", "", "Includes the selected documentation trees, public API headers/schema where useful, and selected code samples. Markdown, reStructuredText, AsciiDoc and Doxygen source retain their original syntax and copyright notices. Generated API pages are not rendered: read the bundled headers/schema for signatures. Images, notebooks, build products, most implementation/test code and unrelated LLVM documentation are omitted. Some upstream cross-references therefore require upstream browsing; use the exact commit URL rather than guessing that a missing page exists locally. Experimental/proposed extension documents are not proof of shipped support.", "", "Unified Runtime is bundled from intel/llvm at the same commit as the SYCL docs; the standalone mirror is deliberately omitted. Intel's proprietary toolkit component manuals (including complete oneMKL, IPP, MPI, VTune, Advisor and Fortran compiler references) are not mirrored; see ../references/toolkit-and-openmp.md for official online routes. Khronos SYCL reference is explanatory; the linked SYCL specification governs normative language questions.", "", "## Attribution", "", "Each project's original license/notice files are included alongside its sources. Copyright remains with the upstream authors; no blanket license is assigned to this mixed-license corpus. SYCL reference document sources are CC-BY-4.0, code examples Apache-2.0; see its LICENSE.rst, COPYING.rst and LICENSES/. Files are copied without modification; the catalog, indexes and workflow guides are separately authored. Other projects' per-file notices and bundled license files govern their respective files.", "", "| Project | Commit | Commit date | Files |", "|---|---|---|---:|"]
    indexes = destination / "indexes"
    indexes.mkdir()
    for source, entries in summary:
        name = source["project"]
        toc.append(f"| {name} | {len(entries)} | [Page index](indexes/{name}.md) |")
        url = source["url"] + "/tree/" + source["commit"]
        provenance.append(f"| [{name}]({url}) | `{source['commit']}` | {source['commit_date']} | {len(entries)} |")
        lines = [f"# {name}", "", f"Upstream: {url}", "", "Paths preserve the upstream layout. API and example files can also be found with search_docs.py --kind all.", ""]
        for kind in ("doc", "api", "example", "license", "support"):
            group = [e for e in entries if e["kind"] == kind]
            if group:
                lines += [f"## {kind}", ""]
            for e in group:
                label = e["source_path"].replace("[", "\\[").replace("]", "\\]")
                lines.append(f"- [{label}](../{quote(e['path'], safe='/')})")
            if group:
                lines.append("")
        (indexes / (name + ".md")).write_text("\n".join(lines) + "\n")
    provenance += ["", "## Reproduce or update", "", "Selection rules and exact revisions are in scripts/sources.json (copied here as sources.lock.json). Run `python3 scripts/sync_docs.py --sources-root /path/to/checkouts` from the skill directory to reproduce. Every listed checkout must contain its pinned commit; the tool never fetches, switches branches or changes source checkouts. To update, deliberately edit the revisions in scripts/sources.json and review the resulting diff. No automatic tracking of moving branches.", "", "`catalog.json` records project, source path, file kind, byte count and SHA-256 per copied file. Source URL = project tree URL above plus its source path (replace /tree/ with /blob/). `inventory.json` additionally hashes generated indexes and metadata. Run `python3 scripts/sync_docs.py --verify` to check the delivered bundle. Hashes detect accidental drift, not adversarial tampering."]
    (destination / "TOC.md").write_text("\n".join(toc) + "\n")
    (destination / "SOURCE.md").write_text("\n".join(provenance) + "\n")
    inventory = {p.relative_to(destination).as_posix(): digest(p.read_bytes())
                 for p in sorted(destination.rglob("*")) if p.is_file()}
    (destination / "inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    verify_tree(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources-root", type=Path, help="Parent of named upstream Git checkouts; required for rebuild")
    parser.add_argument("--verify", action="store_true", help="Verify the existing bundle without Git checkouts")
    args = parser.parse_args()
    destination = SKILL / "docs"
    try:
        if args.verify:
            print(f"Verified {verify_tree(destination)} upstream files and generated metadata")
            return
        if args.sources_root is None:
            parser.error("--sources-root is required for a rebuild")
        if destination.exists():
            verify_tree(destination)  # Never silently overwrite edits.
        lock = json.loads((SKILL / "scripts/sources.json").read_text())
        with tempfile.TemporaryDirectory(prefix=".oneapi-docs-", dir=SKILL.parent) as temporary:
            staged = Path(temporary) / "docs"
            staged.mkdir()
            build(args.sources_root.resolve(), staged, lock)
            backup = Path(temporary) / "previous"
            if destination.exists():
                destination.rename(backup)
            try:
                staged.rename(destination)
            except BaseException:
                if backup.exists():
                    backup.rename(destination)
                raise
        print(f"Wrote {destination}")
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"sync failed: {exc}\n")


if __name__ == "__main__":
    main()
