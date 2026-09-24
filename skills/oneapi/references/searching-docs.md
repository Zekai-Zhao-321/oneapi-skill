# Finding exact documentation

The bundle is deliberately thick while the entrypoint is small. Open only the
pages needed. All paths in this guide are relative to the skill directory.

## Route before searching

| Need | Search project / location |
|---|---|
| Standard SYCL 2020 queue, memory, kernel or device semantics | `SYCL-Reference/source/iface/` |
| DPC++ options, runtime environment, extensions | `llvm/sycl/doc/` |
| Unified Runtime adapter/loading/tracing | `llvm/unified-runtime/scripts/core/INTRO.rst` |
| Normative oneAPI library contract | `oneAPI-spec/source/elements/` |
| Actual library implementation API/build guide | The named library's project |
| Level Zero compute / tools / system management API | `level-zero-spec/scripts/{core,tools,sysman}/` and `level-zero/include/` |
| Intel GPU driver / IGC architecture | `compute-runtime`, `intel-graphics-compiler` |
| CUDA migration diagnostics / mappings | `SYCLomatic/docs/` |
| Traces, metrics, sampling | `pti-gpu/tools/`, `pti-gpu/sdk/` |
| Working source pattern | `oneAPI-samples`, the library's examples |

`docs/TOC.md` links a complete file index per included project. The upstream
standalone `unified-runtime` mirror is not a search project; use `--project llvm`.

## Bounded ranked search

```bash
python3 /path/to/oneapi/scripts/search_docs.py 'queue in_order' --project SYCL-Reference
python3 /path/to/oneapi/scripts/search_docs.py 'SYCL_UR_TRACE' --project llvm
python3 /path/to/oneapi/scripts/search_docs.py 'column_major gemm' --project oneMath
python3 /path/to/oneapi/scripts/search_docs.py 'zeCommandListAppendMemoryCopy' --project level-zero --kind api
python3 /path/to/oneapi/scripts/search_docs.py 'DPCT1003' --project SYCLomatic
```

This uses standard-library lexical ranking over local text, with title/path and
phrase bonuses. It is not semantic retrieval or a language model. The default is
eight hits, capped at 50; each includes a path, line and short snippet. Narrow the
project or symbol if a broad query gives poor results. `--json` produces structured
hits; `--list-projects` lists exact project names. No network or index build needed.

For an exact identifier, `rg` can be faster:

```bash
rg -n -F 'SYCL_UR_TRACE' /path/to/oneapi/docs/upstream/llvm/sycl/doc
rg -n -i 'scratchpad' /path/to/oneapi/docs/upstream/oneDNN/doc
```

Then read the surrounding section, not just the matching line. A snippet can omit
the supported types, queue/context requirements or an experimental-status warning.

## Source formats and gaps

Upstream `.md`, `.rst`, `.asciidoc` and `.dox` are preserved verbatim. RST pages may
use `.. include::`, `.. literalinclude::`, substitutions or Doxygen-generated API
sections. An apparently empty page may be a routing page: read its included file
or search the symbol in bundled headers/schema with `--kind all`. Do not invent
the contents of an unresolved include. If a source is omitted, open its upstream
commit URL from `docs/SOURCE.md` and the source path in `docs/catalog.json`.

Absolute RST includes such as `/_include_files/options_def.rst` are relative to
that project's documentation source root, not the filesystem root. Doxygen
`@ref` and Sphinx `:ref:` labels may require a text search rather than a file lookup.

For normative SYCL language disputes, consult the [Khronos SYCL specification](https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html).
The bundled SYCL reference explains APIs but is not the normative specification.
For installed behavior, inspect the user's compiler/runtime headers and release
notes. An extension proposal in `experimental/` or `proposed/` is not a guarantee
that their toolkit implements it.

## Provenance and refresh

- `docs/SOURCE.md`: included projects, exact revisions, licenses and gaps.
- `docs/catalog.json`: original source path, local path, kind, bytes and SHA-256.
- `docs/inventory.json`: hashes of raw files and generated metadata.
- `scripts/sources.json`: reviewed selection rules and pinned commit IDs.

Run `python3 scripts/sync_docs.py --verify` from the skill directory to verify the
installed copy without Git or network access. To reproduce, pass `--sources-root`
the parent of the named checkouts. To update, intentionally change pinned commits
and rebuild; the script reads Git objects, not dirty working-tree files, and stages
all sources before replacing the old bundle. It refuses to overwrite bundle edits.
Keep custom guidance in `references/`, not under generated `docs/`.

For attribution in an answer use the local file and upstream URL containing the
recorded commit. Do not call a pinned snapshot the latest documentation.
