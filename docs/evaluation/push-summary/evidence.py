"""Command recorder; no skill decisions or canned expected outcomes."""
from pathlib import Path
import subprocess,json,datetime
ROOT=Path(__file__).parent
MANIFEST=json.loads((ROOT/'manifest.json').read_text())
def run(case,*argv,check=True):
    repo=Path(MANIFEST[case]['repo'])
    r=subprocess.run(argv,cwd=repo,text=True,capture_output=True)
    item={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cwd':str(repo),'argv':list(argv),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    with (ROOT/case/'commands.jsonl').open('a') as fp: fp.write(json.dumps(item,ensure_ascii=False)+'\n')
    print('$ '+' '.join(repr(a) for a in argv)+'\n'+r.stdout+r.stderr+'[exit '+str(r.returncode)+']')
    if check and r.returncode: raise RuntimeError('Recorded command failed')
    return r

def decide(case,decision,evidence,question=None):
    item={'decision':decision,'evidence':evidence,'question':question,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with (ROOT/case/'decisions.jsonl').open('a') as fp: fp.write(json.dumps(item,ensure_ascii=False)+'\n')
    print(json.dumps(item,ensure_ascii=False,indent=2))
