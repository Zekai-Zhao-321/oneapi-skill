# Performance measurement and profiling

Begin with a correct executable and a specific question: host overhead, transfers,
kernel throughput, memory bandwidth, layout/reorder cost, scheduling or collective
communication. Preserve workload dimensions, dtype, algorithm and accuracy goal.

## Establish a comparable baseline

Record compiler/options, library versions, GPU/backend/driver, input size/layout,
thread/rank/device mapping and timing method. Warm up deliberately when reporting
steady state; report first-use/JIT/setup cost separately if it matters. Use
repeated samples and report variability, not a single favorable timing.

A wall-clock measurement around asynchronous submission measures enqueue time
unless it waits for completion. Separate:

- End-to-end time, including required transfers and synchronization.
- Device kernel/event time.
- One-time context creation, JIT, allocation or primitive construction.

For queue event timing, check `sycl::aspect::queue_profiling` and create the queue
with `sycl::property::queue::enable_profiling`. After completion, read event
`command_start` and `command_end` through `get_profiling_info`; their difference is
in nanoseconds. It is not the complete application's wall time. Do not compare
unrelated device clocks as if they shared an epoch. Read the SYCL reference
[queue page](../docs/upstream/SYCL-Reference/source/iface/queue.rst) and search
`command_start` for exact event semantics.

## Select an instrument

| Question | Tool / source |
|---|---|
| Which kernels or transfers dominate? | `unitrace --device-timing`; [unitrace guide](../docs/upstream/pti-gpu/tools/unitrace/README.md) |
| Are host submissions/transfers overlapping? | unitrace host/device Chrome-format traces |
| Hardware metrics, stalls, sampling | unitrace/oneprof or PTI SDK; check supported device and permission requirements |
| Production instrumentation via API | [PTI SDK](../docs/upstream/pti-gpu/sdk/README.md) and its bundled headers |
| oneDNN dispatch, reorders, primitive creation | oneDNN verbose/benchdnn |
| Application/CPU/GPU system analysis | Installed Intel VTune; use its versioned guide and local help |
| Roofline/offload analysis | Intel Advisor where supported; use its versioned guide |

For an installed unitrace, verify `unitrace --help` first, then a short run:

```bash
unitrace --device-timing ./app
unitrace --chrome-call-logging --chrome-kernel-logging -o ./trace ./app
```

Check the tool's reported output filenames rather than assuming the `-o` basename
is the final trace name. The bundled guide also covers format choices and SYCL,
UR, MPI and library tracing. Older binaries may not have newer options.

Metrics collection can require permissions/configuration beyond ordinary workload
execution and can alter timing or serialize work. Report a permissions blocker
instead of silently changing system-wide profiling settings. Kernel timing or
logging may still work when hardware counters do not. Keep diagnostic traces
separate from performance baselines and bound captures to the relevant phase.

## Optimize the observed bottleneck

| Observation | Candidate change to measure |
|---|---|
| Transfers dominate | Retain data on device; avoid round trips; batch work; inspect shared-USM migrations |
| Many tiny kernels | Fuse appropriate operations, batch submissions; consider supported command graphs |
| Poor memory access | Align layout with coalesced access; remove unnecessary gathers/reorders |
| Excess allocations/setup | Reuse workspace, allocations or primitive descriptors with correct lifetimes |
| Kernel compute bottleneck | Suitable library, vectorization, subgroup/local-memory design, precision only if allowed |
| Host oversubscription | Coordinate TBB/OpenMP/BLAS threads and MPI ranks |
| Inter-device communication | Check rank mapping, topology, collective choice and overlap |

Change one cause at a time, rerun the same correctness check and compare the same
timing scope. Don't hard-code a work-group/subgroup width or copy tuning knobs
from another GPU generation without evidence. A layout optimization or reduced
precision can change semantics; report that change explicitly.

The compiler's persistent cache and in-memory cache are distinct. Search
`SYCL_CACHE_PERSISTENT` and `SYCL_CACHE_IN_MEM` in the environment docs; do not delete
a user's global cache as a routine benchmark step. If cold-cache behavior is
required, use a task-specific cache location and record the setup.

## Conclude with a bounded claim

A useful report states the actual device and workload, before/after timings,
repetitions/variability, timing scope, numerical check and profiler finding that
motivated the change. If no compatible hardware exists, provide the profiling
commands and hypotheses while labeling them unmeasured.
