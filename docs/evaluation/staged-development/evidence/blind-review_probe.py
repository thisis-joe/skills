from pathlib import Path
import subprocess,sys,os,json,tempfile,socket,time,http.client
ROOT=Path(__file__).resolve().parent
results={}
def cli(d,script,*args):
 r=subprocess.run([sys.executable,'-B',str(d/script),*map(str,args)],capture_output=True,text=True,timeout=5)
 return {'code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
for d in sorted(ROOT.iterdir()):
 if not (d/'BRIEF.md').exists(): continue
 checks={};results[d.name]=checks
 if (d/'catalog.py').exists():
  for args in [[],['--offset',0,'--limit',3],['--offset',3,'--limit',3],['--offset',6,'--limit',3],['--offset',100],['--offset',-1],['--limit',0],['--limit',-1]]:
   checks[str(args)]=cli(d,'catalog.py',*args)
 elif (d/'totals.py').exists():
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'input.csv'
   for label,content in [('signed','amount\n2\n7\n-1\n'),('empty','amount\n'),('bad','amount\noops\n'),('missing','other\n3\n'),('missing_cell','other,amount\nx\n')]:
    p.write_text(content)
    for fmt in [[],['--format','json']]: checks[label+str(fmt)]=cli(d,'totals.py',p,*fmt)
 elif (d/'ledger.py').exists():
  with tempfile.TemporaryDirectory() as td:
   db=Path(td)/'data.db'
   seq=[['list'],['total'],['add','z',12],['add','a',-7],['add','zero',0],['add','z',12],['list'],['add','a',99],['list'],['total'],['add','max',2**63-1],['total']]
   for i,args in enumerate(seq): checks[str(i)+str(args)]=cli(d,'ledger.py','--db',db,*args)
 elif (d/'service.py').exists():
  with socket.socket() as sock:
   sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
  proc=subprocess.Popen([sys.executable,'-B',str(d/'service.py'),'--port',str(port)],env={**os.environ,'SUM_TOKEN':'review-token'},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  def request(method,path,body=b'',auth='Bearer review-token'):
   conn=http.client.HTTPConnection('127.0.0.1',port,timeout=3)
   try:
    conn.request(method,path,body,{} if auth is None else {'Authorization':auth})
    resp=conn.getresponse();return {'status':resp.status,'body':resp.read().decode()}
   finally: conn.close()
  try:
   for _ in range(50):
    try: checks['health']=request('GET','/health');break
    except ConnectionRefusedError: time.sleep(.02)
   cases=[('signed',b'{"amounts":[2,-7,10]}'),('empty',b'{"amounts":[]}'),('bool',b'{"amounts":[true]}'),('float',b'{"amounts":[1.0]}'),('bad_json',b'{'),('shape',b'[]'),('missing',b'{}'),('utf8',b'\xff')]
   for label,body in cases: checks[label]=request('POST','/sum',body)
   for auth in [None,'Bearer wrong','bearer review-token','Bearer review-token ']: checks['auth '+str(auth)]=request('POST','/sum',b'{"amounts":[]}',auth)
   for size in [1024,1025]: checks[str(size)]=request('POST','/sum',b'{"amounts":[]}'+b' '*(size-14))
   checks['other_post']=request('POST','/other',auth=None)
  finally:
   proc.terminate();out,err=proc.communicate(timeout=5);checks['server_stderr']=err.decode()
 elif (d/'index.html').exists():
  content=(d/'index.html').read_text()
  checks['source']=content
  if 'id="save"' in content:
   checks['exact_expected']=content=='<!doctype html><html><body><button id="save">Save changes</button><p>Saved records</p></body></html>\n'
Path('review-probes.json').write_text(json.dumps(results,indent=2))
for name,checks in results.items():
 print(name,json.dumps(checks) if 'health' in checks else str(len(checks))+' checks recorded')
