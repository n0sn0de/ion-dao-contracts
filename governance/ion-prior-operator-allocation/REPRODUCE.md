# Reproducing the vesting assessment

All commands are read-only. Supply a trusted Osmosis RPC endpoint.

```bash
export NODE='https://YOUR-TRUSTED-OSMOSIS-RPC'
export DAO='osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm'
export VESTING='osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk'
export STAKE='osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc'
```

## Pin chain time

```bash
osmosisd status --node "$NODE"
osmosisd query block --node "$NODE" -o json
```

Spendable/locked vesting values change with block time. Record height and time with every published snapshot.

## Query proposals 10–12

```bash
for id in 10 11 12; do
  osmosisd query wasm contract-state smart "$DAO" \
    "{\"proposal\":{\"proposal_id\":$id}}" \
    --node "$NODE" -o json
done
```

Inspect `msgs[0].stargate.type_url` and base64-decode `msgs[0].stargate.value` with the protobuf definition for `cosmos.vesting.v1beta1.MsgCreateVestingAccount`.

For proposal 12, require:

```text
from_address = ION DAO contract
recipient    = vesting address
amount       = 3407040000 uion
end_time     = 1850742000
delayed      = false
```

Do not copy the failed proposal 10/11 source address or payload into the executed-proposal receipt.

## Query account and balances

```bash
osmosisd query auth account "$VESTING" --node "$NODE" -o json
osmosisd query bank balances "$VESTING" --node "$NODE" -o json
osmosisd query bank spendable-balances "$VESTING" --node "$NODE" -o json
osmosisd query bank total-supply-of uion --node "$NODE" -o json
```

Require account type:

```text
/cosmos.vesting.v1beta1.ContinuousVestingAccount
```

Compute locked bank balance as:

```text
current bank uion - current spendable uion
```

## Query legacy stake and claims

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  "{\"staked_value\":{\"address\":\"$VESTING\"}}" \
  --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  "{\"claims\":{\"address\":\"$VESTING\"}}" \
  --node "$NODE" -o json
```

Known bounded holdings are bank ION plus legacy staked value plus any outstanding claim. Do not label the remainder “sold” without tracing its destinations.

## Reproduce concentration scenario

Use integer atomic values:

```text
resulting total power = current total active power + current spendable bank ION
recipient potential power = current recipient stake + current spendable bank ION
potential share = recipient potential power / resulting total power
```

This is a maximum-current-spendable scenario, not an assertion that the recipient will stake.

## Separate exploit evidence

Query deposits/proposals `22`–`39` and compare the depositor address to the vesting address. Different addresses do not prove different real-world controllers, but they also do not prove common control. Report the evidence boundary.

## Endpoint and arithmetic checks

- repeat account, spendable, stake, and supply queries through a second endpoint;
- retain raw JSON and hashes;
- calculate only in integer atomic units or exact decimal arithmetic;
- do not mix values from materially different block times without disclosure;
- do not infer legal ownership or breach from a balance query.
