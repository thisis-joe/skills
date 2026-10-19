Read/apply [core](automate.md) first; no new authority.

## Conditional workflow specification only

Use when the requested result is a reusable workflow specification rather than execution, including
an experimental workflow-design interview. Inspect task-authorized notes, current tools, existing
commands and examples of the user's actual repeated work before proposing a workflow.
Identify the outcome, trigger, cadence/event source, input locations, decisions, current pain,
dependencies, checkpoints and where human judgment must remain. Ask only unresolved decisions;
discover available facts rather than requiring the user to retype their tool inventory.

Produce a self-contained implementable specification with stable stages, inputs/outputs, authorized
data sources/destinations, owner, acceptance, evidence, retries, idempotency, recovery and stop rules.
Separate deterministic mechanics from model judgment and manual steps. State which available tool
performs each action, which capability is missing and what must be verified before activation.
Fit the workflow to existing tools and conventions; do not prescribe a new standing system without
a demonstrated need. Preserve alternatives and open decisions when evidence is insufficient.
End with the specification and next implementation boundary. Do not run the workflow, create a
schedule, install a service, post data or activate an agent simply because those steps appear in it.
Label experimental source techniques as optional and revise from observed use rather than turning
an untested interview preference into a universal requirement.
