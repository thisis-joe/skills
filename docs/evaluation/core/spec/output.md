# Specification result

Updated the existing specs/ISSUE-42.md to v1 from issue-42.md, preserving the approved public export_invoices(rows)->str boundary. No re-interview, implementation, new SPEC file or tracker publication occurred.

The contract captures ordered CSV, exact columns and lowercase booleans, empty-result header, formula-like text safety and preserved caller filtering. The approved library-level test seam catches formatting and cell values; it cannot establish browser/download UI behavior, which is outside this issue. Commands are linked to the standing README rather than a second policy.

No product decision was reopened. The original issue's term “formula-like” is retained; an exhaustive classification is not supplied by the fixture, so exact sanitization-set completeness remains a specification precision limitation rather than an invented accepted rule.
