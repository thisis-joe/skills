"""Prospective explicit model selection; the historical native engine stays unchanged."""
from datetime import datetime, timedelta, timezone
import json
import os
import re
from pathlib import Path

MODEL='gpt-6.1-sol'
EFFORT='high'


def bind_args(args):
    if args[:2] != ['codex','exec']:
        raise ValueError('Model pin only supports the recorded native Codex exec command')
    if '--model' in args or '-m' in args or any('model_reasoning_effort' in value for value in args):
        raise ValueError('Refusing an already-overridden native command')
    index=args.index('resume')+1 if 'resume' in args else 2
    return args[:index]+['--model',MODEL,'-c','model_reasoning_effort="'+EFFORT+'"']+args[index:]


class ModelSubprocess:
    """Bind one engine module's Popen call, without modifying subprocess globally."""
    def __init__(self, original):self.original=original
    def __getattr__(self,name):return getattr(self.original,name)
    def Popen(self,args,**kwargs):
        # The engine's invocation receipt refers to this same list. Its running
        # and final records therefore retain the command actually executed.
        args[:]=bind_args(args)
        return self.original.Popen(args,**kwargs)


def verify_contexts(result,contexts):
    started=datetime.fromisoformat(result['started_at'].replace('Z','+00:00'))
    finished=datetime.fromisoformat(result['finished_at'].replace('Z','+00:00'))
    fresh=[]
    for context in contexts:
        try:timestamp=datetime.fromisoformat(context.get('timestamp','').replace('Z','+00:00'))
        except (ValueError,TypeError,AttributeError):continue
        if timestamp.tzinfo is not None and started <= timestamp <= finished:fresh.append((timestamp,context))
    if not fresh:return {'verified':False,'reason':'No model context within this invocation time window','thread':result.get('thread')}
    latest=max(fresh,key=lambda item:item[0])[1]
    observed={k:latest.get(k) for k in ['model','effort']}
    return {'verified':observed=={'model':MODEL,'effort':EFFORT},'requested_model':MODEL,
            'requested_effort':EFFORT,'observed':observed,'thread':result.get('thread'),
            'matched_context_timestamp':latest['timestamp'],'matched_turn_id':latest.get('turn_id'),
            'source':'fresh turn_context within this invocation started_at/finished_at, returned native session only'}


def session_model(result):
    thread=result.get('thread')
    if not isinstance(thread,str) or not re.fullmatch(r'[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}',thread):
        return {'verified':False,'reason':'No returned native thread ID'}
    # Read only the session returned by this exact native invocation. Never copy
    # prompts, credentials or unrelated sessions into the experiment evidence.
    root=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions'
    started=datetime.fromisoformat(result['started_at'].replace('Z','+00:00')).astimezone(timezone.utc)
    paths=[]
    for day in [started-timedelta(days=1),started,started+timedelta(days=1)]:
        paths.extend((root/day.strftime('%Y/%m/%d')).glob('*'+thread+'*.jsonl'))
    contexts=[]
    for path in sorted(set(paths)):
        for line in path.read_text(errors='replace').splitlines():
            try:value=json.loads(line)
            except ValueError:continue
            if value.get('type')!='turn_context':continue
            payload=value.get('payload',{})
            contexts.append({'model':payload.get('model'),'effort':payload.get('effort',payload.get('reasoning_effort')),
                             'timestamp':value.get('timestamp'),'turn_id':payload.get('turn_id')})
    return verify_contexts(result,contexts)
