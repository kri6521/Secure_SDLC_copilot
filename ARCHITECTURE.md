# Architecture and security decisions

## Agent roles

- Requirement Agent: transforms untrusted text into a normalized requirement.
- Planning Agent: creates an implementation plan.
- Developer Agent: creates code in the sandbox.
- Code Review Agent: performs an LLM-based review.
- Security Agent: performs an LLM-based security review.
- Gatekeeper: combines deterministic checks and blocks failures.
- Release Coordinator: records evidence; deployment still requires a human.

## Coordination

LangGraph carries a typed state object between nodes. Agents exchange structured
artifacts through the state rather than directly calling one another.

## Human approval

A release cannot move to `RELEASED` without `human_approved=True`. The prototype
does not provide the release agent with deployment credentials.

## Defense in depth

LLM findings are advisory. Deterministic tools such as pytest, Bandit and pip-audit
provide independent checks. A failure in a critical check blocks the release.

## Prompt injection

The requirement is explicitly classified as untrusted data. A pre-check looks for
common instruction-hijacking indicators. In a production system this would be
supplemented by content provenance, instruction/data separation, sandboxing and
tool authorization policies.

## Least privilege

Agent permissions are conceptualized as capabilities rather than a shared superuser.
The developer can write only to the sandbox; no agent has real deployment credentials.

## Audit evidence

`app/core/audit.py` writes JSON Lines containing timestamp, stage, actor, action,
result and evidence. This supports post-run traceability.

## Production improvements

- isolated ephemeral containers for generated code
- signed commits/artifacts
- SBOM generation and image scanning
- OIDC/workload identity instead of static credentials
- policy-as-code
- secret manager integration
- branch protection and mandatory reviews
- immutable audit storage
- stronger prompt-injection defenses
- separate credentials and network policies per agent
- CI/CD integration with explicit approval environments
