# Response options and recommendations

## Decision matrix

| Option | ION DAO alone? | Recipient consent? | Osmosis governance? | Technical feasibility | Governance/legitimacy risk | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Voluntary immediate return of spendable ION | Yes, as recipient | Yes | No | High | Low | Pursue |
| Voluntary periodic returns as ION vests | Yes | Yes | No | High | Low | Pursue |
| Bounded bank authz to DAO-controlled executor | Yes after grant | Yes | No | Plausible; prototype first | Medium because grant is revocable and executor must be correct | Pursue as implementation option |
| New escrow funded from spendable ION | Yes | Yes | No | High | Low/medium | Use if settlement requires schedule |
| Recipient transfers account key | No safe design | Yes | No | Bad custody practice | Extreme | Reject; never request keys |
| ION DAO contract pulls unvested funds | No | No | No | Impossible under current account type | N/A | Reject |
| ION DAO blacklists the address in standard DAO DAO | No standard support | No | No | Requires custom voting code | High | Reject for launch |
| Per-address voting cap/quadratic module | Custom contract | No | No | Possible with audit | High; changes token rights and UI assumptions | Defer unless separately mandated |
| Security Council veto window | Yes | No | No | Supported by DAO DAO | Medium; bounded trusted role | Recommended if credible council exists |
| Treasury subDAO with message filters/spend caps | Yes | No | No | Possible with reviewed modules | Medium complexity | Evaluate after modernization |
| Court/contract enforcement | Off-chain | Not necessarily | No | Depends on agreement/jurisdiction | High cost; legal review required | Only if documented rights exist |
| Osmosis software-upgrade clawback | No | No | Yes | Technically possible as bespoke state transition | Extreme precedent and chain risk | Last resort only under extraordinary evidence |
| Social pressure/doxxing | No legitimate authority | No | No | Harmful | Extreme | Reject |
| No action plus monitoring | Yes | No | No | High | Low | Valid baseline |

## Option 1 — voluntary immediate return

The recipient sends an agreed amount of currently spendable `uion` directly to the verified ION DAO core.

Controls:

- ION governance approves the settlement and receiver;
- recipient verifies the receiver from chain queries, not chat text;
- send a dust test first;
- publish transaction hashes and updated arithmetic;
- no intermediary wallet;
- no claim over unvested funds beyond the signed agreement.

Advantages:

- simple;
- final;
- no custom code;
- no Osmosis governance;
- lowest custody risk.

Limit: only currently spendable ION can move.

## Option 2 — periodic voluntary returns

The recipient sends a fixed amount monthly or quarterly as vesting unlocks.

A schedule should specify:

- total settlement amount;
- retained compensation;
- installment amount/date;
- verified destination;
- treatment of missed payments;
- final reconciliation;
- public reporting;
- whether obligations are moral, contractual, or both.

Advantages:

- works with native continuous vesting;
- no custom account transformation;
- easy to verify.

Risks:

- requires continuing cooperation;
- recipient may stop;
- long monitoring horizon.

## Option 3 — bank authz

The recipient may grant a `cosmos.bank.v1beta1.SendAuthorization` to a reviewed grantee, potentially the new ION DAO core or a narrow executor.

Recommended bounds:

- denom: `uion` only;
- spend limit: settlement amount only;
- allowlist: verified ION DAO receiver if supported by the deployed SDK message;
- expiration: shortly after `2028-08-24T15:00:00Z`;
- no generic authorization for other message types;
- public grant and revoke monitoring.

Important limitations:

- authz does not make unvested ION spendable;
- execution succeeds only for currently spendable amounts;
- the grantor can normally revoke the authorization;
- DAO DAO must be proven able to emit the exact `MsgExec` as grantee;
- a contract grantee and signer context must be tested on the current Osmosis app version;
- a failed or over-large send must not block future installments permanently;
- the executor must not receive discretionary custody.

Validation plan:

1. reproduce current Osmosis authz protobuf and message-server behavior;
2. create a dust grant from a test account;
3. execute through a disposable DAO DAO core or narrow test contract;
4. prove receiver, spend-limit decrement, expiration, and revocation;
5. test an amount above spendable balance and require safe failure;
6. audit any helper contract;
7. only then encode the settlement mechanism.

Do not describe authz as irrevocable escrow.

## Option 4 — voluntary escrow

The recipient transfers currently spendable ION to an audited vesting/escrow contract whose beneficiary is the ION DAO or a defined split.

Use only if settlement terms need staged release or mutual conditions. A direct return is safer when no staging is needed.

Requirements:

- verified source and reproducible Wasm;
- self-admin or no-admin policy approved by ION governance;
- explicit beneficiaries and schedule;
- no deployer withdrawal path;
- no arbitrary migration admin;
- emergency/recovery behavior documented;
- test amounts before meaningful value.

This cannot move currently unvested ION out of the original account.

## Option 5 — governance safeguards without clawback

### Public monitoring

Monitor only public chain behavior:

- bank sends from/to the vesting address;
- new ION stakes, unstakes, and claims;
- proposal votes and voting power;
- authz grants/revocations;
- vesting unlock milestones;
- concentration as share of active voting power.

Alerts should report facts, not label normal transfers as malicious.

### Voting configuration

Recommended modernization settings:

- 30% quorum;
- strict majority;
- five-day voting;
- revoting enabled;
- seven-day unstaking;
- 3% active threshold;
- members-only proposals;
- 1 ION `OnlyPassed` deposit.

These improve notice and spam resistance. They do not prevent majority control if the address stakes enough.

### Veto-only Security Council

If the community appoints a credible five-member council:

- three-of-five member DAO;
- no treasury;
- no main-core admin;
- 48-hour timelock;
- `early_execute=false`;
- veto only malicious, exploit-driven, or payload-mismatched proposals;
- public rationale;
- replaceable by ION DAO governance.

This can stop obvious treasury theft after a whale-controlled vote. It must not become a political override for ordinary policy.

### Treasury compartmentalization

After modernization, consider moving operating budgets to subDAOs with:

- fixed funding caps;
- allowed receiver/message filters;
- timelocks;
- periodic renewal;
- public accounting;
- main-DAO recall or replacement path subject to the same timelock.

Do not move the entire treasury behind an unaudited filter or signer service.

## Option 6 — custom voting restrictions

Possible designs include:

- per-address voting cap;
- square-root/quadratic voting;
- conviction/time-weighted voting;
- delegation caps;
- excluding a named address;
- dual-house voting.

Problems:

- standard DAO DAO token-staked module does not provide them;
- address caps are Sybil-fragile unless identity exists;
- excluding one address is political disenfranchisement and can be bypassed by transfers where spendable;
- quadratic voting without Sybil resistance is mostly cosplay;
- custom modules require audit, source verification, migration planning, and UI testing;
- daodao.zone may not expose stake/config actions correctly.

Recommendation: do not block modernization on custom voting. Research separately only if the community wants constitutional change, not revenge against one holder.

## Option 7 — legal enforcement

This repository cannot determine legal rights.

A qualified reviewer should examine whether an enforceable agreement created:

- milestones;
- continuing service;
- representations that induced the grant;
- return obligations;
- IP delivery conditions;
- fraud or mistake claims;
- jurisdiction and remedy.

If valid rights exist, a legal settlement or order may produce voluntary transfer or other relief without a chain-sovereign state rewrite.

Do not publicly assert breach before reviewing the actual agreement and giving the other party a response opportunity.

## Option 8 — Osmosis governance intervention

### What it would actually require

The target is a normal `ContinuousVestingAccount`. There is no ordinary ION or Osmosis governance message that revokes it.

A forced change would likely require:

1. a new Osmosis software release;
2. an upgrade handler or tightly scoped state-migration code;
3. exact pre-upgrade account/balance assertions;
4. conversion, freeze, or bank-balance/account-state rewrite;
5. exact destination and vesting treatment;
6. validator adoption of the release;
7. post-upgrade invariants and rollback/failure handling.

That is chain-sovereign intervention in an account, not a smart-contract migration.

### Risks

- undermines credible neutrality and property expectations;
- creates precedent for governance confiscation after political disappointment;
- can corrupt vesting/bank supply invariants if implemented badly;
- exposes validators and contributors to legal and reputational risk;
- may split validator/community support;
- can be mistaken for rescuing price rather than remedying theft;
- consumes substantial governance attention.

### Minimum extraordinary-evidence standard

Do not proceed unless there is:

- verified fraud, theft, mistake, or enforceable breach;
- a precise amount and remedy;
- notice and response opportunity;
- independent legal review;
- independent technical audit;
- public upgrade source and reproducible build;
- narrow one-time invariants;
- broad chain-level legitimacy beyond the interested ION DAO.

“Whale is no longer aligned” is not enough. If that became sufficient, no token grant would be final and governance would be a seizure committee.

## Recommended sequence

1. approve the neutral evidence package off-chain;
2. search for contributor agreements and missing terms;
3. independently value delivered work;
4. publish a voluntary settlement invitation;
5. negotiate for 30 days, with one possible 14-day extension;
6. if accepted, use direct return plus tested authz/periodic transfers;
7. approve final terms through the modernized ION DAO;
8. if declined, publish closure and apply governance safeguards;
9. do not escalate to Osmosis governance without extraordinary new evidence.

## Proposal design if a voluntary settlement is reached

The ION DAO proposal should contain:

- no accusation or threat;
- exact retained and returned amounts;
- current spendable and locked balances at a pinned height;
- settlement schedule;
- verified receiver;
- authz/escrow code and message details if used;
- revocation/default behavior;
- recognition of delivered IBCX work;
- release/dispute terms reviewed appropriately;
- public monitoring and final completion criteria.

It should not contain private identities, private communications without consent, keys, internal infrastructure, or claims that exceed evidence.

## No-action baseline

If no agreement or enforceable right exists, the clean answer may be to leave the vesting account alone.

Then:

- make the concentration visible;
- harden governance against sudden execution;
- compartmentalize treasury authority;
- design future grants correctly;
- stop spending community attention on an unwinnable confiscation campaign.

Governance maturity includes knowing when not to swing the chain like a hammer.
