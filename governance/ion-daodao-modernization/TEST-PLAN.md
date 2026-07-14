# Risk-proportionate test and acceptance plan

The cutover moves governance authority and a multi-asset treasury, retires an old state machine, and asks 1,925 active stakers to use a new voting module. Testing must match that blast radius.

A green unit test is not permission to move the treasury. The required evidence is layered.

## Test principles

1. **No Osmosis production write before a frozen, independently reviewed package.**
2. **Every derived address is checked two ways.** Use both a local instantiate2 derivation and a signed chain simulation with the factory `expect` guard.
3. **Every balance is reconciled in atomic units.** No screenshots as accounting evidence.
4. **User custody is tested separately from treasury custody.** The legacy stake pool is not a treasury source.
5. **Failure tests matter more than happy-path screenshots.** Force wrong addresses, wrong admin, insufficient balances, inactive DAO, failed execution, and premature claims.
6. **UI success is not chain success.** Verify direct smart and module queries even when daodao.zone looks correct.
7. **Retain raw receipts.** Hash snapshots, unsigned payloads, decoded transactions, simulations, and final queries.

## Layer 1 — source and artifact verification

### DAO DAO source

- checkout the exact production tag and commit;
- verify the tag signature/history where available;
- identify all feature flags used for Osmosis builds;
- reproduce each Wasm artifact in the DAO DAO documented optimizer environment;
- compare reproduced SHA-256 with the live Osmosis code hash;
- if reproduction differs, stop and explain why before using the code ID;
- review security advisories and changes between the Mad Scientists `2.5.0` example and candidate version;
- confirm the UI registry still maps Osmosis to the selected code IDs.

### Legacy source

- pin the live governance `0.0.2` source and stake `0.0.1` source;
- confirm execute message serialization for stake `UpdateConfig`, stake CosmWasm `UpdateAdmin`, core `UpdateConfig`, `PauseDAO`, bank sends, and the proposal wrapper;
- verify pause is enforced on governance executes but not on direct staking contract claims/unstakes;
- verify setting old stake duration to `None` makes new unstakes immediately liquid and does not rewrite existing claims;
- verify transferring both old stake admin layers to the predicted new core does not alter stake, claims, or custody;
- verify legacy proposal execution is transaction-atomic when a nested message fails.

### Required negative tests

- wrong DAO DAO code ID;
- code ID with correct CW2 name but wrong hash;
- factory with a non-null internal admin;
- factory with unexpected CosmWasm admin;
- module admin set to deployer instead of core;
- only one of the two legacy stake admin layers transferred;
- core internal admin set to external address;
- automatic token discovery accidentally enabled;
- unreviewed proposal module included.

Gate: exact artifact/hash/admin matrix signed off by two reviewers.

## Layer 2 — deterministic payload validation

For the full candidate instantiate message:

- encode nested pre-propose, proposal, voting, and core JSON canonically;
- decode every base64 field back to JSON and compare byte-for-byte with the reviewed files;
- publish salt as UTF-8, hex, and base64;
- derive core and child addresses locally;
- set factory `expect` to the derived core address;
- simulate with a deliberately wrong `expect` and require failure;
- simulate with the correct `expect` and require the predicted instantiate/admin events;
- decode the complete legacy proposal messages after transaction generation;
- reject extra messages, receivers, denoms, funds, hooks, initial actions, or admins.

Gate: machine manifest and human table agree exactly.

## Layer 3 — state-export and accounting tests

Run the complete snapshot at one height.

### Governance and deposits

- export all 39 proposals, status transitions, total/base deposits, claimability, and execution messages;
- export every deposit using correct composite-key pagination;
- verify there are no duplicate or skipped keys;
- compute separate sums for claimable, passed-but-unexecuted, forfeited, nominal exploit principal, and unsafe overage;
- independently reproduce the cutover ION amount from raw rows;
- query contract bank balances before and after every arithmetic classification.

### Staking

- export every historical staker address;
- query each current stake and all claims;
- assert nonzero-staker count, active total, claim count, and claim total;
- assert active total plus claims equals staking ION bank custody;
- verify the latest claim maturity against the snapshot time;
- identify non-ION balances separately;
- do not assign non-ION stake-contract dust to users or treasury without a contract path and governance policy.

### Treasury

- query all bank balances, not only legacy `token_list`;
- query metadata and supply for every denom where possible;
- verify transferability/freeze/admin status for tokenfactory assets;
- determine whether IBC paths are live or merely historical;
- ensure no CW20/CW721 holdings are missed by bank-only queries;
- repeat the full inventory immediately before proposal submission and execution.

Gate: accounting equation balances and no asset is silently omitted.

## Layer 4 — local integration harness

Build a test harness containing:

- legacy ION governance `0.0.2`;
- legacy stake `0.0.1`;
- DAO DAO factory/core/voting/proposal/pre-propose exact candidate Wasm;
- native `uion` supply and representative holders;
- representative treasury denoms;
- old stakers and mature/unmatured claims;
- proposals/deposits covering all reconciliation classes.

### Happy path

1. pass the legacy cutover proposal;
2. execute refunds;
3. set old stake duration to `None`;
4. instantiate deterministic self-admin DAO DAO graph;
5. transfer all approved treasury assets;
6. pause legacy governance forever;
7. claim an old mature claim;
8. unstake an old active position immediately;
9. stake in the new module;
10. activate the new DAO;
11. submit, vote, execute, and close/refund new proposals.

### Failure path matrix

| Case | Required result |
| --- | --- |
| One refund exceeds balance | Whole cutover reverts |
| One treasury denom changed | Whole cutover reverts or retained delta is explicitly expected |
| Wrong factory expected address | Instantiation fails and whole cutover reverts |
| Wrong child code hash/ID | Preflight rejects; no execution |
| Proposal module admin is wallet | Acceptance fails |
| New active threshold unmet | Propose fails; treasury cannot be governed yet |
| Nonmember proposes | Pre-propose rejects |
| Exact 1 ION deposit absent | Propose rejects |
| Rejected proposal | Deposit follows `OnlyPassed` policy |
| Passed proposal | Deposit returns exactly once |
| Execution transiently fails | Proposal remains retryable |
| Old governance paused | New old-governance execute calls fail |
| Old stake claim after pause | Claim still succeeds |
| New old-stake unstake after duration removal | Immediate return succeeds |
| Existing old claim | Original release condition preserved |
| Unexpected token sent to core | Automatic CW token lists do not mutate |

Gate: full suite runs from a clean checkout in CI.

## Layer 5 — completed Juno mainnet proof

The bounded Juno proof established:

- exact DAO DAO `2.7.0` core, proposal, pre-propose, voting, and factory Wasm hashes matching the selected Osmosis deployments;
- instantiate2 predicted core address enforced by factory `expect`;
- core internal and CosmWasm self-admin;
- child module admins set to core;
- existing native-denom staking;
- active threshold;
- members-only pre-propose;
- exact `OnlyPassed` deposit;
- auto-vote and snapshot voting power;
- revoting-safe full voting expiry;
- permissionless execution of an approved bank send;
- deposit refund on execution;
- unstake claim and final recovery;
- direct rendering in daodao.zone, including the executed proposal.

See [`JUNO-VALIDATION.md`](JUNO-VALIDATION.md).

The test intentionally used short block durations and one JUNO. It did not test Osmosis-specific legacy execution, ION distribution, production periods, or treasury amounts.

## Layer 6 — Osmosis signed simulations

No broadcast.

### New graph only

From a funded nonproduction account or the exact legacy proposal execution context where simulation supports it:

- simulate the factory instantiate2 message;
- retain gas, events, predicted addresses, admin update, and contract versions;
- query that expected addresses are absent before any real execution;
- validate module initialization against the manifest.

### Full legacy proposal

Generate the exact legacy `Propose` call and later `Execute` call.

- sign without broadcasting;
- submit tx bytes to `/cosmos/tx/v1beta1/simulate`;
- require code `0` and a complete nested event trace;
- verify every refund receiver and amount;
- verify every treasury receiver, denom, and amount;
- verify old stake config event and internal-admin handoff;
- verify old stake CosmWasm admin-update event;
- verify core and child instantiate events;
- verify final legacy pause event;
- compare gas used against the configured transaction gas with at least a 40% safety margin;
- repeat against a second endpoint.

Simulation from the wrong sender is not evidence. Authorization and message context must match production.

Gate: two independent reviewers decode the signed transaction and simulation.

## Layer 7 — canary policy

Do not move treasury to a separately deployed “canary DAO” and later repeat governance. That creates a second production address and extra vote.

The Juno deployment is the cross-chain canary. On Osmosis, the one atomic cutover is the production event. Risk is bounded by preflight, deterministic address enforcement, atomic rollback, active threshold, and a fully reconciled terminal legacy balance.

If reviewers insist on an Osmosis canary, it must use a clearly named disposable DAO, dust-only funds, distinct salts, and no production authority. It cannot substitute for the full signed legacy simulation.

## Layer 8 — post-cutover verification

Run immediately after execution and again after 1 hour, 24 hours, 7 days, and 30 days.

### Immediate

- transaction code, height, block ID, gas, and event trace;
- all contract addresses, code IDs, hashes, versions, creators, and admins;
- exact module graph and enabled status;
- all configuration queries;
- all treasury balances;
- legacy pause state;
- old stake config, both admin layers, and claims;
- terminal legacy balance after every approved refund and treasury transfer;
- direct daodao.zone page rendering.

### 1 hour

- no unexpected admin/config updates;
- no unexpected proposal/module/token additions;
- holder stake migration started;
- old claims still payable;
- indexer/UI pages stable.

### 24 hours

- voting power and holder-count reconciliation;
- transfer, refund, and terminal-balance deltas explained;
- monitor proposal creation attempts while inactive;
- publish public receipt.

### 7 days

- active threshold progress;
- first harmless production proposal lifecycle;
- legacy/new staking migration statistics;
- security council monitoring if enabled.

### 30 days

- decide whether the active threshold, deposit, period, and veto profile performed as intended;
- do not change parameters solely because participation was inconvenient;
- archive legacy UI/query instructions permanently.

## Production acceptance checklist

- [ ] Frozen code/tag/commit/hash manifest
- [ ] Two-endpoint code and contract verification
- [ ] Complete state and claim export
- [ ] Deposit reconciliation approved
- [ ] Treasury inventory approved
- [ ] Deterministic addresses derived twice
- [ ] Wrong-address negative test passed
- [ ] Local happy/failure integration suite passed
- [x] Bounded Juno mainnet lifecycle passed
- [x] daodao.zone rendered the Juno proof DAO and executed proposal
- [ ] Exact Osmosis full signed simulation passed twice
- [ ] Independent payload reviews complete
- [ ] One public voting deadline communicated
- [ ] Legacy proposal passed and atomic execution code `0`
- [ ] Admin matrix verified
- [ ] Treasury, refunds, and terminal legacy balance reconciled
- [ ] Legacy governance paused
- [ ] Legacy stake internal and CosmWasm admins transferred to new core
- [ ] Old stake claims and exits verified
- [ ] New active threshold reached by multiple holders
- [ ] First production DAO DAO proposal executed
- [ ] Public post-cutover receipt published

No unchecked item should be hand-waved because the UI looks nice.
