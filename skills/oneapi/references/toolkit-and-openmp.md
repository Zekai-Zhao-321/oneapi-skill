# Intel toolkit components and OpenMP offload

The bundle is strongest for open-source oneAPI components. Intel's distribution
also includes separately documented products. Do not treat an open-source oneAPI
specification or oneMath guide as the complete manual for those installed products.

## Compiler and OpenMP path

- `icx` / `icpx`: Intel C/C++ compiler drivers; `-fsycl` selects SYCL compilation.
- `ifx`: Intel Fortran compiler; use its OpenMP offload path for suitable Fortran
  code. Do not promise that C++ SYCL APIs are Fortran interfaces.
- `icx-cl`: Windows MSVC-style driver; command syntax and host prerequisites differ.
- The upstream DPC++ `clang++` executable must be distinguished from system Clang.

For a supported Intel compiler release on Linux, a documented OpenMP GPU offload
command shape is:

```bash
icpx -O2 -fiopenmp -fopenmp-targets=spir64 app.cpp -o app
# For a Fortran source, use ifx and the actual .f90 input instead.
OMP_TARGET_OFFLOAD=MANDATORY ./app
```

`MANDATORY` helps expose device unavailability where OpenMP would otherwise fall
back. It is not sufficient evidence that a specific region ran on the intended
GPU: check that execution reaches the target region, query/record device identity
where available, and check `omp_is_initial_device()` inside the region. A host-only
program also exits successfully under this variable.

Inspect target/data map clauses, persistent device data, updates and the lifetime
of asynchronous target work. `nowait` and dependency clauses require explicit
reasoning about host access. Compare numerical outputs with the host baseline.
Use [the oneAPI-samples index](../docs/indexes/oneAPI-samples.md) for C++/Fortran
OpenMP examples and their requirements.

Official references for these command shapes:
[OpenMP offload compilation](https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-0/compiling-and-running-an-openmp-application.html),
[offload target option](https://www.intel.com/content/www/us/en/docs/dpcpp-cpp-compiler/developer-guide-reference/2025-0/fopenmp-targets-qopenmp-targets.html).
They are versioned examples; select the user's installed release in the online
manual. Windows uses its documented driver-option forms.

## Component-specific online routes

These product entrypoints lead to documentation/downloads; verify the installed
version, platform and support matrix before adopting an option or package.

| Component / gap | Official route | What to resolve |
|---|---|---|
| Intel compiler / ifx | [oneAPI technical documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/documentation.html) | Exact driver flags, language support, runtime compatibility |
| Intel oneMKL | [oneMKL documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl-documentation.html) | Interface width, threading, CPU/SYCL API, link line and backend |
| Intel MPI | [MPI documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library-documentation.html) | Launcher, transport, affinity, GPU-aware behavior |
| Intel IPP | [IPP documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/ipp-documentation.html) | Supported domain/API and dispatch; not just cryptography |
| VTune | [VTune documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler-documentation.html) | Collection type, target, permissions and result/report options |
| Advisor | [Advisor documentation](https://www.intel.com/content/www/us/en/developer/tools/oneapi/advisor-documentation.html) | Supported analyses and target hardware |
| Installation and toolkit layout | [oneAPI documentation hub](https://www.intel.com/content/www/us/en/developer/tools/oneapi/documentation.html) | OS, release and component-specific installation requirements |

No current support claim is implied by the presence of old toolkit samples. If
network access is unavailable and the required product API is not bundled, use
installed headers/help/local manuals and say what remains unresolved.

## oneMKL integration details that often matter

For C/Fortran interfaces, determine LP64 versus ILP64 integer width before linking
or choosing typedefs. Match the application declarations to the chosen library
interface. Threaded/sequential variants and OpenMP/TBB runtime choices are separate
from integer width; avoid multiple incompatible threading runtimes.

For SYCL APIs, use the installed oneMKL SYCL headers and supported compiler/device
combination. Don't copy an open oneMath CMake target into an Intel oneMKL build.
Use the installation's exported targets or Intel's Link Line Advisor, verify the
actual final link command, then run a small numerical check on the explicit target.

## MPI and GPU-aware execution

A host MPI operation and a device-pointer-capable operation have different
requirements. Check the MPI implementation/version, supported memory types,
transport and enabled GPU support. Don't pass a device pointer to an API just
because another stack accepts it. Establish local rank/device mapping and
synchronization between SYCL/OpenMP work and communication before benchmarking.
