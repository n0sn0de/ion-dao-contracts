# Recommended ION DAO DAO production configuration

These are review recommendations, not executable JSON. Exact production messages must be generated from the pinned schemas and independently simulated.

## Core

| Field | Recommended value | Rationale |
|---|---|---|
| Name | `ION DAO` | Preserve recognizable identity |
| Description | Explicitly identify this as the DAO DAO successor and link the archived legacy address | Prevent UI/address confusion |
| DAO URI | Immutable governance charter and migration manifest URI | Keep policy and receipts discoverable |
| Image URL | Community-approved immutable asset or `null` | Do not depend on a dead project domain |
| Automatically add CW20s | `false` | Prevent unsolicited CW20 receive callbacks from polluting the core registry |
| Automatically add CW721s | `false` | Prevent unsolicited NFT receive callbacks from polluting the core registry |
| Internal admin | `null` at instantiate, causing self-admin | No wallet or deployer control |
| Wasm admin | Core itself through the self-admin factory | Upgrades remain token-governed |
| Initial items | Manifest hash, legacy address, evidence height, and charter URI only | Make continuity machine-readable |
| Initial actions | Empty | Do not hide authority or asset movement in instantiate |

The successor should be predeployed empty with ordinary `InstantiateContractWithSelfAdmin`. A deterministic address is unnecessary once deployment and treasury handoff are separate. Do not publish or rely on production `Instantiate2` salts.

## Admin topology

| Contract | Internal/application admin | CosmWasm admin |
|---|---|---|
| New DAO core | Core itself | Core itself |
| New voting module | Core/DAO relation | New core |
| New proposal module | New core | New core |
| New pre-propose module | Proposal/core relation | New core |
| Legacy stake during Phase 2 | Legacy DAO | Legacy DAO |
| Legacy stake after final handoff | New core | New core |
| Approved IBCX application contracts after acceptance | New core | New core after final handoff |

Factory and deployer retain nothing.

### Exact legacy stake updates

`UpdateConfig` assigns both fields unconditionally. Omitting `admin` is not “preserve current”; it becomes `None`.

Transition-enabling proposal:

```json
{
  "update_config": {
    "admin": "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm",
    "duration": null
  }
}
```

Final handoff proposal:

```json
{
  "update_config": {
    "admin": "NEW_SUCCESSOR_CORE",
    "duration": null
  }
}
```

The final proposal must also transfer the legacy stake contract’s CosmWasm admin to `NEW_SUCCESSOR_CORE`.

## Voting module

Use `dao-voting-token-staked` with the existing native `uion` denom.

| Field | Recommended value | Rationale |
|---|---|---|
| Token | Existing native `uion` | Do not create a replacement ION token |
| Unstaking duration | 7 days | Covers the five-day vote plus operational notice while improving on 14 days |
| Active threshold | Dynamic 3% of current ION supply | Prevent dust activation |
| Delegation module | `null` at launch | Reduce launch complexity and proxy capture surface |

The serialized active threshold is percentage `0.03`. On every `IsActive` query, the contract reads current bank supply and ceilings 3% to atomic units.

At snapshot supply `21,293.014966 ION`:

```text
3% = 638.79044898 ION
contract ceiling = 638.790449 ION
```

A supply increase can deactivate the DAO without an unstake. The final handoff gate therefore requires at least 4% staked, not merely the 3% boundary.

### What the active threshold does not solve

It does not cap address-level voting power. The prior-operator vesting concentration can exceed half of the resulting staked pool if all presently spendable ION is staked while other stake remains constant. Address-specific caps require a custom voting system, alter token rights, and need separate legitimacy/UI/audit analysis.

## Single-choice proposal module

| Field | Recommended value | Rationale |
|---|---|---|
| Threshold | Strict majority | More Yes than No among opinionated votes |
| Quorum | 30% | Matches the established participation expectation |
| Maximum voting period | 5 days | Shorter than legacy seven days without reducing notice below a business week |
| Minimum voting period | 48 hours | Prevent immediate execution if revoting is changed later |
| Allow revoting | `true` | Makes vote changes explicit and prevents early completion |
| Only members execute | `true` | Reduce outsider execution-grief surface |
| Close on execution failure | `true` | Avoid permanent passed-but-unexecuted zombie proposals and indefinite bond escrow |
| Veto config | `null` | No unreviewed external veto authority |

`close_proposal_on_execution_failure = true` trades retryability for finality. A voting member could still execute at a bad time. Production proposals must avoid unstated external preconditions, and the UI/runbook must state when execution is safe. If the community prefers retryability, it must also accept that a failed Passed proposal can retain its `OnlyPassed` bond indefinitely.

## Pre-propose module

| Field | Recommended value | Rationale |
|---|---|---|
| Submission policy | Specific: `dao_members = true`, empty allowlist and denylist | Only stakers may consume governance attention |
| Deposit | Exactly `1,000,000 uion` / 1 ION | Material spam bond without reproducing partial-top-up logic |
| Refund policy | `OnlyPassed` | Refund Executed proposals; under v2.7.0 with close-on-failure, failed execution is also refunded because the Executed completion hook runs before the error reply changes status |

Important semantics:

- `OnlyPassed` is refunded when the pre-propose module receives an `Executed` completion hook.
- With `close_proposal_on_execution_failure = true`, v2.7.0 emits that hook before the failed-submessage reply changes final status to `ExecutionFailed`; the proposer is therefore refunded on execution failure too.
- Rejected, Closed, and Vetoed completion-hook handling must be verified against the exact v2.7.0 source/tests.
- With retryable execution failures (`close_proposal_on_execution_failure = false`), a Passed proposal’s bond can remain escrowed indefinitely.
- Deposit settlement must be tested exactly once for Executed, Rejected, Closed, and ExecutionFailed statuses.

### Pre-propose balance withdrawal

The withdrawal path transfers the **entire selected-denom balance**. It does not calculate “excess over outstanding deposits.”

Never withdraw while refundable deposits remain. Required gate:

```text
sum(outstanding refundable deposit liabilities) == 0
```

Then query the selected denom balance, withdraw the entire balance once, and reconcile the receiving treasury. Add a negative test proving that withdrawal with outstanding bonds would break later refunds.

## Veto and Security Council

Baseline production configuration: `veto = null`.

A future council is a separate design, not part of this launch recommendation. Before recommending one, publish and test:

- exact CW4 member DAO graph and all code IDs/hashes;
- exact council threshold, voting period, revoting, execution, proposal, and deposit configuration;
- complete four-field main proposal `VetoConfig` including `veto_before_passed`;
- council response time shorter than the main timelock;
- membership weights and conflict/recusal rules;
- sunset and replacement/removal mechanics;
- the fact that a standard council core can execute arbitrary messages unless code restricts it;
- the fact that an incumbent vetoer may veto its own replacement;
- a bounded Juno/Osmosis proof of the entire graph.

Do not call a prose-only mandate technically bounded.

## Execution and retries

- `OnlyPassed` does not mean “successful execution only” under the recommended v2.7.0 close-on-failure combination; failed execution also refunds because of hook ordering.
- Members-only execution reduces, but does not eliminate, bad-timing execution risk.
- Every proposal with external state preconditions must query them immediately before voting closes and before execution.
- Failed final handoff execution must not partially mutate state; exact simulation and Cosmos transaction atomicity must be verified.

## Legacy holder migration

The user guide must distinguish shares from value:

1. query legacy voting-power/share balance;
2. query legacy `staked_value`;
3. record the current share-to-backing ratio;
4. submit `Unstake` with the **share amount**;
5. verify received `uion` equals the contract formula;
6. claim any prior mature claim;
7. stake received ION in the successor;
8. verify successor voting power.

The old stake contract remains callable forever and still accepts `Stake` and `Fund`. It cannot be retired by configuration. Mark it obsolete in every UI and document, and test a funded/share-divergence scenario before publishing the migration guide.

## IBCX controls

The production manifest must separately list for each IBCX-family contract:

- Wasm admin;
- application `gov`;
- `pending_gov`;
- fee collector;
- accrued fee-realization requirement;
- exact source-reviewed update and accept messages;
- post-state receipt.

Backing portfolios are user/index-token assets, not DAO treasury. The transition changes control fields only.

## Metadata

The legacy `UpdateConfig` replaces the entire configuration. Do not send an informal “metadata update.” Either omit it or publish an exact before/after full-config diff proving every nonmetadata field is byte-for-byte preserved.

## Settings deliberately deferred

- vote delegation;
- rewards distributor;
- multiple-choice proposals;
- subDAOs and spending filters;
- address-level voting caps;
- Security Council/veto;
- custom treasury automation;
- token migration or replacement.

Modern software does not justify enabling every feature on day one.

## Required production manifest

Before any binding proposal, publish:

- DAO DAO tag and source commit;
- all code IDs and live hashes;
- instantiate permissions;
- complete core/voting/proposal/pre-propose JSON;
- ordinary factory self-admin instantiate message;
- expected admin matrix;
- active and 4% handoff thresholds at pinned supply;
- all periods and percentage encodings;
- exact deposit and status semantics;
- legacy stake Phase 2 and final JSON;
- product-control handoff messages;
- complete treasury and liability tables;
- final proposal deposit refund;
- residual-fund limitations;
- simulation receipt;
- independent reviewer sign-off.
