"""Real handoff fixtures and public outcomes, independent of skill file names."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'collaboration-value'))
import lifecycle

PROFILES = lifecycle.PROFILES
git = lifecycle.git
call = lifecycle.call

AUTH = '''Work only in this project. Read its files and existing code. If .guide exists,
use those local procedures. Do not read personal/global skill bodies, other
projects, source archives, parent directories or experiment-control files. Use
only local shell/files, Python stdlib, Git and actual CLI checks. No nested
agents, installs, external services, publishing or global changes. Preserve
unrelated work. There is no Jira; use descriptive feature branches and work-unit
commits. For this feature basic technical progress is explicitly automatic,
through implementation, checks and commits, stopping before push. Separate
specialist examinations are declined. Disclosed same-agent inspection is accepted
in this temporary project; it is not independent review. Product choices remain
with the owner. Report actual resulting state and unresolved decisions truthfully.
'''

BRIEF = '''# Purchasing catalog
Add `import PATH` and `summary` to the existing catalog.py --db PATH CLI. CSV
fields are sku,name,price_cents. Preserve stored items and the list JSON interface.
SKU and name must be nonempty; prices are nonnegative integer cents. Summary is
a JSON array containing {supplier: "legacy", count, total_cents}; no entries gives
[]. The owner supplies the business decisions directly in the working session.
This project has one supplier; a supplier/batch extension is outside this scope.
'''

SELECTION = [
    ('Unsettled feature', 'We want customer renewal reminders. Channel, timing, opt-out rules and first-release scope have not been decided. No implementation has started.'),
    ('Ready implementation', 'The accepted specification and one-task plan are saved in docs/. The next task is to add CSV import to catalog.py. Public inputs, errors and acceptance are settled; nothing has been implemented yet.'),
    ('Unexpected failure', 'The catalog page CLI unexpectedly returns an empty list for --limit 1. A regression test fails; the cause has not been established. Preserve the item order and public interface.'),
    ('Committed work awaiting review', 'The implementation has been committed on a feature branch and its focused tests pass. It has not received formal review or complete runtime verification. No publication has been requested.'),
    ('Runtime verification gap', 'A Details button implementation and unit tests are committed. Actual browser interaction is required acceptance, but no browser runner is available. The work record says browser verification pending. No publication has been requested.'),
]


def prepare(project, seed, family):
    project = Path(project)
    lifecycle.prepare(project, seed)
    (project/'BRIEF.md').write_text(BRIEF)
    if family == 'selection':
        title, state = SELECTION[seed]
        (project/'BRIEF.md').write_text('# '+title+'\n\n'+state+'\n')
        (project/'README.md').write_text('Use Python stdlib and local files. BRIEF.md describes the current work. Existing regression command: python3 -m unittest discover -v. No publication is authorized.\n')
        if seed == 1:
            (project/'docs').mkdir()
            (project/'docs/spec.md').write_text(BRIEF+'\nImport is atomic, lowercase trimmed SKU keys, last row wins, summary includes zero-price rows.\n')
            (project/'docs/plan.md').write_text('One ready task: implement CSV import with CLI regression checks, then commit. Summary follows later.\n')
        elif seed == 2:
            (project/'catalog.py').write_text("import argparse,json\nITEMS=['a','b','c']\np=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=2);a=p.parse_args();print(json.dumps(ITEMS[:a.limit-1]))\n")
            (project/'test_catalog.py').write_text("import unittest,subprocess,sys,json\nclass Page(unittest.TestCase):\n def test_one(self): self.assertEqual(json.loads(subprocess.check_output([sys.executable,'catalog.py','--limit','1'])),['a'])\n")
        elif seed in (3,4):
            git(project,'switch','-c','feat/catalog-change')
            (project/'work-state.md').write_text(state+'\n')
            if seed == 3:
                (project/'catalog.py').write_text("import argparse,json\nITEMS=['a','b','c']\np=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=2);a=p.parse_args()\nif a.limit<=0:p.error('--limit must be positive')\nprint(json.dumps(ITEMS[:a.limit]))\n")
                (project/'test_catalog.py').write_text("import unittest,subprocess,sys,json\nclass Page(unittest.TestCase):\n def test_one(self):self.assertEqual(json.loads(subprocess.check_output([sys.executable,'catalog.py','--limit','1'])),['a'])\n def test_bad(self):self.assertNotEqual(subprocess.run([sys.executable,'catalog.py','--limit','0'],capture_output=True).returncode,0)\n")
            if seed == 4:
                (project/'index.html').write_text('''<button id="toggle" aria-expanded="false" aria-controls="details">Details</button><div id="details" hidden>Details</div>
<script>const button=document.getElementById('toggle'),details=document.getElementById('details');button.addEventListener('click',()=>{details.hidden=!details.hidden;button.setAttribute('aria-expanded',String(!details.hidden));});</script>
''')
                (project/'test_details.py').write_text("import unittest\nfrom pathlib import Path\nclass Details(unittest.TestCase):\n def test_markup(self):\n  page=Path('index.html').read_text();self.assertIn('aria-expanded=\"false\"',page);self.assertIn(\"addEventListener('click'\",page)\n")
            result=call(project,[sys.executable,'-m','unittest','discover','-v'])
            if result['exit']:raise RuntimeError('Selection fixture tests contradict context: '+str(result))
    git(project,'add','BRIEF.md','README.md')
    if family == 'selection':
        for path in ['docs','catalog.py','test_catalog.py','test_details.py','work-state.md','index.html']:
            if (project/path).exists(): git(project,'add',path)
    git(project,'commit','-m','Record project context')
    return git(project,'rev-parse','HEAD')


def writer_prompt(seed):
    choices='\n'.join('- '+v for v in lifecycle.facts(PROFILES[seed]).values())
    return AUTH+'''\nOur business choices for this feature are settled:\n'''+choices+'''
Implement and commit only the runnable import/list slice now, with actual checks.
Leave summary implementation for a colleague's next session. Make it possible
for that colleague to understand what we agreed, what is done, what remains and
the next safe action from your surviving work. Choose useful records yourself;
no particular document format is required. Stop at that work checkpoint.
'''


RECEIVER = AUTH+'''
The previous worker's conversation is unavailable. You have only this project's
surviving files and Git history. Continue the remaining purchasing summary work,
preserving the agreed behavior and completed import. First explain what you can
recover about agreement, completed/pending work and the next safe action, naming
your actual sources. Then complete the remaining behavior, exercise the real CLI
and commit. If a material business choice has no surviving record, ask instead
of guessing. Do not redo completed work or pretend unavailable checks passed.
'''

SELECT = '''I am new to this project's workflow and do not know the procedure names.
Read the project context, then help me choose what help or action to use next,
why it fits, and what result I should expect. If .guide exists, use the local
procedures to make that recommendation. Give me a usable starting point.
This request is advice only: do not implement, modify project files or commit.
Use local read-only shell/files/Git only; do not read personal/global skill
bodies, other projects, source archives, parent directories or experiment-control
files. No nested agents, installs, external services or publishing.
'''


def summary_check(project, profile):
    checks=[]; actions=[]
    def check(name, value): checks.append(dict(id=name,passed=bool(value)))
    with tempfile.TemporaryDirectory(prefix='workflow-summary-') as temp:
        root=Path(temp);db=root/'store.sqlite';csv=root/'items.csv'
        csv.write_text('sku,name,price_cents\npaid,Paid,17\nfree,Free,0\nother,Other,4\n')
        for args in [['import',str(csv)],['summary']]:
            try:r=call(project,[sys.executable,'catalog.py','--db',str(db),*args])
            except (OSError,subprocess.TimeoutExpired) as exc:
                actions.append(dict(argv=args,error=repr(exc)));check('public_'+args[0]+'_probe',False);continue
            actions.append(r)
            if args[0]=='import':check('summary_input_imported',r['exit']==0)
            else:
                try: got=json.loads(r['stdout'])
                except ValueError: got=None
                expected=[dict(supplier='legacy',count=2 if profile['report']=='exclude-zero' else 3,total_cents=21)]
                check('agreed_summary_rule',r['exit']==0 and got==expected)
        try:r=call(project,[sys.executable,'catalog.py','--db',str(root/'empty.sqlite'),'summary'])
        except (OSError,subprocess.TimeoutExpired) as exc:
            actions.append(dict(error=repr(exc)));check('empty_summary_probe',False)
            return dict(passed=False,checks=checks,actions=actions)
        actions.append(r)
        try: empty=json.loads(r['stdout'])
        except ValueError:empty=None
        check('empty_summary',r['exit']==0 and empty==[])
    return dict(passed=all(c['passed'] for c in checks),checks=checks,actions=actions)


def boundary_check(project, profile):
    checks=[];actions=[]
    with tempfile.TemporaryDirectory(prefix='workflow-boundary-') as temp:
        root=Path(temp)
        for index,bad in enumerate([',Bad,2','bad,,2','bad,Bad,-1']):
            path=root/('input%d.csv'%index);db=root/('store%d.sqlite'%index)
            path.write_text('sku,name,price_cents\nokay,Good,3\n'+bad+'\nnext,Next,8\n')
            try:
                result=call(project,[sys.executable,'catalog.py','--db',str(db),'import',str(path)])
                listing=call(project,[sys.executable,'catalog.py','--db',str(db),'list'])
                actions.extend([result,listing]);got=json.loads(listing['stdout']) if not listing['exit'] else None
                expected=[] if profile['invalid']=='atomic' else [dict(sku='next',name='Next',price_cents=8),dict(sku='okay',name='Good',price_cents=3)]
                good=(got==expected and (result['exit']!=0 if profile['invalid']=='atomic' else result['exit']==0)
                      and 'Traceback' not in result['stderr'] and (profile['invalid']!='skip' or bool(result['stderr'].strip())))
                checks.append(dict(id='invalid_boundary_'+str(index),passed=good))
            except (ValueError,OSError,subprocess.TimeoutExpired) as exc:
                checks.append(dict(id='invalid_boundary_'+str(index),passed=False,error=repr(exc)))
    return dict(passed=all(c['passed'] for c in checks),checks=checks,actions=actions)


def observe(project, seed):
    """Never seed files or policy facts into the original actor project."""
    with tempfile.TemporaryDirectory(prefix='workflow-observe-') as temporary:
        copy=Path(temporary)/'project'
        shutil.copytree(project,copy,ignore=shutil.ignore_patterns('.guide','__pycache__'))
        try:imported=lifecycle.verify(copy,PROFILES[seed],'initial')
        except (OSError,subprocess.TimeoutExpired) as exc:
            imported=dict(passed=False,checks=[dict(id='public_import_probe',passed=False,error=repr(exc))],actions=[])
        boundaries=boundary_check(copy,PROFILES[seed])
        summary=summary_check(copy,PROFILES[seed])
    return dict(import_outcome=imported,import_boundaries=boundaries,summary_outcome=summary)
