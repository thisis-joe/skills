from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
text=(root/'WORKFLOW.md').read_text()
checks={
 'notes_preserved': (root/'NOTES.md').read_text() == 'Wanted artifact: a workflow specification for bug intake and a server-side webhook. No activation, scheduling, network requests or messages are authorized. Source and adapter identities are undecided.\n',
 'authority_and_open_decisions': all(s in text for s in ['prepared specification only','Source and destination','Trusted triage identity','fail closed']),
 'stable_stages': all('| '+str(i)+'.' in text for i in range(8)),
 'retry_and_recovery': all(s in text for s in ['atomic transaction','Unknown','before retry','three','compensation']),
 'server_credential_boundary': all(s in text for s in ['server-side','secret facility','browser code','authenticated']),
 'activation_and_runtime_limits': all(s in text for s in ['## Next implementation boundary','Only\nlocal document completeness checks were run','no workflow behavior']),
}
print(json.dumps({'check_type':'static document completeness, not workflow execution','checks':checks},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
