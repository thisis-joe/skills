# Refund policy: two decisions to settle

Settled behavior remains: support approves a refund for a captured payment, funds return to the original payment method, store credit is excluded, and cumulative refunds cannot exceed captured money. “Refund”, “Return” and “Shipping charge” retain their approved glossary meanings. No glossary or ADR was changed.

Both decisions below are ready now and independent; answering either does not require the other.

| Decision | Alternatives | Recommendation for discussion and consequence |
|---|---|---|
| Eligibility window after delivery | 14, 30 or 60 calendar days | Recommend 30 days as the middle option in this supplied range; 14 narrows access and 60 extends the support period. This is a proposed choice, not an approved requirement. |
| Include the separately itemized outbound shipping charge? | Exclude it, or refund it with the captured item amount | Recommend excluding it for a clearly itemized item-only policy; including it returns more money per eligible claim. No existing policy or legal requirement is inferred. |

Ready questions: Which eligibility window should apply (14/30/60 calendar days)? Should the separately itemized shipping charge be included?

Draft acceptance once W and shipping choice S are settled: a request within W days can enter support approval; a request beyond W follows the chosen ineligible outcome rather than being automatically paid; payout goes to the original method; payout amount follows S and never exceeds unrefunded captured money. The selected W and shipping choice S will fill this policy draft; neither is treated as approved by this evaluation.

Scope remains policy clarification only. The two choices remain explicitly open, so there is no claim of a settled implementation contract and no automatic spec publication or build. Inputs and unchanged glossary are recorded in evidence/inputs-read.json.
