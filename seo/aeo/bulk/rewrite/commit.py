#!/usr/bin/env python3
"""Mark the pending batch as applied.

Run ONLY after the mutation emitted by next.py returned with empty userErrors.
Because done.json advances here and nowhere else, an interrupt between the two
leaves the state consistent -- the same batch is simply re-emitted next time.
"""
import json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
SF = os.path.join(D, "done.json")
PF = os.path.join(D, "pending.json")
if not os.path.exists(PF):
    sys.stderr.write("no pending.json -- run next.py first\n")
    sys.exit(1)

order = json.load(open(os.path.join(D, "order.json")))
done = set(json.load(open(SF))) if os.path.exists(SF) else set()
done |= set(json.load(open(PF)))
json.dump(sorted(done), open(SF, "w"))
print(f"recorded. done={len(done)}/{len(order)}  remaining={len(order) - len(done)}")
