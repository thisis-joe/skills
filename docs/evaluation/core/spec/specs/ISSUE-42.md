# ISSUE-42 v1

## Objective
Users need a CSV representation of the invoices currently visible to their caller. This contract synthesizes the approved [issue](../issue-42.md) and uses the approved Invoice/Visible invoices terminology in [glossary.md](../glossary.md).

## Behavior
Public operation `export_invoices(rows) -> str` returns UTF-8-compatible CSV text for the supplied, already-filtered and sorted invoice rows. Preserve row order; do not fetch, refilter or resort. Columns are exactly invoice_id,total_cents,paid in that order. paid serializes as lowercase true or false. Each invoice remains one logical CSV record, with ordinary CSV quoting for commas/newlines/quotes.

An empty result still has the header. Formula-like text fields receive an apostrophe prefix for spreadsheet safety, as required by the issue; ordinary text keeps its meaning. Numeric total_cents remains numeric text, with no invented currency conversion. The issue does not enumerate an exhaustive formula-like classifier; this draft preserves that accepted term and does not manufacture a broader sanitization rule.

## Scope
Library CSV output only. Preserve on-screen filtering and sorting by consuming the caller's visible rows. No file picker, HTTP endpoint, browser download, email, new UI or persistence behavior is added. Authoritative task progress remains outside this spec.

## Acceptance
- Input invoice_id INV-1, total_cents 1250, paid True produces a record interpreted by stdlib csv.reader as ["INV-1","1250","true"] under the exact header.
- Two rows preserve caller order, including when their IDs would sort differently.
- Empty input produces the header and no data rows.
- False serializes as false. Text with a comma or quote round-trips as one field.
- A formula-like invoice_id such as =SUM(1,2) is read back with a leading apostrophe and remains one text field. The example demonstrates the agreed safety behavior; exhaustive classifier completeness is not established by this fixture.

## Tests
Reuse the already approved public export_invoices(rows)->str seam and Python stdlib csv reader, with literal independent expected cells. It detects order, header, booleans, quoting and the defined safety examples. It does not verify a real spreadsheet application's interpretation or any browser journey. The issue explicitly requires no browser check for this library-only task. Use the standing regression command and conventions in [README.md](../README.md); no command was run because this request only writes the contract and no implementation is provided.

## Open issues
No product decision is reopened by this synthesis. Precision limitation: the input uses “formula-like” without an exhaustive character/classification contract. Preserve the approved safety requirement; a future implementation must not claim exhaustive coverage from the one example. No implementation choices, measured performance promise or new test boundary is silently approved.

Source/version: issue-42.md approved settlement -> ISSUE-42 v1. No external publication or implementation is included.
