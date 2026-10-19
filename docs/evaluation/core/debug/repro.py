"""Disposable concurrency repro; never touches network or production data."""
import argparse
import hashlib
import json
from pathlib import Path
import threading
from worker import process

p = argparse.ArgumentParser()
p.add_argument("--mode", choices=["sequential", "race"], required=True)
p.add_argument("--attempts", type=int, default=10)
args = p.parse_args()
results=[]
for trial in range(args.attempts):
    seen=set()
    effects=[]
    statuses=[]
    if args.mode == "sequential":
        statuses=[process("order-17:v1", seen, effects), process("order-17:v1", seen, effects)]
    else:
        barrier=threading.Barrier(2, timeout=2)
        errors=[]
        def run():
            try:
                statuses.append(process("order-17:v1", seen, effects, before_effect=barrier.wait))
            except BaseException as exc:
                errors.append(repr(exc))
        threads=[threading.Thread(target=run) for _ in range(2)]
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=3)
        if errors or any(thread.is_alive() for thread in threads):
            print(json.dumps({"setup_errors":errors,"trial":trial}))
            raise SystemExit(2)
    results.append({"trial":trial,"effects":effects,"statuses":statuses,"expected_effect_count":1})
failures=sum(len(row["effects"]) != 1 for row in results)
print(json.dumps({"target_sha256":hashlib.sha256(Path("worker.py").read_bytes()).hexdigest(),"mode":args.mode,"attempts":args.attempts,"duplicate_failures":failures,"results":results},indent=2))
raise SystemExit(1 if failures else 0)
