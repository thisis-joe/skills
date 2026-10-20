# Question patterns

Read when composing the next question. Each pattern names a depth level; move up a level after a solid answer and down after a missed one. Replace placeholders with the actual identifiers and `path:line` locations from the selected scope. Ask one question per turn.

## Depth levels

| Level | Purpose | Shape |
|---|---|---|
| 1. Observe | Confirm what the code does now | "What happens when ...?", "What does this return for ...?" |
| 2. Explain | Connect behavior to its mechanism | "Why does ... happen in this order?", "Which rule makes ... safe?" |
| 3. Apply | Predict behavior under a new condition | "If ... changed to ..., what would break or change?" |
| 4. Compare | Weigh the chosen design against an alternative | "What would you gain or lose by ... instead?" |
| 5. Extend | Design or diagnose beyond the current code | "How would you support ... without breaking ...?" |

## Patterns by topic

### Language/framework principles

- Observe: "When `<state>` changes in `<Component>`, which parts re-render?"
- Explain: "Why does `<annotation/keyword>` make `<method>` behave this way at runtime?"
- Apply: "If this were called from two threads at once, what could go wrong at `<path:line>`?"
- Compare: "What changes if this hook dependency list is removed or emptied?"

### Code connections and execution flow

- Observe: "Starting at `<entry point>`, which function handles the request next?"
- Explain: "Where does `<value>` come from by the time it reaches `<path:line>`?"
- Apply: "If `<API>` returns an error, which layer surfaces it and what does the user see?"
- Order: "Put these steps in execution order: ..." (multiple choice mode only)

### Design and architecture

- Observe: "Which module owns `<responsibility>` here?"
- Explain: "Why might `<logic>` live in `<layer>` rather than `<other layer>`?"
- Compare: "What would merging or splitting `<A>` and `<B>` cost?"
- Extend: "Where would you add `<new feature>` so the dependency direction stays intact?"

### Performance and optimization

- Observe: "What is the complexity of `<loop/query>` in terms of `<n>`?"
- Explain: "What does `<cache/memo/index>` avoid repeating?"
- Evidence: "What measurement would show that this change actually helped?"
- Compare: "When would this optimization cost more than it saves?"

### Code style and readability

- Observe: "What does the name `<identifier>` promise to a reader?"
- Explain: "Which repository convention does this structure follow?"
- Compare: "Would extracting `<block>` into a function help or hurt here, and why?"

### Testing, errors and reliability

- Observe: "Which test covers `<behavior>`, and what does it assert?"
- Explain: "What input would reach the `<catch/else>` branch at `<path:line>`?"
- Apply: "Name one edge case not covered by the current tests."
- Extend: "How would you verify this change without relying only on a unit test?"

## Feedback shape

1. **Correct:** what the answer got right, briefly.
2. **Gap:** what is missing or inaccurate, with the reason.
3. **Explanation:** the mechanism tied to concrete code locations; label any inferred intent.
4. **Next:** one question at the adjusted level, or the pending question after a detour.

For multiple choice, offer 3 to 4 plausible options with one correct answer and explain each distractor after the answer. For interview mode, ask as an interviewer would, allow follow-up probing, and assess structure, accuracy and trade-off reasoning at the end of each answer.

## Session summary on stop

- Topics and questions covered, with the user's level per topic.
- Concepts to reinforce.
- Code locations worth rereading.
- Unmeasured or unverified claims that came up, if any.
