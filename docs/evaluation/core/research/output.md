# Why 300ms?

The historical reason for 300ms is unknown in the available evidence. Current code establishes the literal and conversion, but does not establish the author's intent.

At the revision in base.txt, client.py:1 sets REQUEST_TIMEOUT_MS=300; client.py:4 passes timeout=0.3 to client.get. The capture probe confirms the passed value with no real HTTP request (`evidence/probe.json`, exit 0). The downstream client's interpretation and effective network deadline are not established because no client package/version is supplied.

Rename-aware `git log --follow`, blame and the introducing commit show only “Initial imported fixture”, with no rationale (`evidence/history.json`). README.md explicitly says historical design records were not retained; the available non-Git files are client.py and README.md. No decision record was found in this scope. Tracker, contemporary PR/review, incident and telemetry evidence are unavailable by the request's source boundary. An absent record is not evidence that the decision lacked a reason.

Possible latency-budget, operational-regression or arbitrary-default explanations remain competing hypotheses; none has support sufficient to call it causal. No metric, sample period or user promise is inferred from the number.

Cheapest useful next check: obtain the pre-import change/review or linked incident that introduced the threshold; if the goal later becomes changing it, obtain the applicable request budget and failure distribution first. Explanation-only scope ends here; the constant is unchanged.
