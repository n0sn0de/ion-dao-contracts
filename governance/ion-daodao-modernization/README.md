# ION DAO modernization roadmap

Status: **reviewed architecture and transition plan only**. This package does not authorize or perform an Osmosis deployment, proposal, vote, migration, treasury transfer, or broadcast.

This revision incorporates hostile source review. It deliberately rejects the earlier one-transaction cutover design. Saving one ballot is not worth creating a DAO that can lock its own treasury or publishing a front-runnable `Instantiate2` address.

## Executive decision

Create a **new standard DAO DAO v2.7.0 successor** on Osmosis. Do not migrate the legacy governance or staking storage into unrelated DAO DAO contracts.

Use a staged handoff:

1. approve the reviewed configuration and transition policy;
2. predeploy an empty self-admin successor using ordinary factory `InstantiateContractWithSelfAdmin`, not `Instantiate2`;
3. enable low-friction exits from legacy staking and begin the IBCX application-governance handoff;
4. require the successor to become active with margin, execute a harmless proposal, and accept IBCX application governance;
5. only then execute a final legacy proposal that settles deposits, transfers admins and reconciled treasury assets, and permanently pauses legacy governance.

The successor must be live, active, inspected, and proven before receiving the treasury. An inactive self-admin DAO cannot submit a proposal to lower its own active threshold. Calling that condition a “safety lock” would hide a chain-governance recovery dependency.

## Primary addresses

| Role | Address |
|---|---|
| Legacy ION governance | `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm` |
| Legacy ION staking | `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc` |
| DAO DAO self-admin factory | `osmo1qpszqk458arkkdff5z4vrqlqv4k2n9a0tjme23vn00uyt30nrr7sfe87cv` |
| Mad Scientists DAO reference core | `osmo1gtx8ka0d4jxcf5yyypll8824tz33ykmr27v04ff0r6dn9ucykr0shev4h7` |

The production successor address does not exist yet. It must not be guessed or presented as approved.

## Companion documents

- [`EVIDENCE.md`](EVIDENCE.md) — pinned live-state and code evidence
- [`CONFIGURATION.md`](CONFIGURATION.md) — recommended clean launch settings
- [`TEST-PLAN.md`](TEST-PLAN.md) — source, simulation, canary, and acceptance gates
- [`JUNO-VALIDATION.md`](JUNO-VALIDATION.md) — completed bounded Juno proof and its limits
- [`REPRODUCE.md`](REPRODUCE.md) — height-pinned read-only query recipe
- [`SOURCE-PINS.md`](SOURCE-PINS.md) — immutable source references for transition semantics
- [`evidence-manifest.json`](evidence-manifest.json) — SHA-256 manifest for retained evidence receipts in [`evidence/`](evidence/)
- companion assessment: [PR #8](https://github.com/n0sn0de/ion-dao-contracts/pull/8)

## What is being replaced

The legacy DAO combines:

- proposal creation and partial deposits;
- token voting with Yes, No, Abstain, and token-holder Veto;
- execution of arbitrary Cosmos messages;
- treasury token registration;
- governance configuration;
- a reference to a custom share-based staking contract.

Modern DAO DAO separates those concerns:

- `dao-dao-core` — treasury, metadata, module registry, self-administration;
- `dao-voting-token-staked` — native-token staking and voting snapshots;
- `dao-proposal-single` — proposal lifecycle and execution;
- `dao-pre-propose-single` — member gate and atomic proposal deposit.

The modern architecture is better because each boundary is explicit and queryable. It is not storage-compatible with the legacy contracts.

## Why direct migration is rejected

### Governance storage

Legacy state contains `config`, `proposal_count`, `proposals`, composite deposit records, ballots, token registrations, and pause state. DAO DAO core expects a module registry, voting-module address, proposal modules, item map, pause state, internal admin, metadata, and DAO URI.

DAO DAO’s migrate entrypoint upgrades DAO DAO state. It is not an importer for `ion-dao` storage. Pointing the legacy address at DAO DAO code would not preserve governance history; it would reinterpret unrelated keys and likely brick the DAO.

The legacy governance contract is adminless. Another in-place migration would also require Osmosis governance or equivalent chain authority.

### Staking storage and semantics

The legacy stake contract uses shares. `Unstake { amount }` burns **share units**, and payout is:

```text
shares burned × current backing / total shares
```

Permissionless `Fund` can change the share-to-ION ratio. At the retained snapshot it was 1:1, but that is not a permanent invariant.

DAO DAO token-staked voting has different storage, snapshots, claims, DAO identity, and configuration. Its migrate entrypoint does not import legacy shares or claims.

### Adapter path

A proxy cannot unstake a holder’s legacy position because ownership is keyed by the direct sender. A custom adapter would preserve old share semantics and incompatible stake actions while adding a fresh audit surface. That is the worst of both worlds: custom risk plus permanent legacy dependency.

### Successor path

A clean successor makes each holder choose when to migrate. The final design never moves user stake custody. The legacy stake contract remains perpetually callable—it has no retire or pause message—even after all users exit. Public interfaces must mark it obsolete, but users retain direct `unstake` and `claim` access.

## Live evidence boundary

The retained governance/balance snapshot is Osmosis height `66276760`, block time `2026-07-14T05:23:22.014415229Z`.

At that boundary:

- legacy governance held `1,931.931671 ION` plus five non-ION bank denoms;
- active staking backing and voting shares were `1,671.832757 ION`;
- 177 mature staking claims totaled `173.848282 ION`;
- stake-contract ION custody reconciled exactly:

```text
1,671.832757 active backing
+ 173.848282 mature claims
= 1,845.681039 ION held
```

The full holder/claim export was paginated over moving head state and reconciled exactly to the pinned aggregate balances. Production must repeat the export at one archive height and retain raw responses.

## Deposit classes that must be resolved

| Class | Amount | Required decision before final pause |
|---|---:|---|
| Older deposits presently marked claimable | 0.551671 ION | Manual refund recommended |
| Passed-but-unexecuted proposals 10 and 11 | 1.000000 ION | Explicit refund or forfeiture decision |
| Rejected/nonclaimable legacy deposits | 1.450000 ION | Treat according to original rules unless governance decides otherwise |
| Actual principal behind affected proposals 22–39 | 9.000000 ION | Refund or expressly forfeit; do not call it a pending reserve |
| Unsafe recorded overage | 653.000000 ION | Reject as nonphysical accounting overage |
| Future transition-enabling proposal deposit | 0.500000 ION | Claim normally before final pause |
| Future final-handoff proposal deposit | 0.500000 ION | Manually refund inside final execution before pause |

A permanent pause blocks later `ClaimDeposit`. Therefore no intended liability may remain “pending” in the old DAO.

Using the preferred illustration—refund `0.551671`, refund the `1.0`, refund the actual `9.0`, reject the `653` overage, and separately account for the future proposal deposits—the retained-height successor transfer starts from:

```text
1,931.931671 - 0.551671 - 1.000000 - 9.000000
= 1,921.380000 ION
```

That is not an executable amount. The transition-enabling and final-handoff proposal deposits, claims made in the interim, incoming funds, and all other bank denoms must be included in a fresh production reconciliation.

## IBCX control is governance state, not treasury

The legacy DAO controls three live IBCX-family contracts:

| Product | Contract | CW2 | Legacy control |
|---|---|---|---|
| New IBCX | `osmo14klwqgkmackvx2tqa0trtg69dmy0nrg4ntq4gjgw2za4734r5seqjqm4gm` | `ibcx-core 0.1.2` | Wasm admin, application `gov`, fee collector |
| stIBCX | `osmo1xqw2sl9zk8a6pch0csaw78n4swg5ws8t62wc5qta4gnjxfqg6v2qcs243k` | `ibcx-core 0.1.1` | Wasm admin, application `gov`, fee collector |
| Old IBCX | `osmo1yhd9tzp09d833u7ray4pc6wwp72aewtt2xwakszn3lzlf2klnlwscjwhxt` | `ibcx-core 0.1.1` | Wasm admin, application `gov`, fee collector |

Their backing portfolios belong to index-token holders. They are **not DAO treasury** and must never be swept during modernization.

Application governance is a two-step transfer:

1. legacy DAO sets `pending_gov` to the successor;
2. successor executes `accept_gov`.

This cannot be atomic across both DAOs. It is a reason to stage the transition rather than pretending one omnibus transaction is safer.

Before changing any fee collector, production source review must determine whether accrued fees require `realize {}` and must verify the exact update message. Keep the legacy fee collector unchanged until the successor is active and has accepted application governance.

## Revised transition roadmap

### Phase 0 — freeze policy and evidence off-chain

Produce an immutable review package containing:

- DAO DAO tag, source commit, code IDs, live hashes, and instantiate permissions;
- exact core, voting, proposal, and pre-propose JSON;
- every admin field;
- a pinned-height legacy export;
- complete bank-denom inventory;
- known CW20/CW721 discovery results and limitations;
- deposit settlement table;
- IBCX governance/admin/fee-collector handoff table;
- user migration guide;
- abort, communication, and residual-fund policies.

Policy disagreements must be settled before a technical ballot. Do not bury contested deposit treatment or product-control decisions inside an unreadable omnibus payload.

### Phase 1 — predeploy the empty successor

Use the existing adminless factory’s ordinary `InstantiateContractWithSelfAdmin` path.

Do **not** use production `Instantiate2`:

- the successor is deployed before any treasury handoff, so a predictable address is unnecessary;
- the factory is permissionless;
- an `Instantiate2` address depends on factory, code hash, and salt—not on the external caller or init message;
- a published or mempool-visible salt can be occupied first, making a governance-approved payload unexecutable.

Deployment requirements:

- successor starts with no production treasury or authority;
- factory and deployer retain no admin;
- core internal admin is self;
- core Wasm admin is self;
- child-module Wasm admins are core;
- exact code hashes and configuration match the manifest;
- direct daodao.zone routes load;
- no legacy contract changes occur.

A bad predeployment is abandoned. No chain-governance recovery is required because no production authority has moved.

### Phase 2 — transition-enabling legacy proposal

Use exactly one documented `0.5 ION` depositor. The proposal should:

1. ratify the exact deployed successor address and manifest hash;
2. update the old stake config with **both fields explicitly serialized**:

```json
{
  "update_config": {
    "admin": "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm",
    "duration": null
  }
}
```

3. set each approved IBCX contract’s `pending_gov` to the successor;
4. leave current fee collectors and Wasm admins unchanged;
5. contain no treasury transfer, permanent pause, or stake custody movement.

After execution:

- verify the legacy stake internal admin remained the old DAO;
- verify new unstakes have no delay while old mature claims remain claimable;
- claim the proposal’s `0.5 ION` deposit normally;
- retain the claim receipt before proceeding.

Omitting `admin` from `UpdateConfig` deserializes it as `None` and burns the internal admin. Schema validation alone does not protect this field.

### Phase 3 — activate and prove the successor

Holders migrate voluntarily:

1. query legacy share balance **and** staked value;
2. submit `Unstake` using the share amount;
3. verify the received ION amount;
4. claim any existing mature claim;
5. stake ION in the successor voting module;
6. verify voting power.

The final handoff is blocked until all of the following hold:

- `IsActive == true`;
- staked power is at least 4% of current total supply, providing margin over the 3% threshold;
- participation is distributed across multiple independent holders;
- no migration operator has custody of holder funds;
- a harmless successor proposal has been submitted, voted, successfully executed, and reconciled;
- daodao.zone renders configuration and proposal state correctly.

The 3% threshold is dynamic. The contract reads current supply and ceilings 3% on every `IsActive` query. A supply increase can deactivate the DAO without anyone unstaking, so the 4% handoff margin is a minimum, not a guarantee.

### Phase 4 — accept IBCX application governance

After the successor is active and the legacy proposal has set `pending_gov`, create a dedicated successor proposal that:

- calls `accept_gov` on all approved IBCX contracts;
- performs any source-reviewed fee realization after acceptance;
- updates fee collectors only after acceptance, if approved;
- includes no unrelated treasury action;
- verifies post-state `gov == successor`, `pending_gov == none`, and the approved fee collector for every contract.

Do not permanently pause legacy governance until every accepted product-control receipt is complete. If any product is intentionally excluded or abandoned, governance must say so explicitly.

### Phase 5 — final legacy handoff proposal

Submit with exactly `0.5 ION` from one documented depositor. After the proposal is fully funded, re-export proposals, deposits, balances, admins, IBCX controls, stake state, and code state.

The exact message order should be:

1. manual refund of the final proposal’s `0.5 ION` deposit;
2. every other approved legacy deposit refund;
3. old stake `UpdateConfig` with explicit successor admin and `duration: null`;
4. old stake CosmWasm `UpdateAdmin` to successor;
5. approved IBCX CosmWasm admin transfers to successor;
6. exact treasury bank sends for every approved native denom;
7. optional legacy metadata update **only** as an exact full-config before/after diff preserving all nonmetadata fields;
8. `PauseDAO { Never }` as the final message.

The stake update must be explicit:

```json
{
  "update_config": {
    "admin": "NEW_SUCCESSOR_CORE",
    "duration": null
  }
}
```

The legacy proposal schema has no `Instantiate2` message. The final proposal references an already-deployed, already-active successor.

Do not:

- instantiate production contracts in the final handoff;
- migrate legacy governance or stake storage;
- transfer stake-contract ION;
- sweep IBCX backing portfolios;
- leave intended deposit liabilities behind;
- omit an admin field;
- assume static bank sends capture funds received after proposal creation.

### Static-balance residual policy

Legacy BankMsg sends are static. Anyone can send extra coins to the old DAO during voting. The final payload cannot dynamically sweep “all current balances.”

Therefore:

- publish exact approved amounts and a cutoff height;
- monitor the legacy account through execution;
- warn users never to send funds to the legacy address;
- acknowledge that unsolicited post-snapshot funds may remain stranded after permanent pause;
- do not claim exhaustive zero balance if an unsolicited transfer appears;
- document any residual and the fact that recovery may require Osmosis chain authority.

This is an unavoidable limitation of permanently retiring an adminless address, not something documentation should conceal.

## Recommended configuration

See [`CONFIGURATION.md`](CONFIGURATION.md). The baseline contains no external vetoer. A Security Council is not part of this production recommendation until a separate complete module graph, four-field veto config, code/hash manifest, enforceable or honestly social mandate, sunset, replacement path, and bounded mainnet proof exist.

## Governance-attention budget

The safe path requires more than one ballot:

| Action | Venue | Why it cannot be skipped |
|---|---|---|
| Transition-enabling proposal | Legacy ION DAO | Removes exit delay and starts two-step product governance handoff |
| Harmless lifecycle proposal | Successor | Proves active governance and execution before authority moves |
| IBCX acceptance proposal | Successor | Completes cross-DAO two-step product control |
| Final handoff proposal | Legacy ION DAO | Settles deposits, transfers admins/treasury, and retires old governance |

That is two legacy votes and two successor votes. It is more attention than a one-ballot cutover, but materially safer. The package keeps each ballot narrow enough to review and avoids asking one binary vote to approve policy, deployment, activation, product custody, treasury transfer, and irreversible retirement simultaneously.

## Abort gates

Abort or replace a proposal if:

- any code ID, hash, admin, address, or config differs from the reviewed manifest;
- the successor is inactive or falls below the 4% handoff margin;
- the harmless successor proposal fails;
- product `gov`, `pending_gov`, fee collector, or Wasm admin differs from plan;
- old stake share:value ratio changes unexpectedly;
- any claim/deposit/refund table fails reconciliation;
- any intended treasury denom is missing;
- a known CW20/CW721 discovery path is incomplete without explicit limitation;
- the final proposal deposit is not manually included;
- exact simulation fails or nested events are incomplete;
- policy decisions remain disputed.

## Completion criteria

Modernization is complete only when:

- successor code/config/admin matrix is verified;
- successor is active with margin and distributed participation;
- harmless successor governance lifecycle succeeded;
- approved IBCX application governance is accepted by successor;
- final legacy proposal executed successfully;
- final proposal deposit and all approved legacy deposits were settled exactly once;
- legacy stake internal and CosmWasm admins are successor-controlled;
- approved IBCX Wasm admins and fee collectors match policy;
- every treasury bank denom reconciles;
- legacy governance is permanently paused;
- legacy stake and governance addresses are clearly marked obsolete;
- users can unstake/claim old positions and stake/vote in the successor;
- direct daodao.zone pages render correctly;
- raw receipts, tx hashes, and residual limitations are published.

## Work deliberately not performed

- no Osmosis production deployment;
- no production successor salt or address publication;
- no legacy proposal creation, funding, vote, execution, or pause;
- no treasury or IBCX control movement;
- no user stake migration;
- no direct storage migration;
- no Security Council deployment.
