# Mailing-list form acceptance: incomplete

Target: `fixtures/form.html`, desktop source width 960px. Job: submit one email and receive the server's actual subscription result. Primary action: Subscribe. The referenced happy-path desktop screenshot has no local image file in this evaluation, and no browser driver is available. An associated label exists in source; this is not live accessibility proof. The source has no async status announcement and fixed width merits a narrow-layout check.

| State / interaction | Required user observation | Concrete next check |
|---|---|---|
| Initial/empty | Email label, requirement, visible focus; useful instruction | Open isolated test app at `/subscriptions/new`; inspect label/heading/page language |
| Loading | Status announced, duplicate submit prevented, entered email retained | Delay authorized fixture POST response; activate Subscribe twice; observe one request and `Submitting…` |
| Validation failure | Specific associated error, focus at first invalid input | Submit empty and malformed address with keyboard; verify server validation and error association |
| Server/network failure | Human-readable error with retry; no false success | Make test adapter return 500 and disconnect; retry after restoring; confirm retained input and actual request result |
| Success | Visible/announced result agrees with API; saved result independently read back | Submit `learner@example.test`; inspect response and fixture subscription readback |
| Permission/rate policy | Explain blocked action without leaking account details | Exercise configured 401/429 fixture states; do not infer policy absent contract |
| Keyboard | Tab order, visible focus, Enter activation; no trap | Use only Tab/Shift+Tab/Enter from page start through retry/success |
| Mobile/resizing | No horizontal overflow, usable touch targets, readable errors | Render 320px, 768px and 1280px; long email/error text; zoom 200%; capture actual screenshots |

Runtime evidence still required: reload exact target snapshot; compare normal/error/loading screenshots at widths, actual DOM/computed contrast, console/network, focus and persistence. Contrast needs actual colors/rendering; a source label cannot certify it. When browser access returns, run these steps with an isolated fixture account, reset subscription data and retain result receipts after cleanup.

Acceptance states: source-label check passed; loading/error/success/permission/keyboard/mobile rendering and console/network checks **unavailable**. Do not mark the UI complete from the desktop screenshot or the local unit suite. No product implementation or accessibility certification occurred.
