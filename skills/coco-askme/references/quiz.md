# Quiz procedure

Read the [question patterns](question-patterns.md) when composing a quiz, not on every entry. Ground questions in selected code and the [entrypoint evidence rules](../SKILL.md#evidence-gathering-deep).

1. Start at current behavior, then move through mechanism, application, alternatives and deeper reasoning as answers demonstrate understanding.
2. Ask **exactly one question** with its source location, then stop and wait. Never reveal the answer, model answer or next question in that turn.
3. After the user's answer, briefly identify what is correct and missing, explain from concrete source locations and underlying principles, then ask the next single question at an adjusted depth. Accept valid design alternatives with their trade-offs rather than grading only agreement with the code.
4. If the user asks their own question, answer it first and offer to resume the pending quiz. A detour does not automatically create a new investigation; apply the evidence-gap rule.

Default to open-ended questions. Keep multiple-choice or interview mode when requested. Support hint (one narrowing clue without the answer), easier, deeper, next, change scope/topic and stop. For "I don't know" or "show answer", explain the answer and ask an easier confirming question. On stop, summarize covered topics, concepts to reinforce, useful locations and unverified claims; ask no further question.
