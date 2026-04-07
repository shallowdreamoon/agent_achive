#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"


class HttpFailure(Exception):
    pass


def write_json(name: str, payload: Any) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    (OUTPUTS / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def call_json(method: str, url: str, *, json_payload: Optional[Dict[str, Any]] = None, timeout: int = 120) -> Any:
    body = None
    headers = {}
    if json_payload is not None:
        body = json.dumps(json_payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url=url, method=method, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="ignore")
        raise HttpFailure(f"HTTP {exc.code} at {method} {url} body={raw[:400]}") from exc


def wait_for_backend(base_url: str, timeout_seconds: int = 45) -> bool:
    start = time.time()
    while time.time() - start <= timeout_seconds:
        try:
            call_json("GET", f"{base_url}/api/health", timeout=3)
            return True
        except Exception:  # noqa: BLE001
            time.sleep(1)
    return False


def step(name: str, func):
    try:
        return func()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"{name} failed: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify demo delivery and write runtime evidence files.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Backend API base URL.")
    parser.add_argument("--start-backend", action="store_true", help="Auto start uvicorn if backend is not reachable.")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    backend_proc: Optional[subprocess.Popen] = None
    backend_log = OUTPUTS / "backend_start.log"

    try:
        if not wait_for_backend(base_url, timeout_seconds=3):
            if not args.start_backend:
                print("FAIL: step=check_backend detail=backend not reachable (use --start-backend to auto start)")
                return 1
            OUTPUTS.mkdir(parents=True, exist_ok=True)
            with backend_log.open("w", encoding="utf-8") as logf:
                backend_proc = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
                    cwd=ROOT,
                    stdout=logf,
                    stderr=logf,
                )
            if not wait_for_backend(base_url, timeout_seconds=45):
                print(f"FAIL: step=start_backend detail=backend failed to start, see {backend_log}")
                return 1

        step("get_health", lambda: write_json("health_check.json", call_json("GET", f"{base_url}/api/health")))
        step("get_config", lambda: write_json("config_check.json", call_json("GET", f"{base_url}/api/config")))

        run_payloads = {
            "run_qa.json": {
                "query": "我们在美国推出EchoNova音箱，商标风险是什么？",
                "agent_type": "qa",
                "extra_params": {"country": "US", "top_k": 4},
            },
            "run_layout.json": {
                "query": "我们的电池管理算法将在美国和加拿大商用，如何规划专利布局？",
                "agent_type": "layout",
                "extra_params": {"country": "US,CA", "top_k": 4},
            },
            "run_litigation.json": {
                "query": "收到美国NPE专利警告函，应诉路径是什么？",
                "agent_type": "litigation",
                "extra_params": {"country": "US", "top_k": 4},
            },
        }
        for filename, payload in run_payloads.items():
            step(f"post_{filename}", lambda f=filename, p=payload: write_json(f, call_json("POST", f"{base_url}/api/run", json_payload=p)))

        benchmark = step("post_benchmark", lambda: call_json("POST", f"{base_url}/api/benchmark/run", timeout=300))
        write_json("benchmark_summary.json", benchmark["summary"])
        write_json("benchmark_results.json", benchmark["detailed_results"])

        print("PASS")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}")
        return 1
    finally:
        if backend_proc is not None:
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                backend_proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
