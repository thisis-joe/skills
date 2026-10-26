# Full comparison recovery: blocked by native service capacity

**No valid matched pair completed. The F4 comparison and operational adoption
gate remain unmet.** This recovery provides no candidate quality, superiority,
no-regression, speed or human-effort conclusion. It does not authorize merge or
publication. The retained blind packet is ungraded.

The fixed comparison was current `622975e349e6276b225aa9ef02ee69d664dd2927`
against candidate `42f6c58ed8b6f271b26ac029b0b691c00c0f03af`, which includes
the emerging-constraint guard from `1250ffd`. Release compatibility with
`84a59a2` remains a separate assessment. Neither recovery attempt replaces,
resumes, pools or regrades the historical `17e3425` partial cohort.

## Actual execution

Each prospective cohort prepared the same five current/candidate policy pairs
and two candidate-only preservation probes. A preparation is not an observation.

| Item | Recovery attempt 1 | Recovery revision 2 |
| --- | ---: | ---: |
| Prepared disposable projects | 12 | 12 |
| Projects admitted | 2: current 0, candidate 0 | 1: current 0 |
| Projects not admitted | 10 | 11 |
| Product actor calls | 2 | 3 |
| Owner-classifier calls during projects | 2 | 2 |
| Availability / sensitivity control calls | 4 | 1 |
| All actual native calls | 8 | 6 |
| Stable completed trials | 0 | 0 |
| Valid matched pairs | 0 | 0 |

The fourteen calls are an all-attempt operational count, not a pooled sample.
The two preservation probes were not attempted in either cohort. All native
calls used the same CLI engine and default model without overrides. Actor calls
retained the 420-second limit; classifier calls retained 90 seconds. No budget
was enlarged, no failed actor was resumed, and no development actor or owner
classifier was replaced by a collaboration agent or manual answer.

Attempt 1's two actor turns completed and only asked questions. Both project
states remained identical to their initial checkpoint, both public observers
reported unimplemented behavior, and both range observations returned empty
output and failed. Their owner classifiers encountered HTTP 429; one reached
its 90-second cap and the other was cooperatively interrupted. No owner answer
or oracle feedback reached either actor. The remaining ten projects were not
admitted. These are unavailable preimplementation records, not paired results.

After the provider cooldown, revision 2's single availability control passed
in 6.445 seconds. One current project then completed two actor turns and two
owner classifications. Its ordinary owner reply and bounded corrective reply
were actually delivered. The third actor call encountered another HTTP 429,
was cooperatively stopped, and emitted no command or final response. It was
not counted as a completed repair. No candidate actor ran in revision 2; the
other eleven prepared projects were not admitted. The partial product evidence
is preserved without assigning quality grades or a comparative interpretation.

## Instrument defect and prospective repair

An independent read-only reviewer found that attempt 1's range oracle used
Python list equality. A mixed response could emit the first large value as
`9.223372036854776e18`, retain the larger value as an integer, and still compare
equal after ordinary JSON parsing. That exponent denotes 192 cents more than
the expected `9223372036854775808`. This was a material oracle defect.

Attempt 1 was sealed before repair, including all nine original frozen files.
No accepting range observation or related actor feedback had occurred. The
repair lives in the separate [revision 2 runner](revision2/run.py); the original
recovery runner, protocol and tests remain unchanged. Revision 2 requires every
returned price to have exact integer type as well as full expected-list equality.

Before revision 2 actors, [instrument tests](revision2/test_instrument.py) passed
for all five profiles: the independent reference passed, an added price ceiling
failed, the mixed float/integer output failed despite satisfying the old equality
check, and restoration passed. Owner-range routing withheld unasked private
facts, and the unknown-choice fixture stayed unresolved. Three tests passed in
8.909 seconds. The reviewer then confirmed the known strict-type fix and negative
control read-only before primary dispatch. These are instrument checks, not
evidence that candidate skill users performed better.

Revision 2 reused the three passing native classifier controls with exact-byte
provenance because their prompt, topics, owner facts and engine were unchanged.
It also ran the one fresh range-classification availability control. Both source
manifests and ten frozen protocol/runner/dependency hashes were verified before
dispatch and remained unchanged at collection.

## Capacity, pacing and cleanup

Attempt 1's candidate owner call received HTTP 429 at
`2026-10-26T10:12:42.727272Z` with a 513.999589959-second retry delay. The current
owner call received the same error at `10:12:49.784965Z` with 506.999844167 seconds.
The next check was eligible after `10:21:17Z`; the actual revision 2 availability
call began after `10:24:15Z`. Earlier successful controls were not treated as a
guarantee that the full study could finish.

Revision 2 admitted only one project and enforced at least 30 seconds between
native call starts, retaining actual pacing receipts. Its third actor call still
received HTTP 429 at `10:28:40.338534Z`, requesting another 340.999900833 seconds.
The cooperative stop was recorded at `10:28:56.512110Z`. No further availability
check, cohort or actor run was scheduled. Because the recurrence occurred in a
development actor, the failure was not confined to owner-classifier calls.

The interrupted leader, PID 79747, exited after the accepted SIGINT; its owned
process group was absent. All six revision 2 native PIDs were subsequently
absent, and the driver returned exit 0 after recording the stopped queue. The
four attempt 1 project-call PIDs were also absent before retry. Descendant cleanup
remains separately unverified as recorded by the native engine. Revision 2's
post-stop project state exactly matched its last completed checkpoint; it was
not resumed or assigned a synthetic successful exit.

Attempt 1's eight native calls sum to 264.119 seconds. Revision 2's six calls sum
to 203.324 seconds, including the availability control; its primary wall interval
was 245.379 seconds and recorded admission pacing totaled 47.586 seconds. Native
duration sums are not wall time, especially for attempt 1's overlapping calls.
Preparation, analysis and archive work are outside these primary intervals.
Actual token records remain per call; missing completion usage is unavailable,
not zero. None of these costs establishes a speed benefit or a complete-run cost.

## Retained evidence and release consequence

All archive entries were reread without extraction and checked against their
exact byte hashes and file modes. The original historical native and blind
archives were not changed.

| Archive | SHA-256 |
| --- | --- |
| [Attempt 1, including frozen original instrument](evidence/recovery-attempt1-preimplementation.tar.gz) | `81b53376ff0e61656a23268d2bd410ae8da9a7823cab27d513742c6e62b3334d` |
| [Revision 2 native evidence and repaired frozen inputs](evidence/recovery-revision2-native.tar.gz) | `c51337e7e4a82e78ad3834b1642f185d62f9c4d542612c33af9e1f3a8e955396` |
| [Revision 2 blind packet, ungraded](evidence/recovery-revision2-blind-ungraded.tar.gz) | `579b503c7282d0e255dc2546f7a0fb1f3b8e317eea36c48bec18182e4d1d13e2` |

Adjacent manifest files contain every retained file hash and mode. The
[shutdown and cost receipt](evidence/recovery-revision2-shutdown-and-costs.json)
retains exact calls, exits, PIDs and available usage. The blind packet contains
one partial project, eleven explicitly unattempted projects and two false-
completion controls. Its bytes and modes match the frozen packet manifest.
`collect.py validate` was not run because no grades exist; the
[packet integrity receipt](evidence/recovery-revision2-packet-integrity.json)
states this distinction. The collection-only adapter preserves the new public
range contract and passed its local wrong-output and missing-browser checks.

The required five-pair comparison is externally blocked. Source validation,
package checks or an isolated fixture cannot stand in for these missing paired
observations. Operational adoption, merge and publication therefore remain
pending under the existing gate. Finishing the comparison would require an
explicitly recorded future operational plan after native capacity is available;
this report does not authorize another retry or continuation of stopped projects.
