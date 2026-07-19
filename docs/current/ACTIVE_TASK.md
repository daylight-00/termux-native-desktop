# Active task: review the qualified libXdamage candidate for bounded provider authority

> Task ID: `review-libxdamage-production-candidate-bounded-provider-authority`
>
> Expected state on completion: the exact qualified Class C `libXdamage.so.1.1.0` candidate is either accepted for an explicitly bounded GTK 3.24.49 GDK X11 capability or rejected/deferred with a precise missing-evidence disposition. No upstream submission, publication, installation, target population, deployment or activation occurs.

## Objective

Perform the authority decision that is deliberately separate from recipe and artifact qualification. Review exact capability, necessity, consumer binding, conflicts, update and rollback boundaries for the qualified candidate.

## Why now

The recipe and artifact qualification task is complete with stable repeated hashes and production/harness separation. Provider authority was deliberately not inferred from successful construction, so the next proportional-assurance step is a non-building authority review.

## Authoritative inputs

```text
source:                 libXdamage 1.1.6
source SHA-256:         52733c1f5262fca35f64e7d5060c6fcd81a880ba8e1e65c9621cf0727afb5d11
recipe candidate tree:  46fe3064b0537aa7b4327d3cefc6891fa3b2cba5
package SHA-256:        09062711dd28f7268f3d7f75c85b3b42a55d3e6d70d1644a9853ee0b4c0e7890
member:                 libXdamage.so.1.1.0
member SHA-256:         391916aff0965656e7b81ece7766e3b22068462867b1dd88a0a051b3db9c2d7c
SONAME:                 libXdamage.so.1
result archive SHA-256: 462b613a0d6a2c2e2eefdff6742fd16014311f87606916ab0982220998612f6c
```

## In scope

- bind the exact member to the selected GTK 3.24.49 GDK X11 damage-region capability;
- verify the required symbol surface and exact direct dependency closure;
- assess collisions and exclusions, including bionic and Debian oracle bytes;
- define update, removal and rollback conditions for the exact candidate identity;
- decide bounded provider authority without widening to composition or target authority.

## Out of scope

Upstream submission or publication, treating the local artifact as approved-repository supply, package installation, target layout, materialization, deployment, activation, or authority for GTK/GDK core.

## Required reading

- `docs/evidence/libxdamage-production-recipe-candidate-result-review.md`
- `docs/evidence/libxdamage-provider-evidence-blocker.md`
- `docs/evidence/missing-glibc-provider-production-boundary.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None. The exact candidate evidence is retained. Upstream submission or supplier publication is a later separately authorized action.

## Completion criteria

One machine-readable and narrative authority decision records the exact candidate, scope, necessity, consumer binding, dependency closure, collision/exclusion state, update boundary, rollback boundary and prohibited inferences. The decision must preserve seven unresolved selected identities unless libXdamage is explicitly accepted, and must keep target population and activation blocked.

## Stop conditions

Stop without authority if capability or consumer necessity is not exact, required symbols are missing, direct dependencies are not already accepted, collision/update/rollback semantics are ambiguous, or evidence relies on uncontrolled live-prefix loading.

## Next valid action

Review the retained candidate evidence only. Do not rebuild merely to repeat already stable hashes unless a decision-critical evidence gap is identified.
