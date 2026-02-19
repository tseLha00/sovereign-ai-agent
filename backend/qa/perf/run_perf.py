import argparse
import json
import time
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import httpx


def percentile(sorted_vals, p: float):
    if not sorted_vals:
        return None
    k = int((len(sorted_vals) - 1) * p)
    return sorted_vals[k]


def detect_repo_root() -> Path:
    # run_perf.py is at backend/qa/perf/run_perf.py -> parents[3] is repo root
    return Path(__file__).resolve().parents[3]


def git_rev(repo_root: Path) -> str | None:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(repo_root))
        return out.decode().strip()
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/v1/chat/completions")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    payload = {"model": "apertus-8b", "messages": [{"role": "user", "content": "Hello"}]}

    lock = threading.Lock()
    latencies_ms: list[int] = []
    status_codes: dict[str, int] = {}
    errors = 0

    def do_one():
        nonlocal errors
        start = time.perf_counter()
        try:
            with httpx.Client() as client:
                r = client.post(args.url, json=payload, timeout=30)
            elapsed = int((time.perf_counter() - start) * 1000)

            with lock:
                latencies_ms.append(elapsed)
                status_codes[str(r.status_code)] = status_codes.get(str(r.status_code), 0) + 1
                if r.status_code >= 400:
                    errors += 1
        except Exception:
            with lock:
                errors += 1

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [ex.submit(do_one) for _ in range(args.requests)]
        for _ in as_completed(futures):
            pass
    total = time.perf_counter() - t0

    lat_sorted = sorted(latencies_ms)

    repo_root = detect_repo_root()
    rev = git_rev(repo_root)

    result = {
        "timestamp": int(time.time()),
        "datetime": datetime.now().isoformat(timespec="seconds"),
        "git_rev": rev,
        "url": args.url,
        "requests": args.requests,
        "concurrency": args.concurrency,
        "total_time_s": round(total, 3),
        "throughput_rps": round(args.requests / total, 2) if total > 0 else None,
        "success": args.requests - errors,
        "errors": errors,
        "latency_ms": {
            "min": lat_sorted[0] if lat_sorted else None,
            "mean": round(sum(lat_sorted) / len(lat_sorted), 2) if lat_sorted else None,
            "median": percentile(lat_sorted, 0.5),
            "p90": percentile(lat_sorted, 0.9),
            "p95": percentile(lat_sorted, 0.95),
            "max": lat_sorted[-1] if lat_sorted else None,
        },
        "status_codes": status_codes,
        "payload": payload,
    }

    out_path = args.out
    if out_path is None:
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = repo_root / "evidence" / "perf"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = str(out_dir / f"{ts}_results.json")

    Path(out_path).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
