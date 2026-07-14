# Evidence and live-state reconciliation

This document records the evidence used to choose the successor-DAO architecture. All addresses and balances are public chain state. Re-query before any production artifact is generated.

## Snapshot boundary

- chain: `osmosis-1`
- height: `66276760`
- block time: `2026-07-14T05:23:22.014415229Z`
- block ID: `5FC1C267BB0A1668D14CC6A568E9A00512D8C3C476521DCBBC99978D4891747A`
- local capture completion: `2026-07-14T05:23:24.848115Z`

The state was queried through a direct Osmosis full node and checked against public LCD/RPC behavior. Production evidence must use at least two independent endpoints and retain raw responses.

The proposal/balance boundary was height `66276760`. The full 2,870-address staker/claim enumeration completed later over moving head state because the public query interface paginates by address. Its aggregate still matched the retained-height staking balance equation exactly, and all 177 claims predated the snapshot. It is corroborating reconciliation, not a claim that every per-address response came from one historical height. Production capture should query a retained historical height for every paginated page.

## Legacy governance

| Field | Value |
| --- | --- |
| Contract | `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm` |
| Label | `ION governance contract` |
| Code ID | `1900` |
| Code hash | `37BB98453DDF9495C2CDF9A2667D515164EF9E09B15385921EABA9270D148F3E` |
| CW2 | `crates.io:ion-dao 0.0.2` |
| CosmWasm admin | empty |
| Instantiate permission for code 1900 | `Nobody` |
| Staking contract | `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc` |
| Governance denom | `uion` |
| Proposal count | `39` |
| Legacy claim cutoff | `66198261` |

Legacy config:

| Setting | Value |
| --- | ---: |
| Approval threshold | 50% |
| Quorum | 30% |
| Veto threshold | 30% |
| Voting period | 604,800 seconds (7 days) |
| Deposit period | 604,800 seconds (7 days) |
| Target proposal deposit | 500,000 uion (0.5 ION) |
| Minimum initial deposit | 50,000 uion (0.05 ION) |

## Legacy staking

| Field | Value |
| --- | --- |
| Contract | `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc` |
| Code ID | `2` |
| Code hash | `9306B0CE4AA88AB4E0750BBC42226231C423B8D36CA14DA752343A873DBC749A` |
| CosmWasm admin | legacy governance contract |
| Denom | `uion` |
| Unstaking duration | 1,209,600 seconds (14 days) |
| Active voting power/value | 1,671,832,757 uion |
| Nonzero stakers | 1,925 |
| Historical staker addresses queried | 2,870 |
| Outstanding claims | 177 |
| Outstanding claim amount | 173,848,282 uion |
| Latest claim maturity | 2026-05-31T17:18:08Z |
| Contract ION bank balance | 1,845,681,039 uion |

Reconciliation:

```text
1,671,832,757 active stake
+ 173,848,282 mature claims
= 1,845,681,039 ION in staking custody
```

Every outstanding claim was mature at the snapshot. The migration must not move this ION to the new treasury. It belongs to stakers and claimants.

The staking contract also held `5,000,000` atomic units of IBC LOKI and `7 uosmo`. Those assets are outside its ION accounting and the contract exposes no general rescue path. Treat them as stranded/accidental until a separately audited recovery path exists.

## ION supply and concentration

- bank supply at snapshot: `21,293,014,966 uion` = `21,293.014966 ION`
- largest active stake: prior-operator vesting address, `151.7 ION`
- largest stake as share of active power: approximately `9.0739%`
- 3% active-threshold reference: `638.79044898 ION`
- 2.5% reference: `532.32537415 ION`
- 5% reference: `1,064.6507483 ION`

The separate prior-operator assessment shows that staking all presently spendable balance while other stakes remain constant would give that address approximately `54.40%` of the resulting active stake. Standard DAO DAO configuration cannot wish this concentration away.

## Legacy governance bank balances

The legacy contract's internal token registry returned only `uion`. The bank module returned six denoms:

| Denom | Atomic amount | Notes |
| --- | ---: | --- |
| `uion` | `1,931,931,671` | Requires deposit/exploit reconciliation |
| `uosmo` | `2,100,008` | Transfer if still present at cutover |
| `factory/osmo14klwqgkmackvx2tqa0trtg69dmy0nrg4ntq4gjgw2za4734r5seqjqm4gm/uibcx` | `10,757,359` | IBCX-related tokenfactory asset; sparse metadata |
| `factory/osmo1xqw2sl9zk8a6pch0csaw78n4swg5ws8t62wc5qta4gnjxfqg6v2qcs243k/stuibcx` | `7,345,624` | stIBCX-related tokenfactory asset; sparse metadata |
| `factory/osmo1yhd9tzp09d833u7ray4pc6wwp72aewtt2xwakszn3lzlf2klnlwscjwhxt/uibcx` | `3,000` | IBCX-related tokenfactory asset; sparse metadata |
| `ibc/C360EF34A86D334F625E4CBB7DA3223AEA97174B61F35BB3758081A8160F7D9B` | `5,000,000` | metadata identifies LOKI from `transfer/channel-258/loki` |

A production inventory must query bank balances directly and include any new denom received after this snapshot.

## Deposit-state classification

There were 31 unclaimed deposit records totaling `665.001671 ION`. That number is not a valid liability total.

### Older claimable deposits

| Proposal | Unclaimed | `deposit_claimable` | Treatment recommendation |
| ---: | ---: | --- | --- |
| 16 | 0.051671 ION | true | Refund before cutover |
| 18 | 0.5 ION | true | Refund before cutover |

Subtotal: `0.551671 ION`.

The remediation cutoff now prevents direct legacy claims even though these proposal records are otherwise claimable. Manual reconciliation is required.

### Passed but unexecuted deposits

| Proposal | Unclaimed | Status | Treatment recommendation |
| ---: | ---: | --- | --- |
| 10 | 0.5 ION | passed | Refund unless review establishes a contrary obligation |
| 11 | 0.5 ION | passed | Refund unless review establishes a contrary obligation |

Both proposals attempted an earlier form of the developer vesting allocation. They remain passed but unexecuted, so their deposits never became claimable through normal legacy execution. Subtotal: `1 ION`.

### Rejected/nonclaimable deposits

Proposals `14`, `15`, `17`, `19`, `20`, and `21` contain `1.45 ION` of unclaimed deposits with `deposit_claimable=false`. Under the legacy state machine they were forfeited, not refundable liabilities. The cutover proposal should disclose and affirm this classification rather than silently absorb it.

### Exploit-era entries

Proposals `22`-`39` contain:

- recorded unclaimed deposits: `662 ION`;
- nominal proposal deposit across 18 proposals: `9 ION`;
- unsafe recorded overage: `653 ION`.

The `653 ION` overage was not deposited and is not a valid claimant entitlement. The hardened contract quarantines all of these legacy entries. Quarantine prevents payout; it does not itself adjudicate the `9 ION` nominal principal.

Because the recommended cutover permanently pauses the legacy DAO, the principal cannot remain “pending” there without making a future resolution depend on Osmosis governance. The production proposal must either refund the exact `9 ION` actually deposited or explicitly forfeit it. The preferred clean-exit illustration below refunds it while rejecting the overage.

### Illustrative transfer arithmetic

If governance approves:

- refunding `0.551671 ION` of older claimable deposits;
- refunding the `1 ION` passed-but-unexecuted deposits;
- refunding `9 ION` nominal exploit principal while rejecting the `653 ION` overage;
- treating rejected/nonclaimable deposits and unsafe overage as treasury;

then the snapshot transfer amount is:

```text
1,931.931671 ION physical balance
-   0.551671 ION older refunds
-   1.000000 ION proposal 10/11 refunds
-   9.000000 ION nominal exploit-principal refunds
= 1,921.380000 ION successor treasury
```

This is not a production amount. Re-query at proposal generation and again before execution.

## DAO DAO deployment evidence on Osmosis

The DAO DAO UI registry at commit `cfd87b031c1cdc4819d52513366be8d1cddc2cb0` lists Osmosis DAO DAO `2.7.0` code IDs. Live queries returned:

| Contract | Code ID | Code hash | Live CW2 check |
| --- | ---: | --- | --- |
| `cw-admin-factory` | 1571 | `AFA01543F33794A2A02FB0E6C72E766EA9C276FCF625A325E788F6B129F7F08B` | factory source/tag pinned separately |
| `dao-dao-core` | 1574 | `5D078FC9AEC04DF18C335446EB8DF03D24C73EE745F76FD39624D4C5FA768B4C` | `crates.io:dao-dao-core 2.7.0` |
| `dao-pre-propose-single` | 1579 | `FA78CE6D59B9BE90DE24E4D08D282E9C0CF3EF6D5811673AB4BF877A863C6862` | `crates.io:dao-pre-propose-single 2.7.0` |
| `dao-proposal-single` | 1581 | `E38FC5BB1B5E74EF154340567C673492515498B2120E5F15B0C990CD9FA5FE6A` | `crates.io:dao-proposal-single 2.7.0` |
| `dao-voting-token-staked` | 1588 | `A0C2DDD47CE95BA97F5F1E020EC69CD50230B67C0EAC0499EA181C8E5DAA313B` | `crates.io:dao-voting-token-staked 2.7.0` |

The source tag `v2.7.0` resolved locally to commit `beb2376c169e231ea44320b2695fc2751684f138`.

The live permissionless Osmosis admin factory is:

- address: `osmo1qpszqk458arkkdff5z4vrqlqv4k2n9a0tjme23vn00uyt30nrr7sfe87cv`;
- code ID: `1571`;
- CosmWasm admin: empty;
- internal factory admin query: `null`;
- instantiate permission: `Everybody`.

Re-verify this immediately before use. An address in a roadmap is not authority.

## Mad Scientists DAO comparison

The user-supplied reference core is `osmo1gtx8ka0d4jxcf5yyypll8824tz33ykmr27v04ff0r6dn9ucykr0shev4h7`.

It proves that DAO DAO renders Osmosis DAOs with the expected home, proposals, treasury, subDAO, members, and apps surfaces. It is **not** a configuration template for ION:

- core CW2 is DAO DAO `2.5.0`, not `2.7.0`;
- voting is NFT-staked (`dao-voting-cw721-staked`), not fungible ION;
- it has two proposal modules;
- its single-choice module uses 20% quorum, five-day voting, member-only execution, revoting, and close-on-failure;
- its referenced pre-propose module uses a 10 OSMO always-refunded deposit;
- it has no active threshold;
- automatic CW20 and CW721 discovery are both enabled.

Copying those settings would be cargo-cult governance. The useful lesson is the self-admin module graph and UI compatibility.

## Juno proof relationship

The Juno mainnet proof used DAO DAO `2.7.0` code hashes matching the five Osmosis artifacts listed above. It instantiated a deterministic self-admin core and standard modules, staked native tokens, created and auto-voted a proposal, executed a bank send, refunded an `OnlyPassed` deposit, unstaked, claimed, and loaded in daodao.zone.

See [`JUNO-VALIDATION.md`](JUNO-VALIDATION.md). It proves the exact Wasm architecture and UI path. It does not replace an Osmosis signed simulation of the final legacy proposal.
