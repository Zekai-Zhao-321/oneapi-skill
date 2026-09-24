# oneAPI research index

This project is a local reading workspace for the oneAPI programming model, Intel's implementation, and related open source projects. Each directory under `references/` is an independent upstream Git clone. The checkouts are ignored by this project's Git repository; this index records where to find and update them.

The distributable [oneAPI skill](skills/oneapi/SKILL.md) includes a pinned offline
documentation corpus, workflow guides, search/probe helpers and a SYCL smoke-test
example. It does not depend on these local checkouts at runtime. See
[the repository README](README.md) for packaging and verification.

## Start here

1. Read the [oneAPI specification](references/oneAPI-spec/) for the programming model.
2. Browse [oneAPI samples](references/oneAPI-samples/) for small working examples.
3. Follow a SYCL program through the [compiler](references/llvm/), [unified runtime](references/unified-runtime/), [Level Zero loader](references/level-zero/), and [Intel GPU driver](references/compute-runtime/).
4. Choose a library below for a specific workload.

## Compiler and runtime

| Local checkout | Upstream | Role |
| --- | --- | --- |
| [llvm](references/llvm/) | [intel/llvm](https://github.com/intel/llvm) | DPC++/SYCL compiler and LLVM fork |
| [unified-runtime](references/unified-runtime/) | [oneapi-src/unified-runtime](https://github.com/oneapi-src/unified-runtime) | Backend abstraction used by the SYCL runtime |
| [unified-memory-framework](references/unified-memory-framework/) | [oneapi-src/unified-memory-framework](https://github.com/oneapi-src/unified-memory-framework) | Memory allocation framework |
| [level-zero](references/level-zero/) | [oneapi-src/level-zero](https://github.com/oneapi-src/level-zero) | Level Zero API headers and loader |
| [compute-runtime](references/compute-runtime/) | [intel/compute-runtime](https://github.com/intel/compute-runtime) | Intel GPU Level Zero and OpenCL driver runtime |
| [intel-graphics-compiler](references/intel-graphics-compiler/) | [intel/intel-graphics-compiler](https://github.com/intel/intel-graphics-compiler) | Intel GPU backend compiler |

## Libraries

| Local checkout | Upstream | Role |
| --- | --- | --- |
| [oneTBB](references/oneTBB/) | [uxlfoundation/oneTBB](https://github.com/uxlfoundation/oneTBB) | Task parallelism on CPUs |
| [oneDPL](references/oneDPL/) | [uxlfoundation/oneDPL](https://github.com/uxlfoundation/oneDPL) | Parallel C++ standard library algorithms |
| [oneMath](references/oneMath/) | [uxlfoundation/oneMath](https://github.com/uxlfoundation/oneMath) | Open math interfaces and backend dispatch |
| [oneDNN](references/oneDNN/) | [uxlfoundation/oneDNN](https://github.com/uxlfoundation/oneDNN) | Deep learning primitives |
| [oneCCL](references/oneCCL/) | [uxlfoundation/oneCCL](https://github.com/uxlfoundation/oneCCL) | Collective communications |
| [oneDAL](references/oneDAL/) | [uxlfoundation/oneDAL](https://github.com/uxlfoundation/oneDAL) | Data analytics algorithms |
| [scikit-learn-intelex](references/scikit-learn-intelex/) | [uxlfoundation/scikit-learn-intelex](https://github.com/uxlfoundation/scikit-learn-intelex) | scikit-learn acceleration using oneDAL |
| [cryptography-primitives](references/cryptography-primitives/) | [intel/cryptography-primitives](https://github.com/intel/cryptography-primitives) | Cryptographic primitives |

## Specification, examples, and tools

| Local checkout | Upstream | Role |
| --- | --- | --- |
| [oneAPI-spec](references/oneAPI-spec/) | [uxlfoundation/oneAPI-spec](https://github.com/uxlfoundation/oneAPI-spec) | oneAPI specification source |
| [SYCL-Reference](references/SYCL-Reference/) | [KhronosGroup/SYCL_Reference](https://github.com/KhronosGroup/SYCL_Reference) | SYCL 2020 API reference and examples |
| [level-zero-spec](references/level-zero-spec/) | [oneapi-src/level-zero-spec](https://github.com/oneapi-src/level-zero-spec) | Level Zero programming guide and API schema |
| [oneAPI-samples](references/oneAPI-samples/) | [oneapi-src/oneAPI-samples](https://github.com/oneapi-src/oneAPI-samples) | Example programs |
| [SYCLomatic](references/SYCLomatic/) | [oneapi-src/SYCLomatic](https://github.com/oneapi-src/SYCLomatic) | CUDA-to-SYCL migration tool |
| [pti-gpu](references/pti-gpu/) | [intel/pti-gpu](https://github.com/intel/pti-gpu) | Intel GPU profiling and tracing interfaces |

## Working with the checkouts

The repository URLs above are the clone sources. The local folder names stay fixed for links in this index. New checkouts use Git's `--filter=blob:none`: their current files and commit history are available locally, while older file contents download on demand. The pre-existing `compute-runtime` checkout is a full clone. The `oneCCL` checkout also has its declared submodules initialized under `references/oneCCL/deps/`.

To inspect a checkout's exact source and revision, run `git -C references/<folder> remote -v` and `git -C references/<folder> log -1 --oneline`. To update it, run `git -C references/<folder> pull --ff-only`. These commands affect only that upstream clone, not this research project's Git history.

The repositories are source references, not a complete installed oneAPI toolkit. Some Intel products and binaries are distributed separately. Consult current upstream documentation before using build or installation instructions.
