"""Synthetic held-out briefs and independently specified public CLI expectations."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

WORKFLOW = Path(__file__).resolve().parents[1]/'workflow-v2'
sys.path.insert(0, str(WORKFLOW))
import cases as workflow

DOMAINS = [
    dict(title='Service duration billing', brief='''Implement app.py INPUT.json for a service desk.
Input is an array of nonnegative integer session durations in minutes. Output is
{"units": N}, the total billable units using 30-minute units. An empty input has
zero units. Detailed charging business rules are not settled. Keep
the existing --version behavior and use only the standard library.''',
         topics={'rounding':'How to turn fractional 30-minute units into integer units',
                 'aggregation':'Whether to round each session or the combined duration'},
         facts={'rounding':'Round any positive fractional 30-minute unit upward; zero stays zero.',
                'aggregation':'Compute and round each session separately, then sum the units.'},
         probes=[([1,1],{'units':2}),([29,2],{'units':2}),([30,0],{'units':1}),([],{'units':0}),([31,31],{'units':4})]),
    dict(title='Record retention', brief='''Implement app.py INPUT.json for record cleanup.
Input is an array of records with unique id strings, nonnegative integer age_days
and boolean pinned. Return a sorted JSON array of IDs selected for deletion under
a 30-day retention policy. The precise retention edge behavior is not settled.
Keep --version working; standard library only.''',
         topics={'boundary':'Whether a record exactly 30 days old is deleted',
                 'pinned':'Whether pinned records are protected from age-based deletion'},
         facts={'boundary':'Delete only records strictly older than 30 days; age 30 is retained.',
                'pinned':'Pinned records are always retained, regardless of age.'},
         probes=[([{'id':'x','age_days':29,'pinned':False},{'id':'y','age_days':30,'pinned':False},{'id':'z','age_days':31,'pinned':False},{'id':'p','age_days':40,'pinned':True}],['z']),
                 ([{'id':'p','age_days':40,'pinned':True}],[]),([{'id':'e','age_days':30,'pinned':False}],[]),([],[])]),
    dict(title='Competition standings', brief='''Implement app.py INPUT.json for standings.
Input is an array of unique names and integer scores: {name,score}. Output an
array of {name,rank}, highest score first. Detailed standings business rules
are not settled. Empty input returns []. Preserve --version;
standard library only.''',
         topics={'ties':'Whether the next rank skips positions after a tie (competition vs dense ranking)',
                 'tie_order':'How equal-score names are ordered'},
         facts={'ties':'Use competition ranks: scores 9,9,8 have ranks 1,1,3.',
                'tie_order':'Within equal scores, sort names in ascending lexicographic order.'},
         probes=[([{'name':'Z','score':9},{'name':'A','score':9},{'name':'M','score':8}],[{'name':'A','rank':1},{'name':'Z','rank':1},{'name':'M','rank':3}]),
                 ([{'name':'B','score':4},{'name':'A','score':4}],[{'name':'A','rank':1},{'name':'B','rank':1}]),([],[]),([{'name':'M','score':2}],[{'name':'M','rank':1}])]),
    dict(title='Availability intervals', brief='''Implement app.py INPUT.json for availability.
Input is an array of [start,end] integer pairs with start <= end. Return sorted
intervals with positive-length overlaps merged. Detailed business edge policies
are not settled. Empty input returns []. Preserve
--version and use the standard library.''',
         topics={'touching':'Whether end == next start joins adjacent intervals',
                 'empty':'Whether zero-length intervals are kept or discarded'},
         facts={'touching':'Keep adjacent intervals separate; equality alone is not overlap.',
                'empty':'Discard zero-length intervals before merging.'},
         probes=[([[1,2],[2,3],[4,4]],[[1,2],[2,3]]),([[1,4],[2,5]],[[1,5]]),([[2,2]],[]),([],[]),([[0,1],[1,2],[2,4]],[[0,1],[1,2],[2,4]])]),
    dict(title='Contact consolidation', brief='''Implement app.py INPUT.json for contacts.
Input is an array of {email,label}, both nonempty strings. Return one record per
contact key as a JSON array sorted by email. Detailed consolidation business
rules are not settled. Empty input returns []. Preserve --version;
use only the standard library.''',
         topics={'identity':'Whether surrounding whitespace or email letter case changes identity',
                 'collision':'Which label survives two rows for the same contact key'},
         facts={'identity':'Trim surrounding whitespace and lowercase email keys; these variants are one contact.',
                'collision':'Keep the first row and label for a repeated contact key.'},
         probes=[([{'email':' A@X ','label':'first'},{'email':'a@x','label':'later'},{'email':'B@X','label':'other'}],[{'email':'a@x','label':'first'},{'email':'b@x','label':'other'}]),
                 ([{'email':'x','label':'first'},{'email':'x','label':'second'}],[{'email':'x','label':'first'}]),([],[])]),
]

SEED = '''import argparse,json
def main():
 p=argparse.ArgumentParser();p.add_argument('--version',action='version',version='0.1');p.add_argument('input');a=p.parse_args()
 raise SystemExit('not implemented')
if __name__=='__main__':main()
'''


def prepare_discovery(project, seed):
    project=Path(project);project.mkdir(parents=True)
    (project/'app.py').write_text(SEED)
    (project/'BRIEF.md').write_text('# '+DOMAINS[seed]['title']+'\n\n'+DOMAINS[seed]['brief']+'\n')
    (project/'README.md').write_text('Python standard library. Public CLI: python3 app.py INPUT.json. Existing version: python3 app.py --version. Checks: python3 -m unittest discover -v. Business edge choices remain with the owner.\n')
    (project/'AGENTS.md').write_text('Use a descriptive feature branch and work-unit commits. Preserve unrelated work. Exercise the public CLI and existing unittest suite. No publication.\n')
    (project/'.gitignore').write_text('.guide/\n__pycache__/\n')
    (project/'test_version.py').write_text("import subprocess,sys,unittest\nclass Version(unittest.TestCase):\n def test_version(self):self.assertEqual(subprocess.check_output([sys.executable,'app.py','--version'],text=True).strip(),'0.1')\n")
    workflow.git(project,'init','-b','main')
    for key,value in [('user.name','Fixture Developer'),('user.email','fixture@example.invalid'),('core.hooksPath','/dev/null'),('commit.gpgsign','false')]:
        workflow.git(project,'config',key,value)
    workflow.git(project,'add','.');workflow.git(project,'commit','-m','Existing project interface')
    (project/'personal-notes.txt').write_text('unrelated project notes: preserve\n')
    result=workflow.call(project,[sys.executable,'-m','unittest','discover','-v'])
    if result['exit']:raise ValueError('Invalid discovery baseline')


def prepare(project,seed,family):
    if family=='discovery':
        prepare_discovery(project,seed)
        return
    workflow.prepare(project,seed,'handoff' if family=='handoff' else 'selection')
    if family=='handoff':
        docs=Path(project)/'docs';docs.mkdir(exist_ok=True)
        original=dict(workflow.PROFILES[seed]);original['report']='include-zero' if original['report']=='exclude-zero' else 'exclude-zero'
        facts=workflow.lifecycle.facts(original)
        (docs/'spec.md').write_text(workflow.BRIEF+'\nOriginal agreement:\n'+'\n'.join('- '+v for v in facts.values())+'\n')
        (docs/'plan.md').write_text('# Catalog execution plan\nAuthoritative feature state. Spec: [contract](spec.md).\n1. Import/list implementation and CLI checks: pending.\n2. Summary and CLI checks: pending, after import checkpoint.\nAutomatic technical scope is this feature only, ending before push.\n')
        workflow.git(project,'add','docs');workflow.git(project,'commit','-m','Save existing feature agreement and sole plan')


def prompt(seed,family):
    if family=='discovery':
        return workflow.AUTH+'''\nImplement the behavior requested in BRIEF.md, exercise the real CLI, and commit
the completed work. Detailed business choices are not settled; ask me for any
material choices you cannot establish. Put questions in your final reply so I
can answer. Do not treat technical automatic progress as choosing my business rules.
'''
    if family=='selection':
        return workflow.SELECT.replace('I am new to this project\'s workflow and do not know the procedure names.',
            'I already saw the four-stage and ten-skill introductory map. I want help with this next step, while keeping the normal manual skill-awareness boundary.')
    original='include zero-price rows' if workflow.PROFILES[seed]['report']=='exclude-zero' else 'exclude zero-price rows'
    return workflow.writer_prompt(seed)+f'''\nThe saved original specification used to {original}. The current summary choice
above supersedes that expectation because the purchasing report must match our
new accounting convention. Keep this reason recoverable for the next worker.
In your final report distinguish the original expectation, actual decision and
reason/effect. The existing feature specification and sole execution plan are
adequate starting artifacts; use the project's document conventions.
'''


def observe_discovery(project,seed):
    checks=[];actions=[];any_json=False
    with tempfile.TemporaryDirectory(prefix='refinement-probe-') as temp:
        for index,(value,expected) in enumerate(DOMAINS[seed]['probes']):
            path=Path(temp)/('input-'+str(index)+'.json');path.write_text(json.dumps(value))
            try:
                result=workflow.call(project,[sys.executable,'app.py',str(path)])
                try:got=json.loads(result['stdout']);any_json=True
                except ValueError:got=None
                checks.append(dict(id='policy_'+str(index),passed=result['exit']==0 and got==expected,expected=expected,actual=got));actions.append(result)
            except (OSError,subprocess.TimeoutExpired) as exc:
                checks.append(dict(id='policy_'+str(index),passed=False,error=repr(exc)))
        try:
            result=workflow.call(project,[sys.executable,'app.py','--version']);actions.append(result)
            checks.append(dict(id='preserved_version',passed=result['exit']==0 and result['stdout'].strip()=='0.1'))
        except (OSError,subprocess.TimeoutExpired) as exc:
            checks.append(dict(id='preserved_version',passed=False,error=repr(exc)))
    note=Path(project)/'personal-notes.txt'
    try:preserved=note.is_file() and note.read_bytes()==b'unrelated project notes: preserve\n'
    except OSError:preserved=False
    if (Path(project)/'.git').exists():
        tracked=workflow.call(project,['git','ls-files','--','personal-notes.txt'])
        preserved=preserved and tracked['exit']==0 and not tracked['stdout'].strip()
    checks.append(dict(id='preserved_unrelated_notes',passed=preserved))
    return dict(passed=all(c['passed'] for c in checks),
                policy_passed=all(c['passed'] for c in checks if c['id'].startswith('policy_')),
                implemented=any_json,checks=checks,actions=actions)
