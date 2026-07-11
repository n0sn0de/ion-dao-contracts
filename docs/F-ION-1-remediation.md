# F-ION-1 proposal-deposit remediation

## Scope

`ion-dao` v0.0.1 could record immediately refunded proposal funds as later
claimable deposits. The resulting liability could exceed the funds retained for
that proposal and consume unrelated DAO liquidity.

The v0.0.2 source remediation restores these invariants:

- proposal and depositor state records only funds retained by the contract;
- a pending proposal uses its immutable `deposit_base_amount`, not mutable
  global configuration;
- an upgrade from potentially vulnerable code quarantines every proposal
  submitted at or before the first quarantine migration block; and
- a rejected quarantine claim does not mark the deposit claimed or emit a bank
  transfer.

The contract also rejects any claim where the proposal's aggregate stored
`total_deposit` exceeds its immutable `deposit_base_amount`.

## Upgradeable instances

The empty object is the only accepted migration message:

```json
{}
```

Migration is restricted to CW2 identity `crates.io:ion-dao` version `0.0.1` and
always records `legacy_deposit_claim_cutoff_height`. There is deliberately no
quarantine opt-out: multiple historical artifacts report v0.0.1, so CW2
metadata and normal-looking aggregate totals cannot prove that an instance is
safe. Legacy config changes can produce undercollateralized records at or below
the proposal's original base. Repeated migration of v0.0.2 is rejected.

After migration, verify all of the following from chain state:

1. CW2 reports `crates.io:ion-dao` version `0.0.2`.
2. `get_config` reports the expected
   `legacy_deposit_claim_cutoff_height`.
3. A proposal query exposes its immutable `deposit_base_amount`.
4. The uploaded code checksum matches the reviewed release artifact.

The inclusive cutoff is deliberate. Transactions earlier and later in one block
share a height, so a proposal submitted before migration in the migration block
is conservatively quarantined. After migration, the contract rejects new
proposals for the rest of that block and rejects top-ups to any quarantined
pending proposal; this prevents accepting fresh funds that cannot enter the
ordinary claim path.

## Adminless instances and the observed ION DAO

A source patch cannot migrate a contract without an admin. At the
F-ION-1 research snapshot, the observed Osmosis governance contract
`osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm`
had no admin. Merging or uploading v0.0.2 therefore does **not** alter that
contract, neutralize its open proposals, or reconcile its stored deposits.

That live instance needs a separately reviewed governance and incident-response
plan. Depending on chain state and available authority, that may require vetoing
unsafe proposal outcomes, deploying a replacement DAO, moving only legitimate
treasury assets through governance, and defining a transparent settlement for
quarantined or disputed deposits. This repository does not guess payer-level
allocations that legacy storage cannot prove.

## Verification boundary

The remediation is a source and release fix. It is not proof that any deployed
instance was upgraded, that an adminless instance can be upgraded, or that a
specific historical claim is legitimate. Deployment evidence must include the
chain ID, contract address, code ID and checksum, migration transaction, CW2
version, cutoff query, and relevant proposal/deposit state.
