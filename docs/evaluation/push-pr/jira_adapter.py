"""LOCAL MOCK JIRA: file-backed adapter. It never connects to an external server."""
from pathlib import Path
import sys,json,datetime
case=Path(sys.argv[1]);operation=sys.argv[2];arg=sys.argv[3];folder=case/'jira'
tasks=json.loads((folder/'tasks.json').read_text());config=json.loads((folder/'config.json').read_text())
log={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'adapter':config['label'],'operation':operation,'argument':arg}
exit_code=0
if operation=='search-number':
    result=[t for key,t in tasks.items() if key.rsplit('-',1)[-1]==arg]
elif operation=='read':
    result=tasks.get(arg)
    if result is None: exit_code=4
elif operation=='update':
    patch=json.loads(Path(sys.argv[4]).read_text());log['payload']=patch;log['before']=tasks.get(arg)
    if set(patch)-{'summary','description','expected_version'}:
        result={'error':'field restriction'};exit_code=5
    elif config['reject_updates']:
        result={'error':'LOCAL MOCK 403: Summary/Description update denied'};exit_code=3
    elif tasks[arg]['version']!=patch['expected_version']:
        result={'error':'LOCAL MOCK 409: version mismatch'};exit_code=6
    else:
        tasks[arg].update(summary=patch['summary'],description=patch['description'],version=tasks[arg]['version']+1)
        (folder/'tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2)+'\n')
        result={'ok':True,'key':arg,'version':tasks[arg]['version']}
    log['after']=tasks.get(arg)
else:
    result={'error':'unsupported operation'};exit_code=2
log['result']=result;log['exit']=exit_code
with (folder/'adapter.jsonl').open('a') as fp: fp.write(json.dumps(log,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(exit_code)
