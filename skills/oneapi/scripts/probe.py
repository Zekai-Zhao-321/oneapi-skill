#!/usr/bin/env python3
"""Read-only tool/environment inventory. Does not install, source scripts or run workloads."""
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

COMMANDS = {
    "icpx": ["--version"], "icx": ["--version"], "icx-cl": ["--version"],
    "ifx": ["--version"], "dpcpp": ["--version"], "clang++": ["--version"],
    "cmake": ["--version"], "sycl-ls": [], "c2s": ["--version"], "dpct": ["--version"],
}
VARIABLES = ("ONEAPI_ROOT", "CMPLR_ROOT", "MKLROOT", "TBBROOT", "DPL_ROOT", "DALROOT",
             "CCL_ROOT", "DNNLROOT", "ONEAPI_DEVICE_SELECTOR", "SYCL_DEVICE_FILTER",
             "SYCL_UR_TRACE", "SYCL_PI_TRACE", "SYCL_CACHE_PERSISTENT", "OMP_TARGET_OFFLOAD")


def inspect_tool(name, args, timeout):
    executable = shutil.which(name)
    if executable is None:
        return {"status": "missing"}
    result = {"path": executable, "command": [executable, *args]}
    # Files avoid accumulating arbitrarily large subprocess output in memory.
    with tempfile.TemporaryFile() as output:
        try:
            run = subprocess.run([executable, *args], stdin=subprocess.DEVNULL, stdout=output,
                                 stderr=subprocess.STDOUT, timeout=timeout, check=False)
            result.update(status="ok" if run.returncode == 0 else "error", exit_code=run.returncode)
        except subprocess.TimeoutExpired:
            result.update(status="timeout")
        except OSError as exc:
            result.update(status="error", error=str(exc))
        output.seek(0)
        data = output.read(16001)
        result.update(output=data[:16000].decode(errors="replace"), truncated=len(data) > 16000)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=10, help="Seconds per tool, default 10")
    parser.add_argument("--skip-devices", action="store_true", help="Do not invoke sycl-ls")
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("--timeout must be in (0, 60]")
    report = {"os": platform.system(), "release": platform.release(), "architecture": platform.machine(),
              "environment": {k: os.environ[k] for k in VARIABLES if k in os.environ},
              "tools": {name: inspect_tool(name, command, args.timeout) for name, command in COMMANDS.items()
                        if not (args.skip_devices and name == "sycl-ls")},
              "note": "Tool discovery is not compilation or device-execution validation. clang++ may be a non-SYCL compiler."}
    dri = Path("/dev/dri")
    if platform.system() == "Linux" and dri.is_dir():
        report["render_nodes"] = [{"path": str(p), "readable": os.access(p, os.R_OK), "writable": os.access(p, os.W_OK)}
                                  for p in sorted(dri.glob("renderD*"))]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
