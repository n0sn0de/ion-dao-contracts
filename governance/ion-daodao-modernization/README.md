# ION DAO modernization roadmap

Status: **architecture and transition plan only**. This directory does not authorize or perform an Osmosis deployment, migration, treasury transfer, vote, or broadcast.

## Executive decision

Do **not** migrate the legacy ION governance or staking contracts in place to DAO DAO code.

Create a new, self-administered DAO DAO successor on Osmosis, let holders move their own liquid ION into the standard DAO DAO native-token staking module, and retire the legacy governance contract through one atomic legacy-DAO proposal after every preflight gate passes.

This is not a cosmetic front-end swap. The legacy contract is one monolithic governance state machine. DAO DAO is a graph of independently administered core, voting, proposal, and pre-propose modules. Their storage layouts, lifecycle semantics, proposal IDs, deposit accounting, and admin assumptions are different. Pretending otherwise is how treasuries get orphaned.

The recommended path gives ION holders the DAO DAO UI without making Osmosis chain governance the new DAO's administrator:

- the DAO DAO core is both its internal admin and its CosmWasm migration admin;
- proposal, voting, and pre-propose module CosmWasm admins are the core;
- governance changes and future upgrades execute through ION DAO proposals;
- no wallet, deployer, validator, or Osmosis governance account retains production admin power;
- the permissionless DAO DAO admin factory is used only to create the self-admin graph;
- Osmosis governance remains an emergency chain-sovereign last resort, not an operating dependency.

## Recommended transition shape

Use **one on-chain legacy governance proposal**, preceded by off-chain publication, deterministic payload generation, independent review, and exact signed simulation.

The executable proposal should be atomic and ordered:

1. refund the legacy deposits that governance explicitly determines remain valid or equitably refundable;
2. set the legacy staking contract's duration to `None`, so future unstakers receive ION immediately;
3. instantiate the optional veto-only Security Council DAO, if the bounded-security profile is selected;
4. instantiate the new ION DAO DAO core with `Instantiate2ContractWithSelfAdmin`, pinned expected addresses, reviewed code IDs, and the configuration in [`CONFIGURATION.md`](CONFIGURATION.md);
5. transfer the reconciled legacy treasury assets to the predicted new core address;
6. update legacy metadata to state that governance has moved, if the legacy execute interface permits the reviewed update;
7. pause the legacy governance contract with `Expiration::Never` as the final message.

If any message fails, CosmWasm transaction atomicity reverts the entire execution. The legacy DAO remains unpaused, the new deployment and transfers disappear, and the passed proposal can be diagnosed before any retry. That is the right rollback boundary.

Do **not** split treasury transfer and legacy retirement across casually spaced proposals. A half-migrated DAO is an attack surface with two competing authorities.

## Why one governance vote is enough

The risk work belongs before the vote, not in a parade of signaling proposals.

The recommended process is:

- publish this roadmap and the final machine-readable package for public review;
- run all static, local, Juno, and Osmosis simulations;
- obtain independent payload review and a named treasury reconciliation sign-off;
- submit one final executable proposal containing the entire atomic cutover;
- communicate a single voting deadline and a single holder migration guide.

A separate signaling proposal adds attention cost but does not add execution safety. Use one only if the community genuinely disputes the architecture or the deposit-liability policy. Do not manufacture governance theater.

## Current-state facts that constrain the design

The detailed receipt is in [`EVIDENCE.md`](EVIDENCE.md). At Osmosis height `66276760`:

- legacy governance: `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm`;
- code ID `1900`, CW2 `crates.io:ion-dao 0.0.2`, no CosmWasm admin;
- legacy staking: `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc`;
- code ID `2`; admin is the legacy governance contract;
- ION supply: `21,293.014966 ION`;
- active legacy voting power: `1,671.832757 ION` across `1,925` nonzero stakers;
- staking custody: `1,845.681039 ION`;
- mature unstaking claims: `173.848282 ION` across `177` claims;
- the active stake plus mature claims equals the staking contract's ION bank balance exactly;
- legacy governance ION balance: `1,931.931671 ION`;
- the legacy governance bank account also holds OSMO, three IBCX-related tokenfactory denoms, and an IBC LOKI balance;
- the legacy token registry knows only `uion`, so a migration that trusts the registry instead of the bank account will strand assets;
- proposals `22`-`39` contain `662 ION` of quarantined recorded claims, composed of `9 ION` nominal deposits and `653 ION` unsafe overage; the `9 ION` must be explicitly refunded or forfeited before permanent retirement;
- two older, currently claimable deposits total `0.551671 ION`;
- proposals `10` and `11` contain another `1 ION` in passed-but-unexecuted deposits that need an explicit refund/forfeit decision;
- older rejected or underfunded deposits totaling `1.45 ION` are not marked claimable under the legacy rules.

These classes are not interchangeable. The final treasury amount must be recalculated at the execution preflight height.

## Architecture decision record

### Option A — direct migration of the legacy governance contract

**Rejected.**

DAO DAO core expects its own configuration, module registry, admin record, pause state, item map, proposal-module prefixes, and voting-module address. The legacy contract stores proposals, ballots, deposits, treasury denoms, staking address, and governance config under unrelated keys. DAO DAO's normal migrate entrypoint upgrades DAO DAO state; it is not an importer for `ion-dao` state.

A direct `MigrateContract` would require a bespoke, audited state transformer that also creates and wires child modules during migration, maps admin ownership, decides what happens to 39 historical proposals and every deposit, and proves no key collision. The current target is adminless, so attempting this would again require Osmosis chain governance. It gives maximum blast radius and no user benefit over a successor DAO.

### Option B — direct migration of the legacy staking contract

**Rejected.**

The legacy staking contract uses share accounting and maintains user stakes, total share supply, active pool value, and time-based claims. DAO DAO `dao-voting-token-staked` uses its own balance snapshots, total power snapshots, claims controller, DAO identity, denom, active threshold, and configuration keys. Their migrate entrypoints are not cross-product importers.

Migrating user custody through an unaudited storage transform would put all staked and unbonding ION behind a first-time code path. That is exactly the wrong place to save two user transactions.

### Option C — voting adapter around the legacy stake contract

**Rejected for production.**

An adapter can expose voting-power queries, but it leaves the new DAO dependent on the old contract's share semantics, admin relation, claim model, and UI-incompatible stake actions. A proxy cannot unstake a user's legacy position because the legacy contract keys ownership by the direct sender. A custom voting module also increases DAO DAO UI compatibility and audit risk.

An adapter is acceptable only as a throwaway comparison oracle during testing.

### Option D — standard DAO DAO successor with voluntary restaking

**Recommended.**

Holders retain custody and choose when to migrate. The old staking contract continues honoring active stakes and mature claims. The cutover removes the old 14-day delay for new unstakes. The new DAO uses the audited, standard UI-supported token-staked module with one ION equal to one vote.

The cost is two user transactions per active staker: unstake from the old contract and stake into the new module. That inconvenience is smaller than migrating user funds through bespoke code.

## Target module graph

```text
DAO DAO admin factory (permissionless, no retained authority)
  └─ instantiate2 ION DAO core
       ├─ internal admin: core itself
       ├─ CosmWasm admin: core itself
       ├─ voting module: dao-voting-token-staked (uion)
       │    └─ CosmWasm admin: core
       └─ proposal module A: dao-proposal-single
            ├─ CosmWasm admin: core
            └─ pre-propose: dao-pre-propose-single
                 └─ CosmWasm admin: core

Optional bounded-security profile:
Security Council member DAO (no treasury, no general admin)
  └─ address used only as proposal-module vetoer during 48-hour timelock

Legacy stake contract during holder wind-down
  ├─ internal config admin: new ION DAO core
  └─ CosmWasm migration admin: new ION DAO core
```

Launch with one single-choice proposal module. Do not add multiple-choice, vote delegation, rewards, payroll, or arbitrary app modules merely because they exist. Every module is code, permissions, UI surface, and future migration work. Add features when a real governance need survives review.

## Cutover roadmap

### Phase 0 — freeze the specification

Deliverables:

- final module/code-ID manifest pinned to a specific DAO DAO UI registry commit;
- source tag and source commit for every deployed Wasm artifact;
- code hashes queried independently from two Osmosis endpoints;
- exact self-admin factory address, code hash, admin query, and contract history;
- deterministic salts and predicted core/module addresses;
- final DAO metadata and immutable `dao_uri` document;
- final legacy-deposit adjudication table;
- final treasury-denom inventory from the bank module, not the legacy registry;
- final executable message bundle and human-readable decode;
- review acknowledgements from at least two technically competent reviewers who did not generate the payload.

Gate: no unresolved address, code hash, liability class, or admin field.

### Phase 1 — complete live-state reconciliation

At a single retained height:

1. query chain ID, app version, block height, and time;
2. query legacy governance and stake contract info, history, code IDs, hashes, CW2, creator, and admins;
3. export all proposals, votes, deposits, and current status;
4. export all stakers, current voting power, active stake value, and all claims;
5. sum claims and prove active pool plus claims equals staking ION custody;
6. query every bank balance held by legacy governance and staking;
7. query ION total supply and denom metadata;
8. classify legacy governance ION into:
   - valid/refundable legacy deposits;
   - passed-but-unexecuted deposit policy items;
   - forfeited deposits;
   - quarantined nominal exploit deposits;
   - quarantined unsafe overage;
   - unencumbered treasury;
9. record all non-ION assets and whether the target UI resolves their metadata;
10. archive the raw snapshot and a checksum manifest.

Gate: arithmetic reconciles to atomic units. A label such as “treasury” is not arithmetic.

### Phase 2 — resolve deposit policy before drafting the transfer

Recommended treatment:

- refund `0.551671 ION` associated with the two older entries that are both unclaimed and marked `deposit_claimable=true`;
- refund the `1 ION` tied to passed-but-unexecuted proposals `10` and `11`, unless reviewers find a legal or chain-state reason not to;
- treat the `1.45 ION` of rejected/nonclaimable deposits according to the legacy rules as treasury, while disclosing the classification;
- resolve the `9 ION` nominal principal behind proposals `22`-`39` before permanent retirement. The preferred clean-exit policy, absent contrary evidence, is to refund only the actual `0.5 ION` deposited for each proposal while rejecting the `653 ION` fictitious overage. Governance may instead forfeit the principal, but it must say so explicitly;
- reject the `653 ION` unsafe recorded overage as a valid liability; it arose from broken accounting, not deposited funds;
- never copy the `662 ION` recorded-claim total into the new DAO as a liability or send it to the exploit claimant.

At the referenced snapshot, the preferred clean-exit policy would transfer `1,921.38 ION` after `10.551671 ION` of refunds (`1.551671 ION` older items plus `9 ION` nominal exploit principal). That is an illustration, not an executable amount. Recalculate immediately before submission and execution.

Do not pause the legacy DAO forever while calling the `9 ION` “pending.” A permanent pause removes the ordinary ION-governance path to resolve it and would recreate an Osmosis-governance dependency. If the community cannot adjudicate the principal, the cutover is not ready.

Gate: the proposal body contains the full table, addresses, amounts, and policy rationale. No euphemisms.

### Phase 3 — build deterministic deployments

Use the DAO DAO `v2.7.0` Osmosis deployment currently recognized by the UI, unless a newer release is deployed and independently reviewed before proposal freeze.

Required mechanics:

- execute the existing permissionless `cw-admin-factory` rather than let a wallet retain admin;
- use instantiate2 with a unique, published salt;
- set `expect` to the independently derived new core address so a derivation mismatch fails closed;
- use unique salts for voting, proposal, pre-propose, and optional Security Council modules;
- set every `ModuleInstantiateInfo.admin` to `CoreModule`;
- set core instantiate `admin` to `None`, which makes the core its internal admin;
- set the core's CosmWasm admin to itself through the factory reply;
- attach no funds to module instantiation unless required and accounted for;
- include no deployer address in production admin fields.

Gate: signed REST simulation instantiates the exact predicted addresses and emits the exact admin-update events.

### Phase 4 — execute the single atomic legacy proposal

Message order matters:

1. every approved legacy deposit refund, including the explicit decision on the `9 ION` nominal exploit principal;
2. optional Security Council instantiation;
3. new core/module instantiation through the admin factory;
4. old stake `UpdateConfig` setting `duration: None` and internal `admin` to the predicted new core;
5. old stake CosmWasm `UpdateAdmin` setting its migration admin to the predicted new core;
6. exact bank transfers to the predicted core address for every reconciled treasury denom;
7. optional legacy metadata update;
8. legacy `PauseDAO { expiration: Never }` last.

Do not include a migration of either legacy contract. Do not transfer the legacy staking contract's ION balance. It belongs to active stakers and claimants. The two stake-admin handoffs preserve a self-governed recovery path without changing custody or user balances.

The execution transaction must be simulated from an account allowed to execute the passed proposal. Simulation must prove all nested messages, transfers, instantiations, and the final pause. A generated transaction is not a simulation.

Gate: code `0`, expected gas margin, exact events, and no unexpected message or receiver.

### Phase 5 — holder migration

Publish one short holder guide:

1. claim any mature legacy unstaking claim;
2. unstake legacy ION; after the cutover this should return immediately for newly created unstakes;
3. verify the new voting-module address from the published manifest and DAO DAO page;
4. stake the chosen amount in the new DAO DAO UI;
5. verify voting power through both the UI and a direct smart query.

The old stake contract remains live until every holder chooses to exit. Pausing legacy governance does not pause direct stake claims or unstakes.

Set the new active threshold to `3%` of total ION supply. At the referenced supply this is approximately `638.790449 ION`. The new DAO remains inactive—and therefore cannot accept proposals—until enough holders migrate. This is a safety lock, not a participation target.

Gate: active threshold met by more than one independent holder, no single migration operator custody, and voting-power sums reconciled.

### Phase 6 — production acceptance

Before declaring success, verify:

- daodao.zone renders the Osmosis core by direct URL;
- name, description, image, DAO URI, proposal module, voting module, members, and treasury pages load;
- core internal admin equals core;
- core CosmWasm admin equals core;
- module CosmWasm admins equal core;
- factory has no authority over the deployed DAO;
- ION denom and total supply queries succeed;
- active threshold, staking duration, threshold, quorum, periods, revoting, submission policy, deposit, refund policy, execution policy, veto, and delegation settings match the manifest;
- every transferred denom and amount matches the cutover receipt;
- legacy governance is paused forever;
- legacy staking claims remain payable;
- legacy stake internal and CosmWasm admins equal the new core during wind-down;
- the legacy governance terminal balance matches the approved accounting, ideally zero `uion` after refunds and transfer;
- no unexpected admin, allowlist, hook, proposal module, subDAO, or token appears;
- a small production proposal can be submitted, voted, and executed through DAO DAO;
- proposal deposit behavior is correct for both passed and rejected paths.

## Rollback and contingency matrix

| Failure point | Expected behavior | Response |
| --- | --- | --- |
| Preflight mismatch | No transaction signed | Regenerate snapshot and package |
| Signed simulation fails | No broadcast | Fix payload; invalidate old checksums |
| Legacy proposal rejected | No state change | Publish result; revise only if community asks |
| Proposal execution message fails | Entire execution reverts | Diagnose retained passed proposal before retry |
| New DAO instantiates but later message fails | Instantiation reverts with transaction | Verify predicted address remains absent |
| Treasury amount changed before execution | Bank send fails or leaves disclosed delta | Re-simulate and, if necessary, replace proposal rather than improvise |
| Active threshold not met | New treasury is locked from proposals | Continue holder migration; do not lower threshold from a wallet |
| DAO DAO UI outage | Contracts remain usable by direct queries/transactions | Publish CLI fallback; UI is not authority |
| Bad module/admin state after success | Stop holder migration and treasury actions | Use only self-governed correction paths; consider chain governance solely for an otherwise unrecoverable chain-level defect |

There is no rollback that restores a completed treasury transfer and permanent legacy pause without another authorized path. That is why the atomic proposal and fully reconciled terminal legacy balance are load-bearing.

## Governance-fatigue budget

The modernization should require:

- one public review period;
- one legacy governance proposal and vote;
- no separate Osmosis governance proposal;
- no vote merely to “signal support” unless architecture is disputed;
- one holder migration guide;
- one first proposal on the new DAO to prove production governance, preferably a harmless metadata or receipt action.

Do not combine the prior-operator vesting dispute with the modernization execution. That issue is documented separately in the companion assessment. Bundling a contentious clawback demand into the infrastructure cutover is a good way to make both fail.

## Work still requiring explicit authorization

This roadmap does not authorize:

- creation of the production Security Council or selection of its members;
- generation of a production Osmosis instantiate payload;
- submission of the legacy ION proposal;
- voting or execution;
- any refund, treasury transfer, pause, migration, or chain-governance request;
- any change to the prior operator's vesting account.

The next authorized implementation phase should produce reviewable, unsigned artifacts first.

## Companion documents

- [`CONFIGURATION.md`](CONFIGURATION.md) — concrete recommended production values and rationale
- [`EVIDENCE.md`](EVIDENCE.md) — live-state, DAO DAO, Mad Scientists, and accounting evidence
- [`TEST-PLAN.md`](TEST-PLAN.md) — risk-proportionate validation and acceptance matrix
- [`JUNO-VALIDATION.md`](JUNO-VALIDATION.md) — completed bounded Juno mainnet proof and limitations
- [`REPRODUCE.md`](REPRODUCE.md) — infrastructure-neutral read-only query recipe
- companion PR: prior-operator vesting allocation assessment and response options
