#!/usr/bin/env python3
"""Mark the pending batch as applied.

Run ONLY after the mutation emitted by next.py returned with empty userErrors.
Because done.json advances here and nowhere else, an interrupt between the two
leaves the state consistent -- the same batch is simply re-emitted next time.

Pass the number of product ids the mutation actually returned:

    python3 commit.py 4

It must match the pending batch size, or nothing is recorded. This catches a
mutation that was truncated in transit and only partly applied -- the failure
mode that keeps batch sizes honest.
"""
import json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
SF = os.path.join(D, "done.json")
PF = os.path.join(D, "pending.json")
if not os.path.exists(PF):
    sys.stderr.write("no pending.json -- run next.py first\n")
    sys.exit(1)

pending = json.load(open(PF))
if len(sys.argv) > 1:
    got = int(sys.argv[1])
    if got != len(pending):
        sys.stderr.write(
            f"REFUSING: mutation returned {got} products but the batch held "
            f"{len(pending)}. Nothing recorded. Re-send the batch.\n"
        )
        sys.exit(1)
else:
    sys.stderr.write("warning: no returned-count given, skipping the truncation check\n")

order = json.load(open(os.path.join(D, "order.json")))
done = set(json.load(open(SF))) if os.path.exists(SF) else set()
done |= set(pending)
json.dump(sorted(done), open(SF, "w"))
FF = os.path.join(D, "fixups.json")
if os.path.exists(FF):
    json.dump([p for p in json.load(open(FF)) if p not in pending], open(FF, "w"), indent=0)
print(f"recorded. done={len(done)}/{len(order)}  remaining={len(order) - len(done)}")
