# Library selection and integration

Start from the operation and the user's existing dependencies. Prefer a suitable
library implementation over writing a new kernel, while preserving numerical,
device and portability requirements. oneAPI specification pages define contracts;
a particular library build determines what is available.

## Choose the component

| Work | Component | First bundled source |
|---|---|---|
| CPU task parallelism, flow graphs, concurrent containers | oneTBB | [oneTBB index](../docs/indexes/oneTBB.md) |
| Parallel STL-style algorithms, iterator pipelines, reductions | oneDPL | [getting started](../docs/upstream/oneDPL/documentation/get_started/onedpl_gsg.rst) |
| BLAS, LAPACK, FFT, RNG, sparse math with backend dispatch | oneMath, or installed Intel oneMKL | [oneMath introduction](../docs/upstream/oneMath/docs/introduction.rst) |
| Neural-network primitives, layouts, fusion, graph partitions | oneDNN | [oneDNN index](../docs/indexes/oneDNN.md) |
| Analytics algorithms and tables | oneDAL | [oneDAL index](../docs/indexes/oneDAL.md) |
| Accelerating an existing scikit-learn program | sklearnex | [configuration contexts](../docs/upstream/scikit-learn-intelex/doc/sources/config-contexts.rst) |
| Rank-based collective communication | oneCCL | [current implementation overview](../docs/upstream/oneCCL/README.md) |
| CPU cryptographic primitives | Intel Cryptography Primitives | [overview](../docs/upstream/cryptography-primitives/OVERVIEW.md) |
| Memory providers and allocation pools | Unified Memory Framework | [overview](../docs/upstream/unified-memory-framework/README.md) |

## Inspect before linking

For the chosen library establish installed version, headers, namespace/API flavor,
CPU/GPU backend, compiler ABI, shared/static linkage and exported CMake targets.
Use that installation's CMake config or docs. Don't infer package identity from a
similar name. Include paths compiling successfully do not establish that the
runtime backend libraries will load.

Keep a small reproducible operation with a known answer before expanding to the
whole model/dataset. Check layout, dtype, dimensions, strides, batch size,
transposition, queue/context, workspace and event lifetimes.

## oneTBB: host task parallelism

Use `oneapi::tbb::parallel_for`, `parallel_reduce`, task arenas and concurrent
containers according to their contracts. oneTBB is CPU task scheduling; a
`parallel_for` is not a GPU launch. A common installed CMake integration is:

```cmake
find_package(TBB REQUIRED COMPONENTS tbb)
target_link_libraries(app PRIVATE TBB::tbb)
```

Check thread ownership and oversubscription when mixing TBB with OpenMP, a BLAS
thread pool, MPI ranks or application threads. Partitioning/grain size and arena
limits are performance choices; first establish race-free semantics. Stateful
reduction bodies and container updates need the documented thread-safety contract.

## oneDPL: algorithms on a chosen queue

Select an execution policy deliberately. A host `par` policy does not imply GPU
offload. Device policies connect an algorithm to a SYCL queue:

```cpp
#include <oneapi/dpl/execution>
#include <oneapi/dpl/algorithm>
// q is a configured SYCL queue. data is compatible, initialized USM.
auto policy = oneapi::dpl::execution::make_device_policy(q);
oneapi::dpl::sort(policy, data, data + n);
q.wait_and_throw();
```

Ensure earlier asynchronous producers have completed or are ordered before the
algorithm; don't assume a normal algorithm accepts a dependencies argument. Check
iterator support, USM accessibility and restrictions on device lambdas. Host
container iterators may imply copying; use the actual passing-data guide.

Read [execution policies](../docs/upstream/oneDPL/documentation/library_guide/parallel_api/execution_policies.rst),
[passing data](../docs/upstream/oneDPL/documentation/library_guide/parallel_api/pass_data_algorithms.rst)
and [CMake support](../docs/upstream/oneDPL/documentation/library_guide/cmake_support.rst).
Experimental asynchronous/range/dynamic-selection APIs have separate contracts.

## oneMath versus Intel oneMKL

These are not interchangeable package names:

| Installed interface | Typical header / namespace | Integration |
|---|---|---|
| Open oneMath | `<oneapi/math.hpp>`, `oneapi::math` | `find_package(oneMath REQUIRED)`, installed target `ONEMATH::onemath` |
| Intel oneMKL SYCL | `<oneapi/mkl.hpp>`, `oneapi::mkl` | Intel oneMKL's installed CMake config / Link Line Advisor |
| Intel oneMKL C/Fortran | BLAS/LAPACK/DFT/etc. C or Fortran APIs | Choose interface width, threading and linkage explicitly |

The oneMath installed target above is for runtime dispatch. Source-tree
FetchContent targets and specific backend targets differ; read
[using oneMath with CMake](../docs/upstream/oneMath/docs/using_onemath_with_cmake.rst).
Enabled backends and supported domains/types vary. Do not mechanically rename
oneMKL includes and claim the dependency is migrated.

For GEMM verify `m,n,k`, row/column-major convention, transposition and leading
dimensions against the actual shapes. For column-major, leading dimension is the
physical stride between columns, not simply the logical number of columns.
Choose the buffer or USM overload intentionally. USM dependencies/event results
and scratchpad requirements are part of the operation, not optional decoration.
For LAPACK query workspace requirements for the selected API; inspect returned
errors and numerical outputs. For RNG preserve seed, generator and stream intent;
bitwise identity across devices/algorithms must be established, not assumed.

Read [GEMM](../docs/upstream/oneMath/docs/spec/domains/blas/gemm.rst) and use the
[oneMath index](../docs/indexes/oneMath.md) for DFT/RNG/LAPACK/sparse details.
Intel oneMKL-only details route to [toolkit-and-openmp.md](toolkit-and-openmp.md).

## oneDNN: layouts and execution

Pick engine kind/runtime first, then build memory descriptors and primitives or
use the graph API. `format_tag::any` lets a primitive choose a layout; query its
chosen descriptors and reorder inputs/outputs where required. Binding a plain
row-major array to a blocked descriptor is a correctness error.

Distinguish primitive creation from execution, user/library scratchpad ownership,
stream completion and SYCL interop lifetimes. GPU support depends on the library
build/runtime. A graph partition may be unsupported; handle that result explicitly.

For a short diagnostic run, where supported by the installed release:

```bash
ONEDNN_VERBOSE=profile,dispatch ./app
```

The [verbose guide](../docs/upstream/oneDNN/doc/performance/verbose.md) documents
flags, legacy numeric values, profiling queue requirements and overhead. Output
goes to stdout; don't parse the combined output as pure application JSON.
Read [linking](../docs/upstream/oneDNN/doc/getting_started/link.md) for platform
library resolution. Use benchdnn when a targeted primitive repro is appropriate.

## oneDAL and sklearnex: confirm which implementation ran

oneDAL has modern `oneapi::dal` and legacy DAAL interfaces. Use the matching
algorithm descriptors, table APIs and examples; do not mix header/namespace
families. Verify supported device, input dtype/layout and algorithm mode.

For sklearnex, patch before importing the estimators that must be replaced, or use
explicit sklearnex imports. Check installed version and the supported algorithm/
parameter matrix. `config_context(target_offload="gpu")` is a documented route for
appropriate host-data workflows; array API inputs have a separate dispatch route.

Do not infer GPU execution merely because `fit` returns. Read
[array API dispatch and fallback](../docs/upstream/scikit-learn-intelex/doc/sources/array_api.rst),
[GPU usage](../docs/upstream/scikit-learn-intelex/doc/sources/oneapi-gpu.rst) and the
algorithm support page. Distinguish unsupported-parameter fallback, CPU fallback,
input transfers and an actual accelerated GPU operation. Compare model outputs or
metrics with the reference estimator using an appropriate tolerance.

## oneCCL: match the API generation

The bundled checkout has a C API and plugin architecture; older applications and
specification examples may use `ccl::` C++ interfaces. Inspect the installed headers
and library version before copying an example. Its README includes version-specific
build instructions, some mentioning internal repositories; do not assume those
repositories are accessible or required for a user's installed package.

For a collective, every participating rank must agree on communicator, operation,
count/type and ordering. Establish rank-to-device mapping before launch. Keep
buffers alive until the operation completes and connect SYCL work to collective
completion using the API's stream/event contract. Host completion is not always
proof of device completion; inspect the particular overload/runtime behavior.

Diagnose a hang with rank logs, topology, transport and device assignment; don't
retry indefinitely with changed transport environment variables. The newer build
may require runtime plugin discovery (`CCL_PLUGIN`, library path) as documented
in [its README](../docs/upstream/oneCCL/README.md). Legacy `CCL_*` tuning settings
must be checked against the installed backend/version.

## Cryptography and memory frameworks

The bundled Cryptography Primitives docs cover its APIs, not the entire Intel IPP
product. Preserve the requested algorithm/protocol and use supported APIs; this
skill does not design cryptographic protocols. UMF providers/pools concern
allocation policy. They do not establish SYCL command dependencies or make every
allocation accessible from every device/context.
