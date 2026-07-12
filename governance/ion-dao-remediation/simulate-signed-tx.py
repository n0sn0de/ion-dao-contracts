#!/usr/bin/env python3
"""Simulate a signed Cosmos SDK transaction without broadcasting it."""

import json
import subprocess
import sys
import urllib.error
import urllib.request

if len(sys.argv) != 4:
    raise SystemExit(
        f"usage: {sys.argv[0]} CLI SIGNED_TX_JSON SIMULATE_URL"
    )

cli, signed_tx, endpoint = sys.argv[1:]
encoded = subprocess.check_output(
    [cli, "tx", "encode", signed_tx], text=True
).strip()
request = urllib.request.Request(
    endpoint,
    data=json.dumps({"tx_bytes": encoded}).encode(),
    headers={"Content-Type": "application/json"},
)
try:
    with urllib.request.urlopen(request, timeout=300) as response:
        payload = json.load(response)
except urllib.error.HTTPError as error:
    print(error.read().decode())
    raise SystemExit(2)

result = payload.get("result") or {}
print(
    json.dumps(
        {
            "gas_info": payload.get("gas_info"),
            "data_length": len(result.get("data") or ""),
            "event_types": [
                event.get("type") for event in result.get("events", [])
            ],
        },
        indent=2,
    )
)
