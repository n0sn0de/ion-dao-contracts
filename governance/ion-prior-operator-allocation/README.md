# ION prior-operator allocation assessment and response plan

Status: **assessment and governance roadmap only**. This directory does not accuse any person of fraud, authorize confiscation, contact a recipient, create an authorization, or submit an ION/Osmosis proposal.

## Executive conclusion

The allocation was a deliberately approved ION DAO treasury spend, not a revocable grant.

ION proposal `12` executed a five-year `ContinuousVestingAccount` holding `3,407.04 ION` for the development contributors. The account is an ordinary recipient-controlled Cosmos auth vesting account. “Recipient-controlled” describes chain authorization, not an off-chain legal conclusion. It is not a module account, does not identify a clawback authority, and contains no milestone, service, revocation, or performance condition. The unvested amount becomes spendable automatically over time through `2028-08-24T15:00:00Z`.

The ION DAO cannot unilaterally pull those coins back. A CosmWasm contract cannot spend from the vesting account without authorization signed by that account. Ordinary Osmosis governance messages and parameter changes do not expose a clawback switch for this account type.

A forced clawback would require an extraordinary Osmosis chain software/state intervention or binding off-chain legal authority. Product abandonment, failed traction, or present token concentration alone is not a sound basis for chain-level confiscation.

The recommended path is:

1. publish the neutral chain facts and correct the “module account” misconception;
2. recognize the IBCX contracts and product work that was delivered;
3. invite a time-bounded voluntary settlement for some or all of the remaining allocation;
4. if the recipient agrees, combine an immediate return of spendable ION with a public, revocable authz/periodic-return mechanism for future vesting;
5. if the recipient does not agree, close the negotiation without harassment and mitigate governance concentration through notice, revoting, unbonding, monitoring, an optional bounded veto council, and treasury compartmentalization;
6. do not ask Osmosis governance to rewrite account ownership absent independently verified fraud, mistake, contractual breach with enforceable evidence, or another chain-level defect that survives due process.

That is not timid. It is the difference between fixing bad incentive design and normalizing political confiscation.

## What the chain proves

At Osmosis height `66276784` / `2026-07-14T05:23:51.419944203Z`:

- vesting recipient: `osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`;
- account type: `cosmos.vesting.v1beta1.ContinuousVestingAccount`;
- original vesting: `3,407.04 ION`;
- start: `2023-08-23T15:54:38Z`;
- end: `2028-08-24T15:00:00Z`;
- bank balance: `3,101.840914 ION`;
- bank spendable: `1,662.138668 ION`;
- bank still locked by vesting: `1,439.702246 ION`;
- active legacy ION stake: `151.7 ION`;
- outstanding legacy stake claims: none;
- known bank plus staked holdings: `3,253.540914 ION`;
- known holdings as current supply: approximately `15.2799%`;
- known original allocation no longer held in those two locations: `153.499086 ION`.

The exact vested/spendable amount changes continuously. Re-query before publishing or negotiating a number.

Proposal history:

- proposal `10`: first developer-allocation attempt, passed but did not execute;
- proposal `11`: execution retry, passed but did not execute;
- proposal `12`: revised developer funding, executed;
- executed amount: `3,407,040,000 uion`;
- destination: the vesting address above;
- executed vesting type: continuous, not delayed and not clawback.

The proposal rationale described the amount as roughly 16% of supply, five years of linear vesting, and approximately `$100,000` per year at the contemporary ION price. It did not record deliverables, milestones, termination, service requirements, a DAO revoker, or a return condition.

## What the chain does not prove

The reviewed state does **not** prove:

- that the recipient committed the later legacy deposit-accounting exploit;
- that the recipient address and exploit depositor are controlled by the same actor;
- fraud, misrepresentation, breach of contract, or unlawful conduct;
- that IBCX work was not delivered;
- that product failure triggered an agreed repayment obligation;
- that the DAO retained beneficial ownership over unvested coins;
- that a social expectation of alignment became an enforceable on-chain condition.

The deposit exploit address recorded in ION proposals `22`-`39` is different from the developer vesting address. No causal or control link was established in this review.

Do not use the phrase “evidence of the exploit” to describe the vesting allocation unless new evidence actually connects them. Sloppy accusations are not accountability.

## Why normal ION governance cannot claw it back

A `ContinuousVestingAccount` is controlled on-chain by its account signer. Vesting changes what is spendable at a given time; it does not preserve sender custody. This statement is about chain authorization, not off-chain beneficial ownership.

ION DAO governance cannot:

- execute a bank send signed by the recipient;
- alter the recipient's auth account state from CosmWasm;
- replace the vesting address's key;
- spend unvested coins through DAO DAO;
- turn a continuous vesting account into a clawback account through a normal contract migration;
- use authz without a grant signed by the recipient.

The vesting account contains no funder/revoker field. The original treasury sender is not an admin.

## Response roadmap

### Phase 1 — publish a neutral fact package

Publish:

- proposal `10`-`12` descriptions and exact decoded messages;
- current auth account JSON;
- current bank, spendable, locked, staked, and claim queries;
- vesting arithmetic and timestamps;
- a plain explanation that the allocation was time-vested but not clawback-enabled;
- a clear separation between the allocation and the later deposit exploit.

Invite corrections with transaction hashes or signed agreements, not screenshots and rumors.

Gate: two reviewers reproduce every number.

### Phase 2 — determine whether off-chain obligations exist

Before asking for a return, locate and review:

- contributor agreements;
- grant or employment terms;
- multisig records;
- accepted forum language incorporated by proposal;
- milestone schedules;
- intellectual-property assignments;
- representations about continued operation;
- governing law and dispute clauses.

The on-chain proposal alone contains no clawback condition. If no other agreement exists, say so.

Gate: counsel or a qualified reviewer distinguishes a moral request from an enforceable claim. This repository does not give legal advice.

### Phase 3 — value delivered work

Create an independent record of:

- IBCX contracts and audits;
- deployed website/front end;
- integrations and maintenance performed;
- treasury expenses already borne by contributors;
- time period of active work;
- product usage and revenue, without pretending failed traction means zero work;
- work promised but not delivered, if documented.

Use this to define a fair retained-compensation floor. The goal is restitution or re-alignment, not retroactive wage theft.

Gate: the DAO can explain why the requested return amount is fair.

### Phase 4 — make one time-bounded voluntary offer

Recommended opening position:

- acknowledge completed IBCX work;
- ask the recipient to return a negotiated portion of the remaining allocation, with the unvested balance at agreement date as the reference ceiling;
- request an immediate transfer from currently spendable ION;
- for future vesting, request a public bank `SendAuthorization` or scheduled voluntary transfers to the new ION DAO core;
- allow a defined retained allocation for delivered work;
- give 30 days to respond and one optional 14-day extension;
- publish the final signed terms and transaction receipts;
- prohibit harassment, doxxing, or key requests.

Do not ask for a mnemonic or private key. Do not accept shared custody of the vesting address.

### Phase 5 — implement only a consented mechanism

If the recipient agrees:

1. the new ION DAO approves the settlement terms;
2. the recipient returns the agreed currently spendable amount directly to the DAO;
3. the recipient grants a bounded `cosmos.bank.v1beta1.SendAuthorization` to an approved DAO-controlled executor, or commits to dated transfers;
4. the authorization is limited to `uion`, a maximum amount, an expiration after the vest end, and the settlement recipient;
5. test authz execution with dust before relying on it;
6. publish a vesting/return schedule and public monitor;
7. execute periodic sweeps only as ION becomes spendable;
8. reconcile every transfer against the agreed total;
9. disclose that authz is revocable unless a different enforceable arrangement exists.

A grant does not override vesting. An attempted send succeeds only to the extent the account has spendable ION.

### Phase 6 — if there is no agreement

- publish that no voluntary agreement was reached;
- stop the negotiation on the stated date;
- do not escalate rhetoric;
- monitor public address activity;
- apply the governance-risk mitigations in [`OPTIONS.md`](OPTIONS.md);
- revisit only if new evidence or a new offer appears.

No-action is a valid policy. Bad original terms do not become reversible merely because the incentive theory failed.

### Phase 7 — extraordinary escalation gate

Consider Osmosis governance only if all are true:

- independently verified evidence establishes fraud, mistake, theft, enforceable breach, or chain-level defect;
- the specific remedy and amount are narrowly tied to that evidence;
- affected parties receive notice and a response opportunity;
- legal and technical reviews are public;
- the implementation is an audited state transition with reproducible pre/post invariants;
- the proposal explains precedent and limits;
- validators can verify the exact account and balance changes;
- ordinary/voluntary remedies are unavailable or exhausted.

Abandonment and concentration by themselves do not satisfy this gate.

## Recommended governance posture

Adopt this resolution separately from the DAO DAO modernization proposal:

1. recognize proposal `12` as a valid historical governance action unless contrary evidence is produced;
2. acknowledge that its vesting design omitted clawback and performance conditions;
3. authorize a neutral voluntary-return outreach process, not confiscation;
4. require any settlement to return funds only to a verified ION DAO-controlled address;
5. require a separate governance approval for final terms;
6. reject harassment and unverified attribution;
7. direct future grants to use milestone escrow, revocable vesting where appropriate, scoped subDAOs, objective deliverables, and explicit termination language.

## Future grant design lesson

The failure was not “vesting.” The failure was time-only vesting with no revocation, milestones, or accountability path.

Future contributor allocations should use:

- milestone tranches;
- clear acceptance criteria;
- a DAO-controlled escrow or revocable vesting contract;
- objective stop conditions;
- a defined dispute process;
- IP/source-code delivery requirements;
- public progress receipts;
- capped operating grants before large long-term allocations;
- no expectation that token ownership automatically creates alignment.

Tokens are not a sacrament. If alignment matters, encode the conditions.

## Separation from modernization

Do not bundle a clawback or settlement demand into the DAO DAO cutover.

The modernization is infrastructure and custody hardening. The allocation issue is a contested historical policy and ownership question. Combining them increases governance fatigue, confuses voters, and creates an easy excuse to reject both.

Use separate documents, separate discussion, and—only if needed—separate ION DAO proposals.

## Companion documents

- [`EVIDENCE.md`](EVIDENCE.md) — proposal, vesting, balance, staking, and concentration receipts
- [`OPTIONS.md`](OPTIONS.md) — technical/governance/legal option matrix and safeguards
- [`REPRODUCE.md`](REPRODUCE.md) — infrastructure-neutral read-only query recipe
- companion PR: ION DAO DAO modernization roadmap
