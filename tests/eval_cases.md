# Behavioral evaluation cases

Use the completed skill with these prompts in fresh agent sessions. These are
evaluation inputs and acceptance criteria, **not recorded agent test results**.
The automated tests exercise helpers, corpus integrity and retrieval; they do not
measure automatic skill triggering or end-to-end agent behavior.

## Trigger and routing

| Prompt | Expected selection / route |
|---|---|
| Build my vector addition kernel with icpx on an Intel GPU. | oneapi; build and environment |
| Why does my SYCL program sometimes read stale USM output? | oneapi; SYCL dependencies |
| Where is ONEAPI_DEVICE_SELECTOR documented? | oneapi; direct offline lookup, no environment probe |
| Find the oneMath GEMM signature and leading-dimension rules. | oneapi; math docs |
| Help migrate this CUDA project using c2s. | oneapi; migration |
| Profile transfers and kernels with unitrace. | oneapi; performance |
| My program loads the wrong Level Zero driver. | oneapi; runtime diagnostics |
| Use ifx to offload this Fortran loop. | oneapi; OpenMP and versioned compiler guide |
| Does sklearnex actually run this estimator on the GPU? | oneapi; support matrix and execution evidence |
| oneCCL hangs with four ranks. | oneapi; API version, mapping, collective ordering |
| Write a generic REST endpoint. | Do not select oneapi |
| Flash the firmware and reset this GPU with xpu-smi. | Administration task outside this skill |
| Optimize a CUDA-only kernel without porting it. | No automatic oneapi selection |

## Offline task exercises

1. **Missing GPU on a Mac:** "Run this SYCL GPU smoke test here." Supply the
   actual probe output. Expect tool/OS blockers, no CPU success relabeled as GPU,
   and no invented execution result or wholesale toolkit install.
2. **Out-of-order USM:** Supply a queue with unrelated memcpy/kernel/memcpy
   submissions and an early free. Expect explicit dependencies and lifetime/error
   handling, with references to USM/queue semantics.
3. **Library identity:** Supply `<oneapi/mkl.hpp>` source and ask to use open
   oneMath. Expect verified API/backend/CMake changes, not a package-name-only edit.
4. **Unavailable extension:** Ask whether an experimental graph document proves
   the installed older compiler implements it. Expect version/macro/capability
   checking and a distinction between proposed, experimental and supported APIs.
5. **Timing:** Supply a timer ending immediately after `q.submit`. Expect an
   explanation of enqueue versus completed work and an appropriate measurement.
6. **Migration:** Supply source plus stale/empty compile_commands.json. Expect
   rebuilding the database and reviewing generated diagnostics; tool exit zero
   is not accepted as a validated port.

## Hardware-dependent acceptance (not run on the authoring Mac)

On a supported host with a selected toolkit: compile the bundled smoke example,
run `--device gpu` on the enumerated backend, inspect printed identity and require
zero exit plus all 4096 outputs checked. A nonexistent backend/device must fail.
Run the CPU variant only if a CPU runtime exists. Validate representative library
and migration workflows against their installed versions before claiming those
paths are execution-tested.
