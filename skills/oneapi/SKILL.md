---
name: oneapi
license: MIT
description: >-
  Develop, build, migrate, debug and profile oneAPI applications using a bundled,
  searchable copy of upstream documentation and examples. Use for Intel oneAPI
  toolkit setup, SYCL or DPC++ C++, icpx/icx/ifx, OpenMP GPU offload, CUDA-to-SYCL
  migration with SYCLomatic or dpct, device selection, USM and queue dependencies,
  Level Zero or Unified Runtime errors, and oneTBB, oneDPL, oneMath/oneMKL, oneDNN,
  oneDAL, oneCCL or sklearnex integration. Also use for exact API, compiler flag,
  environment variable and performance questions in this stack. Not for generic
  REST APIs or GPU firmware/reset/power administration.
---

# oneAPI

Original skill content is [MIT-licensed](LICENSE.txt). Bundled upstream material
retains its own licenses; see [NOTICE.md](NOTICE.md) and [docs/SOURCE.md](docs/SOURCE.md).

Use the bundled docs to turn the user's workload into a buildable, checkable
program, or to answer the specific API question. oneAPI is an ecosystem: identify
the relevant component before selecting commands or APIs.

## Start with the task

For a documentation question, go straight to the routing table and search. No
toolchain installation or hardware probe is needed to explain an API.

For execution, inspect the existing project, its build instructions, compiler,
OS, target device and installed versions first. Preserve its build system and
dependencies. Run the optional inventory helper when that evidence is missing:

```bash
python3 /path/to/oneapi/scripts/probe.py
```

It reports missing tools, exit codes, device listing and selected oneAPI variables.
It does not install or initialize the toolkit, and an inventory is not a GPU test.
All skill paths are relative to this SKILL.md, **not the user's current directory**;
resolve the actual skill location once and use absolute paths in commands.

## The working loop

1. **Identify the layer and version.** SYCL language, compiler, library, Unified
   Runtime adapter, Level Zero loader and GPU driver have different contracts.
   An installed Intel toolkit is not identical to an upstream development checkout.
2. **Read the relevant guide and exact upstream page.** Search symbols/options
   before writing unfamiliar commands. Check experimental status and compatibility
   with the user's installed release. Prefer installed headers/help for availability;
   consult the appropriate standard for semantics.
3. **Make the smallest useful change.** Reuse the project's build. For a new SYCL
   project, use `assets/sycl-smoke/` and [build-and-test](references/build-and-test.md).
   Keep compile and link flags consistent. Make the requested device explicit.
4. **Validate at the level requested.** Distinguish source review, configuration,
   compilation, device enumeration, actual execution, numerical correctness and
   performance measurement. Wait for asynchronous work and surface its errors.
   A CPU result cannot establish a GPU result.
5. **Report the outcome and evidence.** Give the answer/change, exact build/run
   commands, observed device/backend, correctness check and remaining blocker.
   For a docs answer cite the bundled path and pinned upstream URL. Do not imply
   a hardware run when only source or documentation was available.

## Read only what matches

| Task | Workflow reference | Upstream project in docs/ |
|---|---|---|
| Toolkit/environment setup, missing compiler, driver/container visibility | [environment.md](references/environment.md) | llvm, compute-runtime, level-zero |
| Compile/link/CMake, minimal repro, CPU vs GPU smoke test | [build-and-test.md](references/build-and-test.md) | llvm, oneAPI-samples |
| Queues, USM, buffers, dependencies, reductions, work-groups | [sycl-programming.md](references/sycl-programming.md) | SYCL-Reference, llvm |
| Select/integrate a math, parallel, DL, analytics or communication library | [libraries.md](references/libraries.md) | oneMath, oneDPL, oneDNN, oneTBB, oneDAL, oneCCL, scikit-learn-intelex |
| CUDA port, compilation database, DPCT diagnostics, API mappings | [migration.md](references/migration.md) | SYCLomatic, oneAPI-samples |
| No device, runtime error, native interop, multi-GPU/tile, memory allocation | [runtime-and-debugging.md](references/runtime-and-debugging.md) | llvm, level-zero-spec, level-zero, compute-runtime, unified-memory-framework |
| Slow kernel, transfers, timing, traces, PTI/unitrace/VTune | [performance.md](references/performance.md) | pti-gpu, oneDNN, llvm |
| OpenMP/Fortran offload, Intel oneMKL/IPP/MPI, proprietary tool manuals | [toolkit-and-openmp.md](references/toolkit-and-openmp.md) | oneAPI-samples plus official online manuals |
| Find a signature, option, extension, error or sample | [searching-docs.md](references/searching-docs.md) | [docs/TOC.md](docs/TOC.md) |

## The documentation bundle

`docs/upstream/` contains pinned, unmodified upstream documentation source,
selected public headers/schema and examples. It is usable offline without the
original clones. [docs/TOC.md](docs/TOC.md) routes to per-project page indexes;
[docs/SOURCE.md](docs/SOURCE.md) records revisions, attribution and deliberate gaps.
It is **not** a claim to mirror every Intel product manual or release.

```bash
python3 /path/to/oneapi/scripts/search_docs.py 'ONEAPI_DEVICE_SELECTOR' --project llvm
python3 /path/to/oneapi/scripts/search_docs.py 'USM dependencies' --project SYCL-Reference
python3 /path/to/oneapi/scripts/search_docs.py 'gemm' --project oneMath --limit 5
```

Read the returned page around the matching lines. Search defaults to docs;
`--kind api`, `--kind example`, or `--kind all` also finds header/schema/sample
material. `--list-projects` lists valid project names. `rg` works directly on the
tree too. Do not load the whole corpus into context.

## Keep these distinctions intact

- Use `<sycl/sycl.hpp>` and SYCL 2020 constructs for new code unless the project
  targets an older interface. Label Intel/oneAPI extensions and proposed features.
- A default selector can choose an unintended device. Enumerate with `sycl-ls`,
  use an explicit selector, print identity, and scope `ONEAPI_DEVICE_SELECTOR` to
  the command when needed. Do not invent an enumeration index.
- USM pointers do not automatically create data dependencies. Connect commands
  with events or a deliberately in-order queue; keep allocations alive until use
  finishes. Shared memory is not permission for host/device data races.
- A successful build, device listing, or timed-out process is not successful
  execution. Check outputs and asynchronous errors; diagnose a hang before retries.
- oneMath is the open interface/dispatch project; Intel oneMKL is a separate
  implementation/product. Match headers, namespaces, CMake targets and backends.
- Bundled docs span different development snapshots. Unified Runtime comes from
  the same intel/llvm revision as SYCL, but the library commits are independent.
  Check installed versions before adopting source-tree defaults or new flags.
- Follow the user's requested scope for installations or machine changes. A
  compile/debug request does not authorize GPU resets, firmware writes, broad
  device permissions or persistent driver/profiling configuration changes.
