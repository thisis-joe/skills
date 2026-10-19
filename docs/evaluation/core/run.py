import json, os, subprocess, sys, time
from pathlib import Path
cwd=Path(sys.argv[1]); label=sys.argv[2]; cmd=sys.argv[3:]
env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,env=env)
row={'cwd':str(cwd),'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
case=cwd if (cwd/'input.md').exists() else cwd.parent
out=case/'evidence'; out.mkdir(exist_ok=True)
(out/(label+'.json')).write_text(json.dumps(row,indent=2))
(out/(label+'.txt')).write_text('$ '+' '.join(cmd)+'\n'+p.stdout+p.stderr+'\nexit='+str(p.returncode)+'\n')
print(json.dumps(row,indent=2)); sys.exit(p.returncode)
