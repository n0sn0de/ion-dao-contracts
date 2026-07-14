# ION prior-operator allocation assessment and response plan

Status: **technical and governance assessment only**. This package does not determine legal ownership, accuse any person of misconduct, contact a recipient, authorize confiscation, or broadcast a transaction.

## Executive conclusion

ION DAO proposal `12` is recorded as executed and created a roughly five-year `/cosmos.vesting.v1beta1.ContinuousVestingAccount` with original vesting of `3,407.04 ION`.

The account is:

- an ordinary auth vesting account, not a module account;
- not a `ClawbackVestingAccount`;
- missing any funder, revoker, or admin authority;
- controlled on-chain by its account signer;
- locked linearly only to the extent required by the schedule ending `2028-08-24T15:00:00Z`.

No currently available message that the ION DAO contract can validly sign authorizes conversion, key replacement, or clawback of this account. The source address acquired no continuing signer privilege when it created the account.

This is a technical conclusion, not a legal one. The reviewed proposal text contains no express on-chain revocation or return mechanism. The chain does not determine whether an off-chain agreement created repayment, employment, fiduciary, fraud, IP, inducement, or other rights or remedies.

## Companion documents

- [`EVIDENCE.md`](EVIDENCE.md) — height-pinned proposal/account/balance evidence
- [`OPTIONS.md`](OPTIONS.md) — response matrix and technical/legal boundaries
- [`REPRODUCE.md`](REPRODUCE.md) — archive-height query and decoding procedure
- companion modernization roadmap: [PR #7](https://github.com/n0sn0de/ion-dao-contracts/pull/7)

## Height-pinned account state

Snapshot:

- height: `66276784`
- time: `2026-07-14T05:23:51.419944203Z`
- account: `osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`
- type: `/cosmos.vesting.v1beta1.ContinuousVestingAccount`
- account number: `906739`
- sequence: `135`

ION state at that exact height:

| Item | Amount |
|---|---:|
| Original vesting field | 3,407.040000 ION |
| Schedule vested | 1,967.405060 ION |
| Schedule locked/unvested | 1,439.634940 ION |
| Bank balance | 3,101.840914 ION |
| Spendable bank balance | 1,662.205974 ION |
| Active legacy stake | 151.700000 ION |
| Legacy stake claims | none |
| Bank plus active stake | 3,253.540914 ION |
| Arithmetic difference from original vesting amount | 153.499086 ION |

The final line is arithmetic only. Fungible balances may include later inflows or other holdings. It is not a finding that particular grant units were sold, spent, returned, or moved to a known destination.

Bank plus active stake represented approximately `15.279851%` of the retained ION supply. This is current concentration, not proof of common control with any other address or proof of misconduct.

## Proposal chronology

| Proposal | Source field | Denom | End time | Current status | Technical reading |
|---|---|---|---|---|---|
| 10 | `osmo14hj2...2r9g9` | `uion` | 2028-07-27T00:00:00Z | passed, unexecuted | Required signer/source is not the executing DAO contract |
| 11 | ION DAO | `ion` | 2028-08-12T13:00:00Z | passed, unexecuted | Encoded `ion`; proposal 12 identifies correction to `uion` |
| 12 | ION DAO | `uion` | 2028-08-24T15:00:00Z | executed | Corrected message created the account |

Proposal 12 execution transaction:

`1E15143F3135DEAB9D902F03F5D54D4B53EB65D8593E77CDDA773AC57CEFE245`

- height: `11126209`
- time/account schedule start: `2023-08-23T15:54:38Z`

Do not attribute proposals 10 or 11 to a nonempty target-account failure without a transaction receipt establishing that cause.

## What the proposal text and public record support

The proposal record represented that contributors had performed ION DAO/IBCX work and requested funding/compensation. Public evidence also includes:

- later IBCX migration activity;
- Osmosis proposal 504’s IBCX upload-permission record;
- public IBCX source repositories;
- archived evidence that the product site existed.

This supports a finding that development activity occurred. It does not independently establish the complete scope, authorship, audit coverage, maintenance obligations, expense basis, IP ownership, or fair valuation of every claimed deliverable.

Before using “work delivered” as a settlement valuation fact, independently verify:

- source authorship and commit history;
- deployed code and audits;
- expenses;
- maintenance/support periods;
- domains and UI assets;
- IP ownership/licensing;
- any signed service, employment, grant, or side agreement.

The proposal encoded no objective payment milestones, DAO revoker, termination trigger, or express return obligation. It did contain forward-looking roadmap, use-of-funds, dedication, and value-accrual statements whose off-chain significance requires separate review.

## Separation from the proposal-deposit accounting incident

The address associated with anomalous deposit records in proposals `22`–`39` is:

`osmo1fuzlaeajk7t80ujags2c3jlfemauv2cayvm82e`

The vesting address is different.

This proves only that the on-chain addresses differ. It proves neither different nor common real-world identity/control. No reviewed evidence established a common-control link.

Use neutral terms:

- “address associated with affected proposals 22–39”;
- “proposal-deposit accounting incident”;
- “anomalous deposit records”;
- “v0.0.1 accounting flaw.”

Do not call the vesting allocation evidence of that incident.

## Governance concentration scenario

At the pinned height:

```text
current active stake      1,671.832757 ION
newly staked spendable    1,662.205974 ION
resulting active stake    3,334.038731 ION

recipient current stake     151.700000 ION
newly staked spendable    1,662.205974 ION
potential voting power    1,813.905974 ION

potential share ≈ 54.405666%
```

Assumptions:

- all spendable bank ION is staked;
- no other holder changes stake;
- no intervening transfers or vesting changes;
- standard one-token/one-vote staking.

This demonstrates governance concentration risk. It is not a prediction, attribution of intent, or claim that specific vesting units would be used.

## Normal clawback is unavailable

Osmosis supports a separate `ClawbackVestingAccount` class with a recorded funder. The subject account is not that type.

A normal `MsgClawback` path requires:

1. the target account to be a clawback account; and
2. the signer to match the recorded funder.

The subject `ContinuousVestingAccount` has no such fields. ION DAO cannot:

- sign as the account;
- debit its bank balance;
- convert it to a clawback account;
- replace its key;
- blacklist native `uion` through a denom admin;
- invoke ordinary clawback successfully.

Osmosis proposal `772`, “Demand return of IonDAO funding,” passed with an empty messages array. It was a political expression, not an executable transfer or new clawback authority.

## Recommended process

### 1. Preserve evidence

Retain at one archive height:

- proposals 10–12 and exact decoded payloads;
- proposal 12 execution transaction;
- auth account;
- bank and spendable balances;
- legacy stake/claims;
- supply;
- vesting/clawback SDK source;
- relevant public work/deployment/audit records.

### 2. Search for off-chain rights

Use a counsel-controlled confidential process to locate:

- signed service/employment/grant agreements;
- IP assignments or licenses;
- expense records;
- milestone/termination/return terms;
- settlement or side-letter records;
- relevant jurisdiction and parties.

Do not demand public disclosure of privileged, confidential, or personal material.

### 3. Independently verify work and obligations

Separate:

- what the proposal represented;
- what public chain/source evidence verifies;
- what remains unsupported;
- what qualified counsel or a competent forum concludes.

### 4. Define a negotiation mandate

A separate ION DAO proposal should define:

- negotiators and conflicts;
- requested-return formula or range;
- evidence they may rely on;
- approved destination;
- confidentiality authority;
- time limit;
- reporting format;
- no custody of keys or mnemonic material;
- no authority to threaten, dox, blacklist, or promise chain intervention.

### 5. Seek voluntary resolution

Possible consensual components:

- direct transfer of a negotiated spendable amount;
- dated future transfers as more ION vests;
- limited receiver-allowlisted Authz, only after exact deployed-path testing;
- IP/domain/source handover if relevant;
- governance abstention covenant;
- mutual release or other consideration reviewed by counsel.

Publish only governance-approved, redacted, non-privileged terms and on-chain receipts consistent with consent and legal obligations.

### 6. If no agreement

Close the process neutrally. Do not imply guilt, breach, or refusal of a valid debt unless supported by a competent finding.

Use prospective controls:

- public concentration monitoring;
- long-enough voting and execution notice;
- distributed participation targets;
- segregated/filtered treasury mandates after separate review;
- conflict disclosures;
- incident response and address-change alerts.

## Extraordinary chain intervention

A bespoke Osmosis software upgrade could technically rewrite auth/bank state. A governance vote alone does not perform that state change: it would require a specific binary, audited upgrade handler, validator adoption, and exact state invariants.

Consider even investigating that path only if:

- credible authenticated evidence is reviewed by qualified counsel or a competent forum;
- the issue is a specifically defined unauthorized transfer, material transactional error, or adjudicated/enforceable obligation—not political regret;
- affected parties receive notice, evidence access, and a meaningful response opportunity;
- conflicts and independent decision-makers are disclosed;
- proportionality and least-intrusive remedies are analyzed;
- only redacted, non-privileged summaries are published;
- unrelated denoms, account key, account number, sequence, and state are preserved;
- amounts and vesting fields are computed at a pinned execution block;
- bank, supply, delegation, and vesting invariants are independently audited.

Absent that evidentiary threshold, a retroactive state intervention creates serious credible-neutrality, precedent, validator-adoption, fork, exchange, and legal risks.

## Explicit boundaries

This package does not establish:

- the legal owner or beneficiary of the account;
- breach, fraud, theft, abandonment, or unjust enrichment;
- the complete scope/value of delivered work;
- current controller identity;
- common control with affected proposal addresses;
- a right to seize, freeze, blacklist, dilute, fork, or exclude the account;
- that Authz will work through DAO DAO without a dedicated proof.

It establishes account type, proposal execution, vesting schedule, pinned balances, on-chain authority limits, and a measured process for resolving uncertainty.
