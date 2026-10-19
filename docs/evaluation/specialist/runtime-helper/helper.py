"""Cold-reader scaffold; cannot certify the intentionally unreachable UI baseline."""
import json
from pathlib import Path
import subprocess
import sys

base = Path(__file__).resolve().parent
proof = base.parent / 'evidence' / 'runtime-helper'
proof.mkdir(parents=True, exist_ok=True)
action = sys.argv[1]
code = 0
if action == 'launch':
    result = subprocess.run([sys.executable, str(base/'launch.py')], capture_output=True, text=True)
    data = {'action':action,'exit':result.returncode,'stdout':result.stdout.strip(),'instance_created':False}
    code = result.returncode
elif action == 'doctor':
    data = {'action':action,'target':'scratch-expense-ui-v2','ready':False,
            'required_fixture_exists':(base/'fixture-state.json').exists(),
            'owned_process_exists':False,'driver_available':False,'auth_checked':False}
    code = 2
elif action == 'drive':
    data = {'action':action,'feature':'expense.create','status':'unavailable',
            'reason':'launch never established a usable instance; no browser driver',
            'actions_executed':[],'route':'/expenses/new'}
    code = 2
elif action == 'capture':
    data = {'action':action,'status':'unavailable','screenshot':None,
            'reason':'no rendered target; failed launch/doctor evidence retained'}
    code = 2
elif action == 'cleanup':
    data = {'action':action,'removed_owned_processes':0,'removed_scratch_records':0,'proof_retained':True}
elif action == 'check-evidence':
    paths = [proof/f'{name}.json' for name in ['launch','doctor','drive','capture','cleanup']]
    data = {'action':action,'all_receipts_exist':all(p.exists() for p in paths),
            'proof_paths':[str(p) for p in paths], 'journey_verified':False}
else:
    raise SystemExit('unknown helper action')
(proof/f'{action}.json').write_text(json.dumps(data, indent=2)+'\n')
print(json.dumps(data, sort_keys=True))
raise SystemExit(code)
