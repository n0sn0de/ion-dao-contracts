# Reproducing the live-state evidence

All commands are read-only. Use an archive-capable Osmosis endpoint and one explicit height for every query.

```bash
export NODE='https://YOUR-TRUSTED-ARCHIVE-OSMOSIS-RPC'
export H='66276760'
export DAO='osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm'
export STAKE='osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc'
export FACTORY='osmo1qpszqk458arkkdff5z4vrqlqv4k2n9a0tjme23vn00uyt30nrr7sfe87cv'
```

## Pin and retain the block

```bash
osmosisd query block "$H" --node "$NODE" -o json > block-$H.json
jq '.header | {chain_id,height,time,app_hash}' block-$H.json
```

If any subsequent query says height unavailable or pruned, stop and use another archive endpoint. Do not silently fall back to latest state.

## Contract identity

```bash
osmosisd query wasm contract "$DAO" --height "$H" --node "$NODE" -o json
osmosisd query wasm contract "$STAKE" --height "$H" --node "$NODE" -o json

DAO_CODE=$(osmosisd query wasm contract "$DAO" --height "$H" --node "$NODE" -o json | jq -r '.contract_info.code_id')
STAKE_CODE=$(osmosisd query wasm contract "$STAKE" --height "$H" --node "$NODE" -o json | jq -r '.contract_info.code_id')

osmosisd query wasm code-info "$DAO_CODE" --height "$H" --node "$NODE" -o json
osmosisd query wasm code-info "$STAKE_CODE" --height "$H" --node "$NODE" -o json
```

## Legacy configuration and aggregates

```bash
osmosisd query wasm contract-state smart "$DAO" \
  '{"get_config":{}}' --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$DAO" \
  '{"paused":{}}' --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"get_config":{}}' --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"info":{}}' --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"total_power_at_height":{"height":null}}' --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"total_value":{}}' --height "$H" --node "$NODE" -o json
```

## Balances and supply

```bash
osmosisd query bank balances "$DAO" --height "$H" --node "$NODE" -o json
osmosisd query bank balances "$STAKE" --height "$H" --node "$NODE" -o json
osmosisd query bank total-supply-of uion --height "$H" --node "$NODE" -o json
```

Do not rely on the legacy token list as an exhaustive balance source.

## Proposal and deposit pagination

Proposal pagination uses proposal IDs. Deposit pagination uses the composite `(proposal_id, depositor)` key nested inside `query.everything.start`.

First deposit page:

```bash
osmosisd query wasm contract-state smart "$DAO" \
  '{"deposits":{"query":{"everything":{"start":null}},"limit":30,"order":"asc"}}' \
  --height "$H" --node "$NODE" -o json
```

For the next page, use the final tuple from the previous result:

```json
{
  "deposits": {
    "query": {
      "everything": {
        "start": [25, "LAST_DEPOSITOR_ADDRESS"]
      }
    },
    "limit": 30,
    "order": "asc"
  }
}
```

Do not place `start` beside `query`; the legacy deserializer ignores that shape.

## Stakers and claims

The staker map is address-paginated with an exclusive `start_at`. Every page must use `--height "$H"`.

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  '{"range_stakers":{"start_at":null,"limit":30,"order":"asc"}}' \
  --height "$H" --node "$NODE" -o json
```

For each returned address:

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  '{"claims":{"address":"STAKER_ADDRESS"}}' \
  --height "$H" --node "$NODE" -o json
```

Verify:

```text
active backing + sum(all claims) == stake-contract uion bank balance
```

Retain page inputs and outputs so another reviewer can prove no address was skipped.

## IBCX control state

```bash
export IBCX_NEW='osmo14klwqgkmackvx2tqa0trtg69dmy0nrg4ntq4gjgw2za4734r5seqjqm4gm'
export IBCX_ST='osmo1xqw2sl9zk8a6pch0csaw78n4swg5ws8t62wc5qta4gnjxfqg6v2qcs243k'
export IBCX_OLD='osmo1yhd9tzp09d833u7ray4pudxjnx2q7zcq2s0g9r7cl2w73mj5qqcjwhxt'

for A in "$IBCX_NEW" "$IBCX_ST" "$IBCX_OLD"; do
  osmosisd query wasm contract "$A" --height "$H" --node "$NODE" -o json
  osmosisd query wasm contract-state smart "$A" \
    '{"config":{}}' --height "$H" --node "$NODE" -o json
  osmosisd query bank balances "$A" --height "$H" --node "$NODE" -o json
done
```

If the exact query variant differs, inspect the pinned schema/source rather than guessing. Preserve `gov`, `pending_gov`, fee collector, pause/rebalance state, and backing balances.

## DAO DAO artifacts

```bash
for ID in 1571 1574 1579 1581 1588; do
  osmosisd query wasm code-info "$ID" --height "$H" --node "$NODE" -o json
done

osmosisd query wasm contract "$FACTORY" --height "$H" --node "$NODE" -o json
osmosisd query wasm contract-state smart "$FACTORY" \
  '{"admin":{}}' --height "$H" --node "$NODE" -o json
```

Also pin the DAO DAO UI registry commit and the `dao-contracts` tag/commit. Live code state is authoritative for what executes; source reproduction is required before deployment.

## CW20/CW721 discovery

Bank state is insufficient. Document:

- known token/collection balance queries;
- historical Wasm transfer/send/receive event search;
- indexed account-contract holdings results;
- project manifest comparison;
- archive/indexer gaps.

## Second-endpoint verification

Repeat at the exact same `H` through a second archive endpoint:

- block hash/app hash;
- governance/stake contract info and code hashes;
- treasury/stake balances;
- supply;
- proposal/deposit boundaries;
- IBCX control state.

Mismatch is an abort condition.

## Production boundary

The retained height above is evidence for this roadmap, not a production amount. Before each transition proposal:

1. choose and publish a new archive height;
2. repeat every relevant query at that height;
3. retain raw responses and hashes;
4. recompute refunds, proposal deposits, balances, threshold margins, and product controls;
5. independently review before signing.
