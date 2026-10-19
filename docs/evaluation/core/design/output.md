# Receipt delivery contract

Select a persistent delivery service that owns intent and delivery state, while queue consumers submit one stable intent. Current caller has only order_id/address and otherwise would have to coordinate retries itself (`caller.py`). The accepted brief supplies provider idempotency/lookup and database uniqueness; this design depends on those capabilities and requires checking their real semantics before implementation.

Caller usage:
```python
status = receipts.deliver(DeliveryIntent(
    key="receipt:O-17:v1", order_id="O-17", version=1, address="buyer@example.invalid"
))
# A duplicate retry reuses the identical intent/key.
status = receipts.status("receipt:O-17:v1")
```

`deliver(intent) -> DeliveryStatus` durably accepts/reads an intent. The stable key derives from receipt intent (order/version), never from retry number, UUID generated per attempt or timestamp. A different order version has a different key. Store a canonical request fingerprint including address; same key/different fingerprint returns IntentConflict before any effect. Parse external payload at this boundary.

`DeliveryStatus` is one of pending, succeeded(provider_receipt), unknown(last_attempt), failed_terminal(reason). Unknown is an observed uncertainty, not failure and not success. Read-only `status(key)` returns the current durable state or not_found. These shapes prevent a boolean false from ambiguously meaning safe-to-retry and outcome-unknown. No latency target was supplied.

| Candidate | Caller burden / locality | Failure behavior | Testability / transition |
|---|---|---|---|
| Queue handler directly calls provider and returns bool | Small signature, but every queue adapter must understand acknowledgement, deduplication, crash recovery and provider outcomes | Timeout false encourages duplicate effects; queue retry owns knowledge scattered across callers | Fast to wire; meaningful race/crash tests require rebuilding missing state ownership |
| Persistent service owns intent/state (selected) | Caller supplies intent, consumes status; database/provider/queue details stay with one owner | Atomic claim, explicit pending/unknown, reconciled retries and stable provider key handle the named crash windows | Public service seam with real local DB plus controlled provider boundary; moderate persistence/migration cost |

Ordering: atomically insert unique key+fingerprint+pending before send. Concurrent duplicates read the stored result or receive pending; they never both initiate a distinct effect. A queue message may acknowledge only after durable acceptance; thereafter owned reconciliation work is persisted so a crash does not lose recovery. A lease can identify work to inspect, but expiration alone does not prove the effect failed.

Persist send intent before provider call; reuse the stable provider key. On timeout or crash around send, persist/retain unknown and reconcile with provider lookup. Resume the original intent with the same provider key only under the provider's documented safe retry semantics; absence from an eventually consistent lookup is not conclusive failure. Terminal validation/provider rejection stays failed_terminal. Transport failure before durable acceptance can ask the queue to retry the identical intent.

Retention is 45 days under the supplied operational policy, longer than the maximum allowed 30-day redelivery/replay horizon. Expired replay must have an explicit rejection/archival policy; do not silently treat it as a fresh receipt. No obsolete public API exists in this fixture. Migrate the single on_message caller to construct the intent and consume statuses; remove any handler-local duplicate policy.

Observable test seam: service deliver/status, real transactional uniqueness, deterministic provider adapter that records actual requested keys/effects. Verify simultaneous identical submissions -> one intent/effect; different key -> second effect; same key/changed address -> conflict/no second effect; crash before/after call; timeout after actual provider success -> unknown then succeeded by lookup; pending duplicate -> no extra effect; delayed replay within horizon -> same result; retention boundary -> explicit disposition. Assertions must check effects and returned state, not private helper calls. No prototype was necessary to choose the contract, and no runtime correctness is claimed by this design draft.
