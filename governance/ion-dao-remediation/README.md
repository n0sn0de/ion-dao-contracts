# ION DAO Osmosis governance remediation package

Status: **submitted as expedited Osmosis proposal `1024` with the full 20,000
OSMO deposit; validator proposer YES vote verified on-chain**.

For the reproducible preflight and direct-signing procedure, use
[`VALIDATOR-SUBMISSION-RUNBOOK.md`](VALIDATOR-SUBMISSION-RUNBOOK.md). The
canonical submission and vote receipts are in
[`submission-receipt.json`](submission-receipt.json).

- Proposal: `1024`
- Submission tx: `9AED184C40B6760DA628F0B118120168AEE992467902E60D9296C73AF25558AB`
- Validator YES vote tx: `E1882CDBCD68A06C8850D22856C3D656481640A04CC7AE97E689F78CC049A85D`
- Voting end: `2026-07-13T04:31:54.995897773Z`

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
| Complete package | `ipfs://bafybeicbxxiui3zmkpojc22kr774h526qskv77ych7wzrjkxeh26kfjtei` |
| Cosmos governance metadata | `ipfs://bafkreif6ksnwsneyjqlkyjb3qswtofzp7xsq6ctovmpfvk3qt3m6lfvgvy` |
| Full proposal document | `ipfs://bafkreibjw2ogu477jn2vgqsivojsr72ipdhmr23lgdo52zrehb7oixm57m` |

Public gateways:

- <https://ipfs.io/ipfs/bafybeicbxxiui3zmkpojc22kr774h526qskv77ych7wzrjkxeh26kfjtei/>
- <https://bafybeicbxxiui3zmkpojc22kr774h526qskv77ych7wzrjkxeh26kfjtei.ipfs.dweb.link/>
- <https://gateway.pinata.cloud/ipfs/bafybeicbxxiui3zmkpojc22kr774h526qskv77ych7wzrjkxeh26kfjtei/>

The revised metadata, proposal Markdown, package manifest, and Wasm were
retrieved across `ipfs.io`, `dweb.link`, and Pinata, with SHA-256 matching local
files.

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
| `VALIDATOR-SUBMISSION-RUNBOOK.md` | Fail-closed direct-signing instructions for a validator-controlled Linux host |
| `validator-submission-manifest.json` | Structured validator identity, funding, deposit, simulation, and file-hash receipt |
| `submission-receipt.json` | Chain-verified proposal submission, full deposit, and validator YES vote receipt |
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
