"""Fixture baseline startup. No app starts when its required state is missing."""
import json
from pathlib import Path
import sys

base = Path(__file__).resolve().parent
required = base / 'fixture-state.json'
if not required.exists():
    print(json.dumps({'state':'blocked','required':str(required),'reason':'baseline fixture-state is absent; server not started'}))
    sys.exit(2)
print(json.dumps({'state':'blocked','reason':'fixture startup contains no UI server; production baseline unavailable'}))
sys.exit(2)
