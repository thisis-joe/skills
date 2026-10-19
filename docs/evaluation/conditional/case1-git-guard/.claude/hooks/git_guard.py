#!/usr/bin/env python3
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
