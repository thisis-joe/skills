from pathlib import Path
import json,subprocess,os,sys,hashlib,shutil
r=Path('/tmp/lets-conditional-validation/case4-wizard'); (r/'inputs/.github/workflows').mkdir(parents=True); (r/'helpers').mkdir(); (r/'evidence').mkdir()
(r/'inputs/.env.example').write_text('RESEND_API_KEY=\nAPP_ORIGIN=https://reports.example.invalid\nUNRELATED=keep-me\n')
(r/'inputs/.github/workflows/send.yml').write_text('jobs:\n  report:\n    steps:\n      - run: python3 send.py\n        env:\n          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}\n          APP_ORIGIN: ${{ vars.APP_ORIGIN }}\n')
(r/'inputs/brief.md').write_text('''Write a disposable human-operated wizard, not a repository installation. Only local .env capture is authorized. Never send email or write remote secrets. The approved public origin is https://reports.example.invalid. A person supplies an already approved Resend sending key for the intended domain. Dashboard: https://resend.com/api-keys. Open it, log in if needed, select/use the approved key; if a new key is needed its creation is a separate human approval boundary. Newly created key values are visible only once. Destination .env must preserve unrelated fields and existing permissions. This fixture reads .env as literal shell-style quoted words through shlex.split, never by sourcing or eval. No dotenv expansion is permitted.
Primary documentation: https://resend.com/docs/dashboard/api-keys/introduction; it links the dashboard URL and states key values cannot be viewed after creation. Exact logged-in creation screen labels are not verified in this run.
''')
store=r'''#!/usr/bin/env python3
"""Project literal .env syntax: KEY=one shlex-parsed word; no interpolation or eval."""
from pathlib import Path
import os, sys, re, shlex, tempfile, stat, fcntl
KEY=re.compile(r'^[A-Z_][A-Z0-9_]*$')
def parse(text):
    values={}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        key,sep,raw=line.partition('=')
        if not sep or not KEY.fullmatch(key): raise ValueError('invalid env key syntax')
        words=shlex.split(raw,comments=False,posix=True)
        if len(words)>1: raise ValueError('env value must be one quoted word')
        values[key]=words[0] if words else ''
    return values

def read(path):
    if path.is_symlink(): raise ValueError('symlink env file is unsupported')
    return parse(path.read_text()) if path.exists() else {}

def upsert(path,key,value):
    if not KEY.fullmatch(key) or any(x in value for x in ('\x00','\n','\r')): raise ValueError('invalid single-line env input')
    if path.is_symlink() or (path.exists() and not path.is_file()): raise ValueError('unsupported env target')
    # Atomic replace in one local operator-owned directory; no broader filesystem targets.
    with open(path.parent/'.setup.lock','a') as lock:
        os.chmod(lock.name,0o600); fcntl.flock(lock,fcntl.LOCK_EX)
        text=path.read_text() if path.exists() else ''
        parse(text) # retain prior valid syntax rather than overwriting parse failures
        mode=stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
        lines=text.splitlines(keepends=True); out=[]; inserted=False
        for line in lines:
            if line.startswith(key+'='):
                if not inserted: out.append(key+'='+shlex.quote(value)+'\n'); inserted=True
            else: out.append(line if line.endswith('\n') else line+'\n')
        if not inserted: out.append(key+'='+shlex.quote(value)+'\n')
        fd,name=tempfile.mkstemp(prefix='.env-upsert-',dir=path.parent)
        try:
            os.fchmod(fd,mode)
            with os.fdopen(fd,'w') as stream:
                stream.write(''.join(out)); stream.flush(); os.fsync(stream.fileno())
            os.replace(name,path)
        finally:
            if os.path.exists(name): os.unlink(name)
if __name__=='__main__':
    try:
        action,path,key=sys.argv[1:]; path=Path(path)
        if action=='set': upsert(path,key,sys.stdin.read())
        elif action=='present':
            value=read(path).get(key)
            print(key+': '+('present' if value else 'missing')); sys.exit(0 if value else 1)
        else: raise ValueError('unknown operation')
    except (ValueError,OSError):
        print('Environment helper failed; value redacted. Check local file syntax/permissions.',file=sys.stderr);sys.exit(2)
'''
(r/'helpers/env_store.py').write_text(store)
# A supplied app reader proving exact syntax with data parsing, not shell evaluation.
(r/'inputs/app_config.py').write_text('import importlib.util\nfrom pathlib import Path\np=Path(__file__).parents[1]/"helpers/env_store.py"\ns=importlib.util.spec_from_file_location("env_store",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\ndef load_env(path): return m.read(Path(path))\n')
wizard=r'''#!/usr/bin/env bash
set +x
set -euo pipefail
umask 077
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
STORE="$SCRIPT_DIR/helpers/env_store.py"
ENV_FILE=${1:-"$SCRIPT_DIR/.env"}
[[ -t 0 && -t 1 ]] || { printf '%s\n' 'Human-operated only: run in a terminal.' >&2; exit 2; }
command -v python3 >/dev/null || { printf '%s\n' 'python3 is required.' >&2; exit 2; }
[[ -d "$(dirname -- "$ENV_FILE")" ]] || { printf '%s\n' 'Destination parent must exist.' >&2; exit 2; }
stage() { printf '\n[%s/3] %s\n' "$1" "$2"; }
confirm() { local answer; IFS= read -r -p "$1 [y/N] " answer </dev/tty; [[ "$answer" == y || "$answer" == Y ]]; }
open_url() {
  local url=$1
  printf 'Open: %s\n' "$url"
  if command -v open >/dev/null; then open "$url"
  elif command -v xdg-open >/dev/null; then xdg-open "$url"
  else confirm 'Open that exact URL manually, then continue?' || exit 1
  fi
}
write_value() { local key=$1 value=$2; printf '%s' "$value" | python3 "$STORE" set "$ENV_FILE" "$key"; }
stage 1 'Capture the approved sending key locally'
if python3 "$STORE" present "$ENV_FILE" RESEND_API_KEY; then
  if confirm 'Replace the locally captured key?'; then replace_key=yes; else replace_key=no; fi
else replace_key=yes; fi
if [[ "$replace_key" == yes ]]; then
  open_url 'https://resend.com/api-keys'
  printf '%s\n' 'Log in and obtain the previously approved key. Key creation/revocation is a separate human choice; this wizard performs neither.'
  confirm 'Ready to capture the approved value locally?' || exit 1
  key_value=''
  IFS= read -r -s -p 'RESEND_API_KEY (hidden): ' key_value </dev/tty
  printf '\n' >/dev/tty
  [[ -n "$key_value" ]] || { printf '%s\n' 'No key captured; prior stages retained.' >&2; exit 1; }
  write_value RESEND_API_KEY "$key_value"
  unset key_value
fi
stage 2 'Record the agreed public application origin'
if python3 "$STORE" present "$ENV_FILE" APP_ORIGIN; then
  printf '%s\n' 'Existing origin retained. To change it, edit the approved inventory and rerun a reviewed wizard.'
else write_value APP_ORIGIN 'https://reports.example.invalid'; fi
stage 3 'Safe readback and manual CI handoff'
python3 "$STORE" present "$ENV_FILE" RESEND_API_KEY
python3 "$STORE" present "$ENV_FILE" APP_ORIGIN
printf '%s\n' 'Local preparation complete. No remote secret/variable was written and no message was sent.'
printf '%s\n' 'Pending human CI setup, if separately authorized: secret RESEND_API_KEY; variable APP_ORIGIN (see supplied workflow references). Never copy a key into logs.'
printf '%s\n' 'Keep this local .env out of version control. Retain it only for intended local use; remove it manually when that use ends. Rerun preserves already captured stages.'
'''
(r/'setup-wizard.sh').write_text(wizard); (r/'setup-wizard.sh').chmod(0o700)
checks=[]
def record(name,command,p):
    (r/'evidence'/f'{name}.txt').write_text(p.stdout+p.stderr)
    checks.append({'name':name,'command':command,'exit':p.returncode,'evidence':f'evidence/{name}.txt'})
cmd=['bash','-n',str(r/'setup-wizard.sh')];record('syntax',cmd,subprocess.run(cmd,text=True,capture_output=True))
# Test the helper with synthetic fake values only; do not launch the wizard.
spec=__import__('importlib.util',fromlist=['x']).spec_from_file_location('env_store',r/'helpers/env_store.py');m=__import__('importlib.util',fromlist=['x']).module_from_spec(spec);spec.loader.exec_module(m)
t=r/'evidence/fake.env'; t.write_text('# retained comment\nUNRELATED=keep-me\nRESEND_API_KEY=old\nRESEND_API_KEY=duplicate\n'); t.chmod(0o640)
fake='FAKE_ONLY a\'b"c # $HOME `touch SHOULD_NOT_EXIST` \\ trailing'
m.upsert(t,'RESEND_API_KEY',fake); first=t.read_bytes();m.upsert(t,'RESEND_API_KEY',fake)
assert first==t.read_bytes() and m.read(t)['RESEND_API_KEY']==fake and m.read(t)['UNRELATED']=='keep-me'
assert (t.stat().st_mode & 0o777)==0o640 and t.read_text().count('RESEND_API_KEY=')==1
assert '# retained comment' in t.read_text() and not (r/'SHOULD_NOT_EXIST').exists()
cmd=[sys.executable,str(r/'helpers/env_store.py'),'present',str(t),'RESEND_API_KEY'];p=subprocess.run(cmd,text=True,capture_output=True);record('readback',cmd,p);assert fake not in p.stdout and p.stdout=='RESEND_API_KEY: present\n'
new=r/'evidence/new-fake.env';m.upsert(new,'RESEND_API_KEY','FAKE_ONLY');assert new.stat().st_mode & 0o777==0o600
try:m.upsert(t,'RESEND_API_KEY','bad\nvalue');raise AssertionError('accepted newline')
except ValueError:pass
link=r/'evidence/link.env';link.symlink_to(t)
try:m.upsert(link,'RESEND_API_KEY','FAKE_ONLY');raise AssertionError('accepted symlink')
except ValueError:pass
(r/'checks.json').write_text(json.dumps({'commands':checks,'helper_tests':{'literal_roundtrip':True,'duplicate_upsert_idempotent':True,'unrelated_key_and_comment_preserved':True,'existing_mode_0640_preserved':True,'new_mode_0600':True,'secret_readback_presence_only':True,'newline_rejected':True,'symlink_rejected':True},'shellcheck':'unavailable: executable absent','wizard_execution':'not performed: interactive human-only deliverable','remote_effects':'none','real_dashboard_logged_in_steps':'unavailable; documented URL redirects to login'},indent=2)+'\n')
(r/'STAGES.md').write_text('''# Setup wizard stage/value trace
| Stage | Journey/source | Value and classification | Destination | Boundary and recovery |
|---|---|---|---|---|
| 1 | Open documented https://resend.com/api-keys; log in and use approved existing sending key. Logged-in labels not verified. | RESEND_API_KEY; secret, hidden capture | local .env only, literal parser in inputs/app_config.py | Person controls credential creation; no remote action here. Rerun keeps present key unless replacement confirmed. Failure before upsert keeps old file. |
| 2 | Agreed origin from supplied .env.example/brief | APP_ORIGIN; public, settled https://reports.example.invalid | local .env, preserve existing value | Atomic idempotent upsert; existing differing value retained, owner resolves change separately. |
| 3 | .github/workflows/send.yml env references | same secret/public names | presence-only local readback; manual future CI secret/variable handoff | Remote storage not authorized or executed; no email send. Partial local state stays resumable. |

Exact future human invocation: `bash /tmp/lets-conditional-validation/case4-wizard/setup-wizard.sh /path/to/owned/project/.env` in a real terminal. Do not source the env file; use the supplied data parser. This syntax is fixture-specific, not a promise of compatibility with every dotenv library. Existing malformed env syntax blocks rather than overwrites.

Prepared and Bash syntax checked; helper unit behavior checked on labelled fake values. ShellCheck unavailable. Interactive completion and authenticated dashboard behavior unverified. The wizard itself was never executed. Nothing was committed; this requested output is disposable. Retain the helper alongside the wizard until local setup is done. Keep the resulting .env private for its intended lifetime; human removes it at the end of that use. No remote secret copy is retained here.

[Resend's primary key documentation](https://resend.com/docs/dashboard/api-keys/introduction) links the verified URL and explains single-view values. Browser evidence was public docs/login only; it did not verify an authenticated account or create a key. Local fake artifacts contain conspicuous synthetic values, never real credentials.
''')
print(json.dumps({'case':4,'bash_syntax':checks[0]['exit'],'helper_checks':8,'interactive_executed':False}))
