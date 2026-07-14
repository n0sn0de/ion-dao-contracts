# Prior-operator allocation evidence

## Snapshot boundary

- chain: `osmosis-1`
- reference height: `66276784`
- reference time: `2026-07-14T05:23:51.419944203Z`
- ION total supply near snapshot: `21,293.014966 ION`

Values that depend on vesting time must be recomputed when cited later.

## Proposal chronology

### Proposal 10

- title: `[Treasury Spend] Allocate ION incentives to the ION DAO dev contributors`
- submitted: `2023-07-19T13:02:02.339375976Z`
- current status: `passed`
- deposit: `0.5 ION`, not claimable because the proposal was never successfully executed
- intended recipient: `osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`
- intended amount: `3,407.04 ION`
- intended end time: `2028-08-24T15:00:00Z`
- message type: `/cosmos.vesting.v1beta1.MsgCreateVestingAccount`
- vesting style: continuous (`delayed=false`)

The body described:

- the ION DAO development contributors as working for more than one year;
- an allocation of approximately 16% of ION supply;
- five-year linear vesting;
- a compensation rationale of about `$100,000` per year at the contemporary ION price;
- work on ION DAO and IBCX.

The body did not define milestone, revocation, service, termination, or repayment conditions.

### Proposal 11

- title: `Execution of the Dev Funding`
- submitted: `2023-08-04T13:00:37.875470040Z`
- current status: `passed`
- deposit: `0.5 ION`, not claimable because execution did not complete
- intended recipient and amount: same as proposal 10
- intended end time in the encoded message: `2028-08-24T23:00:00Z`
- message type: `/cosmos.vesting.v1beta1.MsgCreateVestingAccount`

The body says the earlier execution failed because the target account was not empty, which prevented the vesting-account creation path.

### Proposal 12

- title: `[Revised Proposal] dev funding`
- submitted: `2023-08-16T15:54:00.934735016Z`
- current status: `executed`
- deposit: `0.5 ION`, claimed
- source: ION DAO governance contract
- destination: `osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`
- amount: `3,407,040,000 uion`
- end time: `2028-08-24T15:00:00Z`
- delayed flag: `false`
- message type: `/cosmos.vesting.v1beta1.MsgCreateVestingAccount`

The current auth account independently proves that this message succeeded.

## Decoded executed message

Human-readable protobuf fields:

```text
from_address: osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm
recipient:    osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk
amount:       3407040000 uion
end_time:     1850742000 (2028-08-24T15:00:00Z)
delayed:      false
```

The source address encoded in the executed proposal is the live ION DAO governance contract. Production reviewers should independently decode the protobuf bytes rather than trust this table.

## Current auth account

Account query returned:

```text
@type: /cosmos.vesting.v1beta1.ContinuousVestingAccount
original_vesting: 3407040000 uion
start_time: 1692806078
end_time: 1850742000
account_number: 913967
sequence: 24
```

Converted times:

- start: `2023-08-23T15:54:38Z`
- end: `2028-08-24T15:00:00Z`

The account JSON contains no funder, revoker, clawback address, DAO admin, or module owner.

## Current balances and vesting state

At the reference time:

| Quantity | Atomic uion | ION |
| --- | ---: | ---: |
| Original allocation | 3,407,040,000 | 3,407.040000 |
| Current bank balance | 3,101,840,914 | 3,101.840914 |
| Current spendable bank balance | 1,662,138,668 | 1,662.138668 |
| Current locked bank balance | 1,439,702,246 | 1,439.702246 |
| Active legacy stake | 151,700,000 | 151.700000 |
| Outstanding legacy stake claims | 0 | 0 |
| Known bank plus staked holdings | 3,253,540,914 | 3,253.540914 |
| Original allocation not in those locations | 153,499,086 | 153.499086 |

The “not in those locations” line is not proof of sale or recipient. It may reflect transfers or other positions not included in this bounded inventory. A broader forensics exercise would be needed before characterizing destination or use.

## Supply and voting concentration

Using total supply `21,293.014966 ION`:

- original allocation: approximately `16.0007%` of current supply;
- known bank plus staked holdings: approximately `15.2799%` of current supply;
- current active stake: approximately `9.0739%` of legacy active voting power.

If the address staked its entire currently spendable bank balance while every other current stake stayed constant:

```text
current total active stake     1,671.832757 ION
+ newly staked spendable ION   1,662.138668 ION
= resulting active stake       3,333.971425 ION

recipient current stake          151.700000 ION
+ newly staked spendable ION   1,662.138668 ION
= potential voting power       1,813.838668 ION

potential share ≈ 54.4047%
```

This is a scenario, not a prediction. It demonstrates that quorum or a 3% active threshold does not eliminate concentration risk.

## Account-type implications

`ContinuousVestingAccount` enforces a time-dependent spendable balance. It does not:

- lock the account's key away from the recipient;
- keep the original sender as owner;
- create a revocable escrow;
- track milestones;
- allow a CosmWasm DAO to override bank spendability;
- grant Osmosis governance an ordinary clawback message.

Once ION vests, the recipient can transfer or stake it. Unvested ION remains unavailable for ordinary sends until time unlocks it.

## Separation from the deposit exploit

The quarantined deposit entries in ION proposals `22`-`39` are associated with:

`osmo1fuzlaeajk7t80ujags2c3jlfemauwqg3s6t7dk`

The developer vesting recipient is:

`osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`

They are different addresses. This review found no chain evidence proving common control.

The exploit was a legacy proposal-deposit accounting flaw. The developer allocation was an executed governance spend. Treat them as separate unless stronger evidence says otherwise.

## Evidence quality and gaps

Strong chain evidence:

- proposal status and encoded messages;
- current account type and vesting fields;
- current bank, spendable, locked, staking, claim, and supply queries;
- distinct vesting and exploit addresses.

Not established here:

- real-world identity/control;
- full transaction graph for the `153.499086 ION` not in bounded holdings;
- off-chain contributor contracts;
- intellectual-property ownership;
- legal enforceability;
- present intent of the recipient;
- social-channel statements or promises.

Those gaps must remain gaps. Vibes are not evidence.
