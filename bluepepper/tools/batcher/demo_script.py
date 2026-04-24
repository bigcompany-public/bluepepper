"""
Demo job script. simulates a 10-second task.
Prints BP_PROGRESS=<n> every second so BatcherWidget can track progress.
"""

import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("--id", default="?")
args = parser.parse_args()

STEPS = 10

print(f"[Job {args.id}] Starting demo job...")
sys.stdout.flush()

for step in range(1, STEPS + 1):
    time.sleep(1)
    pct = int(step / STEPS * 100)
    print(f"[Job {args.id}] Step {step}/{STEPS} complete.")
    sys.stdout.flush()
    print(f"BP_PROGRESS={pct}")
    sys.stdout.flush()

print(f"[Job {args.id}] Done.")
sys.stdout.flush()
sys.exit(0)
