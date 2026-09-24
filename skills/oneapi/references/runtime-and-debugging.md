# Runtime diagnosis and native interop

## Locate the failing layer

For a typical Intel GPU SYCL application:

```text
Application / library
  -> SYCL runtime
  -> Unified Runtime loader + selected adapter
  -> Level Zero loader -> Intel GPU user-mode driver -> kernel/device
                         (or another backend such as OpenCL)
```

IGC compiles device code for Intel graphics; it is not the SYCL host compiler.
Level Zero loader installation alone does not install a GPU driver. UMF provides
allocation machinery; it is not a command scheduler or proof of memory coherence.

Modern UR development is under `intel/llvm/unified-runtime`. The standalone
`oneapi-src/unified-runtime` checkout is a mirror. This bundle uses the intel/llvm
copy so its SYCL and UR docs share a revision. Don't assume an older installed
SYCL runtime uses the same trace variables or adapter defaults.

## Reproduce in stages

1. Capture the exact failing command, stderr, exit status and relevant tool/driver
   versions. Preserve the original environment before altering a filter or path.
2. Inspect compiler selection and library resolution; run `sycl-ls` in the same
   initialized shell/environment as the application.
3. Run the bundled explicit-device smoke test on the requested device. If that
   fails too, reduce to the stack/environment; if it passes, focus on the app's
   dependencies, memory, kernels and library use.
4. Enable a narrowly targeted trace for one bounded repro. Save it to a file and
   read the relevant region; don't stream an entire production trace into context.
5. Fix one cause, rerun the correctness check, then remove diagnostic settings
   before measuring performance.

For binaries you built/trust, `ldd` on Linux or the platform's dependency tools
can reveal libraries from mixed toolkit installations. Prefer passive inspection
such as `readelf -d` for an unknown executable; don't run arbitrary binaries merely
to inspect their dependencies.

## Tracing

The bundled [environment variable guide](../docs/upstream/llvm/sycl/doc/EnvironmentVariables.md)
defines `SYCL_UR_TRACE`: 1 = discovery, 2 = UR calls, -1 = all. Confirm availability
in the installed version, then use a process-scoped setting:

```bash
SYCL_UR_TRACE=1 ONEAPI_DEVICE_SELECTOR=level_zero:gpu ./sycl-smoke --device gpu
```

UR logging uses a different grammar, for example:

```bash
UR_LOG_LOADER='level:info;output:stderr' ./app
```

Read [UR INTRO.rst](../docs/upstream/llvm/unified-runtime/scripts/core/INTRO.rst)
for exact log fields, validation/tracing layers and adapter settings. Do not
blindly substitute historical `SYCL_PI_TRACE` or assume every `UR_*` setting is
recognized. Unsupported environment variables can be silently inert.

## Symptom routing

| Symptom | First evidence / next step |
|---|---|
| Compiler missing or header not found | Environment initialization, actual executable path, compiler version |
| No platform/device | Active filters, runtime/adapter/driver presence, render-node access, container assignment |
| Unexpected CPU or duplicate GPU | Default selector, backend choice, app-reported device identity |
| Adapter/driver load failure | Dependency paths and ABI; trace the loader before reinstalling unrelated packages |
| Device image/kernel build error | Requested target, extensions/aspects, driver/IGC compatibility, minimal kernel |
| Invalid memory access | Allocation type/context, bounds, pointer capture, dependencies, allocation lifetime |
| Stale or intermittent output | Missing USM events, host access before completion, premature buffer/USM release |
| Hang at a kernel/collective | Divergent barriers, dependency cycle, rank mismatch, hardware/driver event logs |
| Tile count or memory changes | Root versus subdevice enumeration and backend/driver exposure |
| Performance regression only under trace | Instrumentation overhead, serialization and cache effects |

Read [MultiTileCardWithLevelZero.md](../docs/upstream/llvm/sycl/doc/MultiTileCardWithLevelZero.md)
for topology semantics. Never equate a tile index with a stable PCI identity or
assume allocations are interchangeable across contexts or tiles.

Device sanitizers and validation layers are release/backend-specific. Search the
compiler/runtime docs and installed help before selecting ASan/TSan/MSan flags;
a host sanitizer alone does not establish GPU-memory correctness.

## Level Zero programming

Use [level-zero-spec](../docs/indexes/level-zero-spec.md) for the API programming
model/schema and [level-zero headers](../docs/indexes/level-zero.md) for generated
function declarations. These projects are independently versioned: match the
installed header/runtime API version when constructing native code.

- Distinguish compute `ze*`, tools `zet*` and system management `zes*` APIs.
- Enumerate drivers/devices and create resources with the matching context.
- Initialize required descriptor `stype`, `pNext` and other fields correctly;
  do not assume every descriptor has identical fields or enum values.
- Check every return code, enumeration count and capability required by the task.
- Use command queue/list/event semantics explicitly. Regular and immediate lists
  differ; submission is not completion. Use the appropriate synchronization call.
- Keep allocations, events, command resources and imported/native handles alive
  until their last use completes. Respect ownership rules across SYCL interop.
- Use the documented extension/version discovery before calling optional entrypoints.

`zes*` discovery and metric access do not authorize reset, power/frequency changes
or firmware updates. Those are a different administration task.

## Timeouts and recovery evidence

Bound an unknown repro with a supported external timeout or process controller.
Record timeout separately from application exit. Terminating the host process
alone does not prove the GPU is idle or healthy. Inspect process/device/driver
state before another workload; avoid repeating a hung test in a loop. Preserve
logs rather than automatically resetting the GPU or clearing error counters.
