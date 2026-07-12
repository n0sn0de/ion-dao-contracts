# ION DAO Osmosis governance remediation package

Status: **prepared for public review; not signed or broadcast on Osmosis**.

For direct submission from the selected validator operator account, use
[`VALIDATOR-SUBMISSION-RUNBOOK.md`](VALIDATOR-SUBMISSION-RUNBOOK.md). The
validator package uses a 5,000 OSMO initial expedited deposit and documents the
remaining 15,000 OSMO required before the 24-hour vote starts.

## Recommendation

Use an **expedited** Osmosis `x/gov` proposal unless the full standard deposit
can enter voting before the safe standard cutoff.

| Track | Full deposit to start voting | Minimum initial submission | Vote | Yes threshold |
| --- | ---: | ---: | ---: | ---: |
| Standard | 6,000 OSMO | 1,500 OSMO | 5 days | >50% |
| Expedited | 20,000 OSMO | 5,000 OSMO | 24 hours | >66.7% |

The minimum initial amount only creates a proposal in deposit period. It does
not start voting. The package uses the full `20,000 OSMO` expedited deposit.

The earliest ION proposal expires at `2026-07-17 11:09:01 UTC`. The recommended
standard start cutoff with a six-hour safety margin was
`2026-07-12 05:09:01 UTC`. Once that passes, the expedited round is the only
configured voting period that can finish before the incident window.

See [`proposal.md`](proposal.md) for the full rationale, tradeoffs, exact action,
limits, validation evidence, proof receipts, failure behavior, and vote guidance.

## Immutable IPFS publication

| Item | URI |
| --- | --- |
| Complete package | `ipfs://bafybeiftjocrkmwojm5t57lrlkjyzxg2xjb5czzlkhm2mnba76g5ghjhny` |
| Cosmos governance metadata | `ipfs://bafkreihki5gssufsdhwtcfpupfv2bnlfq3b7iqtaxxiqyocqi5nq62cduq` |
| Full proposal document | `ipfs://bafkreifslgs4iu4t3opqtwv7gtfshastxeocpj2rrbm634vwvvmqcekt6q` |

Public gateways:

- <https://ipfs.io/ipfs/bafybeiftjocrkmwojm5t57lrlkjyzxg2xjb5czzlkhm2mnba76g5ghjhny/>
- <https://bafybeiftjocrkmwojm5t57lrlkjyzxg2xjb5czzlkhm2mnba76g5ghjhny.ipfs.dweb.link/>
- <https://gateway.pinata.cloud/ipfs/bafybeiftjocrkmwojm5t57lrlkjyzxg2xjb5czzlkhm2mnba76g5ghjhny/>

Retrieval of metadata, proposal Markdown, and Wasm was independently verified
through all three gateway families, with SHA-256 matching local files.

## Public review

- Source remediation: <https://github.com/n0sn0de/ion-dao-contracts/pull/3>
- Proposal/preflight discussion: <https://github.com/n0sn0de/ion-dao-contracts/pull/4>
- Incident disclosure: <https://github.com/n0sn0de/ion-dao-contracts/issues/1>
- Research correction: <https://github.com/n0sn0de/jason-research/pull/12>

## Files

| File | Purpose |
| --- | --- |
| `proposal.md` | Comprehensive human-readable proposal and decision analysis |
| `metadata.json` | Cosmos governance metadata referenced by the on-chain proposal |
| `proposal-expedited.json` | Generic `osmosisd tx gov submit-proposal` input with exact message, IPFS metadata URI, full deposit, and expedited flag |
| `unsigned-expedited-tx.json` | Generated, inspectable unsigned transaction |
| `proposal-expedited-initial-5000.json` | Same expedited proposal with the minimum 5,000 OSMO initial submission deposit |
| `unsigned-validator-initial-5000.json` | Generated unsigned tx with the selected validator account as proposer |
| `VALIDATOR-SUBMISSION-RUNBOOK.md` | Fail-closed local-node direct-signing instructions plus authz risk analysis |
| `validator-submission-manifest.json` | Structured validator identity, funding, deposit, authz, and file-hash receipt |
| `simulate-signed-tx.py` | Signed-but-unbroadcast REST simulation helper |
| `ion_dao_v0.0.2.osmosis.wasm` | Exact optimized production Wasm embedded by the proposal |
| `manifest.json` | Structured chain, incident, governance, source, artifact, IPFS, and proof evidence |
| `ipfs-package/` | Exact directory pinned under the complete-package CID |

## Final pre-broadcast gate

Do not broadcast the committed unsigned transaction blindly. Immediately before
submission:

1. re-query chain ID, target code/admin/CW2, proposals 22-39, governance params,
   wallet balance, account number, and sequence;
2. reproduce or checksum the artifact and embedded gzip bytes;
3. regenerate the generic proposal transaction from `proposal-expedited.json`;
4. decode and inspect outer/inner protobuf fields;
5. sign without broadcasting and call `/cosmos/tx/v1beta1/simulate`;
6. require sufficient balance for `20,000 OSMO` plus the simulated fee;
7. broadcast only with explicit user approval for the exact reviewed payload;
8. record tx hash, proposal ID, deposit status, voting end, and execution result.
