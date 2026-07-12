# ION DAO governance migration preflight

Status: **source merged; Juno proof passed; Osmosis proposal not submitted**.

This note is the independently reviewable preflight for upgrading the live,
adminless ION DAO contract on Osmosis. It does not ask readers to trust an
operator narrative. The contract, authority, artifact hashes, message type,
mainnet proof receipts, and funding blocker are listed below.

## Live Osmosis target

The target contract was first queried at Osmosis height `66090917` on
2026-07-11. Subsequent target/CW2 reads during package assembly returned the
same code ID, empty admin, and version. The manifest's `preflight_height`
`66097384` is the later chain-header checkpoint recorded when the final package
was generated, not a claim that every read occurred atomically at one height.
The incident-state snapshot is separately time-stamped in the manifest.

| Field | Value |
| --- | --- |
| Chain | `osmosis-1` |
| Contract | `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm` |
| Current code ID | `3` |
| Chain admin | none |
| Label | `ION governance contract` |
| CW2 source | `crates.io:ion-dao` |
| CW2 version | `0.0.1` |
| Governance authority | `osmo10d07y265gmmuvt4z0w9aw880jnsr700jjeq4qp` |

An ordinary DAO `WasmMsg::Migrate` cannot migrate this contract because its
chain admin is empty. Osmosis governance can execute the purpose-built
`/cosmwasm.wasm.v1.MsgStoreAndMigrateContract` message under the governance
module authority. This is the narrow in-place route; uploading code separately
does not repair the missing admin.

## Patch boundaries

Reviewed source: <https://github.com/n0sn0de/ion-dao-contracts/pull/3>

The migration:

- accepts only CW2 source `crates.io:ion-dao` at version `0.0.1`;
- upgrades CW2 to `0.0.2` and cannot be repeated;
- records an inclusive migration-height cutoff;
- blocks claims for proposals created before or in the migration block;
- fixes accounting for proposals created after migration; and
- preserves normal one-time claims for post-migration proposals.

It **does not** identify historical payers, repay historical losses, or perform
a fair reconciliation of legacy deposits. Those questions require a separate
proposal with evidence. The migration deliberately quarantines unsafe legacy
claims instead of pretending aggregate state proves ownership.

## Production artifact

The Rust `1.64.0` release build at reviewed source commit
`81736b1bcfebdd1e3239ae37f18cef24f32d9272` produced:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Unoptimized `ion_dao.wasm` | 2,323,964 | `005a7a3272b2e7a704a8869453ca7f6cb0caf50a1b911c0c20cca1e5c4ede1e0` |
| Store-and-migrate artifact | 447,489 | `37bb98453ddf9495c2cdf9a2667d515164ef9e09b15385921eaba9270d148f3e` |
| Deterministic gzip payload produced by `osmosisd` | 150,198 | `37e6e3ff0eddfc9b4bb162ffd241d39d3d204f1cfa76cfef7510bd4fe1c099f5` |

The store-and-migrate artifact was produced twice, byte-identically, with
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

The proposal CLI gzip-compresses the artifact before embedding it. The
decompressed bytes hash back to the 447,489-byte artifact above.

## Exact governance message

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgStoreAndMigrateContract",
  "authority": "osmo10d07y265gmmuvt4z0w9aw880jnsr700jjeq4qp",
  "contract": "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm",
  "wasm_byte_code": "<base64 deterministic gzip payload; SHA-256 37e6e3ff0eddfc9b4bb162ffd241d39d3d204f1cfa76cfef7510bd4fe1c099f5>",
  "instantiate_permission": {
    "permission": "Nobody",
    "addresses": []
  },
  "msg": {}
}
```

Use `Nobody` because this proposal needs to migrate one named contract, not
create a publicly instantiable code family.

## Public proposal package

The definitive explorer/IPFS-ready proposal is now published in
[`governance/ion-dao-remediation/`](../governance/ion-dao-remediation/).
That package contains:

- the comprehensive human proposal and expedited-vs-standard analysis;
- Cosmos governance `metadata.json`;
- exact `proposal-expedited.json` input;
- generated unsigned transaction;
- exact optimized Wasm;
- structured manifest; and
- immutable IPFS publication receipts.

**Definitive title**

> Expedited: Patch ION DAO Accounting and Quarantine Legacy Claims

The on-chain summary is 1,018 characters and uses simple Markdown headings for
explorer rendering. It links the source review, public proposal review, immutable
metadata, and complete proposal document.

Immutable publication:

- metadata:
  `ipfs://bafkreihki5gssufsdhwtcfpupfv2bnlfq3b7iqtaxxiqyocqi5nq62cduq`;
- full proposal:
  `ipfs://bafkreifslgs4iu4t3opqtwv7gtfshastxeocpj2rrbm634vwvvmqcekt6q`;
- complete package:
  `ipfs://bafybeiftjocrkmwojm5t57lrlkjyzxg2xjb5czzlkhm2mnba76g5ghjhny`.

## Corrected deposit and timing gate

Live Osmosis parameters distinguish the minimum amount required to **submit**
from the full amount required to **start voting**:

| Track | Minimum initial submission | Full voting deposit | Voting period | Yes threshold |
| --- | ---: | ---: | ---: | ---: |
| Standard | 1,500 OSMO | 6,000 OSMO | 5 days | >50% |
| Expedited | 5,000 OSMO | 20,000 OSMO | 24 hours | >66.7% |

The earlier zero-deposit simulation correctly reported the 1,500 OSMO standard
initial-submission floor. That amount alone would only enter deposit period; it
would not start the five-day vote. The definitive expedited payload therefore
uses the full `20000000000uosmo` deposit so its 24-hour vote starts immediately.

The earliest ION expiry is `2026-07-17 11:09:01 UTC`. The recommended standard
start cutoff with six hours of margin was `2026-07-12 05:09:01 UTC`. Once that
passes, expedited voting is the only configured route that can finish before the
incident window. No real Osmosis proposal has been submitted.

Do not broadcast the committed unsigned transaction blindly. Re-query all live
state, regenerate, sign without broadcasting, simulate the exact funded payload,
and obtain explicit approval for the reviewed transaction first.

## Juno mainnet proof receipts

Juno cannot run the Osmosis custom bindings directly, so the proof artifacts
changed only the custom message/query types to `Empty`; the governance,
migration, and deposit state logic remained the reviewed source. This proves
the contract mechanics and authorization ordering, not Osmosis' native
governance execution path.

| Item | Receipt |
| --- | --- |
| v0.0.1 proof code | Juno code `5142`, tx `661E8EC0DFA61DBBC45DDA688E36D0B6E493FD8400E344F0567C86FB8311ED76` |
| v0.0.2 proof code | Juno code `5143`, tx `BA74B1C93A9D7A7A148AF0AF34141EDF2DEBD960BCC40FFF4B3FD6CD196B5028` |
| Proof DAO | `juno1hanfjy97f87gc8va6lymvn9dcsgc40pv4n8099rjqk74x89ayk9st9ge8t` |
| Self-admin transfer | `5DE54DF9F28991AD56DE71A4345F7A369CD85DB161A07CAE3FB32C84B1B45C2B` |
| Atomic proposal 2 + YES vote | `8DC1C19E0B699DA54BCEBA3C2F707D234282665C32D6C31589606B66603EA22D` |
| DAO-executed migration | `757A13EBBC9C53A8DF6E014B51C2B3EC28FC8DA103AA5781473EDE8D610583E1` |
| Post-migration proposal | `A9997AF214F9329EBC35D3C6E946462C61AA2BAD278DAE5A7B401406B7893C68` |
| Post-migration execute | `ADC23AE82F3AD5DA3F4D0C841CA120B1F334667927E3A145DCAB62DBA7E2339D` |
| Post-migration claim | `AE7EF212BA0FBF7671EEEDCC4D9522A1C7AF519711898D4411BD1066C19E8A82` |

Verified outcomes:

1. Wallet privilege ended after the proof DAO became its own chain admin.
2. A passed DAO proposal migrated the contract from code `5142` to `5143`.
3. Migration set cutoff height `39710117`.
4. A signed legacy-claim simulation failed with
   `Deposit claim requires manual reconciliation`.
5. A proposal created after migration executed normally, and its 1ujuno deposit
   was claimed exactly once (`claimed: true`).

One intentionally over-tight three-block vote expired before inclusion. That
failed receipt is recorded too:
`28D0CA8CE51B0523BDE46BED37EC23EE65991C51CC7CDAF16784E73B1DAABEB8`.
The proof recovered by batching proposal creation and voting in one simulated
transaction. No failure is hidden; mainnet receipts are the audit trail.
