# Expedited: Patch ION DAO Accounting and Quarantine Legacy Claims

## Executive summary

This proposal asks Osmosis governance to atomically store reviewed ION DAO
contract code and migrate the live, adminless ION DAO contract at its existing
address:

```text
osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm
```

The live contract reports code ID `3`, no admin, and CW2 identity
`crates.io:ion-dao` version `0.0.1`. Because the admin is empty, neither a wallet
nor the ION DAO itself can perform an ordinary `WasmMsg::Migrate`. The narrow
in-place repair route is Osmosis native governance (`x/gov`) executing:

```text
/cosmwasm.wasm.v1.MsgStoreAndMigrateContract
```

under the Osmosis governance module authority:

```text
osmo10d07y265gmmuvt4z0w9aw880jnsr700jjeq4qp
```

The patch does two things:

1. it fixes proposal-deposit accounting for proposals created after migration;
2. it quarantines deposit claims for proposals created before or in the
   migration block, pending a separate evidence-based reconciliation decision.

It does **not** reconstruct historical payers, distribute treasury funds, or
claim that aggregate legacy storage proves who should be paid.

## Why this proposal is urgent

At the read-only incident snapshot on 2026-07-11 at `19:27:02 UTC`, direct
contract queries showed:

| Field | Verified value |
| --- | --- |
| Affected proposals | IDs `22` through `39` |
| Count | `18` |
| Status | all `open` |
| Executable messages | none |
| Stored proposal deposits | `662 ION` total |
| Normal retained base at creation | `9 ION` total (`18 × 0.5 ION`) |
| Apparent excess claim exposure | `653 ION` |
| Currently claimable | none |
| Earliest voting expiry | `2026-07-17 11:09:01 UTC` |
| Latest voting expiry | `2026-07-17 11:30:35 UTC` |
| Current votes | exactly `1 ION` Veto on each; all other buckets zero |
| Snapshot voting power | `1,671.832757 ION` |
| Veto threshold | `30%`, requiring `501.549828 ION` on every proposal |

In v0.0.1, a proposal can record the gross amount received, immediately refund
the excess over the configured base, and later attempt to claim the gross
record. After expiry, ordinary close or execute paths can make those records
claimable. A normal `No` or failed-quorum outcome is not sufficient containment;
only a successful veto path confiscates rather than refunds.

The migration must execute before any ordinary close/execute transaction opens
the legacy claim path. The migration cutoff then covers every proposal created
before or in the migration block.

## Why native Osmosis governance is required

There are two different governance domains:

- **ION DAO governance** can dispatch ordinary CosmWasm messages, but the DAO is
  not the stored chain admin. An ION DAO proposal containing `WasmMsg::Migrate`
  would fail wasmd authorization before the migration entrypoint runs.
- **Osmosis native governance** controls the wasmd governance authorization
  policy. A gov-v1 `MsgStoreAndMigrateContract` signed by the governance module
  authority can atomically store code and migrate the adminless contract.

An ION DAO signaling proposal could request social support, but it cannot grant
itself the missing chain authority. Pretending otherwise would be governance
theater with a deterministic authorization failure.

Osmosis has already passed proposals using this same privileged message type and
governance authority, including proposals `853` and `896` for IBC rate-limit
contract upgrades.

## Why expedited governance is recommended

Expedited governance is not mathematically mandatory if a standard proposal
enters voting early enough. It is operationally necessary once the standard
window is too tight.

Against the first ION expiry at `2026-07-17 11:09:01 UTC`:

- zero-margin latest standard voting start: `2026-07-12 11:09:01 UTC`;
- zero-margin latest expedited voting start: `2026-07-16 11:09:01 UTC`;

Because funding, publication, validator review, and voting coordination were not
complete before the safe standard cutoff, this package recommends **expedited**
submission so voting starts immediately.

### Expedited advantages

- The 24-hour vote can finish well before the legacy claim window.
- Validators and delegators get a focused incident-response decision rather than
  a last-minute standard tally.
- If the message passes, store and migrate execute atomically at tally.
- If execution fails, cached execution prevents a partial code/state mutation.
- Under Cosmos SDK v0.50 behavior, an expedited proposal that misses the
  expedited threshold converts to a regular proposal rather than immediately
  disappearing; its original voting start remains the reference for the
  standard five-day end time.


## Exact proposed action

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgStoreAndMigrateContract",
  "authority": "osmo10d07y265gmmuvt4z0w9aw880jnsr700jjeq4qp",
  "contract": "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm",
  "wasm_byte_code": "<deterministic gzip bytes from the artifact below>",
  "instantiate_permission": {
    "permission": "Nobody",
    "addresses": []
  },
  "msg": {}
}
```

`Nobody` is intentional. Governance is repairing one named contract, not
creating a publicly instantiable code family.

## Patch behavior

The reviewed v0.0.2 migration:

- requires exact CW2 source `crates.io:ion-dao` at version `0.0.1`;
- upgrades CW2 to `0.0.2`;
- rejects unsupported sources, wrong versions, repeated migration, downgrade,
  and option-bearing migration messages;
- accepts only the strict empty migration message `{}`;
- records an inclusive migration-height cutoff;
- rejects new proposals in the migration block;
- blocks fresh top-ups to already quarantined pending proposals;
- rejects claims for proposals created before or in the migration block before
  mutating `claimed` state or constructing a bank send;
- records only net retained funds for post-migration proposal deposits and
  top-ups; and
- uses each proposal's immutable base-deposit snapshot rather than mutable
  global configuration.

## Explicit limits

This proposal does not:

- promise payment to the proposal creator or any other party;
- redistribute ION or OSMO;
- move the ION DAO treasury;
- assign a new contract admin;
- alter the ION staking contract

Quarantine is the honest response when storage proves aggregate liabilities but
not equitable ownership. Guessing who should receive treasury funds would turn a
security patch into an unaudited payout mechanism.

## Artifact and reproducibility evidence

Reviewed source head:

```text
81736b1bcfebdd1e3239ae37f18cef24f32d9272
```

Merged source remediation:

```text
496b2f303e5a8b5606ad7fb82fef2aada5329ab8
```

Artifacts:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Rust 1.64 release `ion_dao.wasm` | `2,323,964` | `005a7a3272b2e7a704a8869453ca7f6cb0caf50a1b911c0c20cca1e5c4ede1e0` |
| Optimized production proposal artifact | `447,489` | `37bb98453ddf9495c2cdf9a2667d515164ef9e09b15385921eaba9270d148f3e` |
| Deterministic gzip bytes embedded by `osmosisd` | `150,198` | `37e6e3ff0eddfc9b4bb162ffd241d39d3d204f1cfa76cfef7510bd4fe1c099f5` |

The optimized artifact was produced twice with byte-identical output using
Binaryen `wasm-opt version 130`:

```sh
wasm-opt -Oz \
  --signext-lowering \
  --strip-debug \
  --strip-dwarf \
  --strip-producers \
  --strip-target-features \
  --strip-toolchain-annotations \
  ion_dao.wasm -o ion_dao_v0.0.2.osmosis.wasm
```

The CLI-compressed bytes decompress to the exact 447,489-byte artifact hash.

## Validation evidence

The exact reviewed head passed:

- `80` ION DAO tests;
- `8` ION stake tests;
- Rust `1.64.0` formatting;
- Rust `1.64.0` strict Clippy;
- locked workspace/all-target validation;
- JSON schema regeneration;
- TypeScript client regeneration and build;
- repeated byte-identical Wasm builds;
- optimizer repeatability and checksum comparison; and
- independent exact-head source/release review.

## Mainnet migration proof

A bounded Juno mainnet proof used adapters that replaced only Osmosis custom
message/query types with `cosmwasm_std::Empty`. Governance, migration, and
deposit state logic remained at the named old and patched source commits.

This proves contract migration/state semantics. It does not claim Juno can prove
Osmosis' native governance authorization or Osmosis-specific custom bindings.

| Proof | Receipt |
| --- | --- |
| v0.0.1 proof code | code `5142`, tx `661E8EC0DFA61DBBC45DDA688E36D0B6E493FD8400E344F0567C86FB8311ED76` |
| v0.0.2 proof code | code `5143`, tx `BA74B1C93A9D7A7A148AF0AF34141EDF2DEBD960BCC40FFF4B3FD6CD196B5028` |
| Proof DAO | `juno1hanfjy97f87gc8va6lymvn9dcsgc40pv4n8099rjqk74x89ayk9st9ge8t` |
| DAO became its own admin | `5DE54DF9F28991AD56DE71A4345F7A369CD85DB161A07CAE3FB32C84B1B45C2B` |
| Atomic migration proposal + Yes | `8DC1C19E0B699DA54BCEBA3C2F707D234282665C32D6C31589606B66603EA22D` |
| DAO-authorized migration | `757A13EBBC9C53A8DF6E014B51C2B3EC28FC8DA103AA5781473EDE8D610583E1` |
| Post-migration proposal + Yes | `A9997AF214F9329EBC35D3C6E946462C61AA2BAD278DAE5A7B401406B7893C68` |
| Post-migration execute | `ADC23AE82F3AD5DA3F4D0C841CA120B1F334667927E3A145DCAB62DBA7E2339D` |
| Post-migration claim | `AE7EF212BA0FBF7671EEEDCC4D9522A1C7AF519711898D4411BD1066C19E8A82` |

Verified results:

1. wallet privilege ended when the proof DAO became its own chain admin;
2. a passed DAO proposal migrated code `5142` to `5143`;
3. migration recorded cutoff height `39710117`;
4. a signed legacy-claim simulation failed with
   `Deposit claim requires manual reconciliation`; and
5. a proposal created after migration executed normally and its 1ujuno deposit
   was claimed exactly once (`claimed: true`).

## Proposal-message preflight

The generated Osmosis proposal payload was decoded and checked for:

- correct outer `cosmos.gov.v1.MsgSubmitProposal`;
- correct inner
  `/cosmwasm.wasm.v1.MsgStoreAndMigrateContract`;
- exact governance authority;
- exact live target contract;
- strict `{}` migration message;
- `Nobody` instantiate permission;
- deterministic embedded Wasm bytes; and
- explicit expedited/full-deposit fields.

A signed but unbroadcast zero-deposit transaction reached the live Osmosis gov
keeper and failed only the expected minimum-deposit validation. The final funded
transaction must be regenerated and simulated again immediately before
broadcast. No Osmosis proposal has been submitted at the time of this document.

## Failure and rollback behavior

- Store and migrate are one message and execute atomically.
- Governance executes passed proposal messages in a cached context. If Wasm
  validation or migration fails, no partial code/state mutation is committed and
  the proposal records a failed execution reason.
- There is no casual wallet rollback because the contract is adminless. A future
  corrective migration would require another reviewed Osmosis governance
  proposal.
- The old code remains immutable chain history, but v0.0.2 intentionally rejects
  repeated/downgrade migration paths.
- Legacy claims remain quarantined until governance approves a separate
  reconciliation design; that is a safety boundary, not an accidental lock.

## Voting guidance

### Yes

Vote Yes if you support an atomic in-place migration that:

- fixes future deposit accounting;
- blocks unsafe pre-migration claims;
- preserves the contract address and non-quarantined state;
- uses reviewed, reproducible code with public evidence.

### No

Vote No if you believe the migration code, evidence, or quarantine policy is
insufficient and prefer the contract remain unchanged. A No outcome leaves the
legacy claim window uncontained unless an independent veto/containment path
succeeds.

### No With Veto

No With Veto should be reserved for the chain's normal abuse/spam standard. Under
current Osmosis parameters, a final veto outcome burns proposal deposits. It
should not be used merely because a voter prefers a different implementation.

### Abstain

Abstain counts toward quorum but not the Yes/No threshold denominator.

## Public evidence

- Source remediation and exact-head review:
  <https://github.com/n0sn0de/ion-dao-contracts/pull/3>
- Live-state preflight and proposal package:
  <https://github.com/n0sn0de/ion-dao-contracts/pull/4>
- Original public incident disclosure:
  <https://github.com/n0sn0de/ion-dao-contracts/issues/1>
- Public research checksum correction:
  <https://github.com/n0sn0de/jason-research/pull/12>

The IPFS metadata URI and complete package CID are recorded in the generated
proposal JSON and package manifest after publication.
