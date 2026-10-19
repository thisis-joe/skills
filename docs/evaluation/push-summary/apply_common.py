"""Reusable mechanical inspection/integration actions, called after fixture selection."""
from evidence import *
def inspect(case):
    m=MANIFEST[case]
    print((ROOT/case/'request.json').read_text());print((Path(m['repo'])/'AGENTS.md').read_text())
    for args in [('git','rev-parse','--show-toplevel'),('git','branch','--show-current'),('git','rev-parse','HEAD'),('git','status','--porcelain=v1','-uall'),('git','ls-files','--stage'),('git','status'),('git','config','--local','--list'),('git','remote','get-url','--all','origin'),('git','remote','get-url','--push','--all','origin'),('git','rev-parse','--abbrev-ref','--symbolic-full-name','@{u}'),('git','ls-remote','--heads','origin','refs/heads/dev','refs/heads/develop','refs/heads/'+m['old_branch'])]:run(case,*args)
    if m['task_key']:run(case,'python3',str(ROOT/'jira_adapter.py'),str(ROOT/case),'read',m['task_key'])
def integrate(case):
    m=MANIFEST[case]
    run(case,'git','fetch','origin','refs/heads/develop');base=run(case,'git','rev-parse','FETCH_HEAD').stdout.strip();run(case,'git','cat-file','-t',base)
    run(case,'git','fetch',m['remote'],'refs/heads/'+m['old_branch']);old=run(case,'git','rev-parse','FETCH_HEAD').stdout.strip();run(case,'git','cat-file','-t',old)
    decide(case,'Pin fetched develop and original remote task refs; preserve both histories.',{'base':base,'old_remote_task':old,'starting_head':m['work'],'single_write_url':m['remote']})
    run(case,'git','merge','--no-commit','--no-edit',old)
    run(case,'git','merge','--no-commit','--no-edit',base)
    run(case,'git','ls-files','-u');run(case,'git','diff','--check');run(case,'git','diff','--cached','--check');run(case,'git','grep','-n','-E','^(<<<<<<< |=======|>>>>>>> )','--','.',check=False)
    run(case,'python3','-m','unittest','discover','-s','tests','-v')
    run(case,'git','diff','--cached','--stat')
    if run(case,'git','rev-parse','--verify','MERGE_HEAD',check=False).returncode==0:run(case,'git','commit','-m','merge: integrate latest develop for fixture publication')
    head=run(case,'git','rev-parse','HEAD').stdout.strip()
    run(case,'git','merge-base','--is-ancestor',old,head);run(case,'git','merge-base','--is-ancestor',base,head)
    run(case,'git','diff',base,head);run(case,'git','log','--oneline',base+'..'+head);run(case,'git','status','--porcelain=v1','-uall')
    pins={'base':base,'old_remote_task':old,'head':head};(ROOT/case/'pinned.json').write_text(json.dumps(pins,indent=2)+'\n');return pins
