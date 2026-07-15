# Active task: classify provider claims under ADR 0005

> Task ID: `provider-claim-classification-under-adr-0005`
>
> Expected state on completion: the paused provider-authority corpus is converted into a bounded claim inventory whose implementation class, project-owned changed boundary, risk modifiers, accepted evidence, remaining gap, and minimum next assurance action are explicit; no new evidence request is issued until that classification is reviewed.

## Objective

Apply accepted ADR 0005 to the provider-authority work accumulated in records 0118–0165. Replace the former blanket producing-build requirement with claim-by-claim assurance classification without silently accepting provider authority, composition, target population, or activation.

## Why now

The documentation and operations control planes are consolidated. Future sessions can start from one full bundle and find current authority without narrative handoffs. The provider workstream can therefore resume at its actual decision boundary: determining what each provider claim needs under proportional assurance before collecting more evidence.

## Current accepted decisions

- `docs/operations/` is the single current operations surface; the former `docs/session-operations/` surface is historical.
- New web-chat sessions start from a user-provided full Git bundle and `START_HERE.md`.
- ADR 0005 is accepted: assurance is proportional to the exact claim, implementation class, project-owned changed boundary, and risk.
- Existing exact supply, semantic-role, artifact comparison, adaptation, and receipt evidence remains evidence; it is not automatically sufficient for every authority claim.
- The 28 unanswered SUP-02 requests remain historical open requests, but blanket completion of all 28 is no longer the default prerequisite.

## In scope

- Identify the distinct claims currently hidden inside provider authority, composition, target population, and activation language.
- Map each claim or coherent claim group to ADR 0005 class A, B, C, or D.
- Record the project-owned changed boundary and relevant risk modifiers.
- Bind existing evidence that already supports the claim.
- State the remaining gap and the minimum proportionate assurance action, including `none` when reference evidence is sufficient.
- Distinguish accepted evidence from accepted authority and from target membership.
- Produce a reviewable classification artifact and a bounded next task.

## Out of scope

- Issuing or fulfilling a new SUP-02 request.
- Collecting new device, custodian, build, or runtime evidence.
- Installing, extracting, promoting, or activating a provider.
- Populating a target layout or selected generation.
- Rewriting historical numbered records to match the new policy.
- Treating package-wide inference or successful launch as global authority.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md`
- `docs/refactor/0139-selected-obsidian-non-priority-generic-source-authority-boundary.md`
- `docs/refactor/0147-selected-obsidian-generic-build-attestation-and-adaptation-review-set.md`
- `docs/refactor/0156-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-request-set.md`
- `docs/refactor/0165-selected-obsidian-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response-producer.md`

The five numbered records are loaded for the explicit historical reconstruction question: which claims and evidence requirements were encoded before ADR 0005 changed the default assurance policy. Do not scan the rest of the numbered corpus unless one of these records points to a specific unresolved definition.

## Known facts

- The canonical provider-object set contains 60 rows, including 59 bounded reviewed objects and optional `libtermux-exec.so`.
- The earlier supply/request machinery grouped 28 root requests and 84 record contracts.
- Zero canonical SUP-02 responses were accepted at the 0165 boundary.
- Exact artifact supply, semantic role, platform adaptation, producing-build provenance, necessity, provider authority, composition, and target population are independent states.
- ADR 0005 permits lower assurance for reference-consumed claims and requires deeper assurance for adapted, independently reproduced, novel, or high-risk changed boundaries.

## Pending external inputs

None. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Construct a claim-classification table from the controlling records and current canonical generated tables. For each claim, record: claim ID, subject, authority state requested, ADR class, changed boundary, risk modifiers, existing evidence, remaining gap, minimum closure action, and prohibited inference. Review the classification before generating any collector, request, or runtime mutation.

## Stop conditions

Stop before evidence collection or repository implementation if:

- one row combines artifact identity, adaptation, authority, composition, and target membership into a single claim;
- classification cannot identify the project-owned changed boundary;
- an existing historical requirement is treated as binding solely because it was previously encoded;
- a lower assurance level would conceal security, ABI, loader, or broad runtime blast radius;
- the proposed next action would collect evidence without a reviewed claim classification;
- any provider or target is implicitly accepted by the classification itself.

## Completion criteria

- A bounded claim inventory covers the currently active provider-authority decision surface.
- Every claim has an ADR 0005 class and explicit risk rationale.
- Existing evidence and remaining gaps are separately recorded.
- The 28 SUP-02 requests are classified as still necessary, narrowed, replaced, or unnecessary rather than assumed uniformly mandatory.
- No provider, composition, target row, or activation is accepted by implication.
- The next active task names one smallest valid assurance or decision phase.
