import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
from pathlib import Path
from datetime import datetime

def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    k = int((len(sorted_vals) - 1) * p)
    return sorted_vals[k]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000/v1/chat/completions")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    payload = {"model": "apertus-8b", "messages": [{"role": "user", "content": "Hello"}]}
    latencies_ms = []
    status_codes = {}
    errors = 0

    def do_one(client: httpx.Client):
        nonlocal errors
        start = time.perf_counter()
        try:
            r = client.post(args.url, json=payload, timeout=30)
            elapsed = (time.perf_counter() - start) * 1000
            latencies_ms.append(int(elapsed))
            status_codes[str(r.status_code)] = status_codes.get(str(r.status_code), 0) + 1
            if r.status_code >= 400:
                errors += 1
        except Exception:
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
    }

    out_path = args.out
    if out_path is None:
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        Path("evidence/perf").mkdir(parents=True, exist_ok=True)
        out_path = f"evidence/perf/{ts}_results.json"

    Path(out_path).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\nSaved to: {out_path}")

if __name__ == "__main__":
    main()
