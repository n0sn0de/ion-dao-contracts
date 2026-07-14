# Risk-proportionate test and acceptance plan

The transition changes governance authority, treasury custody, legacy stake administration, and control of live IBCX contracts. The test program must match that risk.

## Safety rules

1. Production successor is predeployed empty before any authority or treasury moves.
2. Production uses ordinary self-admin factory instantiate, not a public `Instantiate2` salt.
3. No treasury handoff occurs while successor `IsActive == false`.
4. Final handoff requires at least 4% of current ION supply staked, distributed participation, and a successfully executed harmless successor proposal.
5. Every legacy `UpdateConfig` field is explicit. Omitted admin fields are test failures.
6. IBCX backing portfolios are never treated as DAO treasury.
7. Final proposal deposit is manually refunded before permanent pause.
8. Every query in a production evidence package uses one archive height.
9. No signer or broadcaster is introduced by this documentation.

## Layer 1 — source and schema review

### Legacy governance

Confirm against the exact deployed v0.0.2 source:

- self-only rules for pause and full config replacement;
- `pause_d_a_o` serialization;
- proposal execution ordering and transaction atomicity;
- deposit-claimable transition before message dispatch;
- pause blocking `ClaimDeposit`;
- bank, Wasm execute, migrate, update-admin, and custom-message serialization;
- inability to dynamically send an entire runtime balance;
- inability to instantiate2 from the legacy proposal schema.

### Legacy stake

Confirm:

- `UpdateConfig` assigns `admin` and `duration` unconditionally;
- omitted JSON properties deserialize to `None`;
- `Unstake.amount` is shares;
- payout formula under non-1:1 backing;
- `Fund` changes backing/share ratio;
- existing claims retain original release conditions;
- direct unstake/claim remains available when governance is paused;
- contract has no retire, pause, generic sweep, or DAO-reference update.

Required negative test:

```json
{"update_config":{"duration":null}}
```

must demonstrate that omitted `admin` burns the internal admin. Production fixtures must reject this shape.

### DAO DAO v2.7.0

Review exact tag/source for:

- core self-admin behavior;
- ordinary self-admin factory instantiate;
- child-module admin assignment;
- dynamic active-threshold ceiling;
- proposal inactivity rejection;
- revoting completion behavior;
- `only_members_execute` enforcement;
- `close_proposal_on_execution_failure` behavior;
- `OnlyPassed` refund only for successfully Executed status;
- pre-propose whole-denom withdrawal semantics;
- proposal and voting snapshots;
- native `uion` acceptance.

### IBCX contracts

For all three controlled products, pin exact source/code and test:

- `realize` semantics;
- fee-collector update;
- `update_gov` authorization and pending state;
- `accept_gov` authorization;
- Wasm admin transfer;
- current backing portfolios unchanged by control messages.

## Layer 2 — height-pinned state export

At archive height `H`, retain raw responses for:

- block header and app hash;
- legacy contract info, code info, CW2, config, pause state, migration history;
- every proposal, vote aggregate, deposit, and claimability flag;
- legacy DAO bank balances;
- old stake config, shares, backing, claims, and bank balances;
- ION supply;
- IBCX contract config/control/admin/balances;
- successor config/admin/module graph after deployment.

### Complete asset discovery

Native bank inventory is necessary but not sufficient.

Also:

1. query known CW20/CW721 contracts;
2. scan historical transfer/send/receive events involving the legacy address;
3. use at least one indexed account/contract holdings source;
4. compare project manifests and prior disclosures;
5. record archive/indexer gaps explicitly.

Do not assert exhaustive absence of CW20/CW721 assets from bank queries.

## Layer 3 — local deterministic tests

### Successor instantiate fixture

Validate exact production JSON against schemas and Rust types. Assert:

- core internal and Wasm admin = self;
- voting/proposal/pre-propose Wasm admins = core;
- existing `uion` configured;
- dynamic 3% active threshold;
- seven-day unbond;
- majority/30%/five-day/48-hour parameters;
- revoting enabled;
- members-only execution enabled;
- close-on-execution-failure enabled;
- 1 ION pre-propose bond;
- `OnlyPassed` semantics;
- no veto/delegation module;
- no initial actions or production treasury.

### Active-threshold tests

Test:

- below 3%: propose fails `InactiveDao`;
- exactly contract ceiling: active;
- supply increase above current margin: DAO can deactivate;
- 4% handoff margin at current supply;
- no wallet/admin path can lower threshold while inactive.

### Proposal deposit matrix

| Scenario | Expected result |
|---|---|
| Successfully executed proposal | Deposit refunded exactly once |
| Passed but not executed | Deposit remains escrowed |
| Execution fails with close-on-failure | Final status and deposit destination match exact completion hook |
| Rejected proposal | Deposit follows reviewed non-executed policy |
| Duplicate completion hook | Rejected |
| Deposit amount/denom mismatch | Rejected |
| Nonmember propose | Rejected |

### Pre-propose withdrawal matrix

- with any outstanding refundable deposit: withdrawal forbidden by runbook/test gate;
- with zero outstanding liabilities: entire selected-denom balance transfers once;
- negative test: force withdrawal with an outstanding bond and prove later refund would fail;
- never call this an “excess-only” withdrawal.

### Legacy stake migration matrix

Test both 1:1 and funded/non-1:1 cases:

1. query shares and staked value;
2. unstake share amount;
3. verify formula payout;
4. preserve existing claim maturity;
5. stake received ION in successor;
6. reconcile total user value excluding fees.

Test that the legacy contract remains callable after all users exit and can still receive `Stake`/`Fund` calls. UI retirement, not contract retirement, is the available control.

### Exact legacy stake admin fixtures

Phase 2 expected post-state:

```text
internal admin = legacy DAO
Wasm admin     = legacy DAO
duration       = None
```

Final handoff expected post-state:

```text
internal admin = successor core
Wasm admin     = successor core
duration       = None
```

Reject fixtures where either layer is omitted or transferred early.

### Final proposal deposit

Model a final proposal funded with exactly 0.5 ION:

- execution marks its deposit claimable;
- first BankMsg manually refunds exactly 0.5 ION to documented depositor;
- permanent pause follows only after all other approved transfers;
- later `ClaimDeposit` is blocked but no physical liability remains;
- receipt labels the record manually settled.

### Residual-fund test

Send an unsolicited coin to legacy governance after final payload construction. Verify:

- static BankMsg transfer does not sweep the extra coin;
- final pause strands it;
- documentation reports residual rather than claiming zero balance;
- no hidden recovery path exists without chain-level authority.

## Layer 4 — empty Osmosis predeployment

Use ordinary factory `InstantiateContractWithSelfAdmin`.

Before broadcasting:

- pin code IDs/hashes and instantiate permissions;
- validate exact nested JSON;
- simulate the signed transaction;
- verify gas margin and fees;
- ensure no production funds are attached.

After inclusion:

- record tx hash, height, core and module addresses;
- query full admin matrix;
- verify no deployer/factory admin;
- verify core/module CW2 identities;
- verify zero production authority/treasury;
- load direct daodao.zone pages;
- abandon the graph if anything differs.

No salt or predicted address is a production dependency.

## Layer 5 — transition-enabling proposal simulation

Simulate exact legacy proposal execution including:

- full `UpdateConfig` with legacy admin and `duration:null`;
- IBCX `pending_gov` updates;
- unchanged IBCX fee collectors and Wasm admins;
- no treasury transfer;
- no permanent pause;
- no Wasm admin handoff.

Verify nested events and exact post-state. After real execution, claim its 0.5 ION deposit before proceeding.

## Layer 6 — successor activation and lifecycle canary

Block final handoff until:

- `IsActive == true`;
- at least 4% of current supply is staked;
- holder distribution report is reviewed;
- one harmless proposal completes full propose/vote/execute/deposit-refund lifecycle;
- execution and refund receipts reconcile;
- UI renders the result.

The harmless proposal should move a dust amount already held by successor. It must not alter admins, production treasury, IBCX controls, or thresholds.

## Layer 7 — IBCX acceptance

Create a dedicated successor proposal that accepts application governance for approved IBCX contracts.

Test and verify:

- precondition `pending_gov == successor`;
- postcondition `gov == successor`;
- `pending_gov == none`;
- source-reviewed fee realization after acceptance, if required;
- approved fee collector update only after acceptance;
- backing balances unchanged;
- fee collector matches approved policy;
- no unrelated message included.

Do not proceed to final legacy pause if any acceptance fails.

## Layer 8 — final handoff simulation

After the final proposal is fully funded, export state again. Build exact static amounts from that export.

Simulation must verify message order:

1. final proposal 0.5 ION manual refund;
2. every approved historical refund;
3. legacy stake internal admin handoff with duration `None`;
4. legacy stake Wasm admin handoff;
5. approved IBCX Wasm admin handoffs;
6. every approved native-denom treasury transfer;
7. optional exact full-config metadata replacement or no metadata message;
8. permanent legacy pause last.

Require:

- code 0;
- complete nested events;
- exact refund receivers and amounts;
- exact treasury receiver/denoms/amounts;
- exact old/new admin values;
- IBCX backing balances untouched;
- 40% gas headroom;
- no secret or local-path leakage in retained artifacts.

## Fault injection

Every case must fail without partial state changes:

- wrong core/module code ID or hash;
- external core admin;
- wrong child-module admin;
- inactive successor;
- successor below 4% handoff margin;
- failed harmless proposal;
- omitted legacy stake admin field;
- only one stake admin layer transferred;
- wrong IBCX `pending_gov` or current gov;
- missing final proposal deposit refund;
- refund above approved principal;
- missing bank denom;
- attempt to transfer stake-contract ION;
- attempt to sweep IBCX backing assets;
- stale account sequence;
- out-of-gas nested execution;
- final pause placed before another message;
- disputed/unapproved policy hash.

## Post-execution acceptance

Immediately retain:

- final transaction and nested events;
- successor core/module dumps;
- `IsActive` and current supply/threshold;
- all admin relationships;
- successor and legacy bank balances;
- final proposal and deposit record/manual-settlement receipt;
- legacy pause state;
- old stake config, admins, shares, backing, and claims;
- IBCX gov/pending/admin/fee collector/backing balances;
- direct daodao.zone rendering;
- any unsolicited residual funds.

## Holder canary sequence

Before broad communication, use consenting holders with bounded amounts:

1. query legacy shares/value;
2. unstake shares;
3. verify payout;
4. claim existing mature claim if present;
5. stake in successor;
6. vote;
7. verify voting power and UI.

Stop if value reconciliation fails or if UI directs users to the obsolete stake address.

## Governance-attention budget

Expected binding actions:

- one legacy transition-enabling vote;
- one harmless successor lifecycle vote;
- one successor IBCX acceptance vote;
- one final legacy handoff vote.

Profile-B council governance is not included. If later proposed, budget its own creation, monitoring, proposal/vote/execute cycle, and emergency drills.

## Acceptance checklist

- [ ] One-height archive export retained and independently repeated
- [ ] Complete native and documented CW20/CW721 discovery process
- [ ] Empty successor predeployed with ordinary self-admin instantiate
- [ ] Admin matrix verified
- [ ] Phase 2 stake config preserves legacy admin explicitly
- [ ] Transition-enabling deposit claimed
- [ ] Successor active at or above 4% supply
- [ ] Harmless successor proposal successfully executed
- [ ] IBCX application governance accepted and verified
- [ ] Final proposal deposit manually refunded
- [ ] Every approved historical deposit settled exactly once
- [ ] Legacy stake internal and Wasm admins transferred to successor
- [ ] Approved IBCX Wasm admins transferred
- [ ] Every treasury bank denom reconciled
- [ ] IBCX backing portfolios unchanged
- [ ] Legacy governance permanently paused last
- [ ] Legacy stake/governance UI marked obsolete
- [ ] Holder unstake/claim/restake canary passed
- [ ] Residual-fund limitations disclosed
- [ ] Raw receipts and tx hashes published

Failure of any item blocks completion claims.
