"""
Demo job script. simulates a 10-second task.
Prints BP_PROGRESS=<n> every second so BatcherWidget can track progress.
"""

import argparse
import time


def main(some_arg=None):
    # raise RuntimeError
    STEPS = 100
    time.sleep(0.2)

    print("Starting demo job...")
    for step in range(1, STEPS + 1):
        time.sleep(0.02)
        pct = int(step / STEPS * 100)
        print(f"Step {step}/{STEPS} complete.")
        print(f"BLUEPEPPER_BATCHER_PROGRESS={pct}")
        # if pct == 50:
        #     raise Exception("JAJ")
        # if pct == 53:
        #     print("BLUEPEPPER_BATCHER_TERMINATE")

    print("[Job Done]")
    print(type(some_arg))
    print(some_arg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--document_id", default=None)
    args = parser.parse_args()
    main(some_arg=args.document_id)
