# Reproducing the live-state evidence

These are read-only query patterns. Supply your own trusted RPC endpoint. Do not copy a transaction command from this document; there is none.

```bash
export NODE='https://YOUR-TRUSTED-OSMOSIS-RPC'
export DAO='osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm'
export STAKE='osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc'
```

## Chain boundary

```bash
osmosisd status --node "$NODE"
osmosisd query block --node "$NODE" -o json
```

Record chain ID, height, time, and block ID. For a production snapshot, use a node that supports historical queries and pass the same retained height to every query where the CLI/module permits it.

## Contract identity and code

```bash
osmosisd query wasm contract "$DAO" --node "$NODE" -o json
osmosisd query wasm contract-history "$DAO" --node "$NODE" -o json
osmosisd query wasm contract "$STAKE" --node "$NODE" -o json
osmosisd query wasm contract-history "$STAKE" --node "$NODE" -o json
osmosisd query wasm code-info 1900 --node "$NODE" -o json
osmosisd query wasm code-info 2 --node "$NODE" -o json
```

## Legacy config and balances

```bash
osmosisd query wasm contract-state smart "$DAO" '{"get_config":{}}' --node "$NODE" -o json
osmosisd query wasm contract-state smart "$DAO" '{"proposal_count":{}}' --node "$NODE" -o json
osmosisd query wasm contract-state smart "$DAO" '{"token_list":{"start":null,"limit":30,"order":"asc"}}' --node "$NODE" -o json
osmosisd query bank balances "$DAO" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" '{"get_config":{}}' --node "$NODE" -o json
osmosisd query wasm contract-state smart "$STAKE" '{"total_power_at_height":{}}' --node "$NODE" -o json
osmosisd query wasm contract-state smart "$STAKE" '{"total_value":{}}' --node "$NODE" -o json
osmosisd query bank balances "$STAKE" --node "$NODE" -o json
osmosisd query bank total-supply-of uion --node "$NODE" -o json
```

## Proposals

The maximum page size is 30. `proposals.start` is the last proposal ID and is exclusive.

```bash
osmosisd query wasm contract-state smart "$DAO" \
  '{"proposals":{"query":{"everything":{}},"start":null,"limit":30,"order":"asc"}}' \
  --node "$NODE" -o json

osmosisd query wasm contract-state smart "$DAO" \
  '{"proposals":{"query":{"everything":{}},"start":30,"limit":30,"order":"asc"}}' \
  --node "$NODE" -o json
```

## Deposits

Deposit pagination is easy to get wrong. `start` is inside `query.everything` and is a composite `[proposal_id, depositor]`. A top-level `start` is ignored by this legacy interface.

First page:

```bash
osmosisd query wasm contract-state smart "$DAO" \
  '{"deposits":{"query":{"everything":{"start":null}},"limit":30,"order":"asc"}}' \
  --node "$NODE" -o json
```

For the next page, substitute the exact last `(proposal_id, depositor)` from the preceding page:

```bash
osmosisd query wasm contract-state smart "$DAO" \
  '{"deposits":{"query":{"everything":{"start":[LAST_ID,"LAST_DEPOSITOR"]}},"limit":30,"order":"asc"}}' \
  --node "$NODE" -o json
```

Continue until the response is empty. Assert key uniqueness.

## Stakers and claims

Staker pagination uses the last address as `start_at`:

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  '{"range_stakers":{"start_at":null,"limit":30,"order":"asc"}}' \
  --node "$NODE" -o json
```

For every returned historical address:

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  '{"claims":{"address":"STAKER_ADDRESS"}}' \
  --node "$NODE" -o json
```

Sum active values and claims in integer atomic units. Verify:

```text
active ION value + outstanding ION claims = staking contract ION bank balance
```

If pagination spans many blocks, pin a height or prove the aggregate still reconciles to a retained-height balance. Do not call a moving multi-hour scrape a single-height snapshot without this qualification.

## DAO DAO code registry and live code

Pin the DAO DAO UI registry commit before reading code IDs. Then query the selected IDs:

```bash
for id in 1571 1574 1579 1581 1588; do
  osmosisd query wasm code-info "$id" --node "$NODE" -o json
done
```

Query at least one contract instantiated from each module code and require CW2 `2.7.0`. Verify code hashes against reproduced Wasm and a second endpoint.

Factory:

```bash
export FACTORY='osmo1qpszqk458arkkdff5z4vrqlqv4k2n9a0tjme23vn00uyt30nrr7sfe87cv'
osmosisd query wasm contract "$FACTORY" --node "$NODE" -o json
osmosisd query wasm contract-state smart "$FACTORY" '{"admin":{}}' --node "$NODE" -o json
```

This recipe is discovery only. It does not prove a future production payload.
