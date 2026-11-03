# Select and shape evidence-backed posts

Read for candidates, drafts and substantive revisions. The consumer project's editorial agreement takes precedence over these starting points.

## Candidates and publication

Collect work worth revisiting, a choice the team values, or an experience useful to another developer. Completed features, design, prevention, automation, failed experiments, troubleshooting and improvements qualify. Do not require a dramatic incident, minimum improvement percentage or fixed length.

For publication, make first-hand work concrete, explain reasons for consequential choices and provide meaningful support. Measurements, observed behavior, before/after screens, diagrams, tests and attributable feedback are all evidence. Say what they establish and leave open. Test counts alone do not establish product performance or user value.

For each candidate return source, reader/takeaway, possible angle, existing support and essential gaps. A recommendation is not author approval.

## Category, tags and angle

Reuse actual category/tag names, display labels and cardinality. Related fields and multiple tags may be useful; do not invent metadata unsupported by the importer/renderer. The field does not dictate the article's shape.

| Work area | Reader-facing emphasis |
| --- | --- |
| Data | Collection, annotation, quality criteria and observed error patterns |
| AI | Hypothesis, baseline, evaluation conditions, error analysis and limits |
| Infrastructure | Operational constraints, delivery, observation and recovery choices |
| Frontend | User task, interaction/state choices, accessibility or observed behavior |
| Backend | Domain rules, API/data consistency, failures and verification |

Choose an accomplishment, troubleshooting story, experiment/comparison, design decision, guide or retrospective. Accomplishments can follow need → choices → completed behavior → supported effect → remaining work. Troubleshooting can follow reproduction → hypotheses/checks → supported cause → fix/regression check. Experiments need comparable conditions and interpretation. Adapt to the material instead of imposing all these sections on every post.

## Ground claims before polishing

- Distinguish implementation, observation, inferred benefit and unverified hypothesis.
- For numerical claims retain relevant code/data version, method, sample/denominator, repetitions or variation, environment and comparison conditions.
- Give absolute before/after values and units before relative improvements. Distinguish percentage points from relative percentages. Include regressions, costs and limitations that affect the conclusion.
- Do not infer causation from uncontrolled comparisons. A simpler architecture or cache is a design change until its effects are measured or observed.
- Ask for essential facts, qualify unmeasured/unverified effects, or omit unsupported claims with the author. Never manufacture a metric, quotation, benchmark run or design rationale.

## Cover images

When the consumer project renders post thumbnails or cover images, offer to choose or draw one with the author after the manuscript direction is accepted. Skip this when the project has no such field or the author declines; adding thumbnail support to the site is separate implementation work.

- Discover the actual field, accepted formats and size limit, image destination and naming rule, and how layouts crop the image (aspect ratios, `object-fit`, smallest rendered size). Reuse the project's palette and visual language from its documents or stylesheet.
- Propose two or three distinct concepts tied to the post's takeaway and the product's own motifs. Draw them as vector art and render rasters with available local tools; do not use stock, generated or third-party images without a confirmed license, and never show private screens, hosts or credentials.
- Keep the key motif inside the area that survives every crop and large enough to read at the smallest rendered size. Show each candidate as a rendered image in the conversation. Preview the selected one in the site's real layouts at desktop and mobile widths by building a disposable copy outside the source tree with a local image path, never committing that copy or path; revise from what the preview shows.
- The author chooses, asks for changes, or supplies an own image, which follows the same checks. Export to the project's format and size limit.
- Upload only to the project's documented destination with the author's authorization for that upload, and say first if that destination is public before the post is released. When the destination is inside the content repository, that authorization covers staging the image file with the post. Confirm the public URL loads the same file, then reference it from the post metadata. A candidate or local preview is not a published image.

## Collaborate and review

Establish reader prerequisites and useful takeaway, read the selected source, and write separately using the actual schema and draft state. Preserve author voice without exposing private session narrative or internal links.

Ask for facts that change the story; continue supported portions while answers are pending. Offer alternative openings only when they represent a meaningful choice, and retain existing user selections.

The actual contributor confirms facts and public suitability. Check prose, metadata, diagrams, code, images, linked destinations and third-party rights. Redact secrets without echoing them. Pattern scans or a preview prove specific checks, not universal privacy, factual or licensing clearance.

Reread live posts before revising. If an importer reports local changes or a published article, compare and reconcile instead of forcing a reset. Maintain existing public URLs unless changing them is explicitly in scope.
