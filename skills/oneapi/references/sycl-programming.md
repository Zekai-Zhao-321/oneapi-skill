# SYCL programming decisions

Use SYCL 2020 for new code unless the project's compiler contract says otherwise.
The [SYCL reference index](../docs/indexes/SYCL-Reference.md) covers standard APIs;
Intel extensions live separately in `docs/upstream/llvm/sycl/doc/extensions/`.

## Execution model

A queue binds a device and context. A submitted command group describes a kernel
or operation and its dependencies. Submission is asynchronous. Captured kernel
values must be device-copyable; host-only objects, I/O and arbitrary host pointers
are not generally usable inside a device kernel.

Use an explicit selector for a requested device class. Query aspects before
requiring `fp64`, `fp16`, shared/device USM or atomics. Query limits rather than
hard-coding a maximum work-group size or subgroup width. Print the selected
device/platform/driver in repros so host fallback or a different GPU is visible.

Read [queue](../docs/upstream/SYCL-Reference/source/iface/queue.rst),
[device](../docs/upstream/SYCL-Reference/source/iface/device.rst) and
[defining kernels](../docs/upstream/SYCL-Reference/source/iface/defining-kernels.rst).

## Choose a memory model

| Model | Good fit | Dependency and lifetime obligation |
|---|---|---|
| Buffers/accessors | Let runtime infer access dependencies | Declare correct read/write modes; synchronize host access with a host accessor or buffer lifetime |
| Device USM | Explicit transfers and device-resident working sets | Host cannot dereference; connect copy/kernel/copy events; free after completion |
| Shared USM | Pointer-based code with host/device access | Query support; avoid races; migrations still cost time; host reads need synchronization |
| Host USM | Host allocation accessible to supported devices | Query support; device access may be remote/slow; same ordering/lifetime obligations |

A raw pointer captured in a lambda does **not** tell the scheduler what it reads
or writes. Two commands using the same USM pointer are not automatically ordered.
An in-order queue orders that queue's commands, not all queues in the process.

For a USM pipeline, preserve this dependency graph on an out-of-order queue:

```cpp
// Preconditions: q's context owns d_in/d_out; h_in/h_out are valid host arrays;
// n > 0, all sizes are checked, and all allocations outlive the final event.
auto upload = q.memcpy(d_in, h_in, n * sizeof(float));
auto kernel = q.submit([&](sycl::handler& h) {
    h.depends_on(upload);
    h.parallel_for(sycl::range<1>{n}, [=](sycl::id<1> i) {
        d_out[i] = 2.0f * d_in[i];
    });
});
auto download = q.submit([&](sycl::handler& h) {
    h.depends_on(kernel);
    h.memcpy(h_out, d_out, n * sizeof(float));
});
download.wait_and_throw();
// Now validate h_out. Free USM with the owning context after all users finish.
```

In complete code, check allocation failures, handle asynchronous exceptions and
use cleanup that respects pending operations. `sycl::free` does not wait for
outstanding users. Keep host source/destination arrays alive during async copies.
Do not pass an allocation from an unrelated context just because the device name
matches. For multiqueue dependencies, first establish compatible contexts and the
API's dependency rules.

Read [USM allocation](../docs/upstream/SYCL-Reference/source/iface/usm_allocations.rst),
[command groups](../docs/upstream/SYCL-Reference/source/iface/command-group-handler.rst)
and [buffers](../docs/upstream/SYCL-Reference/source/iface/buffer.rst).

## Errors must reach the result

Handle synchronous `sycl::exception` around queue construction/submission and
asynchronous errors through the queue's `async_handler` plus synchronization such
as `wait_and_throw()`. A handler that only logs and returns can make broken work
look successful. Accumulate an error status or propagate it and prevent a PASS
result. `assets/sycl-smoke/smoke.cpp` demonstrates status propagation and checking.

Read [async_handler](../docs/upstream/SYCL-Reference/source/iface/async_handler.rst).
A successful `wait()` alone is not evidence that errors were surfaced or output
was correct.

## Work-groups, barriers and reductions

- Use `range` when explicit local layout is unnecessary. For `nd_range`, make
  global/local sizes valid for the dimensions and device. Pad and bounds-check
  when needed; handle empty workloads on the host before invalid launches.
- A work-group barrier is collective: all participating work-items must reach it
  consistently. A bounds guard around an entire kernel can deadlock a padded
  work-group if it makes some items skip a barrier.
- Local memory is per work-group; its initialization and reuse need the correct
  barriers. There is no ordinary whole-grid barrier inside a kernel. Use separate
  kernel submissions and event dependencies for global phases.
- Prefer group algorithms or `sycl::reduction` when their semantics fit. Verify
  identity, initialization and update behavior; account for floating-point order.
- Choose atomic memory order/scope for the algorithm and device capabilities.
  Atomics are not a replacement for every producer-consumer dependency.

Search `nd_range`, `local_accessor`, `group_barrier`, `reduction`, `atomic_ref` in
the SYCL-Reference project for the exact overload and restrictions.

## Extensions and advanced features

Use command graphs, joint matrix, ESIMD or native interop only when justified by
the workload and available implementation. Read the extension's status, required
aspects/macros, constraints and supported types for the installed release.
A proposed extension's presence in this bundle does not mean it is implemented.

A native handle is not an ownership transfer by default. Respect context,
synchronization and lifetime rules of `get_native`/`make_*`/`interop_handle` and
the selected backend. Read the backend interop page and Level Zero API as needed.

First build a correct standard implementation; measure before introducing a
hardware-specific path, and maintain a fallback only when the user's portability
requirements call for one.
