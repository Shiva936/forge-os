#!/usr/bin/env python3
"""Refresh .forge/config.json runtime capability cache."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def _default_config() -> dict:
    return {
        "format": 1,
        "policy": {
            "scope": "forge-runtime-execution-only",
            "stores_commands_or_scripts": False,
            "allows_autonomous_key_additions": True,
        },
        "last_refreshed_utc": None,
        "runtime": {},
        "notes": (
            "Runtime config cache only. Refresh with .forge/scripts/refresh_runtime_config.py. "
            "Keys may be added autonomously in future; values are environment hints and must be "
            "rechecked when context changes."
        ),
    }


def _run_capture(command: list[str]) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except Exception:
        return 1, ""
    return completed.returncode, completed.stdout or ""


def _detect_wsl() -> tuple[bool, list[str]]:
    code, output = _run_capture(["wsl", "-l", "-q"])
    if code != 0:
        return False, []
    cleaned = output.replace("\x00", "")
    distros = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return True, distros


def build_runtime(repo_root: Path) -> dict:
    host_os = platform.system().lower()
    wsl_available, distros = _detect_wsl() if host_os == "windows" else (False, [])
    return {
        "host_os": host_os,
        "host_shell": "powershell" if host_os == "windows" else "sh",
        "wsl_available": wsl_available,
        "wsl_distros": distros,
        "docker_available": shutil.which("docker") is not None,
        "rancher_desktop_available": shutil.which("rdctl") is not None,
        "forge_venv_available": (repo_root / ".venv").exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh .forge/config.json runtime capability cache")
    parser.add_argument("--repo-root", default=".", help="Repository root (default: current directory)")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    config_path = repo_root / ".forge" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        data = _default_config()

    data["last_refreshed_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    data["runtime"] = build_runtime(repo_root)

    with config_path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")

    print(f"Updated {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
