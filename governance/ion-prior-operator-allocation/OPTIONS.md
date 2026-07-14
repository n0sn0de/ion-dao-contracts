# Response options and recommendations

This document compares technical/governance paths. It is not legal advice and does not determine entitlement.

## Decision matrix

| Option | ION DAO alone? | Recipient consent? | Osmosis state intervention? | Main limitation | Recommendation |
|---|---:|---:|---:|---|---|
| Publish pinned neutral evidence | Yes | No | No | Must protect confidential/legal material | Do now |
| Time-boxed voluntary negotiation | Yes | Yes for transfer | No | No unilateral enforcement | Preferred substantive path |
| Direct return of spendable ION | Yes to accept | Yes | No | Limited to balance spendable at execution | Preferred if agreed |
| Dated future direct transfers | Yes to accept | Yes | No | Requires repeated recipient action | Simple fallback |
| Authz-assisted future transfers | Yes after proof | Yes | No | Revocable, no reservation/scheduler, DAO-grantee path unproven | Conditional only |
| Voluntary voting/transfer covenant | Yes to recognize | Yes | No | Mainly contractual/social enforcement | Supplemental |
| Tender or negotiated buyback | Yes, subject to treasury approval | Yes | No | Valuation, conflicts, market impact | Possible settlement tool |
| Leave allocation intact and monitor | Yes | No | No | Concentration remains | Current technical status quo absent consent or an authorized remedy |
| Prospective treasury segmentation | Yes after modernization | No | No | Does not alter account balance | Worth separate design review |
| Custom voting cap/quadratic module | Requires custom contracts | No | No | Rights change, UI/audit/legitimacy risk | Do not rush into modernization |
| Native `uion` blacklist/freeze | No ordinary path | No | Yes | Bespoke bank-state intervention | Not recommended absent extraordinary evidence/process |
| Forced balance rewrite | No | No | Yes | Software upgrade, validator adoption, legal/precedent/fork risk | Last resort only |
| Replacement-token exclusion/dilution | No simple path | No | Usually | Alters balances/fungibility and can disrupt pools, contracts, IBC representations, integrations, and third parties | Not recommended |

## Option 1 — publish a neutral evidence record

Publish:

- exact proposal 10–12 decoding;
- proposal 12 execution transaction;
- fixed-height account/balance/spendable/stake/supply data;
- account-type and clawback-source analysis;
- uncertainty and off-chain-rights boundaries;
- an invitation to submit corrections through both public and confidential channels.

Do not publish:

- private contracts without authority;
- privileged advice;
- personal data unnecessary to governance;
- unverified identity/control claims;
- allegations not supported by evidence.

This option improves future decision quality without changing balances.

## Option 2 — voluntary negotiation

A governance-approved mandate should define:

- authorized negotiators and conflicts;
- requested-return formula or range;
- evidence scope;
- approved destination;
- confidentiality and counsel role;
- expiration;
- reporting format;
- prohibition on key/mnemonic custody;
- prohibition on threats, doxxing, unsupported accusations, or promised chain intervention.

Possible negotiated terms:

- immediate return from spendable balance;
- future dated installments as more ION vests;
- governance abstention or voting disclosure covenant;
- IP/domain/source transfer if relevant;
- verified expense/work recognition;
- mutual release or other consideration.

Work recognition must be evidence-based. Proposal text represented specified work; public records indicate development activity. Independently verify scope, authorship, deployments, audits, maintenance, expenses, and IP before assigning settlement value.

If negotiations end without agreement, publish only a neutral process-closure statement consistent with confidentiality and legal obligations. Do not imply guilt, breach, or refusal of an established debt.

## Option 3 — direct voluntary transfer

The account can transfer only bank ION that is spendable at execution. Spendable balance changes continuously with vesting and may also change through other transactions.

Safe procedure:

1. agree amount and destination in atomic `uion`;
2. pin a pre-transfer height for the public reference;
3. re-query spendable balance immediately before signing;
4. recipient signs a normal bank send;
5. destination verifies receipt;
6. publish only approved terms and the transaction receipt.

No private key, mnemonic, or shared custody is required or acceptable.

## Option 4 — dated future direct transfers

The simplest future-return method is a schedule of direct sends as ION becomes spendable.

Advantages:

- standard bank messages;
- no custom contract;
- no DAO-as-Authz-grantee uncertainty.

Limitations:

- repeated recipient action;
- missed-payment/monitoring process;
- no automatic reservation of future vested amounts;
- off-chain enforcement depends on agreement and law.

This is preferable to a technically elaborate Authz flow if direct installments are acceptable.

## Option 5 — Authz-assisted future transfers

A `SendAuthorization` may contain:

- `uion` spend limit;
- receiver allowlist.

The expiration is a field of the enclosing Authz `Grant` carried by `MsgGrant`, not a field of `SendAuthorization`.

A DAO-core grantee is not automatically workable. `MsgExec`’s signer is the grantee. An external operator cannot sign as a contract address; a successfully executed DAO proposal must emit the exact `MsgExec`.

Before recommending this mechanism:

1. deploy a bounded test matching current Osmosis app behavior;
2. use a continuous-vesting account, not only an ordinary account;
3. prove the exact DAO core/proposal-module execution path;
4. identify who triggers installments and pays gas;
5. define retries, partial execution, reconciliation, and alerting;
6. handle legacy-staked ION and future claims separately;
7. prove receiver allowlist and spend-limit behavior;
8. prove revocation and insufficient-balance failure behavior.

Even if proven, Authz:

- does not reserve balance or establish priority;
- can be revoked by the grantor;
- does not prevent competing transfers/staking;
- does not move the current 151.7 ION legacy stake;
- does not schedule itself;
- cannot distinguish historical grant units from other fungible `uion`.

Prefer dated direct transfers if contract-grantee execution remains uncertain.

## Option 6 — tender or negotiated buyback

ION DAO could offer consideration for voluntary transfer.

Required controls:

- independent valuation method;
- conflict disclosures;
- treasury affordability;
- market-impact analysis;
- exact authority and spending cap;
- no self-dealing;
- treatment of locked vs spendable amounts;
- public receipts and redacted terms.

A buyback may be economically cleaner than coercion, but it uses current-holder treasury assets and needs clear approval.

## Option 7 — voluntary governance covenant

A recipient could agree to:

- abstain from specified treasury/admin proposals;
- disclose staking/voting intentions;
- return ION as vested;
- avoid governance action during a defined transition.

This can reduce risk but does not change on-chain voting rights unless accompanied by enforceable custody or contract terms. Do not present a social pledge as cryptographic enforcement.

## Option 8 — leave the allocation intact and mitigate prospectively

Absent consent or a separately authorized remedy, leaving the account unchanged is the current technical status quo. This package does not determine the legal baseline.

Prospective controls may include:

- public alerts for bank/stake movements;
- five-day revoting and adequate execution notice;
- active-participation margin before treasury handoff;
- distributed voter participation;
- conflict disclosures;
- narrowly scoped treasury subDAO/filter design after separate review;
- independent payload/admin verification;
- emergency incident response.

These measures reduce operational risk without rewriting an account balance.

## Option 9 — custom voting cap, quadratic voting, or alternate token

These designs may reduce address concentration but create new problems:

- targeted disenfranchisement concerns;
- sybil splitting;
- custom contract audit burden;
- daodao.zone compatibility uncertainty;
- token-rights and legitimacy disputes;
- migration effects on liquidity, IBC, and integrations.

Do not add a custom voting module to the urgent DAO DAO modernization unless separately specified, audited, tested, and broadly approved.

## Option 10 — native blacklist, freeze, fork, or replacement-token exclusion

Native `uion` has no tokenfactory admin blacklist. Implementing a freeze or forced transfer requires bespoke chain logic.

Replacement-token exclusion is economically similar to confiscation and disrupts:

- pools;
- contracts;
- IBC representations;
- fungibility;
- integrations;
- holders beyond the target account.

This is not a normal ION DAO remedy.

## Option 11 — extraordinary Osmosis software intervention

A software-upgrade proposal could authorize a bespoke binary/handler that rewrites state. The governance vote itself does not execute the rewrite.

Minimum process before even drafting code:

- credible authenticated evidence reviewed by qualified counsel or a competent forum;
- specifically defined unauthorized transfer, material transactional error, or obligation established by a competent adjudication/order;
- standing/authority analysis for ION DAO and Osmosis governance;
- notice, evidence access, and meaningful response opportunity;
- independent decision-makers and conflicts;
- least-intrusive-remedy and proportionality analysis;
- public redacted, non-privileged summary;
- exact pinned-block amount and vesting calculation;
- preservation of unrelated denoms, account key, number, sequence, and state;
- preservation of bank/supply/delegation/vesting invariants;
- audited upgrade code and handler;
- validator coordination and adoption plan;
- fork/exchange/custodian/IBC impact analysis;
- rollback and post-upgrade verification.

Mere disappointment with product performance or token concentration does not satisfy this threshold.

## Security Council note

A standard DAO DAO vetoer is not technically bounded merely because a charter says “security only.” A council core may execute arbitrary messages, and an incumbent vetoer may obstruct its own replacement.

PR #7 therefore does not recommend a launch Security Council. Any later proposal requires an exact module graph, four-field veto configuration, timing, sunset, replacement path, conflict rules, operational drills, and independent review.

## Recommended sequence

1. Merge only after the pinned evidence and legal-boundary wording are accepted.
2. Preserve raw archive receipts and source commits.
3. Open a confidential channel for agreements/evidence.
4. Independently verify work, expenses, IP, and obligations.
5. Approve a time-boxed negotiation mandate.
6. Prefer direct voluntary transfer or dated installments.
7. Use Authz only after exact deployed-path proof.
8. If no agreement, close neutrally and apply prospective safeguards.
9. Consider extraordinary state intervention only after the evidentiary/process threshold above.

## Non-negotiable safeguards

- never request or accept a mnemonic/private key;
- no harassment, doxxing, or unsupported accusation;
- no claim that account concentration proves misconduct;
- no claim that proposal execution settles off-chain legal rights;
- no public disclosure of confidential/privileged material without authority;
- no effect on unrelated denoms or account state;
- no chain-intervention promise without code, process, and validator adoption;
- no bundled modernization/confiscation proposal.
