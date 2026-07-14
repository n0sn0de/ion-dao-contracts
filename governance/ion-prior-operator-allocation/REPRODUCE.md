# Reproducing the vesting assessment

All commands are read-only. Use an archive-capable Osmosis RPC and one explicit height for every state query.

```bash
export NODE='https://YOUR-TRUSTED-ARCHIVE-OSMOSIS-RPC'
export H='66276784'
export DAO='osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm'
export STAKE='osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc'
export VESTING='osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk'
```

## Pin the block

```bash
osmosisd query block "$H" --node "$NODE" -o json > block-$H.json
jq '.header | {chain_id,height,time,app_hash}' block-$H.json
```

Expected time:

```text
2026-07-14T05:23:51.419944203Z
```

If the endpoint reports pruning or unavailable height, stop. Do not substitute latest state.

## Account type and vesting fields

```bash
osmosisd query auth account "$VESTING" \
  --height "$H" --node "$NODE" -o json > vesting-account-$H.json

jq . vesting-account-$H.json
```

Expected core fields:

```text
@type:          /cosmos.vesting.v1beta1.ContinuousVestingAccount
account_number: 906739
sequence:       135
start_time:     1692806078
end_time:       1850742000
original uion:  3407040000
```

Retain the full response, including unrelated denoms and delegated fields. Do not alter or characterize unrelated assets.

## Bank and spendable balances

```bash
osmosisd query bank balances "$VESTING" \
  --height "$H" --node "$NODE" -o json > bank-$H.json

osmosisd query bank spendable-balances "$VESTING" \
  --height "$H" --node "$NODE" -o json > spendable-$H.json

jq '.balances[] | select(.denom == "uion")' bank-$H.json
jq '.balances[] | select(.denom == "uion")' spendable-$H.json
```

Expected:

```text
bank uion:      3101840914
spendable uion: 1662205974
locked uion:    1439634940
```

Compute locked as bank minus spendable. Do not combine a bank balance from one height with spendable balance from another.

## Legacy stake and claims

```bash
osmosisd query wasm contract-state smart "$STAKE" \
  "{\"staked_value\":{\"address\":\"$VESTING\"}}" \
  --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  "{\"claims\":{\"address\":\"$VESTING\"}}" \
  --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"total_value":{}}' \
  --height "$H" --node "$NODE" -o json

osmosisd query wasm contract-state smart "$STAKE" \
  '{"total_power_at_height":{"height":null}}' \
  --height "$H" --node "$NODE" -o json
```

Expected:

```text
staked value: 151700000 uion
claims:       []
total value:  1671832757 uion
total power:  1671832757 uion
```

## ION supply

```bash
osmosisd query bank total-supply-of uion \
  --height "$H" --node "$NODE" -o json
```

Expected:

```text
21293014966 uion
```

## Proposals 10–12

```bash
for ID in 10 11 12; do
  osmosisd query wasm contract-state smart "$DAO" \
    "{\"proposal\":{\"proposal_id\":$ID}}" \
    --height "$H" --node "$NODE" -o json > proposal-$ID-$H.json
done
```

Retain:

- title and description;
- status;
- proposer;
- submitted height/time;
- type URL;
- exact protobuf bytes;
- vote/weight fields;
- deposit state.

Decode the exact `/cosmos.vesting.v1beta1.MsgCreateVestingAccount` bytes against the Osmosis/Cosmos SDK protobuf definition pinned to the historical app source. Expected decoded distinctions:

| Proposal | Source | Denom | End time | Status |
|---|---|---|---|---|
| 10 | non-DAO `osmo14hj2...2r9g9` | `uion` | 1848268800 | passed |
| 11 | ION DAO | `ion` | 1849698000 | passed |
| 12 | ION DAO | `uion` | 1850742000 | executed |

Do not reuse proposal 12’s end time for proposals 10 or 11.

## Execution transaction

```bash
export TX='1E15143F3135DEAB9D902F03F5D54D4B53EB65D8593E77CDDA773AC57CEFE245'
osmosisd query tx "$TX" --node "$NODE" -o json > proposal-12-execution.json
```

If the RPC transaction index is pruned, use an archive indexer/explorer and cross-check:

- hash;
- height `11126209`;
- time `2023-08-23T15:54:38Z`;
- ION DAO contract events;
- recipient account creation;
- exact amount and denom.

Explorer reference:

`https://www.mintscan.io/osmosis/tx/1E15143F3135DEAB9D902F03F5D54D4B53EB65D8593E77CDDA773AC57CEFE245?height=11126209`

## Authz grants

```bash
osmosisd query authz grants-by-granter "$VESTING" \
  --height "$H" --node "$NODE" -o json
```

Retain the full response. Absence at one height does not prevent a later grant.

## Affected proposal-address separation

Query proposals/deposits 22–39 at the same height and retain the associated address. Compare it as an address string only.

Do not infer identity or intent from address difference or similarity without additional evidence.

## SDK/source verification

Pin the Osmosis/Cosmos SDK source that defines:

- `ContinuousVestingAccount`;
- `ClawbackVestingAccount`;
- `MsgCreateVestingAccount`;
- `MsgCreateClawbackVestingAccount`/clawback handler, if present in that app version;
- funder/type checks;
- spendable-coin calculation and rounding;
- Authz `SendAuthorization` and `MsgExec` signer semantics.

Record commit URLs and line ranges in the raw evidence package. The account’s concrete type is load-bearing.

## Arithmetic

Use integer atomic units.

```text
locked = bank - spendable
       = 3101840914 - 1662205974
       = 1439634940 uion

bank + active stake
= 3101840914 + 151700000
= 3253540914 uion

arithmetic difference from original
= 3407040000 - 3253540914
= 153499086 uion
```

The last value is not a provenance finding.

Potential staking scenario:

```text
resulting active = 1671832757 + 1662205974 = 3334038731 uion
account power    =  151700000 + 1662205974 = 1813905974 uion
share            ≈ 54.405666%
```

## Second-endpoint verification

Repeat at the exact same `H` through a second archive endpoint:

- block hash/app hash;
- auth account type/number/sequence/schedule;
- bank and spendable balances;
- stake/claims;
- supply;
- proposals 10–12 bytes/status;
- Authz grants.

Mismatch is an abort condition.

## Retained evidence package

This directory now contains:

- raw public-chain query receipts under [`evidence/`](evidence/);
- [`evidence-manifest.json`](evidence-manifest.json) with SHA-256 and byte length for every receipt/source note;
- [`SOURCE-PINS.md`](SOURCE-PINS.md) with immutable source commits and line ranges.

Verify the manifest before relying on the package.

## Publication boundary

Before publication or negotiation:

1. hash raw responses;
2. separate chain facts from proposal representations and analyst inference;
3. remove confidential, privileged, or unnecessary personal data;
4. document archive/indexer limitations;
5. obtain qualified review for legal characterizations;
6. do not label inactivity, breach, ownership, fraud, or entitlement without supporting authority.
