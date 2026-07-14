# Source pins for vesting and Authz conclusions

## Osmosis application

- Osmosis `v31.0.0` binary commit: [`c1adfd5fd510f132137857c2d644db6b2c70981b`](https://github.com/osmosis-labs/osmosis/tree/c1adfd5fd510f132137857c2d644db6b2c70981b)
- Binary-reported Cosmos SDK replacement: `github.com/osmosis-labs/cosmos-sdk v0.50.14-v30-osmo`
- Pinned SDK commit: [`1f78f02de9b2f60779c5062686201b45361fcb3f`](https://github.com/osmosis-labs/cosmos-sdk/tree/1f78f02de9b2f60779c5062686201b45361fcb3f)

## Account types and vesting arithmetic

- Continuous account constructors, vesting, and locked-coin behavior: [`vesting_account.go` lines 171–260](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/x/auth/vesting/types/vesting_account.go#L171-L260)
- Clawback account type, funder field, schedule, type check, and funder check: [`vesting_account.go` lines 544–839](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/x/auth/vesting/types/vesting_account.go#L544-L839)
- Continuous and clawback protobuf schemas: [`vesting.proto` lines 40–114](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/proto/cosmos/vesting/v1beta1/vesting.proto#L40-L114)
- Clawback message signer and fields: [`tx.proto` lines 108–155](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/proto/cosmos/vesting/v1beta1/tx.proto#L108-L155)
- Msg server target-type and original-funder enforcement: [`msg_server.go` lines 368–445](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/x/auth/vesting/msg_server.go#L368-L445)

## Authz

- `SendAuthorization` contains spend limit and receiver allowlist: [`bank authz.proto` lines 11–30](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/proto/cosmos/bank/v1beta1/authz.proto#L11-L30)
- Expiration belongs to the enclosing Authz `Grant`: [`authz.proto` lines 25–32](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/proto/cosmos/authz/v1beta1/authz.proto#L25-L32)
- `MsgExec` signer is the grantee: [`authz tx.proto` lines 50–60](https://github.com/osmosis-labs/cosmos-sdk/blob/1f78f02de9b2f60779c5062686201b45361fcb3f/proto/cosmos/authz/v1beta1/tx.proto#L50-L60)

## ION DAO source

- Reviewed source baseline: [`n0sn0de/ion-dao-contracts@344ead5322601b4553532a3d0ade1409ae73c424`](https://github.com/n0sn0de/ion-dao-contracts/tree/344ead5322601b4553532a3d0ade1409ae73c424)

These pins support technical account/message claims only. They do not determine off-chain ownership, contract, employment, fraud, or remedy questions.
