# Prior-operator allocation evidence

## Snapshot boundary

- chain: `osmosis-1`
- archive height: `66276784`
- block time: `2026-07-14T05:23:51.419944203Z`
- vesting account: `osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`
- ION DAO: `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm`
- legacy stake: `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc`

Every snapshot claim below was re-queried against an archive endpoint at exactly this height. Time-dependent spendable/locked values must not be mixed with another height.

## Proposal chronology and payload decoding

### Proposal 10

- ID: 10
- title: `[Treasury Spend] Allocate ION incentives to the ION DAO dev contributors`
- current status: `passed`, not executed
- payload: `/cosmos.vesting.v1beta1.MsgCreateVestingAccount`
- `from_address`: `osmo14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sq2r9g9`
- recipient: vesting account above
- amount: `3,407,040,000 uion`
- end: Unix `1848268800` / `2028-07-27T00:00:00Z`

Technical reading: the required signer/source is not the executing ION DAO contract. The payload could not be validly dispatched under the DAO’s signer context.

### Proposal 11

- ID: 11
- title: `Execution of the Dev Funding`
- current status: `passed`, not executed
- `from_address`: ION DAO
- recipient: same account
- amount: `3,407,040,000 ion`
- end: Unix `1849698000` / `2028-08-12T13:00:00Z`

Technical reading: the denom is `ion`, not native `uion`. Proposal 12 identifies the correction. Do not attribute the failure to an already-existing target account without a transaction receipt proving that separately.

### Proposal 12

- ID: 12
- title: `[Revised Proposal] dev funding`
- current status: `executed`
- `from_address`: ION DAO
- recipient: same account
- amount: `3,407,040,000 uion`
- end: Unix `1850742000` / `2028-08-24T15:00:00Z`
- `delayed`: false

Execution transaction:

- hash: `1E15143F3135DEAB9D902F03F5D54D4B53EB65D8593E77CDDA773AC57CEFE245`
- height: `11126209`
- time: `2023-08-23T15:54:38Z`
- outer executor: `osmo1udw4032y7my0q9y0mp8ffry5m2u5xl3de46ex0`
- explorer receipt: [Mintscan transaction](https://www.mintscan.io/osmosis/tx/1E15143F3135DEAB9D902F03F5D54D4B53EB65D8593E77CDDA773AC57CEFE245?height=11126209)

The outer executor triggered an already-approved proposal; it was not the source or recipient of the vesting transfer.

## Account schema

Archive account query returned:

```text
@type:          /cosmos.vesting.v1beta1.ContinuousVestingAccount
account_number: 906739
sequence:       135
start_time:     1692806078
end_time:       1850742000
original uion:  3407040000
```

This is not:

- a module account;
- a `ClawbackVestingAccount`;
- a contract escrow;
- an account with a funder/revoker/admin field.

The account has unrelated non-ION bank holdings. This assessment does not characterize or propose action against those assets.

## Height-pinned ION arithmetic

At `H=66276784`:

```text
original vesting     3,407,040,000 uion
schedule vested      1,967,405,060 uion
schedule locked      1,439,634,940 uion
bank balance         3,101,840,914 uion
spendable bank       1,662,205,974 uion
legacy active stake    151,700,000 uion
legacy claims                    0 uion
```

Reconciliation:

```text
bank balance - locked
= 3,101,840,914 - 1,439,634,940
= 1,662,205,974 spendable uion
```

Current bank plus active stake:

```text
3,101.840914 + 151.700000
= 3,253.540914 ION
```

Arithmetic difference from original vesting:

```text
3,407.040000 - 3,253.540914
= 153.499086 ION
```

The difference is not a provenance or disposition finding. Fungible current balances may contain later inflows or other ION. No claim is made that particular grant units were sold, spent, returned, or moved to a known destination.

## Supply and concentration

ION supply at the same height:

```text
21,293.014966 ION
```

Bank plus active stake as a share of supply:

```text
3,253.540914 / 21,293.014966
≈ 15.279851%
```

Potential staking scenario:

```text
current active stake      1,671.832757 ION
spendable bank amount     1,662.205974 ION
resulting active stake    3,334.038731 ION

current account stake       151.700000 ION
plus spendable amount     1,662.205974 ION
potential voting power    1,813.905974 ION
potential share             54.405666%
```

This is a mechanical scenario under fixed assumptions, not a forecast or statement of intent.

## Proposal-text and work evidence

The on-chain proposal narrative represented that contributors had performed work and requested funding/compensation. It contained forward-looking roadmap, use-of-funds, continued-dedication, and value-accrual statements.

Public corroborating evidence includes:

- Osmosis proposal 504’s IBCX upload-permission record;
- public IBCX source repositories;
- later IBCX migration activity;
- archived product-site availability;
- referenced audit activity.

This supports that development activity occurred. It does not independently establish the complete scope, authorship, expenses, IP status, maintenance obligations, or fair value. Those require source/deployment/audit records and any off-chain agreements.

The reviewed proposal text encoded no objective payment milestones, DAO revoker, termination trigger, repurchase term, or express return obligation.

No `$100,000 per year` claim is used because the retrieved on-chain descriptions do not contain that figure and this package does not supply a pinned external price calculation.

## On-chain clawback boundary

Osmosis supports a different vesting class with clawback fields. The subject account is not that class.

For normal clawback, the chain expects:

- `ClawbackVestingAccount` target type;
- matching recorded funder signer.

The subject account contains no funder/revoker field. The ION DAO cannot sign as the account or convert its type through an ordinary message.

Osmosis proposal 772, “Demand return of IonDAO funding,” passed with no executable messages. It did not move funds or create clawback authority.

## Authz state and limits

No relevant Authz grant by the vesting account was identified at the reviewed height.

A future voluntary `SendAuthorization` could specify:

- `uion` spend limit;
- receiver allowlist.

Expiration belongs to the enclosing Authz `Grant` in `MsgGrant`, not to `SendAuthorization` itself.

But it would not:

- reserve bank balance;
- prevent the grantor from revoking;
- prevent other spending or staking first;
- move existing legacy-staked ION or future claims;
- schedule execution automatically;
- identify “grant coins” separately from fungible `uion`;
- let an external wallet sign as a DAO-core grantee.

A DAO core used as grantee must itself emit the exact `MsgExec` through a successfully executed proposal. That deployed path has not been proven on Osmosis.

## Separation from affected proposals 22–39

Address associated with affected proposals and anomalous deposit records:

`osmo1fuzlaeajk7t80ujags2c3jlfemauv2cayvm82e`

Vesting account:

`osmo1g6cjx9fju0le5ptx70rwrucj9qqngv39rzu8rk`

The addresses differ. No reviewed evidence established common control. Different addresses also do not prove different real-world control.

## Proposal 12 stored-threshold reconciliation

The migrated proposal fields reconcile with the stored thresholds:

- turnout `543674660 / 1750300392 = 0.310617915921714539`;
- required quorum votes `525090118`, actual votes `543674660`;
- required Yes votes `269817265`, actual Yes `530889418`;
- Veto votes `0`.

The proposal is recorded as executed, and the transfer/account creation are independently verified.

## What the evidence does not determine

- legal owner or beneficiary;
- current human/controller identity;
- fraud, theft, breach, employment, fiduciary, or restitution rights;
- complete delivered-work scope/value;
- validity or effect of off-chain agreements;
- common control with any affected-proposal address;
- entitlement to confiscate, freeze, dilute, fork, or exclude;
- future account behavior.

Those questions require additional evidence and, where applicable, qualified legal review or a competent forum.
