"""Functional checks for corpus/search/probe behavior; no oneAPI installation needed."""
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/oneapi"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search = load("search_docs")
sync = load("sync_docs")
probe = load("probe")


class CorpusTests(unittest.TestCase):
    def test_sync_uses_committed_objects_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repo = base / "fixture"
            (repo / "docs").mkdir(parents=True)
            (repo / "docs/page.md").write_text("# Committed page\nOriginal text.\n$Format:%h$\n")
            (repo / ".gitattributes").write_text("docs/page.md export-subst\n")
            (repo / "LICENSE").write_text("Fixture license\n")
            (repo / "docs/third-party-programs.txt").write_text("Required nested notice\n")
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "-c", "user.name=Skill Test",
                            "-c", "user.email=skill-test@example.invalid", "-c", "commit.gpgsign=false",
                            "commit", "-qm", "test: seed documentation fixture"], check=True)
            revision = sync.git(repo, "rev-parse", "HEAD").decode().strip()
            lock = {"sources": [{"project": "fixture", "url": "https://example.invalid/fixture",
                                  "commit": revision, "commit_date": "fixture", "docs": ["docs"],
                                  "api": [], "examples": [], "extra": []}]}
            (repo / "docs/page.md").write_text("Dirty uncommitted text\n")
            (repo / "docs/untracked.md").write_text("Untracked\n")
            inventories = []
            for name in ("first", "second"):
                output = base / name
                output.mkdir()
                with contextlib.redirect_stdout(io.StringIO()):
                    sync.build(base, output, lock)
                inventories.append((output / "inventory.json").read_bytes())
                self.assertIn("Original text", (output / "upstream/fixture/docs/page.md").read_text())
                self.assertIn("$Format:%h$", (output / "upstream/fixture/docs/page.md").read_text())
                self.assertFalse((output / "upstream/fixture/docs/untracked.md").exists())
                self.assertEqual((output / "upstream/fixture/docs/third-party-programs.txt").read_text(), "Required nested notice\n")
            self.assertEqual(inventories[0], inventories[1])
            self.assertEqual((repo / "docs/page.md").read_text(), "Dirty uncommitted text\n")

    def test_inventory(self):
        self.assertGreater(sync.verify_tree(SKILL / "docs"), 1000)

    def test_integrity_detects_edits_and_added_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            content = b"original\n"
            (root / "page.md").write_bytes(content)
            catalog = [{"path": "page.md", "sha256": sync.digest(content)}]
            (root / "catalog.json").write_text(json.dumps(catalog))
            inventory = {p.name: sync.digest(p.read_bytes()) for p in root.iterdir()}
            (root / "inventory.json").write_text(json.dumps(inventory))
            self.assertEqual(sync.verify_tree(root), 1)
            (root / "page.md").write_text("edited")
            with self.assertRaisesRegex(ValueError, "Bundle differs"):
                sync.verify_tree(root)
            (root / "page.md").write_bytes(content)
            (root / "extra.md").write_text("not in manifest")
            with self.assertRaisesRegex(ValueError, "Bundle differs"):
                sync.verify_tree(root)

    def test_missing_source_does_not_replace_existing_bundle(self):
        before = (SKILL / "docs/inventory.json").read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run([sys.executable, str(SKILL / "scripts/sync_docs.py"),
                                     "--sources-root", temporary], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, (SKILL / "docs/inventory.json").read_bytes())
        sync.verify_tree(SKILL / "docs")


class SearchTests(unittest.TestCase):
    def test_realistic_retrieval(self):
        cases = [
            ("ONEAPI_DEVICE_SELECTOR", "llvm", "EnvironmentVariables.md", "doc"),
            ("SYCL_UR_TRACE", "llvm", "EnvironmentVariables.md", "doc"),
            ("in_order", "SYCL-Reference", "queue.rst", "doc"),
            ("malloc_shared", "SYCL-Reference", "usm_allocations.rst", "doc"),
            ("column_major gemm", "oneMath", "gemm.rst", "doc"),
            ("ONEMATH::onemath", "oneMath", "using_onemath_with_cmake.rst", "doc"),
            ("ONEDNN_VERBOSE", "oneDNN", "verbose.md", "doc"),
            ("zeCommandListAppendMemoryCopy", "level-zero", "ze_api.h", "api"),
            ("chrome-kernel-logging", "pti-gpu", "tools/unitrace/README.md", "doc"),
            ("query-api-mapping", "SYCLomatic", "options_def.rst", "doc"),
            ("CCL_PLUGIN", "oneCCL", "README.md", "doc"),
            ("sycl_ext_oneapi_graph", "llvm", "sycl_ext_oneapi_graph.asciidoc", "doc"),
        ]
        for query, project, expected, kind in cases:
            with self.subTest(query=query):
                results = search.search(query, project, kind)
                self.assertTrue(any(r["path"].endswith(expected) for r in results), results)
                self.assertLessEqual(len(results), 8)
                self.assertTrue(all(r["project"] == project and r["kind"] == kind for r in results))

    def test_empty_unknown_and_no_match(self):
        with self.assertRaises(ValueError):
            search.search("the and")
        with self.assertRaisesRegex(ValueError, "Unknown project"):
            search.search("queue", "not-a-project")
        self.assertEqual(search.search("qzx_unique_not_a_oneapi_symbol_8172"), [])

    def test_portable_copy_and_other_working_directory(self):
        # A real copied package, without any reference clone or checkout-relative path.
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "copied-oneapi"
            shutil.copytree(SKILL, copy, ignore=shutil.ignore_patterns("__pycache__"))
            result = subprocess.run([sys.executable, str(copy / "scripts/search_docs.py"),
                                     "ONEAPI_DEVICE_SELECTOR", "--project", "llvm", "--json", "--limit", "2"],
                                    cwd=temporary, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)), 2)
            verified = subprocess.run([sys.executable, str(copy / "scripts/sync_docs.py"), "--verify"],
                                      cwd=temporary, text=True, capture_output=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)


class ProbeTests(unittest.TestCase):
    def run_python(self, code, timeout=2):
        with patch.object(probe.shutil, "which", return_value=sys.executable):
            return probe.inspect_tool("fixture", ["-c", code], timeout)

    def test_missing_tool(self):
        with patch.object(probe.shutil, "which", return_value=None):
            self.assertEqual(probe.inspect_tool("missing", [], 1), {"status": "missing"})

    def test_success_and_nonzero(self):
        self.assertEqual(self.run_python("print('ok')")["status"], "ok")
        result = self.run_python("import sys; print('failure'); sys.exit(7)")
        self.assertEqual((result["status"], result["exit_code"]), ("error", 7))
        self.assertIn("failure", result["output"])

    def test_timeout_and_bounded_output(self):
        self.assertEqual(self.run_python("import time; time.sleep(5)", 0.05)["status"], "timeout")
        result = self.run_python("print('x' * 20000)")
        self.assertTrue(result["truncated"])
        self.assertEqual(len(result["output"]), 16000)


if __name__ == "__main__":
    unittest.main()
