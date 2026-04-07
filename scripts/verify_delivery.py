#!/usr/bin/env python3
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
BASE_URL = "http://127.0.0.1:8000"


class VerifyError(Exception):
    """Verification step failed."""


def write_json(filename: str, payload: Any) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    (OUTPUTS / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def request_json(method: str, url: str, payload: Optional[Dict[str, Any]] = None, timeout: int = 30) -> Any:
    body = None
    headers = {}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, method=method, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise VerifyError(f"HTTP {exc.code} {method} {url}: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise VerifyError(f"Network error {method} {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise VerifyError(f"Invalid JSON from {method} {url}: {exc}") from exc


def wait_backend_ready(base_url: str, timeout_seconds: int = 45) -> bool:
    start = time.time()
    while time.time() - start < timeout_seconds:
        try:
            request_json("GET", f"{base_url}/api/health", timeout=3)
            return True
        except Exception:
            time.sleep(1)
    return False


def main() -> int:
    backend_proc: Optional[subprocess.Popen] = None
    try:
        if not wait_backend_ready(BASE_URL, timeout_seconds=3):
            OUTPUTS.mkdir(parents=True, exist_ok=True)
            log_file = OUTPUTS / "backend_start.log"
            with log_file.open("w", encoding="utf-8") as logf:
                backend_proc = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
                    cwd=ROOT,
                    stdout=logf,
                    stderr=logf,
                )
            if not wait_backend_ready(BASE_URL, timeout_seconds=45):
                raise VerifyError("check_backend failed: backend not reachable after auto-start")

        health = request_json("GET", f"{BASE_URL}/api/health")
        write_json("health_check.json", health)

        config = request_json("GET", f"{BASE_URL}/api/config")
        write_json("config_check.json", config)

        run_payload = {
            "query": "我们在美国推出EchoNova音箱，商标风险是什么？",
            "agent_type": "qa",
            "extra_params": {"country": "US", "top_k": 4},
        }
        run_qa = request_json("POST", f"{BASE_URL}/api/run", run_payload, timeout=60)
        write_json("run_qa.json", run_qa)

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
