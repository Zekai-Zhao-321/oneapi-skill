# Build, link and verify execution

## Existing projects

Use the repository's documented build and tests. Record the actual compiler and
linker commands (`cmake --build <build-dir> --verbose` for CMake). Supply a compiler
at the first configure step; use a new build directory when changing compilers.
Changing only `CXX` after configuration often leaves the original compiler cached.

For a SYCL executable, the SYCL option is needed during compilation **and final
linking**. A static library containing device code also needs an appropriate SYCL
final link. Don't fix missing symbols by adding random runtime libraries manually.
Keep the compiler/runtime and dependent C++ library ABI compatible.

## Smallest executable check

`assets/sycl-smoke/` contains a C++17/SYCL 2020 program and CMake file. It requires
an explicit `gpu` or `cpu`, prints identity, waits for asynchronous work, validates
all 4096 integer outputs and fails on missing devices, exceptions or mismatches.
It uses buffers/accessors, so it does not require shared USM support.

From a bash shell with the compiler initialized, replace the skill path:

```bash
icpx -fsycl -std=c++17 -O2 /path/to/oneapi/assets/sycl-smoke/smoke.cpp -o ./sycl-smoke
ONEAPI_DEVICE_SELECTOR=level_zero:gpu ./sycl-smoke --device gpu
```

`icpx` is Intel's compiler driver. An upstream DPC++ installation may instead
provide a SYCL-enabled `clang++`; establish its identity before substituting it.

Equivalent CMake workflow, with a fresh user-owned build directory:

```bash
cmake -S /path/to/oneapi/assets/sycl-smoke -B ./build-sycl-smoke \
  -DCMAKE_CXX_COMPILER=icpx -DCMAKE_BUILD_TYPE=Release
cmake --build ./build-sycl-smoke --parallel
ONEAPI_DEVICE_SELECTOR=level_zero:gpu ./build-sycl-smoke/sycl-smoke --device gpu
```

For CPU testing, enumerate a usable CPU backend first, then run `--device cpu`
under its selector. No CPU backend installed means the CPU test is unavailable;
the existence of a host CPU is not enough to guarantee a SYCL CPU runtime.

On Windows in an initialized developer command prompt, a Ninja CMake build can
use `-DCMAKE_CXX_COMPILER=icx-cl`; the supplied CMake target adds `-fsycl` for compile
and link and `/EHsc` for the MSVC-style frontend. Set the selector with `set
ONEAPI_DEVICE_SELECTOR=level_zero:gpu` and run the produced `.exe`. Verify against
that compiler's accepted options; do not reuse bash environment-assignment syntax.

## Build choices that need evidence

| Choice | Decision |
|---|---|
| JIT / portable intermediate representation | Start with the project's default `-fsycl` target for a small repro |
| AOT GPU target | Read compiler/backend help for the installed release and exact GPU; don't infer an architecture token from a marketing name |
| Optimization | Establish correctness before `-O3`, fast math, fusion or layout changes |
| Debug symbols | Use `-g` and an appropriate optimization level for the problem |
| Experimental extensions | Check extension document status, feature-test macro and implementation availability |
| NVIDIA/AMD backend | Requires the corresponding compiler support, adapter, target and vendor stack; an Intel GPU filter does not make it portable |
| FPGA | Treat old FPGA samples as version/hardware-specific; follow the installed FPGA toolchain's instructions |

Search [UsersManual.md](../docs/upstream/llvm/sycl/doc/UsersManual.md) for
`-fsycl-targets`, `-Xsycl-target-backend`, device code splitting and RDC. A document
from development HEAD can contain a flag absent from the installed compiler.

## Correctness contract

Use an independently computed expected result. Check sizes, shape, every required
element, NaNs/infinities and boundary cases. For floating point use an explicit
absolute/relative tolerance appropriate to the algorithm and conditioning; GPU
parallel reductions can change operation order. Passing after widening tolerance
without an explanation is not a numerical validation.

When a user asked for GPU execution, record compiler version, runtime environment,
backend/device/driver, command, exit status and output validation. These are
separate outcomes:

- Configuration succeeded.
- Compilation and linking succeeded.
- A device enumerated.
- Work executed and completed on the requested device.
- Output matched the defined check.
- A repeatable performance measurement was collected.

Never infer later outcomes from earlier ones. The sample is a smoke test, not a
conformance suite, stability soak, thermal test or throughput benchmark.

## Build failures

- `sycl/sycl.hpp` missing: identify the compiler/install, environment and include
  paths; don't globally copy headers into a system include folder.
- `-fsycl` rejected: likely a different compiler or unsupported driver version.
- Undefined SYCL symbols: inspect the final link and runtime library resolution.
- `invalid device`/no image/kernel build failure: compare target flags, requested
  backend/device and driver/compiler compatibility; use runtime diagnostics.
- Missing library CMake package: inspect installation prefix and exported targets;
  use that component's guide instead of guessing a `find_package` name.

For a full source sample use [the oneAPI-samples index](../docs/indexes/oneAPI-samples.md).
Some samples depend on assets not bundled here. Read their README and fetch the
pinned upstream sample when necessary; the documentation corpus is not a complete
buildable checkout of every project.
