# oneAPI skill: heterogeneous CPU/GPU programming

**Unofficial:** This is a personal project, not an official Intel project.

A portable agent skill for the **oneAPI parallel-computing ecosystem**: SYCL/DPC++,
Intel oneAPI development tools, accelerator runtimes, and performance libraries
for CPU and GPU applications. It helps agents develop, build, migrate, debug and
profile code using bundled upstream documentation and practical workflows.
Start at
[skills/oneapi/SKILL.md](skills/oneapi/SKILL.md).

## Which oneAPI?

[oneAPI](https://www.intel.com/content/www/us/en/developer/articles/technical/oneapi-what-is-it.html)
is an open, standards-based approach to **heterogeneous computing**: programming
CPUs, GPUs and other accelerators. Its ecosystem includes SYCL for writing parallel
C++ kernels and library APIs for workloads such as linear algebra, deep learning,
data analytics, task parallelism and collective communication. The
[oneAPI specification](https://github.com/uxlfoundation/oneAPI-spec) defines the
programming interfaces; individual implementations provide the compilers,
libraries and runtime support.

[Intel oneAPI toolkits](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneapi-toolkit.html)
package compilers, libraries and development tools for this ecosystem. This skill
covers both upstream open-source projects and practical Intel toolchain workflows,
especially SYCL/DPC++ and OpenMP offload on CPUs and GPUs. Supported devices,
backends and features depend on the installed component versions.

## What the skill helps with

| Area | Tasks |
|---|---|
| Programming | SYCL kernels, device selection, queues, USM, buffers, dependencies and correctness checks |
| Toolchains | Intel compiler setup, CMake integration, compile/link errors and OpenMP GPU offload |
| Libraries | oneTBB, oneDPL, oneMath/oneMKL, oneDNN, oneDAL, oneCCL and sklearnex integration |
| Runtime diagnosis | Unified Runtime, Level Zero, Intel GPU driver visibility, memory and synchronization errors |
| CUDA migration | SYCLomatic or dpct workflows, compilation databases, API mappings and migration diagnostics |
| Performance | Kernel and transfer timing, PTI/unitrace tracing, library diagnostics and profiling workflows |

## What is included

The skill combines a short task router, nine workflow references, offline upstream
docs/API headers/examples, bounded search, a read-only environment probe and an
explicit-device SYCL smoke test. The documentation bundle records exact upstream
commits and retains source attribution and licenses.

Copy the entire `skills/oneapi/` directory into
the skill location supported by your agent; no reference checkout is needed for
normal use. Python helpers require Python 3.10+ and its standard library only.
Compiling/running examples requires a compatible compiler, runtime and device.

## Documentation

- [Corpus index](skills/oneapi/docs/TOC.md): projects and per-project file indexes.
- [Source provenance](skills/oneapi/docs/SOURCE.md): exact commits, licenses,
  coverage and deliberate omissions.
- [Local research checkouts](index.md): source repositories used to build the bundle.

The corpus preserves upstream source text and copyright/license notices. It is
not a complete mirror of every proprietary Intel toolkit manual, a rendered
documentation website, or a mutually compatible toolkit release. Upstream images,
datasets, most implementation code and build products are excluded. API headers
and schema supplement documentation generated through Doxygen/Sphinx. The
proprietary component guide links to official versioned/product documentation.

Design references supplied for this work:
[skill-writing guide](https://gist.github.com/joyrexus/ff71917b4fc0a2cbc84974212da34a4a),
[xpu-smi example](https://github.com/Zekai-Zhao-321/xpumanager/tree/claude/jolly-bohr-a3txfa/skills/xpu-smi),
[DuckDB example](https://github.com/Zekai-Zhao-321/duckdb-skills/tree/main/skills_rewrite/duckdb).

## Verify and refresh

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 skills/oneapi/scripts/sync_docs.py --verify
python3 skills/oneapi/scripts/search_docs.py 'ONEAPI_DEVICE_SELECTOR' --project llvm
python3 skills/oneapi/scripts/probe.py
```

Reproduce the bundle with local Git checkouts containing the pinned commits:

```bash
python3 skills/oneapi/scripts/sync_docs.py --sources-root ./references
```

The script reads committed Git objects and stages the full result before replacing
the bundle. It refuses to overwrite modified bundle files and does not fetch or
change upstream checkouts. Update `scripts/sources.json` intentionally to refresh
revisions, then review the regenerated diff. Keep custom guidance in `references/`
inside the skill, separate from its generated `docs/`.

Automated tests cover retrieval, portability, hashes, reproducible committed-source
copying, failure preservation, missing tools, exit status, timeouts and output
bounds. [Behavioral evaluation cases](tests/eval_cases.md) cover selection and
agent workflows; they are test specifications, not claimed agent evaluation runs.
Hardware compilation/execution requires a separate compatible host.

## License

Original skill instructions, workflow guides, code, examples and repository
tooling are licensed under the [MIT License](LICENSE).

Bundled material under `skills/oneapi/docs/upstream/` retains its original
upstream licenses and copyright notices. See the
[source attribution](skills/oneapi/docs/SOURCE.md) and
[skill licensing notice](skills/oneapi/NOTICE.md) for the scope of each license.
