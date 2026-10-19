#!/usr/bin/env python3
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
