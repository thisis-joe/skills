from pathlib import Path
import hashlib,json,subprocess,os,sys
ROOT=Path(__file__).parent
SOURCE=Path('/Users/Joseph/workspaces/skills')
FILES=['skills/coco-push/SKILL.md','skills/_coco-shared/contracts.md','skills/coco-push/references/sync-and-push.md','skills/coco-push/references/branch-and-ticket.md','skills/coco-build/SKILL.md']
hashes={}
for f in FILES:
    b=(SOURCE/f).read_bytes(); hashes[f]=hashlib.sha256(b).hexdigest()
    p=ROOT/'skill-snapshot'/f; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)

if not (ROOT/'skill-hashes-before.json').exists():
    (ROOT/'skill-hashes-before.json').write_text(json.dumps(hashes,indent=2)+'\n')
SETUP=ROOT/'setup-commands.jsonl'
def run(cwd,*args):
    r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    with SETUP.open('a') as fp: fp.write(json.dumps({'cwd':str(cwd),'argv':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr},ensure_ascii=False)+'\n')
    if r.returncode: raise RuntimeError(args,r.stdout,r.stderr)
    return r.stdout.strip()
def put(base,path,text):
    p=base/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def commit(repo,msg):
    run(repo,'git','add','--all');run(repo,'git','commit','-m',msg);return run(repo,'git','rev-parse','HEAD')
def config(repo):
    run(repo,'git','config','user.name','Local Fixture'); run(repo,'git','config','user.email','fixture@example.invalid');run(repo,'git','config','commit.gpgsign','false')
TOKEN_BASE='''def expired(now, expires_at):
    return now >= expires_at
'''
TOKEN_IMPL=TOKEN_BASE+'''
class TokenFamily:
    def __init__(self):
        self.current = "token-0"
        self.used = set()
        self.revoked = False
        self.sequence = 0

    def rotate(self, supplied):
        if supplied in self.used:
            self.revoked = True
            raise ValueError("reused token")
        if self.revoked or supplied != self.current:
            raise ValueError("invalid token")
        self.used.add(supplied)
        self.sequence += 1
        self.current = f"token-{self.sequence}"
        return self.current
'''
TOKEN_TEST='''import unittest
from src.tokens import expired, TokenFamily

class TokenBehavior(unittest.TestCase):
    def test_expiry_boundary(self):
        self.assertFalse(expired(9, 10))
        self.assertTrue(expired(10, 10))
    def test_rotation_returns_fresh_token(self):
        family = TokenFamily()
        next_token = family.rotate("token-0")
        self.assertNotEqual(next_token, "token-0")
        self.assertNotEqual(family.rotate(next_token), next_token)
    def test_reuse_revokes_family(self):
        family = TokenFamily()
        next_token = family.rotate("token-0")
        with self.assertRaisesRegex(ValueError, "reused"):
            family.rotate("token-0")
        with self.assertRaisesRegex(ValueError, "invalid"):
            family.rotate(next_token)
'''
CSV_IMPL='''import csv
import io

def export_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["name", "note"])
    writer.writerows(rows)
    return output.getvalue()
'''
CSV_TEST='''import csv
import io
import unittest
from src.exporter import export_csv

class ExportBehavior(unittest.TestCase):
    def test_quoted_unicode_round_trip(self):
        rows = [["홍길동", 'hello, "world"'], ["Ada", "line1\\nline2"]]
        self.assertEqual(list(csv.reader(io.StringIO(export_csv(rows)))), [["name", "note"], *rows])
    def test_empty_output_still_has_header(self):
        self.assertEqual(list(csv.reader(io.StringIO(export_csv([])))), [["name", "note"]])
'''
CASES=[('scope_drift','431','토큰_만료설정','TEAM-431'),('adequate_summary','432','CSV_내보내기','TEAM-432'),('jira_write_failure','433','토큰_만료설정','TEAM-433'),('ambiguous_project','434','토큰_만료설정',None),('unrelated_collision','435','토큰_만료설정','TEAM-435')]
manifest={}
for name,number,summary,key in CASES:
    base=ROOT/name; base.mkdir(); remote=base/'origin.git'; repo=base/'work'; peer=base/'peer'
    run(base,'git','init','--bare',str(remote));run(base,'git','init','-b','develop',str(repo));config(repo)
    put(repo,'AGENTS.md','# Local fixture rules\n\nBase is origin/develop. Required check: python3 -m unittest discover -s tests -v. Feature branches and work-unit commits are required. Publish the current task branch to origin.\n')
    put(repo,'src/__init__.py','');put(repo,'tests/__init__.py','');put(repo,'README.md','Local isolated token/export fixture.\n')
    put(repo,'.gitignore','__pycache__/\n')
    if name=='adequate_summary':
        put(repo,'src/csv_contract.py','CSV_HEADER = (\"name\", \"note\")\n')
    else:
        put(repo,'src/tokens.py',TOKEN_BASE);put(repo,'tests/test_expiry.py','import unittest\nfrom src.tokens import expired\nclass Expiry(unittest.TestCase):\n    def test_expired(self):\n        self.assertTrue(expired(10, 10))\n')
    initial=commit(repo,'chore: initial fixture base')
    run(repo,'git','remote','add','origin',str(remote));run(repo,'git','push','-u','origin','develop')
    old=f'feat(be)/{number}-{summary}';new=old if name=='adequate_summary' else f'feat(be)/{number}-토큰_회전과_재사용차단'
    run(repo,'git','switch','-c',old)
    if name=='adequate_summary':
        put(repo,'src/exporter.py',CSV_IMPL);put(repo,'tests/test_export.py',CSV_TEST)
        put(repo,'README.md','CSV export preserves Korean text, commas, quotes, and embedded newlines.\n')
    else:
        put(repo,'src/tokens.py',TOKEN_IMPL);put(repo,'tests/test_tokens.py',TOKEN_TEST)
    work=commit(repo,'feat: implement task acceptance behavior')
    run(repo,'git','push','-u','origin',f'{old}:refs/heads/{old}')
    requirements=['Existing expiry boundary stays unchanged.','Rotate returns a new refresh token.','Reusing an old refresh token revokes its token family.','Follow-up: per-device selective revoke UI remains unimplemented.']
    acceptance=['At expiration time the token is rejected.','A valid refresh token rotates twice successfully.','Reusing the prior token blocks the entire family.']
    if name=='adequate_summary':
        requirements=['Export records to CSV including commas, quotes, Unicode, and newlines.','PDF export is outside this task.'];acceptance=['Unicode and quoted cells round-trip.','Empty export has a header.']
    desc='Original requirements\n'+'\n'.join('- '+s for s in requirements)+'\n\nAcceptance criteria\n'+'\n'.join('- '+s for s in acceptance)+'\n\nReference: https://example.invalid/spec/'+number+'\nPeer note (Mina): retain expiry API contract.\n'
    task={'key':key or 'TEAM-'+number,'project':'TEAM','summary':summary,'description':desc,'status':'In Progress','assignee':'mina','priority':'High','version':1}
    tasks={task['key']:task}
    if name=='ambiguous_project':
        tasks['OPS-'+number]={'key':'OPS-'+number,'project':'OPS','summary':summary,'description':'Operations token expiry maintenance. Independent issue with the same numeric id.','status':'To Do','assignee':'ops','priority':'Low','version':4}
    adapter=base/'jira';adapter.mkdir();(adapter/'tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2)+'\n');(adapter/'config.json').write_text(json.dumps({'label':'LOCAL MOCK JIRA - NO EXTERNAL API','reject_updates':name=='jira_write_failure'})+'\n')
    request={'request':'Apply $coco-push to publish this fixture branch, including required branch/ticket alignment. Use origin/develop, preserve existing requirements and acceptance criteria, and use the local mock Jira adapter. This authorizes in-scope synchronization, branch rename, Summary/Description edits, and ordinary push; do not ask again. Stop and record any genuinely missing decision.','jira_key':key,'branch':old,'implementation_source':{'requirements':requirements,'acceptance_criteria':acceptance,'scope_note':'Requirements above are the settled authorized work. Unimplemented follow-up remains visible.'},'jira_adapter':str(adapter),'expected_kind_part':'feat(be)','check':['python3','-m','unittest','discover','-s','tests','-v']}
    (base/'request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n')
    # A second checkout advances develop after the local branch diverges.
    run(base,'git','clone','-b','develop',str(remote),str(peer));config(peer)
    put(peer,'src/platform.py','def default_timeout():\n    return 30\n');put(peer,'tests/test_platform.py','import unittest\nfrom src.platform import default_timeout\nclass Platform(unittest.TestCase):\n    def test_default_timeout(self):\n        self.assertEqual(default_timeout(), 30)\n')
    develop=commit(peer,'feat: shared platform timeout');run(peer,'git','push','origin','HEAD:refs/heads/develop')
    peer_oid=None;collision_oid=None
    if name=='scope_drift':
        run(peer,'git','switch','-c',old,'origin/'+old)
        put(peer,'src/audit.py','def event_name():\n    return "refresh-token-rotated"\n');put(peer,'tests/test_audit.py','import unittest\nfrom src.audit import event_name\nclass Audit(unittest.TestCase):\n    def test_rotation_audit_contract(self):\n        self.assertEqual(event_name(), "refresh-token-rotated")\n')
        peer_oid=commit(peer,'feat: retain peer token rotation audit event');run(peer,'git','push','origin',f'HEAD:refs/heads/{old}')
    if name=='unrelated_collision':
        run(peer,'git','switch','-c',new,'origin/develop')
        put(peer,'TASK.md','Jira issue: OPS-435\nUnrelated operations task. Numeric id collides across Jira projects.\n')
        collision_oid=commit(peer,'ops: unrelated OPS-435 work');run(peer,'git','push','origin',f'HEAD:refs/heads/{new}');run(repo,'git','fetch','origin',f'refs/heads/{new}:refs/heads/{new}')
    manifest[name]={'repo':str(repo),'remote':str(remote),'old_branch':old,'candidate_branch':new,'task_key':key,'initial':initial,'work':work,'base_develop':develop,'peer_commit':peer_oid,'collision_commit':collision_oid}
    (base/'before-refs.txt').write_text(run(repo,'git','show-ref')+'\nREMOTE\n'+run(repo,'git','ls-remote','--heads','origin')+'\n')
    (base/'before-task.json').write_bytes((adapter/'tasks.json').read_bytes())
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(ROOT)
print(json.dumps({name:{'branch':m['old_branch'],'work':m['work'],'develop':m['base_develop']} for name,m in manifest.items()},ensure_ascii=False,indent=2))
