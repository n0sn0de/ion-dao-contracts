# Bounded Juno mainnet validation receipt

## Scope

A live Juno `juno-1` proof exercised the DAO DAO architecture recommended for ION with one native token and short block-based test periods. No Osmosis transaction was signed or broadcast.

The proof used DAO DAO `2.7.0` artifacts whose five relevant code hashes match the selected Osmosis `2.7.0` artifacts exactly.

## Deployed graph

| Role | Juno code ID | Contract | CW2 | CosmWasm admin |
| --- | ---: | --- | --- | --- |
| Admin factory | 4859 | `juno1f3xxy7cw5lvljf38ehhcxavxlawpmkezq7qtrhesvympfudjvlaqzz6exr` | factory | empty |
| Core | 4862 | `juno14szp948haf5p5d3x6n2zhhqt64mavaljnya6r6qz0u35qugcmrfqu84dsj` | `crates.io:dao-dao-core 2.7.0` | core itself |
| Voting | 4879 | `juno1trlhjl5r8xhkw68v2elgxlvrw3xpqe984yusvz3h7yjvyfc0dr0s4ama6c` | `crates.io:dao-voting-token-staked 2.7.0` | core |
| Proposal | 4869 | `juno1rakfkue2waqf9rdz05s0hkvwqc4d6qxgtgpz2j3z5a0kyh2vqa0suqj75n` | `crates.io:dao-proposal-single 2.7.0` | core |
| Pre-propose | 4867 | `juno1pslajwnltcj56kzffr8t0x9amtqzkcvl96mjpr4rczff6x655tpsgua9l2` | `crates.io:dao-pre-propose-single 2.7.0` | core |

Core internal admin query also returned the core address.

## Artifact equivalence

| Artifact | Juno code ID | Osmosis code ID | Shared code hash |
| --- | ---: | ---: | --- |
| `cw-admin-factory` | 4859 | 1571 | `AFA01543F33794A2A02FB0E6C72E766EA9C276FCF625A325E788F6B129F7F08B` |
| `dao-dao-core` | 4862 | 1574 | `5D078FC9AEC04DF18C335446EB8DF03D24C73EE745F76FD39624D4C5FA768B4C` |
| `dao-pre-propose-single` | 4867 | 1579 | `FA78CE6D59B9BE90DE24E4D08D282E9C0CF3EF6D5811673AB4BF877A863C6862` |
| `dao-proposal-single` | 4869 | 1581 | `E38FC5BB1B5E74EF154340567C673492515498B2120E5F15B0C990CD9FA5FE6A` |
| `dao-voting-token-staked` | 4879 | 1588 | `A0C2DDD47CE95BA97F5F1E020EC69CD50230B67C0EAC0499EA181C8E5DAA313B` |

This proves the tested Wasm bytes, not merely matching version strings.

## Test-only configuration

The test used values chosen to finish in minutes:

- native denom: `ujuno`;
- active threshold: `1 JUNO` absolute;
- unstaking duration: 2 blocks;
- proposal deposit: `0.1 JUNO`, refund `OnlyPassed`;
- members-only proposal submission;
- strict majority with 30% quorum;
- minimum voting period: 2 blocks;
- maximum voting period: 5 blocks;
- revoting enabled;
- permissionless execution;
- retry on execution failure;
- no veto and no delegation module;
- automatic CW20/CW721 discovery disabled.

These periods and amounts are not production recommendations.

## Deterministic self-admin creation

The factory `Instantiate2ContractWithSelfAdmin` message used:

- deterministic salt: `jun0n0s-ion-daodao-v270-20260714`;
- expected core: `juno14szp948haf5p5d3x6n2zhhqt64mavaljnya6r6qz0u35qugcmrfqu84dsj`;
- `expect` guard enabled;
- distinct child-module salts;
- core internal admin `None`/self;
- child module admin `CoreModule`.

The exact signed transaction was submitted to the Cosmos SDK REST simulation endpoint before broadcast. Simulation consumed `842,347` gas and emitted the predicted core, voting, proposal, and pre-propose addresses. Broadcast then succeeded.

## Transaction receipts

| Step | Height | Tx hash | Gas used / wanted | Result |
| --- | ---: | --- | ---: | --- |
| Instantiate deterministic self-admin graph | 39,787,391 | `268E70CD839512FC215A34D36FE869D02B6A231B83460CC9087CB67B308E990F` | 842,343 / 4,000,000 | code 0; expected core and modules created |
| Stake 1 JUNO | 39,787,556 | `BB6773A10941BE0DF9CB9B3DBF0B3D37D8E49D2F5143425B99AB0821D021E382` | 179,795 / 500,000 | code 0; DAO active |
| Fund core with 1ujuno test payload | 39,787,560 | `FC36B94F338C296E750BF4A821CC4C837B5EE850FF144C8F7C508BD5EDC48658` | 82,768 / 200,000 | code 0 |
| Submit proposal 1 with 0.1 JUNO deposit and auto-vote yes | 39,787,565 | `541C8036739BFC742C78784D484A9683D9F121491259657154420AE88DF82061` | 495,120 / 700,000 | code 0; voting power 1 JUNO |
| Execute proposal 1 | 39,787,613 | `5DDAF5D694094B543D36BAC93B064467614A0AFC8BC195B92E4688BD56AEB2D8` | 319,909 / 500,000 | code 0; 1ujuno sent and deposit refunded |
| Unstake 1 JUNO | 39,787,638 | `F1E05A9AD97895AE581BFDA7BA785E53E850075039F1126DB124169D6DE90DB9` | 155,320 / 400,000 | code 0; claim release height 39,787,640 |
| Claim 1 JUNO | 39,787,651 | `FBAAC28852AC6DF53C788E0023D5E177E97C462B9B5642BAA0A704ED0A2AB819` | 138,474 / 350,000 | code 0; principal recovered |

Total test fees were `0.49875 JUNO`. The 1 JUNO voting stake and 0.1 JUNO proposal deposit were recovered; the 1ujuno payload returned through proposal execution.

Every state-changing transaction was signed only after an exact tx-bytes REST simulation succeeded.

## Postconditions

Direct queries proved:

- core internal admin = core;
- core CosmWasm admin = core;
- voting/proposal/pre-propose CosmWasm admins = core;
- factory retained no deployment authority;
- proposal 1 status = `executed`;
- yes power = `1,000,000` atomic JUNO;
- proposal deposit balance returned to zero after execution;
- core test balance returned to zero after execution;
- voting power returned to zero after unstake;
- claims list returned empty after claim;
- voting module bank balance returned to zero.

## DAO DAO UI proof

The direct URL loaded successfully:

`https://daodao.zone/dao/juno14szp948haf5p5d3x6n2zhhqt64mavaljnya6r6qz0u35qugcmrfqu84dsj/home`

The UI displayed:

- DAO name and description;
- proposal, treasury, subDAO, member, and app navigation;
- native `ujuno` governance token;
- 30% quorum and majority threshold;
- executed proposal 1, including yes power and the one-ujuno bank-send action.

No registry request or privileged indexing action was needed to use the direct core-address route.

## Limits

This proof does **not** establish:

- correctness of a future Osmosis legacy cutover proposal;
- ION holder migration participation;
- Osmosis gas for the full nested legacy payload;
- production five-day/seven-day/48-hour periods;
- legacy deposit refunds or exploit accounting;
- Security Council veto behavior;
- transferability or UI metadata for every legacy IBCX asset;
- safe production amounts at a future height.

Those remain mandatory gates in [`TEST-PLAN.md`](TEST-PLAN.md).
