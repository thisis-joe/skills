import ast
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
intake=json.loads((root/'intake.json').read_text())
ast.parse((root/'product.py').read_text())
checks={
 'source_coordinate_present': isinstance(intake.get('source_thread'),str) and bool(intake['source_thread']),
 'ready_text_present': intake.get('verdict_marker') == 'ready',
 'trusted_identity_configured': bool(intake.get('trusted_identity')),
 'tracker_compensation_supported': intake.get('tracker_compensation') is True,
 'control_adapter_configured': bool(intake.get('control_adapter')),
}
missing=[name for name,passed in checks.items() if not passed]
report={
 'status':'blocked' if missing else 'needs-origin-and-ownership-validation',
 'checks':checks,
 'missing_prerequisites':missing,
 'marker_authenticity':'unverified; ready text is not a configured trusted verdict',
 'source_validation':'coordinate syntax only; original parent existence and ownership were not verified',
 'allowed_now':['local read-only source/JSON inspection','local diagnostics and evidence artifacts'],
 'not_authorized_or_unavailable':['UI reproduction without a control adapter and trusted verdict','product edits','source replies or tracker writes','webhook delivery or external calls','PR, merge, deployment, activation or schedules'],
 'effect_observation':'This checker only reads local files and prints diagnostics; it invokes no product code or adapters.',
 'snapshot':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['intake.json','product.py']},
}
print(json.dumps(report,indent=2))
raise SystemExit(2 if missing else 3)
