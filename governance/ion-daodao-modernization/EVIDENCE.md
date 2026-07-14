# Evidence and live-state reconciliation

This document records the public-chain evidence used by the roadmap. It is not an executable manifest. Re-query at one archive height before constructing either transition proposal.

## Snapshot boundary

- chain: `osmosis-1`
- retained governance/balance height: `66276760`
- block time: `2026-07-14T05:23:22.014415229Z`
- block hash: `5FC1C267BB0A1668D14CC6A568E9A00512D8C3C476521DCBBC99978D4891747A`

Proposal and aggregate balance reads were retained at that boundary. The full holder/claim enumeration was paginated later over moving head state; its totals exactly reconciled to the retained aggregate stake balance. Production evidence must use one archive height for every page and repeat critical reads through a second independent archive endpoint.

## Legacy governance identity

| Field | Verified value |
|---|---|
| Address | `osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm` |
| Code ID | `1900` |
| CW2 | `crates.io:ion-dao 0.0.2` |
| Wasm admin | none |
| Label | `ION governance contract` |
| Code hash | `37BB98453DDF9495C2CDF9A2667D515164EF9E09B15385921EABA9270D148F3E` |
| Instantiate permission | `Nobody` |
| Migration/cutoff height | `66198261` |

The contract is adminless. Another in-place migration requires Osmosis chain authority or an equivalent state-level path.

### Legacy configuration

- threshold: 50%
- quorum: 30%
- token-holder veto threshold: 30%
- voting period: 7 days
- deposit period: 7 days
- full deposit: 0.5 ION
- minimum initial deposit: 0.05 ION
- stake contract: the address below

The legacy `UpdateConfig` replaces the full config. An optional retirement metadata message must therefore preserve every nonmetadata field exactly or be omitted.

## Legacy staking identity and custody

| Field | Verified value |
|---|---|
| Address | `osmo1yg8930mj8pk288lmkjex0qz85mj8wgtns5uzwyn2hs25pwdnw42sf745wc` |
| Code ID | `2` |
| CW2 | `crates.io:ion-stake 0.0.1` |
| Internal admin | Legacy governance |
| Wasm admin | Legacy governance |
| DAO reference | Legacy governance |
| Denom | `uion` |
| Unstaking duration | 1,209,600 seconds / 14 days |
| Code hash | `93069A8B8B330CC8F009690740BA1DD9B5B5B433E99EA297DF1140BB9173480E` |

Aggregate retained state:

- total shares/voting power: `1,671,832,757`
- active backing value: `1,671,832,757 uion`
- mature claims: `173,848,282 uion` across 177 records
- stake-contract bank ION: `1,845,681,039 uion`

Reconciliation:

```text
1,671,832,757 active backing
+ 173,848,282 claims
= 1,845,681,039 uion custody
```

The snapshot share:value ratio is 1:1. Permissionless `Fund` can change it. Legacy `Unstake.amount` is shares, not guaranteed ION value.

The stake contract also holds 7 `uosmo` and 5,000,000 units of the LOKI IBC denom. Its current execute interface cannot sweep those assets. Never migrate or sweep its `uion` while shares or claims remain.

The stake contract has no retire or pause message and remains callable indefinitely.

## Legacy governance bank balances

| Denom | Raw amount |
|---|---:|
| `uion` | `1931931671` |
| `uosmo` | `2100008` |
| `ibc/C360EF34A86D334F625E4CBB7DA3223AEA97174B61F35BB3758081A8160F7D9B` | `5000000` |
| `factory/osmo14klwqgkmackvx2tqa0trtg69dmy0nrg4ntq4gjgw2za4734r5seqjqm4gm/uibcx` | `10757359` |
| `factory/osmo1xqw2sl9zk8a6pch0csaw78n4swg5ws8t62wc5qta4gnjxfqg6v2qcs243k/stuibcx` | `7345624` |
| `factory/osmo1yhd9tzp09d833u7ray4pc6wwp72aewtt2xwakszn3lzlf2klnlwscjwhxt/uibcx` | `3000` |

The legacy token list reports only `uion`; it is not an exhaustive asset registry.

### CW20/CW721 discovery limitation

Bank queries cannot discover CW20 or CW721 holdings. Before claiming completeness:

1. query balances for every known Osmosis CW20/CW721 associated with ION/IBCX;
2. scan historical Wasm transfer/send/receive events involving the legacy address;
3. inspect indexed contract-account holdings through at least one trusted indexer;
4. compare with project manifests and prior treasury disclosures;
5. publish unresolved indexer/archive gaps.

Do not infer “none exist” from bank state alone.

## Proposal and deposit state

There are 39 legacy proposals at the retained boundary:

- executed: 1, 3–7, 12, 13, 18;
- rejected: 2, 8, 9, 14–17, 19–21;
- passed but unexecuted: 10 and 11;
- affected open proposals: 22–39.

Proposal 10 and 11 payloads remain stale and unexecuted:

| Proposal | Source field | Denom | End time | Technical issue |
|---|---|---|---|---|
| 10 | non-DAO address | `uion` | 2028-07-27 | required signer/source is not the executing DAO |
| 11 | legacy DAO | `ion` | 2028-08-12 | invalid/unfunded denom; proposal 12 identifies this correction |
| 12 | legacy DAO | `uion` | 2028-08-24 | executed successfully |

### Unclaimed deposit classes

| Class | Recorded amount | Present treatment |
|---|---:|---|
| Claimable older deposits, proposals 16 and 18 | 0.551671 ION | Cutoff blocks automatic claim; manual policy required |
| Passed/unexecuted 10 and 11 | 1.000000 ION | Not claimable under current status; manual policy required |
| Rejected/nonclaimable older deposits | 1.450000 ION | Forfeited under current state unless governance changes policy |
| Affected proposals 22–39 actual principal | 9.000000 ION | Manual refund/forfeit decision required |
| Affected records’ unsafe overage | 653.000000 ION | Nonphysical accounting overage; reject as liability |

Future proposal deposits are not in this table. The transition-enabling proposal’s 0.5 ION must be claimed before retirement. The final-handoff proposal’s 0.5 ION must be manually refunded by its own execution before permanent pause.

Preferred retained-height illustration:

```text
1,931.931671 current governance ION
-   0.551671 older claimable refunds
-   1.000000 proposal 10/11 policy refund
-   9.000000 affected-record principal refund
= 1,921.380000 ION
```

This is an illustration only. Production must include future deposits, intervening claims, and all denoms.

## ION supply

Retained supply:

```text
21,293,014,966 uion
= 21,293.014966 ION
```

Dynamic thresholds at that supply:

```text
3% active threshold = ceil(638,790,448.98) = 638,790,449 uion
4% handoff margin   = ceil(851,720,598.64) = 851,720,599 uion
```

The contract recalculates from current supply. A supply increase can deactivate a previously active DAO.

## IBCX control inventory

The legacy DAO controls three application contracts:

| Product | Contract | Code ID | CW2 | Wasm admin | App `gov` | `pending_gov` | Fee collector |
|---|---|---:|---|---|---|---|---|
| New IBCX | `osmo14klwqgkmackvx2tqa0trtg69dmy0nrg4ntq4gjgw2za4734r5seqjqm4gm` | 458 | `ibcx-core 0.1.2` | Legacy DAO | Legacy DAO | none | Legacy DAO |
| stIBCX | `osmo1xqw2sl9zk8a6pch0csaw78n4swg5ws8t62wc5qta4gnjxfqg6v2qcs243k` | 49 | `ibcx-core 0.1.1` | Legacy DAO | Legacy DAO | none | Legacy DAO |
| Old IBCX | `osmo1yhd9tzp09d833u7ray4pc6wwp72aewtt2xwakszn3lzlf2klnlwscjwhxt` | 47 | `ibcx-core 0.1.1` | Legacy DAO | Legacy DAO | none | Legacy DAO |

Each contract holds a multi-asset backing portfolio. Those portfolios are obligations/assets of index-token holders, not DAO treasury.

Application governance uses a two-step `update_gov` then `accept_gov` flow. This cannot be atomically completed by a legacy proposal alone. Product control must be accepted and verified by the active successor before legacy retirement.

Exact fee-realization and fee-collector messages remain a production source-review gate.

## DAO DAO v2.7.0 Osmosis artifacts

At review time, the DAO DAO UI registry and live Osmosis code state identified:

| Component | Code ID | Live hash |
|---|---:|---|
| `cw-admin-factory` | 1571 | `AFA01543F33794A2A02FB0E6C72E766EA9C276FCF625A325E788F6B129F7F08B` |
| `dao-dao-core` | 1574 | `5D078FC9AEC04DF18C335446EB8DF03D24C73EE745F76FD39624D4C5FA768B4C` |
| `dao-pre-propose-single` | 1579 | `FA78CE6D59B9BE90DE24E4D08D282E9C0CF3EF6D5811673AB4BF877A863C6862` |
| `dao-proposal-single` | 1581 | `E38FC5BB1B5E74EF154340567C673492515498B2120E5F15B0C990CD9FA5FE6A` |
| `dao-voting-token-staked` | 1588 | `A0C2DDD47CE95BA97F5F1E020EC69CD50230B67C0EAC0499EA181C8E5DAA313B` |

Registry/source references reviewed:

- DAO DAO UI registry at commit [`d907204679892ca6e8e070d46b5b2a800e179d5d`](https://github.com/DA0-DA0/dao-dao-ui/blob/d907204679892ca6e8e070d46b5b2a800e179d5d/packages/utils/constants/codeIds.json)
- DAO DAO contracts tag/commit [`v2.7.0` / `beb2376c169e231ea44320b2695fc2751684f138`](https://github.com/DA0-DA0/dao-contracts/tree/beb2376c169e231ea44320b2695fc2751684f138)
- ION DAO source baseline [`n0sn0de/ion-dao-contracts@344ead5322601b4553532a3d0ade1409ae73c424`](https://github.com/n0sn0de/ion-dao-contracts/tree/344ead5322601b4553532a3d0ade1409ae73c424)

Code IDs are deployment inputs, not timeless constants. Re-resolve and reproduce hashes before any production deployment.

## Self-admin factory

Factory:

`osmo1qpszqk458arkkdff5z4vrqlqv4k2n9a0tjme23vn00uyt30nrr7sfe87cv`

Verified:

- code ID 1571;
- internal admin `null`;
- Wasm admin none;
- permissionless ordinary and Instantiate2 self-admin paths.

Production recommendation uses ordinary `InstantiateContractWithSelfAdmin` because deployment precedes handoff. The permissionless creator semantics make published/mempool-visible production Instantiate2 salts front-runnable.

## Mad Scientists reference DAO

The supplied reference proves Osmosis and daodao.zone support DAO DAO modules. It is not an ION config template.

Verified core:

- core `osmo1gtx8ka0d4jxcf5yyypll8824tz33ykmr27v04ff0r6dn9ucykr0shev4h7`;
- `dao-dao-core 2.5.0`;
- self Wasm admin;
- CW721-staked voting, not fungible-token voting;
- single-choice and multiple-choice proposal modules;
- no active threshold;
- automatic CW20/CW721 discovery enabled.

Copying those settings would propagate an unrelated NFT DAO’s choices.

## Juno proof boundary

The bounded Juno proof used code hashes matching the five live Osmosis artifacts above. It proved self-admin factory deployment, native staking, proposal/deposit lifecycle, execution, unstake/claim, and direct daodao.zone rendering.

It did **not** prove:

- predeployment/activation/handoff sequencing;
- legacy deposit settlement;
- old stake admin transfer;
- IBCX two-step governance transfer;
- production time periods or active margin;
- CW20/CW721 discovery completeness;
- any Security Council graph.

Those remain explicit production gates.
