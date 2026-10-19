# Resolved integration decisions

| Rule tension | COCO decision | Reason |
|---|---|---|
| Matt red→green, Addy red→green→refactor | Observe a red behavior test, implement minimal green, permit small local naming/duplication cleanup only after green and recheck; structural changes are separate scoped work | Preserve rapid behavioral feedback and prevent scope expansion |
| Matt synthesis only, Addy interview before spec | Read existing agreement first; synthesize it, question missing material decisions only | Keep one requirements agreement |
| TDD versus code-first increment prose | TDD governs behavior changes inside the execution increment; static/no-behavior edits use appropriate direct checks | Distinguish implementation technique from work scheduling |
| Many approval checkpoints versus auto build | Reuse the user's approved scope and chosen execution mode; material new decisions and runtime-required authorization remain boundaries | Consistent progress without manufacturing consent |
| Base...HEAD review versus review before commit | Freeze the task's actual committed/index/worktree/untracked scope; review before the work-unit commit | Prevent omitted new code and premature completion |
| Separate axes versus one ranked finding list | Keep spec, standards and quality verdicts distinct; one actionable finding can link multiple axes | Do not let one passing axis hide a failure or duplicate identical fixes |
| Every increment green versus wide migration integration exceptions | Prefer expand–contract and green batches; if impossible, explicitly label an integration-only branch, ban normal done/ship claims for red intermediate work, and require final integrated checks | Preserve necessary migration capability without pretending intermediate safety |
| Repeated full tests versus efficient checks | Focused loop, project-required closure checks, evidence reuse only for unchanged relevant state | Avoid duplicate runs without reducing verification scope |
| Fixed file counts/test ratios/default metrics | Treat source numbers as starting heuristics, not universal policy; record actual project thresholds and enforce them | Match existing codebases and keep the quality bar explicit |
| Always multiple models/agents versus available runtime | Use independent review when needed and authorized, label unavailable/degraded evidence; no hardcoded models or nested agent trees | Preserve independent reasoning without platform lock-in |
| Cursor setup, transcript globbing and automatic source actions | Replace with supported tools and task-scoped artifacts; no original pstack invocation, private-history sweep, auto-publication or permission expansion | Honor no-Cursor scope and existing user authority |
| Prototype, experimental and niche tools | Explicit opt-in conditional modes, disposable artifacts, primary-source facts, normal checks before adopting production code | Preserve capabilities without making them default workflow |

Every source skill/command is accounted for in `sources/coverage.json` in the repository. That file records the original essential rules and adaptation rationale. The active procedures here are authoritative for COCO; original directives are not reloaded at runtime.
