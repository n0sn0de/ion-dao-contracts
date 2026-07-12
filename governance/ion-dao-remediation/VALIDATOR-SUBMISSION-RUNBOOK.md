# Validator-wallet submission runbook

Status: **prepared and unsigned; no governance proposal has been broadcast**.

This runbook makes the selected validator operator account the on-chain proposal
proposer while signing directly on that wallet's Linux host.

## Recommendation

Use direct validator signing. Do not use `x/authz` unless the validator operator
cannot run the submission transaction directly.

A standard generic authz grant can be limited to message type
`/cosmos.gov.v1.MsgSubmitProposal`, but it cannot be limited to this proposal's
contract, title, Wasm hash, metadata, or deposit amount. During its lifetime the
grantee could submit any governance proposal funded by the validator account.
That is broader than the operation needs. It also renders as a top-level
`MsgExec`, which is less clean than a direct validator-signed
`MsgSubmitProposal` if public provenance is the goal.

## Verified identities

| Role | Address |
| --- | --- |
| Validator operator | `osmovaloper10jm8fvdyqlj78w0j5nawc76wsn4pqmdxgzgh4c` |
| Corresponding proposer account | `osmo10jm8fvdyqlj78w0j5nawc76wsn4pqmdxj4q5zl` |
| Validator status at packaging | `BOND_STATUS_BONDED` |
| jun0n0s account | `osmo1jun0n0s59ens343cews08y0rtlnuruk7lj0grt` |

At Osmosis height `66115148`, the validator account reported sequence `6843`
and `18,925.475869 OSMO`. These are observations, not signing inputs. Query them
again; never hard-code a sequence or assume the observed balance is operationally
available.

The jun0n0s account received the authorized `5,005 OSMO` and reported
`5,055.912255 OSMO`. Those funds have **not** been forwarded to the validator
account by this package.

## Deposit semantics

This package submits:

```text
5,000 OSMO initial deposit
expedited = true
proposer = validator operator account
```

That satisfies the `25%` minimum initial deposit for an expedited proposal, but
it does **not** start voting. The proposal enters `DEPOSIT_PERIOD`.

Voting starts only after total deposits reach:

```text
20,000 OSMO
```

The remaining amount after this initial submission is:

```text
15,000 OSMO
```

Any account may provide that later deposit. Once the cumulative deposit reaches
20,000 OSMO, the 24-hour expedited voting clock starts. Funding the remaining
15,000 late defeats the point; the recommended voting-start deadline in the
published package is `2026-07-16 09:09:01 UTC`.

## Package files

| File | Purpose |
| --- | --- |
| `proposal-expedited-initial-5000.json` | Exact generic proposal input with 5,000 OSMO initial deposit |
| `unsigned-validator-initial-5000.json` | Generated unsigned tx with the validator proposer address |
| `proposal-expedited.json` | Full 20,000 OSMO one-shot alternative |
| `simulate-signed-tx.py` | REST simulation helper; never broadcasts |
| `ion_dao_v0.0.2.osmosis.wasm` | Exact production artifact embedded in the message |

The initial and full-deposit files contain the same authority, target, metadata,
summary, migration message, permissions, and compressed Wasm. Only the deposit
amount differs.

## 1. Set local variables

Run on the Linux host that already has the validator operator key loaded.
Replace the three local keyring values. Do not paste a mnemonic anywhere.

```sh
export CLI=osmosisd
export CHAIN_ID=osmosis-1
export NODE=http://127.0.0.1:26657
export REST=http://127.0.0.1:1317
export OSMOSIS_HOME="$HOME/.osmosisd"
export KEYRING_DIR="$OSMOSIS_HOME"
export KEYRING_BACKEND=file       # or os; use the backend already configured
export VALIDATOR_KEY='<local-validator-operator-key-name>'
export EXPECTED_PROPOSER=osmo10jm8fvdyqlj78w0j5nawc76wsn4pqmdxj4q5zl
export EXPECTED_VALOPER=osmovaloper10jm8fvdyqlj78w0j5nawc76wsn4pqmdxgzgh4c
export GOV_AUTHORITY=osmo10d07y265gmmuvt4z0w9aw880jnsr700jjeq4qp
export TARGET=osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm
export PACKAGE_DIR="$PWD/governance/ion-dao-remediation"
```

If the local node uses a different home, RPC port, REST port, or keyring backend,
change only those local variables.

## 2. Fail-closed chain and key checks

```sh
set -euo pipefail

"$CLI" version --long

NETWORK=$(curl -fsSL "$NODE/status" | jq -r '.result.node_info.network')
[ "$NETWORK" = "$CHAIN_ID" ] || {
  echo "wrong chain: $NETWORK" >&2
  exit 1
}

CATCHING_UP=$(curl -fsSL "$NODE/status" | jq -r '.result.sync_info.catching_up')
[ "$CATCHING_UP" = false ] || {
  echo 'local node is still catching up' >&2
  exit 1
}

PROPOSER=$("$CLI" keys show "$VALIDATOR_KEY" -a \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR")

[ "$PROPOSER" = "$EXPECTED_PROPOSER" ] || {
  echo "wrong signer: $PROPOSER" >&2
  exit 1
}

"$CLI" query staking validator "$EXPECTED_VALOPER" \
  --node "$NODE" -o json \
  | jq '.validator | {operator_address,status,jailed,description}'

"$CLI" query auth account "$EXPECTED_PROPOSER" --node "$NODE" -o json
"$CLI" query bank balance "$EXPECTED_PROPOSER" uosmo --node "$NODE" -o json
```

Require at least `5000200000uosmo` for the initial deposit plus the committed
0.2 OSMO fee. Keep more for operational reserve.

## 3. Re-query the live migration target

```sh
"$CLI" query wasm contract "$TARGET" --node "$NODE" -o json \
  | tee /tmp/ion-target-contract.json \
  | jq '{address,code_id:.contract_info.code_id,admin:.contract_info.admin,label:.contract_info.label}'

jq -e '
  .contract_info.code_id == "3" and
  .contract_info.admin == ""
' /tmp/ion-target-contract.json >/dev/null

"$CLI" query wasm contract-state raw "$TARGET" \
  636f6e74726163745f696e666f \
  --node "$NODE" -o json \
  | jq -r '.data' | base64 -d | tee /tmp/ion-cw2.json

jq -e '
  .contract == "crates.io:ion-dao" and
  .version == "0.0.1"
' /tmp/ion-cw2.json >/dev/null
```

Stop if any assertion fails. Do not “fix” the expected values to make a stale
transaction pass.

## 4. Re-query governance parameters

```sh
curl -fsSL "$REST/cosmos/gov/v1/params/deposit" \
  | jq '.params | {
      min_deposit,
      expedited_min_deposit,
      min_initial_deposit_ratio,
      max_deposit_period,
      voting_period,
      expedited_voting_period
    }'
```

Expected at packaging:

```text
expedited_min_deposit = 20000000000uosmo
min_initial_deposit_ratio = 0.25
expedited_voting_period = 86400s
```

## 5. Verify package bytes and fields

```sh
cd "$PACKAGE_DIR"

printf '%s  %s\n' \
  '37bb98453ddf9495c2cdf9a2667d515164ef9e09b15385921eaba9270d148f3e' \
  'ion_dao_v0.0.2.osmosis.wasm' \
  | sha256sum -c -

jq -e '
  .deposit == "5000000000uosmo" and
  .expedited == true and
  .metadata == "ipfs://bafkreihki5gssufsdhwtcfpupfv2bnlfq3b7iqtaxxiqyocqi5nq62cduq" and
  .messages[0]["@type"] == "/cosmwasm.wasm.v1.MsgStoreAndMigrateContract" and
  .messages[0].authority == "'"$GOV_AUTHORITY"'" and
  .messages[0].contract == "'"$TARGET"'" and
  .messages[0].msg == {} and
  .messages[0].instantiate_permission.permission == "Nobody"
' proposal-expedited-initial-5000.json >/dev/null
```

## 6. Regenerate the unsigned transaction locally

Do not sign the committed unsigned file. Regenerate it with the current CLI and
local node:

```sh
"$CLI" tx gov submit-proposal proposal-expedited-initial-5000.json \
  --from "$VALIDATOR_KEY" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR" \
  --gas 8000000 \
  --fees 200000uosmo \
  --note 'ION DAO v0.0.2 expedited initial submission' \
  --generate-only -o json \
  > unsigned-validator-local.json
```

Inspect the outer and inner messages:

```sh
jq '{
  outer_type:.body.messages[0]["@type"],
  proposer:.body.messages[0].proposer,
  metadata:.body.messages[0].metadata,
  initial_deposit:.body.messages[0].initial_deposit,
  expedited:.body.messages[0].expedited,
  inner_type:.body.messages[0].messages[0]["@type"],
  authority:.body.messages[0].messages[0].authority,
  contract:.body.messages[0].messages[0].contract,
  migration_msg:.body.messages[0].messages[0].msg,
  instantiate_permission:.body.messages[0].messages[0].instantiate_permission,
  fee:.auth_info.fee
}' unsigned-validator-local.json
```

Require:

```text
proposer = osmo10jm8fvdyqlj78w0j5nawc76wsn4pqmdxj4q5zl
initial_deposit = 5000000000uosmo
expedited = true
inner type = /cosmwasm.wasm.v1.MsgStoreAndMigrateContract
```

## 7. Sign without broadcasting and simulate

```sh
"$CLI" tx sign unsigned-validator-local.json \
  --from "$VALIDATOR_KEY" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR" \
  --output-document signed-validator-local.json \
  -o json

python3 simulate-signed-tx.py \
  "$CLI" \
  signed-validator-local.json \
  "$REST/cosmos/tx/v1beta1/simulate"
```

Simulation must succeed. If it returns a keeper, signer, sequence, balance,
authority, Wasm, or metadata error, stop. Do not broadcast and do not retry
blindly.

The committed gas ceiling is 8,000,000 with fee `200000uosmo` at
`0.025uosmo`/gas. If simulation shows the ceiling is insufficient or local fee
policy differs, regenerate from the proposal input with an explicit reviewed
ceiling and fee, then sign again.

## 8. Broadcast only after final review

```sh
"$CLI" tx broadcast signed-validator-local.json \
  --node "$NODE" \
  --broadcast-mode sync \
  -o json \
  | tee submit-result.json

jq '{code,codespace,raw_log,txhash}' submit-result.json
```

Require CheckTx `code: 0`, then wait for inclusion:

```sh
export TXHASH=$(jq -r '.txhash' submit-result.json)

for i in $(seq 1 30); do
  if "$CLI" query tx "$TXHASH" --node "$NODE" -o json \
      > submit-included.json 2>/dev/null; then
    break
  fi
  sleep 2
done

jq '{height,txhash,code,codespace,raw_log,gas_wanted,gas_used}' \
  submit-included.json

jq -e '.code == 0' submit-included.json >/dev/null

export PROPOSAL_ID=$(jq -r '
  [.events[]?.attributes[]?
    | select(.key == "proposal_id")
    | .value][0]
' submit-included.json)

test -n "$PROPOSAL_ID" && test "$PROPOSAL_ID" != null
printf 'proposal_id=%s\n' "$PROPOSAL_ID"
```

## 9. Verify deposit-period state

```sh
"$CLI" query gov proposal "$PROPOSAL_ID" --node "$NODE" -o json \
  | tee proposal-state.json \
  | jq '.proposal | {
      id,
      title,
      proposer,
      status,
      expedited,
      total_deposit,
      deposit_end_time,
      voting_start_time,
      voting_end_time,
      metadata,
      messages:[.messages[] | {
        type:.["@type"],authority,contract,msg,instantiate_permission
      }]
    }'
```

Expected immediately after only 5,000 OSMO:

```text
status = PROPOSAL_STATUS_DEPOSIT_PERIOD
expedited = true
total_deposit = 5000000000uosmo
voting_start_time = zero/unset
```

## 10. Activate voting with the remaining deposit

Any account may deposit the remaining 15,000 OSMO:

```sh
"$CLI" tx gov deposit "$PROPOSAL_ID" 15000000000uosmo \
  --from '<funding-key>' \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend '<funding-keyring-backend>' \
  --keyring-dir '<funding-keyring-dir>' \
  --gas auto \
  --gas-adjustment 1.6 \
  --gas-prices 0.025uosmo \
  --yes
```

After inclusion, re-query the proposal and require:

```text
status = PROPOSAL_STATUS_VOTING_PERIOD
total_deposit = 20000000000uosmo
voting_start_time = set
voting_end_time ≈ voting_start_time + 24 hours
```

Only then can validators and delegators vote.

## 11. Validator vote

```sh
"$CLI" tx gov vote "$PROPOSAL_ID" yes \
  --from "$VALIDATOR_KEY" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR" \
  --gas auto \
  --gas-adjustment 1.6 \
  --gas-prices 0.025uosmo \
  --note 'YES: reviewed ION DAO accounting remediation' \
  --yes
```

Verify the vote from chain state. Do not infer it from CLI success text.

## Optional authz route—not recommended

The standard authz option is a short-lived generic authorization for exactly one
message type:

```sh
export GRANTEE=osmo1jun0n0s59ens343cews08y0rtlnuruk7lj0grt
export EXPIRES=$(date -u -d '+20 minutes' +%s)

"$CLI" tx authz grant "$GRANTEE" generic \
  --msg-type /cosmos.gov.v1.MsgSubmitProposal \
  --expiration "$EXPIRES" \
  --from "$VALIDATOR_KEY" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR" \
  --gas auto --gas-adjustment 1.6 --gas-prices 0.025uosmo \
  --yes
```

After inclusion, query the exact grant:

```sh
"$CLI" query authz grants \
  "$EXPECTED_PROPOSER" "$GRANTEE" \
  /cosmos.gov.v1.MsgSubmitProposal \
  --node "$NODE" -o json
```

The grantee would then generate the inner proposal with
`--from "$EXPECTED_PROPOSER"`, wrap it using:

```sh
osmosisd tx authz exec validator-inner.json --from jun0n0s ...
```

and perform the same sign-without-broadcast and REST simulation gate.

Critical boundaries:

- The 5,000 OSMO deposit is withdrawn from the validator/proposer account, not
  the grantee account.
- The grant does not constrain proposal fields or deposit amount.
- The top-level transaction is `MsgExec`, even though the proposal's `proposer`
  is the validator account.
- Revoke immediately after success or abandonment:

```sh
"$CLI" tx authz revoke "$GRANTEE" \
  /cosmos.gov.v1.MsgSubmitProposal \
  --from "$VALIDATOR_KEY" \
  --chain-id "$CHAIN_ID" \
  --node "$NODE" \
  --home "$OSMOSIS_HOME" \
  --keyring-backend "$KEYRING_BACKEND" \
  --keyring-dir "$KEYRING_DIR" \
  --gas auto --gas-adjustment 1.6 --gas-prices 0.025uosmo \
  --yes
```

Direct validator signing has less authority surface, cleaner explorer provenance,
and fewer transactions. Use it.
