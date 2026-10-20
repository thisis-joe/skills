---
name: coco-askme
description: "Use when the user wants to be quizzed on the current work or a chosen feature, code area or change to understand its principles, code flow, architecture, optimization, style or testing."
license: MIT
---

# coco-askme

Teach through questions grounded in the selected work and code. The default flow is **scope selection → topic selection → one question at a time → feedback on the answer → deeper question or another topic**. Follow the [common contract](../_coco-shared/contracts.md). Localize prompts, option names, feedback and summaries to the user's language; the wording below is in English for illustration.

## 1. Scope selection

Offer these scopes, numbered, and allow several to be combined:

1. **Current work:** tasks done in this conversation and their related changes.
2. **Feature or flow:** inspect the actual code and list numbered feature/flow candidates.
3. **Specific code:** a file, class, function, component or code range.
4. **Specific change:** a selected commit, branch range or diff.

Skip this stage when the invocation already names a resolvable target. If "current work" cannot be established from the conversation, Git state or recent commits, show confirmable candidates (uncommitted changes, recent commits, the current branch range) instead of guessing. For an ambiguous name, list matching locations and ask again. Retain the displayed number-to-target mapping across turns.

## 2. Topic selection

Ask for one or more topics after the scope is fixed, or skip when the request already states them:

| Topic | Question direction |
|---|---|
| Language/framework principles | Mechanisms the selected code relies on: object model, concurrency, rendering, state, hooks, transactions |
| Code connections and execution flow | Call relationships, data movement, request-to-screen or entry-to-storage paths |
| Design and architecture | Responsibility split, dependencies, layers, chosen structure versus alternatives |
| Performance and optimization | Bottlenecks, complexity, caching, rendering cost, cost and effect of an improvement |
| Code style and readability | Naming, abstraction, duplication, repository conventions, maintainability |
| Testing, errors and reliability | Edge cases, failure handling, what is verified and how |

Also offer **balanced mix** and **custom topic**. Java and React are examples only; derive questions from the project's actual languages, frameworks and versions. Ask the topic question in its own turn after scope selection unless both were given together; do not ask scope and topic simultaneously on first invocation.

## 3. Question loop

1. Read the selected code plus only the callers, callees, tests, configuration and history needed to explain its connections. Note relevant language/framework versions from build files.
2. Start with a question about current behavior; move to application, alternative comparison and deeper questions as understanding shows. Pick question shapes from [question patterns](references/question-patterns.md).
3. Ask **exactly one question**, cite the code location it concerns, then stop and wait. Never reveal the answer, model answer or next question in the same turn.
4. After an answer, state what is correct, what is missing or wrong, and the explanation tied to concrete `path:line` locations and the underlying principle. Then ask the next single question at an adjusted depth.
5. If the user asks their own question instead of answering, answer it from the code first, then offer to resume the pending question.

Default to open-ended questions. Switch to multiple choice or interview-practice style on request and keep that mode until changed. For design and style questions judge reasoning and trade-offs: accept a valid alternative the code did not choose and say why it also works and what it costs. Do not fail an answer only because it differs from the implementation.

## 4. In-session controls

Recognize natural-language requests, in any language, such as: hint, I don't know, show answer and explanation, easier, deeper, explain with an example, next question, change topic, change scope, switch to multiple choice or interview mode, and stop.

- **Hint:** give one narrowing clue without the answer; escalate on repeated hints.
- **I don't know / show answer:** give the answer and explanation, then ask an easier confirming question.
- **Change topic or scope:** return to that selection stage while keeping already covered items.
- **Stop:** end with a short summary of topics covered, concepts to reinforce, and code locations worth rereading. Do not ask another question.

## 5. Grounding rules

- Distinguish **actual code behavior** (cited), **general technical principle**, and **inferred design intent**; label inference as such.
- For optimization, separate the applied technique from its measured effect. If no measurement exists, say the effect is unmeasured rather than asserting a speedup; point to `coco-performance` for measurement.
- When an explanation depends on a version-specific framework or language behavior, check the project's version and the official documentation when available; state when it could not be checked.
- Stay centered on the selected scope; read outside it only to explain a connection.
- Do not modify files, run state-changing commands or commit during learning. If the user asks for a change, note it and treat it as a separate implementation request (for example through `coco-build`) after leaving the session or with the user's explicit switch.

## Examples

`$coco-askme` in Codex or `/coco-askme` in Claude Code starts with scope selection. `coco-askme quiz me on connections and architecture across the current work` skips both selections. `coco-askme the selected React component, rendering principles from the basics` fixes scope and topic and starts at a foundational level. Use `coco-docs` for written lessons or learning workspaces rather than interactive questioning.
