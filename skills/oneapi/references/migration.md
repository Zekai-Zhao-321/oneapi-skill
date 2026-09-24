# CUDA to SYCL migration

Use this when the user requests a port or asks about a CUDA API mapping. The
migration tool translates syntax and APIs; it cannot establish numerical
correctness, synchronization equivalence or performance for the application.

## Identify the tool and original build

Open-source SYCLomatic provides `c2s`; Intel's compatibility tooling commonly
uses `dpct`. Some distributions provide aliases. Run the executable actually
installed with `--version` and `--help`, then use that name consistently.

Before changing code, establish a working CUDA build and a baseline test with
known inputs/results when the necessary hardware is available. If CUDA execution
is unavailable, preserve that as a verification gap and use an independent CPU
reference where possible. Record original CUDA toolkit/compiler/library versions.

Read [migration workflow](../docs/upstream/SYCLomatic/docs/dev_guide/migration/migration-workflow.rst)
and [compilation database generation](../docs/upstream/SYCLomatic/docs/dev_guide/migration/generate-compilation-db.rst).
The docs use substitutions such as `|tool_name|`; infer their documented meaning,
not a literal executable of that name.

## Capture real compile commands

For a CMake project using a generator that supports compile-command export:

```bash
cmake -S ./cuda-project -B ./build-cuda -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build ./build-cuda
```

Inspect `build-cuda/compile_commands.json` for the intended CUDA translation
units, original include paths, macros and working directories. CMake's Ninja and
Makefile generators support this export; do not expect it from every generator.
An empty or stale compilation database is not useful evidence.

For Makefile projects the installed `intercept-build` can capture a real build:

```bash
intercept-build make
```

Incremental builds that do no compilation may yield no commands. Generate a
fresh build in a separate directory or follow the project's rebuild procedure;
do not destructively clean unrelated artifacts just to obtain a database.

## Migrate into a distinct output tree

Example shape (replace paths and verify options with the installed tool):

```bash
c2s -p ./build-cuda --in-root=./cuda-project --out-root=./sycl-output \
  ./cuda-project/src/main.cu
```

Keep the original source intact and the output outside the input root. Use
`--process-all` only when the intended scope includes all relevant files; it can
copy additional files. For one symbol, use the documented API mapping query rather
than migrating an unrelated project. Search `_include_files/options_def.rst` for
`query-api-mapping` and the installed tool's spelling.

## Resolve semantics, not just diagnostics

Search each emitted `DPCTxxxx` identifier in the bundled SYCLomatic docs. Open
included diagnostics or mapping tables as needed; do not delete warnings merely
to make generated code look finished.

| CUDA construct | Migration check |
|---|---|
| Streams/events/default stream | Explicit SYCL queue/event ordering; preserve dependencies without assuming all queues are ordered |
| `cudaMalloc` / copies / unified memory | USM type, allocation context, host accessibility, async copy lifetime |
| Thread/block indexing | Dimension order, global/local ranges, bounds and subgroup assumptions |
| Shared memory/barriers | Local accessor size and collective barrier participation |
| Warp intrinsics | Subgroup width, participation and supported group operations |
| cuBLAS/cuFFT/cuSOLVER/cuSPARSE | Actual target library, layout, dtype, workspace, error and event contracts |
| Atomics | Memory order/scope/type/device support |
| Inline PTX or unsupported APIs | Manual implementation/library replacement with a focused correctness test |
| Generated `dpct::` helpers | Compatibility headers/runtime required by the selected tool release |

A generated `.dp.cpp` file may still need dpct compatibility headers and specific
oneAPI libraries. Don't remove those includes or claim compiler independence
without resolving those dependencies. The generated CMake/build-file migration
also needs review; update final link options and actual library targets.

## Validate in stages

Compile a small migrated unit, run on the explicit target, compare outputs against
the original/reference and then exercise boundary cases, asynchronous paths and
multi-device/rank paths that matter to the application. For FP reductions define
tolerances before interpreting differences. Measure only after correctness.

If the tool supports CodePin for the installed release, its instrumentation can
help compare runtime values. It is an aid, not an independent proof. Preserve
input data and expected outputs outside the generated tree so rerunning migration
does not erase the validation evidence.

Deliver the changes, unresolved diagnostic IDs, external dependencies and the
exact scope of executed validation. A successful migration-tool exit is neither
a successful SYCL build nor a validated port.
