# Git guard threat/control/test matrix
| Boundary/asset | Abuse path | Control | Local evidence and limit |
|---|---|---|---|
| Untrusted model/tool command → Git write/discard | push, hard reset, forced clean/delete, whole-tree discard | literal parser denies documented Git forms, exit 2 with diagnostic; never eval/subprocess the payload | tests.json and frozen-reapply-cases1-2.json cover deny inputs; only synthetic payloads |
| Settings merge → unrelated project behavior | replacing existing hook/config drops another check | append to existing Bash group; preserve env and Write group; rollback copy | saved diff/config assertions and simulated other-hook marker; real runtime unavailable |
| Shell syntax → parser | wrapper, expansion, alias, malformed JSON bypasses simple match | unsupported forms hold with exit 2; known literal flags/quoted paths supported | synthetic wrapper/alias/substitution/malformed cases; arbitrary programs/external aliases remain outside boundary |
| Runtime loader → expected enforcement | missing helper/interpreter or unsupported config version | documented onFailure block, target version check before activation | helper execution passes; target version and actual intercepted runtime call unavailable |

No user secret or dangerous Git operation was executed. Intended Git rights remain governed by real runtime/user authority; this helper cannot grant execution. Residual risk: other tools, custom programs, mutable guard config, pre-existing aliases and unrecognized semantics can bypass a convenience command guard. No unsupported full-shell security claim is made.
