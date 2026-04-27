"""
Demo job script. simulates a 10-second task.
Prints BP_PROGRESS=<n> every second so BatcherWidget can track progress.
"""

import sys
import time

STEPS = 100
time.sleep(3)

print("Starting demo job...")
for step in range(1, STEPS + 1):
    time.sleep(0.02)
    pct = int(step / STEPS * 100)
    print(f"Step {step}/{STEPS} complete.")
    print(f"BLUEPEPPER_BATCHER_PROGRESS={pct}")
    if pct > 50:
        raise RuntimeError("JAJ")


print("[Job Done.")
sys.exit(0)
