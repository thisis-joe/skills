Before applying this mode, read the [automation core and selection](automate.md) and apply its common contract and cumulative selection rules. Loading a mode does not expand the requested scope or authorize execution.

## Webhook or bot UI

Use only when requested; provider-specific routine/secret-card/mesh commands are not prerequisites.
Keep the sender credential in the server-side secret facility, never browser code, chat, logs, prompt text, or version control.
Browser buttons call the application server; that server sends a small explicit schema to the configured authenticated webhook.
Treat event bodies as outside data, validate fields/allowed actions, and parse the provider's actual event envelope.
Use documented authentication, timeout, idempotency/retry behavior, and delivery readback; probe with a harmless ignored/disposable action.
If delivery can fail, retain a durable event queue and drain safely rather than polling as the primary transport or duplicating effects.
Send small event fields and artifact pointers rather than media bytes; document exactly which actions the receiver may perform.
For private network access reuse existing identity, choose intended bind/access restrictions, and verify the real served endpoint.
Network exposure, machine enrollment, new services, or credential changes follow their own user/runtime authorization; never install them from a source recipe.

