# Environment and device visibility

Use this for toolchain setup or when a build/run cannot find a compiler, runtime or
device. For pure API questions, skip probing and read the relevant docs.

## Establish what exists

Run `scripts/probe.py` using the skill's absolute path. Its JSON distinguishes
missing executables, command errors and timeouts. A plain `clang++` might be Apple
Clang or another compiler without SYCL. `dpcpp` is a legacy executable name; do not
require it when `icpx` is available. Check the tool the project actually uses.

Record OS/architecture, compiler path/version, selected toolkit version, target
hardware, backend and requested language. Inspect the existing CMake/toolchain
files before changing them. For an existing build, inspect `CMakeCache.txt` and
verbose compiler/link commands: a new PATH does not change a cached compiler.

## Activate an installed toolkit

The Intel distribution has component and unified directory layouts. Locate the
actual installation; these are examples, not proof of its path or version:

```bash
# Component layout, bash shell:
source /opt/intel/oneapi/setvars.sh
icpx --version
sycl-ls
```

A unified layout can instead use `<install-dir>/<version>/oneapi-vars.sh`.
Read that installation's `--help` or versioned programming guide. Do not source
several versions into one shell, force repeated initialization, or permanently
append guessed paths to the user's shell profile.

Environment changes live only in that process and its children. If each shell
call starts fresh, source the setup and execute the build/run in the **same**
invocation, or supply the captured required environment explicitly. Executing
`bash setvars.sh` in a child does not initialize the calling shell.

On Windows, use the installed oneAPI command prompt or `cmd.exe`:

```bat
call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
icx-cl --version
sycl-ls
```

A `.bat` launched from PowerShell does not automatically modify the parent
PowerShell environment. Run the build in the initialized `cmd.exe` session;
match its Visual Studio/MSVC host prerequisites to the compiler release.

Official layout references: [Linux environment scripts](https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2025-1/use-the-setvars-script-with-linux.html),
[Windows environment scripts](https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2025-1/use-the-setvars-script-with-windows.html).
These links are versioned; use the version corresponding to the installation.

## If installation is needed

Distinguish these independently installed parts:

| Missing part | What to establish |
|---|---|
| Compiler / C++ host toolchain | OS/architecture support and required host compiler/SDK |
| SYCL runtime / UR adapter | Runtime matching the compiler and desired backend |
| Level Zero loader | Loader library alone does not contain a GPU implementation |
| GPU user-mode driver | Supported GPU and OS/driver combination |
| Kernel/device access | Working host driver and access to render nodes |
| Library | CPU/GPU backend, ABI and package matching the application |
| Profiler or migration tool | Separate optional tool, not required for an ordinary compile |

Use Intel's [toolkit download selector](https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkits.html)
and [GPU driver installation guide](https://dgpu-docs.intel.com/driver/installation.html)
for the user's current OS and release. Inspect package manager candidates before
installing; don't embed stale repository keys, distribution codenames, package
versions or promises that one giant package installs every component.

Use an existing container, remote build host or supported Linux/Windows machine
when the local OS cannot run the requested target. macOS documentation search and
some CPU libraries remain useful; do not assume an Intel GPU execution stack on
Apple silicon, or silently substitute a CPU workload for requested GPU evidence.

## Enumerate before selecting

```bash
sycl-ls
ONEAPI_DEVICE_SELECTOR=level_zero:gpu sycl-ls
```

The second command restricts enumeration; it does not install or repair a device.
Run with the user's existing environment first. If a filter may be hiding the
hardware, compare in a fresh subprocess without `ONEAPI_DEVICE_SELECTOR` and the
legacy `SYCL_DEVICE_FILTER`; preserve the original values in the report.

`ONEAPI_DEVICE_SELECTOR=level_zero:gpu` chooses a backend and device class. For a
particular device, copy the actual backend/index token reported by `sycl-ls` and
check the program's printed identity. Indices can change with driver, filtering
and topology. The same GPU can appear via both OpenCL and Level Zero. A default
selector need not choose the intended GPU.

Read [the exact selector grammar](../docs/upstream/llvm/sycl/doc/EnvironmentVariables.md)
for multiple filters, exclusions or tile/subdevice syntax. Quote semicolons and
wildcards. Do not mix modern and deprecated selector variables casually.

## Linux and containers

Inspect `/dev/dri/renderD*`, effective group membership and device permissions.
A container needs a compatible host driver, exposed device nodes, appropriate
groups and user-space runtimes. Installing a kernel driver inside the container
will not repair an absent host device. Avoid `--privileged` or `chmod 777` as
first-line fixes. Use the existing cluster scheduler/device assignment.

`sycl-ls` showing a device proves enumeration only. Run the explicit-device smoke
example to establish compilation, dispatch, completion and checked output.

Primary bundled sources:

- [DPC++ getting started](../docs/upstream/llvm/sycl/doc/GetStartedGuide.md)
- [DPC++ environment variables](../docs/upstream/llvm/sycl/doc/EnvironmentVariables.md)
- [Compute Runtime overview](../docs/upstream/compute-runtime/README.md)
- [Level Zero loader overview](../docs/upstream/level-zero/README.md)
