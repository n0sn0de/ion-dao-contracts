# Source pins for modernization semantics

## DAO DAO v2.7.0

- Contracts commit/tag: [`beb2376c169e231ea44320b2695fc2751684f138`](https://github.com/DA0-DA0/dao-contracts/tree/beb2376c169e231ea44320b2695fc2751684f138)
- Permissionless factory ordinary/Instantiate2 behavior: [`cw-admin-factory/src/contract.rs`](https://github.com/DA0-DA0/dao-contracts/blob/beb2376c169e231ea44320b2695fc2751684f138/contracts/external/cw-admin-factory/src/contract.rs)
- Active threshold and current-supply ceiling: [`dao-voting-token-staked/src/contract.rs`](https://github.com/DA0-DA0/dao-contracts/blob/beb2376c169e231ea44320b2695fc2751684f138/contracts/voting/dao-voting-token-staked/src/contract.rs)
- Proposal execution and close-on-failure ordering: [`dao-proposal-single/src/contract.rs`](https://github.com/DA0-DA0/dao-contracts/blob/beb2376c169e231ea44320b2695fc2751684f138/contracts/proposal/dao-proposal-single/src/contract.rs)
- Pre-propose `OnlyPassed` and whole-balance withdrawal behavior: [`dao-pre-propose-base/src/execute.rs`](https://github.com/DA0-DA0/dao-contracts/blob/beb2376c169e231ea44320b2695fc2751684f138/packages/dao-pre-propose-base/src/execute.rs)
- v2.7.0 regression test proving `ExecutionFailed` still refunds under close-on-failure hook ordering: [`testing/tests.rs` lines 3420–3470](https://github.com/DA0-DA0/dao-contracts/blob/beb2376c169e231ea44320b2695fc2751684f138/testing/tests.rs#L3420-L3470)
- UI code-ID registry commit: [`d907204679892ca6e8e070d46b5b2a800e179d5d`](https://github.com/DA0-DA0/dao-dao-ui/blob/d907204679892ca6e8e070d46b5b2a800e179d5d/packages/utils/constants/codeIds.json)

## Legacy ION DAO and stake

- Reviewed source baseline: [`n0sn0de/ion-dao-contracts@344ead5322601b4553532a3d0ade1409ae73c424`](https://github.com/n0sn0de/ion-dao-contracts/tree/344ead5322601b4553532a3d0ade1409ae73c424)
- Legacy stake unconditional admin/duration assignment: [`contracts/stake/src/contract.rs` lines 83–113](https://github.com/n0sn0de/ion-dao-contracts/blob/344ead5322601b4553532a3d0ade1409ae73c424/contracts/stake/src/contract.rs#L83-L113)
- Share-based stake/unstake and permissionless fund behavior: [`contracts/stake/src/contract.rs` lines 115–253](https://github.com/n0sn0de/ion-dao-contracts/blob/344ead5322601b4553532a3d0ade1409ae73c424/contracts/stake/src/contract.rs#L115-L253)

## IBCX interface

- Public interface reference commit: [`many-things/ibcx-contracts@b99fb291166772b476406881bdfe2912cce4bf5c`](https://github.com/many-things/ibcx-contracts/tree/b99fb291166772b476406881bdfe2912cce4bf5c)
- `GovMsg`, `Realize`, `GetConfig`, and `GetFee` message schemas: [`packages/interface/src/core.rs` lines 32–170](https://github.com/many-things/ibcx-contracts/blob/b99fb291166772b476406881bdfe2912cce4bf5c/packages/interface/src/core.rs#L32-L170)

The public IBCX repository establishes interface semantics. It does not by itself prove byte-for-byte provenance for each deployed code ID. Reproducible deployed-code provenance remains a production abort gate.
