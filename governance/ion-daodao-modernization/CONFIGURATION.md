# Recommended ION DAO DAO production configuration

These values are recommendations for the eventual governance proposal. They are not an executable instantiate message.

The rule is simple: retain a legacy value only when it is still defensible. Do not clone old settings because they are old, and do not enable new modules because the product menu is shiny.

## Core

| Field | Recommended value | Rationale |
| --- | --- | --- |
| Name | `ION DAO` | Stable identity; do not append operator branding |
| Description | A concise statement that ION holders govern the treasury and protocol/public-goods decisions | The legacy description is too thin to explain scope |
| Image URL | Immutable IPFS URI reviewed with the proposal | Avoid mutable hosted branding |
| DAO URI | Immutable IPFS URI for charter, addresses, risks, and governance policy | Gives the UI and chain a durable source of governance context |
| Internal admin | Core itself (`admin: None` at instantiate) | No wallet or external DAO receives privileged admin messages |
| CosmWasm admin | Core itself through `cw-admin-factory` | Future migrations are self-governed; no Osmosis governance dependency |
| Automatically add CW20s | `false` | Prevent unsolicited CW20 callbacks from polluting treasury discovery |
| Automatically add CW721s | `false` | Prevent unsolicited NFT callbacks from polluting treasury discovery |
| Initial items | Empty unless a reviewed immutable manifest hash is stored | Avoid decorative state and hidden dependencies |
| Initial actions | Empty | Keep bootstrap deterministic; perform no unrelated action while creating the DAO |

### Admin invariant

The production receipt must prove both layers:

1. DAO DAO core query `admin` returns the core address.
2. Osmosis `wasm contract` query reports the core address as the core's CosmWasm admin.

Proposal, voting, pre-propose, and optional Security Council child modules must report the core (or their own council core) as CosmWasm admin. The factory and deployer must retain nothing.

### Legacy stake wind-down admin

The old stake contract continues to hold user funds while holders exit. In the same atomic cutover, set both its internal config admin and its CosmWasm migration admin to the new ION DAO core, while setting only the legacy exit duration to `None`.

This does not migrate storage or move custody. It preserves a self-governed recovery path if a later audited fix is needed after the old governance contract is permanently paused. Leaving either admin layer on the paused old DAO would recreate an Osmosis-governance dependency.

## Voting module

Use `dao-voting-token-staked` with the existing native denom `uion`.

| Field | Recommended value | Rationale |
| --- | --- | --- |
| Token | Existing native denom `uion` | No new token, wrapper, issuer, or custody layer |
| Voting ratio | 1 atomic ION staked = 1 voting-power unit | Legible and supported by DAO DAO UI |
| Active threshold | `3%` of current total supply | Requires meaningful migration before governance activates; scales if supply changes |
| Unstaking duration | 7 days | Keeps voting capital committed for one five-day vote plus notice margin without preserving the legacy 14-day drag |
| Delegation module | `None` at launch | Avoid proxy concentration and another contract until ION has an explicit delegation policy |
| Hooks | None at launch | No unreviewed callback surface |

At height `66276760`, a 3% threshold was `638.79044898 ION`; the serialized threshold rounds according to DAO DAO's contract rules. Recompute from live supply and validate the exact atomic threshold behavior before proposal freeze.

### Why not a zero active threshold

Without an active threshold, a dust holder could activate an otherwise empty successor immediately after deployment. Quorum is measured against staked power, not total supply, so low initial stake can turn a small holder into a temporary dictator.

### Why not copy the 14-day legacy unbond

Fourteen days is defensible for some high-value protocols, but it doubles the recommended vote period and makes the holder transition unnecessarily sticky. Seven days keeps capital exposed through the governance cycle while reducing exit friction. It can be changed only by the DAO later.

### Whale limitation

Standard token-staked DAO DAO voting does not cap per-address power. The prior-operator vesting address currently has enough spendable plus already-staked ION to exceed 50% of the resulting staked pool if it stakes all presently spendable holdings while other stakes stay constant. Active threshold and quorum do not fix that.

Do not pretend configuration can delete token concentration. The available mitigations are notice, revoting, unbonding, monitoring, a bounded veto window, treasury compartmentalization, or a custom voting module. A custom cap/quadratic module is not recommended for the quick launch because it adds audit and UI risk.

## Single-choice proposal module

| Field | Recommended value | Rationale |
| --- | --- | --- |
| Threshold | Strict majority of non-abstain votes | Familiar, legible, and avoids minority rule |
| Quorum | 30% of total voting power at proposal snapshot | Retains the quorum adopted by ION proposal 4; historical successful participation exceeded it, while 20% is weak for a concentrated treasury DAO |
| Maximum voting period | 5 days | Two days shorter than legacy while preserving weekday/weekend notice |
| Minimum voting period | 48 hours | Prevents instant passage if revoting is ever disabled later |
| Allow revoting | `true` | Gives holders time to react to new information and forces the full five-day window |
| Only members execute | `false` | Execution carries only the already-approved payload; permissionless execution improves liveness |
| Close on execution failure | `false` | Prevents a griefing caller from permanently closing a valid proposal after a transient failure |
| Delegation module | `None` | Match voting-module launch scope |

Because revoting is enabled, proposals do not pass early. This is intentional. The old DAO's seven-day window plus no modern timelock is not a reason to let a whale push a proposal through before the community sees it.

### Execution-failure caveat

Retryable proposals can remain executable after the original vote. Proposal authors must use explicit expirations and bounded payloads for time-sensitive actions. The UI and monitoring should flag old passed-but-unexecuted proposals.

## Pre-propose module

Use `dao-pre-propose-single`.

| Field | Recommended value | Rationale |
| --- | --- | --- |
| Submission policy | DAO members only; empty allowlist; empty denylist | Stops nonmembers from buying proposal spam access with a deposit |
| Deposit denom | Native `uion` | Aligns incentives with ION holders |
| Deposit amount | `1 ION` | Twice the legacy target, still only about 0.0047% of current supply |
| Refund policy | `OnlyPassed` | Passed proposals get their bond back; rejected proposals pay a modest attention cost to the treasury |

DAO DAO collects the required deposit atomically in one pre-propose call. It does not reproduce the legacy partial-deposit/top-up path that enabled inconsistent accounting.

A 1 ION bond is a starting value, not scripture. Review it after six months using actual proposal volume, rejection rate, and token value. Do not index it to a dollar feed without an audited oracle.

## Veto and timelock profiles

The production proposal must select one profile explicitly.

### Profile A — minimal trust

```text
veto = None
```

Use this only if the community cannot appoint a credible, accountable council before cutover.

Advantages:

- no privileged vetoer;
- least code and governance overhead;
- pure token governance.

Risks:

- no timelock after passage;
- concentrated voting power can execute treasury actions immediately after the five-day vote;
- no emergency stop between passage and execution.

### Profile B — bounded security (recommended if membership is ready)

```text
vetoer = Security Council DAO core
veto timelock = 48 hours
early_execute = false
```

Council design:

- separate member-based DAO DAO core;
- five publicly named, independent members;
- three-of-five threshold;
- no treasury;
- no role as main-core admin;
- no arbitrary execution mandate;
- sole charter: veto objectively malicious, exploit-driven, or payload-mismatched proposals during the 48-hour window;
- public rationale required for every veto;
- main ION DAO can replace the vetoer through governance, with that change itself passing through the existing timelock.

The council is a circuit breaker, not a second legislature. It must not veto ordinary policy disagreement.

If five credible members and monitoring cannot be assembled, use Profile A. A fake “security council” composed of one operator and four sleepy friends is centralization theater.

## Modules intentionally deferred

| Feature | Launch decision | Reason |
| --- | --- | --- |
| Multiple-choice proposals | Defer | Single-choice covers migration and treasury actions; add when preference selection is real |
| Vote delegation | Defer | Proxy markets and concentration need a separate policy |
| Rewards distributor | Defer | Governance participation rewards are gameable; define metrics first |
| Payroll factory | Defer | No approved recurring payroll mandate |
| Token swap/vesting modules | Defer | No launch requirement |
| Arbitrary apps | Defer | Each app needs permission and message-surface review |
| Treasury subDAO | Evaluate after launch | Useful for bounded budgets, but should not complicate the cutover without a concrete mandate |
| Custom capped/quadratic voting | Reject for launch | Adds bespoke consensus and UI/audit risk |

## Legacy values not propagated

| Legacy behavior/config | New decision |
| --- | --- |
| Monolithic governance state | Modular DAO DAO graph |
| No CosmWasm admin; Osmosis governance needed for upgrade | Self-admin core and modules |
| 14-day unbond | 7 days in new module; `None` only for legacy exit |
| 7-day maximum vote | 5 days plus optional 48-hour post-pass timelock |
| 50% approval, 30% quorum, 30% token veto | Strict majority, 30% quorum; no token `NoWithVeto` option in DAO DAO single-choice |
| Partial deposits and top-ups | One atomic exact pre-propose deposit |
| Anyone can initiate with minimum deposit | Members-only submission |
| 0.5 ION target / 0.05 ION minimum | 1 ION exact bond |
| Legacy claim accounting | Standard pre-propose escrow and completion hooks |
| Treasury token registry with only `uion` | Bank-state inventory plus DAO DAO treasury view |
| Sparse name/description only | Reviewed image and immutable DAO URI |
| Historical proposals in live state | Immutable legacy archive; new proposal numbering begins at A-1 |

## Proposal-body configuration appendix

The eventual proposal should include:

- human-readable values from this document;
- exact JSON for every instantiate message;
- base64-decoded nested module messages;
- code ID, source tag, source commit, queried code hash, and instantiate permission for every module;
- deterministic salt in UTF-8, hex, and base64;
- predicted addresses and independent derivation commands;
- admin matrix before and after execution;
- chosen veto profile and, if applicable, council members/charter;
- exact treasury and deposit reconciliation;
- all preflight and postflight queries.

If reviewers cannot decode the proposal into this table, the proposal is not ready.
