from pathlib import Path
import json, subprocess, sys, difflib, os
root=Path('/tmp/lets-conditional-validation/case1-git-guard'); root.mkdir()
(root/'.claude/hooks').mkdir(parents=True)
old={'env': {'UNRELATED_SETTING':'keep-me'},'hooks':{'PreToolUse':[{'matcher':'Bash','hooks':[{'type':'command','command':'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/unrelated.py"'}]},{'matcher':'Write','hooks':[{'type':'command','command':'true'}]}]}}
(root/'supplied-settings.json').write_text(json.dumps(old,indent=2)+'\n')
(root/'.claude/hooks/unrelated.py').write_text('from pathlib import Path\nimport os\nPath(os.environ["CLAUDE_PROJECT_DIR"], "other-hook-ran").write_text("ran\\n")\n')
guard=r'''#!/usr/bin/env python3
"""Convenience guard for documented literal shell/Git forms, never command execution."""
import json, shlex, sys

def blocked(reason):
    print('Git guard: '+reason, file=sys.stderr)
    raise SystemExit(2)

def inspect(segment):
    if not segment: return
    # Shell expansion/wrappers/aliases are deliberately unsupported, not interpreted.
    while segment and '=' in segment[0] and segment[0].split('=',1)[0].isidentifier():
        segment=segment[1:]
    if not segment: return
    exe=segment[0].rsplit('/',1)[-1]
    if exe in {'bash','sh','zsh','fish','eval','source','.','env','command','exec','sudo','xargs'}:
        blocked('unsupported command wrapper requires review')
    if exe != 'git': return
    args=segment[1:]; i=0
    value_flags={'-C','-c','--git-dir','--work-tree','--namespace','--super-prefix','--config-env'}
    plain_flags={'--no-pager','--paginate','--literal-pathspecs','--no-literal-pathspecs','--glob-pathspecs','--noglob-pathspecs','--icase-pathspecs','--no-optional-locks'}
    while i<len(args) and args[i].startswith('-'):
        flag=args[i]
        if flag in value_flags:
            if i+1>=len(args): blocked('missing Git flag value')
            if flag in {'-c','--config-env'} and args[i+1].startswith('alias.'):
                blocked('Git aliases require review')
            i+=2; continue
        if flag in plain_flags: i+=1; continue
        if any(flag.startswith(x+'=') for x in value_flags if x.startswith('--')):
            i+=1; continue
        if flag.startswith('-C') or flag.startswith('-c'):
            if flag.startswith('-calias.'): blocked('Git aliases require review')
            i+=1; continue
        blocked('unsupported Git global flag requires review')
    if i==len(args): return
    sub=args[i]; rest=args[i+1:]
    if sub=='push': blocked('push is denied by project policy')
    if sub=='reset' and any(x=='--hard' or x.startswith('--hard=') for x in rest):
        blocked('hard reset is denied')
    if sub=='clean' and any(x=='--force' or (x.startswith('-') and not x.startswith('--') and 'f' in x[1:]) for x in rest):
        blocked('forced clean is denied')
    if sub=='branch' and any(x=='--delete' and '--force' in rest or (x.startswith('-') and not x.startswith('--') and 'D' in x[1:]) for x in rest):
        blocked('forced branch deletion is denied')
    if sub in {'checkout','restore'} and any(x in {'.', './',':/'} for x in rest):
        blocked('whole-tree discard is denied (conservative dot-path match)')
    known={'status','diff','log','show','rev-parse','ls-files','add','commit','checkout','restore','reset','clean','branch','fetch','switch','merge','rebase','stash','tag','config','init','worktree'}
    if sub not in known: blocked('unknown Git command/alias requires review')

try:
    value=json.load(sys.stdin)
    if not isinstance(value,dict) or not isinstance(value.get('tool_input'),dict): blocked('malformed hook payload')
    command=value['tool_input'].get('command')
    if not isinstance(command,str) or not command.strip(): blocked('missing command string')
    if any(x in command for x in ('$','`','\\','\x00','<<')): blocked('unsupported expansion/escape/heredoc requires review')
    lex=shlex.shlex(command,posix=True,punctuation_chars=';&|()<>\n')
    lex.whitespace=' \t\r'; lex.whitespace_split=True; lex.commenters='#'
    tokens=list(lex); segment=[]
    for token in tokens:
        if token in {';','&&','||','|','\n'}:
            inspect(segment); segment=[]
        elif any(c in token for c in '()<>' ):
            blocked('unsupported shell operator requires review')
        else: segment.append(token)
    inspect(segment)
except (ValueError,TypeError,KeyError): blocked('malformed payload or unsupported quoting')
'''
(root/'.claude/hooks/git_guard.py').write_text(guard)
new=json.loads(json.dumps(old)); entry={'type':'command','command':'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/git_guard.py"','onFailure':'block'}
new['hooks']['PreToolUse'][0]['hooks'].append(entry)
(root/'.claude/settings.json').write_text(json.dumps(new,indent=2)+'\n')
(root/'settings-rollback.json').write_text(json.dumps(old,indent=2)+'\n')
(root/'settings.diff').write_text(''.join(difflib.unified_diff(json.dumps(old,indent=2).splitlines(True),json.dumps(new,indent=2).splitlines(True),fromfile='.claude/settings.json.before',tofile='.claude/settings.json.after')))
checks=[('push','git push origin main',2),('push flags','git --no-pager -C "folder with spaces" push origin main',2),('hard reset','git reset --hard HEAD~1',2),('hard equals','git reset --hard=HEAD',2),('forced clean','git clean -fdx',2),('forced clean long','git clean --force -d',2),('branch delete','git branch -D feature/old',2),('branch long','git branch --delete --force feature/old',2),('checkout dot','git checkout -- .',2),('restore dot','git restore --worktree .',2),('status','git status --short',0),('quoted path','git diff -- "file with spaces.ts"',0),('global flags','git -c core.quotePath=false --git-dir=.git status',0),('compound','git status && git push origin main',2),('quoted literal','printf "git push origin main"',0),('wrapper','bash -c "git push"',2),('substitution','git $(printf push)',2),('alias','git -c alias.safe=push safe',2),('invalid quoting',"git status '",2),('pipe','printf x | git push origin main',2),('newline','git status\ngit push',2)]
results=[]
for label,command,expected in checks:
    proc=subprocess.run([sys.executable,str(root/'.claude/hooks/git_guard.py')],input=json.dumps({'tool_input':{'command':command}}),text=True,capture_output=True)
    results.append({'case':label,'command_data_only':command,'exit':proc.returncode,'expected':expected,'diagnostic':proc.stderr.strip(),'pass':proc.returncode==expected and (expected!=2 or bool(proc.stderr))})
for label,payload in [('bad JSON','{'),('missing command','{"tool_input":{}}'),('wrong command type','{"tool_input":{"command":[]}}')]:
    proc=subprocess.run([sys.executable,str(root/'.claude/hooks/git_guard.py')],input=payload,text=True,capture_output=True)
    results.append({'case':label,'payload':payload,'exit':proc.returncode,'expected':2,'diagnostic':proc.stderr.strip(),'pass':proc.returncode==2 and bool(proc.stderr)})
# Simulate only the documented hook ordering; this is NOT Claude Code execution.
subprocess.run(['git','init','-b','fixture/main',str(root/'repo')],capture_output=True,check=True)
env={**os.environ,'CLAUDE_PROJECT_DIR':str(root)}
payload=json.dumps({'tool_name':'Bash','tool_input':{'command':'git status --short'}})
for name in ['unrelated.py','git_guard.py']:
    proc=subprocess.run([sys.executable,str(root/'.claude/hooks'/name)],input=payload,text=True,capture_output=True,env=env)
    assert proc.returncode==0
status=subprocess.run(['git','-C',str(root/'repo'),'status','--short'],capture_output=True,text=True,check=True)
assert (root/'other-hook-ran').exists() and old['env']==new['env']
(root/'tests.json').write_text(json.dumps({'synthetic':results,'all_passed':all(x['pass'] for x in results),'local_dispatch':{'simulated_runtime':True,'other_hook_ran':True,'harmless_git_status_exit':status.returncode},'real_claude_interception':'unavailable: claude executable absent'},indent=2)+'\n')
(root/'README.md').write_text('''# Case 1 — project Git guard preparation
Owner: lets-security for threat/control/negative checks; lets-build would own an authorized real-project implementation/commit. Artifacts only in this fixture; no user-wide setting changed and no runtime hook activated.

Supplied unrelated env entry and existing Bash/Write hooks survive in `.claude/settings.json`; `settings.diff` is reviewable and `settings-rollback.json` is an exact rollback copy. Default deny set used without custom additions to requested Git policy. The parser also holds unsupported syntax for review.

Supported: literal git executable (including absolute path), standard -C/-c and listed long global flags, shell separators/pipes, shell-quoted arguments. Denies push, hard reset, forced clean, forced branch delete, whole-tree checkout/restore. Some safe dot comparisons are conservatively denied. Unsupported shell expansion, aliases, wrappers, escapes, redirection and heredocs block with exit 2. Other programs/alias configuration already existing outside this payload can bypass this helper; this is a convenience guard, not a complete shell security boundary. Rebase/stash and arbitrary programs are outside the proposed deny set.

Actual check: `python3 build_case1.py` invoked the helper on synthetic stdin only, never executed dangerous Git data, then dispatched two hooks through a labelled local stand-in and executed only git init/status. tests.json records every input/exit/diagnostic. Real harmless Claude intercepted call is unavailable because Claude Code is absent; the local stand-in cannot prove runtime loading/matching/version support. Activation remains prepared only. For real activation confirm the target runtime supports onFailure, reload its project hook config, and make one harmless intercepted status call.

Runtime schema, project scope and exit 2 were verified against [official Claude Code hooks documentation](https://code.claude.com/docs/en/hooks). The target runtime version is not supplied; version compatibility remains open.
''')
print(json.dumps({'case':1,'synthetic_passed':sum(x['pass'] for x in results),'synthetic_total':len(results),'actual_runtime_interception':'unavailable'}))
