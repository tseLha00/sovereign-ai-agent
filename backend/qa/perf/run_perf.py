import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from threading import Lock

import httpx


def percentile(sorted_vals, p: float):
    if not sorted_vals:
        return None
    k = int((len(sorted_vals) - 1) * p)
    return sorted_vals[k]


def find_repo_root(start: Path) -> Path:
    """
    Walk upwards until we find a directory that contains both backend/ and docs/.
    This matches your repo layout:
      sovereign-ai-agent/
        backend/
        docs/
        evidence/
        frontend/
        models/
    """
    start = start.resolve()
    for p in [start] + list(start.parents):
        if (p / "backend").is_dir() and (p / "docs").is_dir():
            return p
    # fallback: if structure changes, use a reasonable parent
    return start.parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/v1/chat/completions")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--out", default=None, help="Output path. Relative paths resolve from repo root.")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__))
    evidence_perf_dir = repo_root / "evidence" / "perf"
    evidence_perf_dir.mkdir(parents=True, exist_ok=True)

    payload = {"model": "apertus-8b", "messages": [{"role": "user", "content": "Hello"}]}

    latencies_ms: list[int] = []
    status_codes: dict[str, int] = {}
    errors = 0
    lock = Lock()

    def do_one(client: httpx.Client):
        nonlocal errors
        start = time.perf_counter()
        try:
            r = client.post(args.url, json=payload, timeout=30)
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            with lock:
                latencies_ms.append(elapsed_ms)
                code = str(r.status_code)
                status_codes[code] = status_codes.get(code, 0) + 1
                if r.status_code >= 400:
                    errors += 1
        except Exception:
            with lock:
                errors += 1

    t0 = time.perf_counter()
    with httpx.Client() as client, ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [ex.submit(do_one, client) for _ in range(args.requests)]
        for _ in as_completed(futures):
            pass
    total = time.perf_counter() - t0

    lat_sorted = sorted(latencies_ms)
    result = {
        "timestamp": int(time.time()),
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
        "meta": {
            "repo_root": str(repo_root),
            "default_output_dir": str(evidence_perf_dir),
        },
    }

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = repo_root / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_path = evidence_perf_dir / f"{ts}_results.json"

    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
