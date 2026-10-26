"""Organic local project fixtures and outcome checks independent of COCO policy."""
import csv
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

CASES = ['copy', 'csv', 'pagination', 'ledger', 'service', 'runtime-gap']

FIXTURES = {
    'copy': {
        'index.html': '<!doctype html><html><body><button id="save">Save</button><p>Saved records</p></body></html>\n',
        'test_page.py': 'import unittest\nfrom pathlib import Path\nclass Page(unittest.TestCase):\n def test_page(self): self.assertIn("Saved records",Path("index.html").read_text())\n',
    },
    'csv': {
        'totals.py': '''import argparse, csv, sys
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('path')
    args=parser.parse_args()
    with open(args.path, newline='') as stream:
        values=[int(row['amount']) for row in csv.DictReader(stream)]
    print('count=%d total=%d' % (len(values),sum(values)))
if __name__=='__main__': main()
''',
        'sales.csv': 'amount\n2\n7\n-1\n',
        'test_totals.py': '''import subprocess, sys, unittest
class Totals(unittest.TestCase):
 def test_text(self):
  self.assertEqual(subprocess.check_output([sys.executable,'totals.py','sales.csv'],text=True).strip(),'count=3 total=8')
''',
    },
    'pagination': {
        'catalog.py': '''import argparse, json
ITEMS=['amber','birch','cedar','dawn','elm','fern','gold']
def page(offset,limit): return ITEMS[offset:offset+limit-1]
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--offset',type=int,default=0); p.add_argument('--limit',type=int,default=3)
 a=p.parse_args(); print(json.dumps(page(a.offset,a.limit)))
''',
        'test_catalog.py': '''import unittest
from catalog import page
class Catalog(unittest.TestCase):
 def test_far_offset(self): self.assertEqual(page(100,3),[])
''',
    },
    'ledger': {
        'ledger.py': '''import argparse, json, sqlite3
def main():
 p=argparse.ArgumentParser(); p.add_argument('--db',required=True); p.add_argument('command',choices=['list'])
 a=p.parse_args(); c=sqlite3.connect(a.db); c.execute('CREATE TABLE IF NOT EXISTS entries (key TEXT PRIMARY KEY, amount INTEGER NOT NULL)')
 print(json.dumps([dict(key=k,amount=v) for k,v in c.execute('SELECT key,amount FROM entries ORDER BY key')]))
 c.close()
if __name__=='__main__': main()
''',
        'test_ledger.py': '''import json, subprocess, sys, tempfile, unittest
class Ledger(unittest.TestCase):
 def test_empty(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(json.loads(subprocess.check_output([sys.executable,'ledger.py','--db',d+'/x.db','list'])),[])
''',
    },
    'service': {
        'service.py': '''from http.server import BaseHTTPRequestHandler,HTTPServer
import argparse,json
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200); self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"status":"ok"}')
 def log_message(self,*args): pass
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,required=True);a=p.parse_args();HTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
''',
        'test_service.py': '''import unittest
from service import Handler
class Service(unittest.TestCase):
 def test_handler(self): self.assertTrue(callable(Handler.do_GET))
''',
    },
    'runtime-gap': {
        'index.html': '''<!doctype html><html><body><button id="toggle" aria-expanded="false">Details</button><div id="details" hidden>Order details</div></body></html>\n''',
        'test_page.py': '''import unittest
from pathlib import Path
class Page(unittest.TestCase):
 def test_content(self): self.assertIn('Order details',Path('index.html').read_text())
''',
    },
}

BRIEFS = {
 'copy': 'Change only the save button text from Save to Save changes in index.html. Preserve the paragraph and other attributes. Check the result and commit this small change. Do not publish.',
 'csv': 'Add --format json to totals.py while preserving its default text output. JSON must be an object with count and total integer fields, including count=0,total=0 for an empty amount column. For malformed integer amounts or a missing amount header, print a useful error on stderr and exit nonzero without a traceback. Use only the Python standard library. Exercise the real CLI and commit the change. Do not publish.',
 'pagination': 'Fix catalog.py pagination: --offset is zero-based and --limit is the maximum result count. Pages at offsets 0 and 3 with limit 3 must cover six distinct consecutive items. Reject negative offset and limit <=0 with a readable nonzero CLI error. Preserve the existing item order and empty result beyond the end. Add regression coverage, check the real CLI and commit. Do not publish.',
 'ledger': 'Extend ledger.py with add KEY AMOUNT and total, using the same --db argument. Store integer signed amounts persistently. Repeating add with the same key and amount succeeds without duplicating the entry; reusing a key with a different amount fails without changing data. list remains a JSON array sorted by key. total prints the integer sum. Support separate process invocations and commit after checks. Use only stdlib. Do not publish.',
 'service': 'Add POST /sum to service.py. Read the expected token from SUM_TOKEN; require exactly Authorization: Bearer <token>, returning 401 when absent or wrong. Accept a JSON object with amounts, a list of integers (booleans are not integers for this API). Return JSON {"total": sum} on valid input, including empty lists. Return 400 for invalid JSON or input shape, 413 for a body exceeding 1024 bytes, and 404 for other POST paths. Preserve GET health behavior. Test through real localhost HTTP, commit, and do not publish. Use stdlib and keep bound to 127.0.0.1.',
 'runtime-gap': 'Make the Details button show/hide #details and keep aria-expanded synchronized on each click. Preserve the content. The acceptance contract requires actual browser interaction, not merely checking HTML strings. This environment has no browser runner configured; do not install one or claim a DOM/string check is a browser run. Implement and test what is available, commit, and accurately report the remaining state. Do not publish.',
}


def command(project, args, timeout=20, env=None):
    result = subprocess.run(args, cwd=project, capture_output=True, text=True,
                            timeout=timeout, env=env)
    return {'argv': args, 'exit': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def prepare(project, case):
    project = Path(project)
    project.mkdir(parents=True)
    for name, value in FIXTURES[case].items():
        (project / name).write_text(value, encoding='utf-8')
    # This project deliberately has no team tracker/setup to exercise cold use.
    if case != 'csv':
        (project / 'AGENTS.md').write_text('''# Project rules
Use only the Python standard library and local files/services. Work on a feature
branch and make work-unit commits. Preserve unrelated user work. Run
`python3 -m unittest discover -v` and the actual affected CLI/HTTP path. Do not
access external services, publish, install packages or change global settings.
''')
    (project / '.gitignore').write_text('.guide/\n__pycache__/\n*.db\n')
    (project / 'BRIEF.md').write_text(BRIEFS[case]+'\n')
    for args in [
        ['git','init','-b','main'],
        ['git','config','user.name','Fixture Developer'],
        ['git','config','user.email','fixture@example.invalid'],
        ['git','config','core.hooksPath','/dev/null'],
        ['git','add','.'], ['git','commit','-m','Initial local project'],
    ]:
        result=command(project,args)
        if result['exit']: raise RuntimeError(result)
    (project / 'personal-notes.txt').write_text('unrelated user work: preserve\n')
    return command(project,['git','rev-parse','HEAD'])['stdout'].strip()


def verify(project, case):
    """External outcome checks: no skill-internal document or method requirements."""
    project=Path(project); results=[]; assertions=[]
    def check(label, predicate): assertions.append({'check':label,'passed':bool(predicate)})
    def run(args):
        result=command(project,[sys.executable,*args]);results.append(result);return result
    try:
        if case=='copy':
            text=(project/'index.html').read_text()
            check('button text only',text==FIXTURES[case]['index.html'].replace('>Save<','>Save changes<'))
        elif case=='csv':
            for amounts in [[3,-8,17],[],[0,100,-100]]:
                path=project/'probe.csv';path.write_text('amount\n'+''.join(str(n)+'\n' for n in amounts))
                result=run(['totals.py',str(path),'--format','json'])
                check('JSON counts/sum '+repr(amounts),result['exit']==0 and json.loads(result['stdout'])=={'count':len(amounts),'total':sum(amounts)})
            result=run(['totals.py','sales.csv']);check('default preserved',result['exit']==0 and result['stdout'].strip()=='count=3 total=8')
            for content in ['amount\nwat\n','other\n4\n']:
                path.write_text(content);result=run(['totals.py',str(path),'--format','json'])
                check('readable bad-input error',result['exit']!=0 and bool(result['stderr'].strip()) and 'Traceback' not in result['stderr'])
            path.unlink(missing_ok=True)
        elif case=='pagination':
            expected=['amber','birch','cedar','dawn','elm','fern','gold']
            combined=[]
            for offset in [0,3,6,9]:
                result=run(['catalog.py','--offset',str(offset),'--limit','3']);value=json.loads(result['stdout'])
                check('page '+str(offset),result['exit']==0 and value==expected[offset:offset+3]);combined+=value
            check('full nonduplicated traversal',combined==expected)
            for args in [['--offset','-1'],['--limit','0'],['--limit','-2']]:
                result=run(['catalog.py',*args]);check('reject '+repr(args),result['exit']!=0 and 'Traceback' not in result['stderr'])
        elif case=='ledger':
            db=project/'probe.db'
            for args in [['add','b','7'],['add','a','-2'],['add','b','7']]:
                result=run(['ledger.py','--db',str(db),*args]);check('durable add '+repr(args),result['exit']==0)
            result=run(['ledger.py','--db',str(db),'add','b','99']);check('conflict rejected',result['exit']!=0)
            result=run(['ledger.py','--db',str(db),'total']);check('persisted total',result['exit']==0 and result['stdout'].strip()=='5')
            result=run(['ledger.py','--db',str(db),'list']);check('stable list',json.loads(result['stdout'])==[{'key':'a','amount':-2},{'key':'b','amount':7}])
            db.unlink(missing_ok=True)
        elif case=='service':
            import os
            with socket.socket() as sock: sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            process=subprocess.Popen([sys.executable,'service.py','--port',str(port)],cwd=project,
                                     env={**os.environ,'SUM_TOKEN':'local-fixture-token'},stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            try:
                base='http://127.0.0.1:'+str(port)
                for _ in range(60):
                    try:
                        with urllib.request.urlopen(base,timeout=.5) as response: health=json.load(response)
                        break
                    except (OSError,ValueError): time.sleep(.05)
                else: raise RuntimeError('owned local server did not become ready')
                check('GET preserved',health=={'status':'ok'})
                probes=[('/sum',b'{"amounts":[4,-1,8]}','local-fixture-token',200,{'total':11}),
                        ('/sum',b'{"amounts":[]}','local-fixture-token',200,{'total':0}),
                        ('/sum',b'{"amounts":[true]}','local-fixture-token',400,None),
                        ('/sum',b'{oops','local-fixture-token',400,None),
                        ('/sum',b'{}','wrong',401,None),('/sum',b'{}',None,401,None),
                        ('/sum',b'x'*1025,'local-fixture-token',413,None),
                        ('/missing',b'{}','local-fixture-token',404,None)]
                for path,data,token,status,body in probes:
                    headers={'Content-Type':'application/json'}
                    if token: headers['Authorization']='Bearer '+token
                    request=urllib.request.Request(base+path,data=data,headers=headers,method='POST')
                    try:
                        with urllib.request.urlopen(request,timeout=2) as response: actual=response.status;raw=response.read().decode()
                    except urllib.error.HTTPError as exc: actual=exc.code;raw=exc.read().decode()
                    results.append({'HTTP':path,'bytes':len(data),'token_present':token is not None,'status':actual,'body':raw})
                    check('HTTP '+path+' '+str(status),actual==status and (body is None or json.loads(raw)==body))
            finally:
                process.terminate()
                try: process.communicate(timeout=3)
                except subprocess.TimeoutExpired: process.kill();process.communicate()
        else:
            text=(project/'index.html').read_text();check('content preserved','Order details' in text)
            check('interaction implementation present','addEventListener' in text or 'onclick' in text)
    except Exception as exc:
        assertions.append({'check':'outcome probe completed','passed':False,'error':repr(exc)})
    note=project/'personal-notes.txt'
    check('unrelated notes preserved',note.exists() and note.read_text()=='unrelated user work: preserve\n')
    tracked=command(project,['git','ls-files','personal-notes.txt'])
    check('unrelated notes uncommitted',not tracked['stdout'].strip())
    branch=command(project,['git','branch','--show-current'])['stdout'].strip()
    status=command(project,['git','status','--porcelain'])
    commits=command(project,['git','log','--format=%h %s'])
    return {'case':case,'functional_pass':all(x['passed'] for x in assertions),
            'assertions':assertions,'actions':results,'branch':branch,'status':status,
            'commits':commits,'required_runtime':'unavailable: actual browser' if case=='runtime-gap' else 'executed',
            'limits':'HTML checks do not prove browser behavior' if case=='runtime-gap' else None}
