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

1. Discover the actual field, accepted formats and size limit, image destination and naming rule, and how layouts crop the image (aspect ratios, `object-fit`, smallest rendered size). Read the consumer's image/brand guide for approved characters, reference assets, palette and visual language. Keep project character names and asset locations in that guide, not in this reusable skill. If no guide exists, reuse the author's confirmed references; do not invent project mascots or search private photo collections.
2. Before proposing or generating concepts, ask whether to use the project's approved characters. Name the available characters and offer each individually, both when applicable, no character, and a recommendation. Reuse an already settled choice instead of asking again. If no characters are known, offer the ordinary concept route without blocking on a mascot. When asked for a recommendation, explain suitability and let the author select before generation. If a character seems unsuitable for the article, briefly explain why and offer a character-free alternative; the author retains the choice. Declining characters does not mean declining the thumbnail itself.
3. For a selected character, inspect its approved reference and preserve identifying appearance, clothing, markings and proportions. Use only the selected character(s); do not substitute, redesign or add another mascot silently. Ask for the reference if unavailable rather than inventing its appearance. Propose two or three scenes tied to the post's actual takeaway, describing the character's action, composition, background and minimal props. For the no-character route, propose technical concepts, tools or problem-solving scenes with the same editorial care. Agree on a direction before drawing; reuse composition and palette decisions already given.
4. Create candidate images using the runtime's supported image-generation/editing tool when appropriate, or local vector/raster tools for code-native art. Follow applicable tool instructions and the project's asset policy; use author-approved reference assets and confirm applicable usage rights rather than assuming every supplied or generated image has a license. Never expose private screens, hosts, credentials or incidental people from reference photos. Show rendered candidates in the conversation, not just prompts.
5. Invite focused feedback on composition, expression, props and background. Revise the selected candidate through the available image tool until the author accepts it or chooses to stop. Preserve settled character and visual decisions across revisions; do not regenerate unrelated alternatives or treat choosing a concept as acceptance of the final image.
6. Keep the key motif inside the area that survives every crop and large enough to read at the smallest rendered size. Preview the selected image in the site's real list/recommendation/detail layouts where present, at desktop and mobile widths, using a disposable copy outside the source tree with a local image path. Never commit that copy or path. Show any crop/readability issue and revise with the author before final acceptance. If preview or generation tooling is unavailable, say which step remains unverified; a prompt or mockup is not a rendered/verified final image. Export the accepted image to the project's format and size limit.
7. Upload only to the project's documented destination with the author's authorization for that upload, and say first if that destination is public before the post is released. When the destination is inside the content repository, that authorization covers staging the image file with the post. Confirm the public URL loads the same file, then reference it from the post metadata. Character selection, candidate acceptance and local previews are not upload or publication permission.

## Collaborate and review

Establish reader prerequisites and useful takeaway, read the selected source, and write separately using the actual schema and draft state. Preserve author voice without exposing private session narrative or internal links.

Ask for facts that change the story; continue supported portions while answers are pending. Offer alternative openings only when they represent a meaningful choice, and retain existing user selections.

The actual contributor confirms facts and public suitability. Check prose, metadata, diagrams, code, images, linked destinations and third-party rights. Redact secrets without echoing them. Pattern scans or a preview prove specific checks, not universal privacy, factual or licensing clearance.

Reread live posts before revising. If an importer reports local changes or a published article, compare and reconcile instead of forcing a reset. Maintain existing public URLs unless changing them is explicitly in scope.
