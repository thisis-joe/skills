from pathlib import Path
import json, difflib, urllib.request, tarfile, io, hashlib, subprocess, shutil
r=Path('/tmp/lets-conditional-validation/case2-fixtures'); (r/'before').mkdir(parents=True); (r/'proposed').mkdir(); (r/'evidence').mkdir()
package={'name':'fixture-migration-case','private':True,'packageManager':'npm@10.9.2','type':'module','scripts':{'test':'node --experimental-strip-types --test request.test.ts','typecheck':'tsc --noEmit'},'devDependencies':{'typescript':'5.7.3'}}
(r/'package.json').write_text(json.dumps(package,indent=2)+'\n')
(r/'package-lock.json').write_text(json.dumps({'name':package['name'],'lockfileVersion':3,'packages':{'':{'name':package['name'],'devDependencies':package['devDependencies']},'node_modules/typescript':{'version':'5.7.3'}}},indent=2)+'\n')
(r/'ci.yml').write_text('steps:\n  - run: npm ci --ignore-scripts\n  - run: npm run typecheck\n  - run: npm test\n')
production='''export type Request = {
  body: { id: string };
  method: string;
  headers: Record<string, string>;
};
export function getUser(request: Request): string {
  if (typeof request.body.id !== "string") throw new TypeError("id must be string");
  return request.body.id;
}
export function auditRequest(request: Request): string {
  return `${request.method}:${request.headers["x-trace"]}:${request.body.id}`;
}
'''
for d in ['before','proposed']: (r/d/'request.ts').write_text(production)
before='''import { strict as assert } from "node:assert";
import { test } from "node:test";
import { getUser, auditRequest, type Request } from "./request.ts";

test("partial fixture preserves id", () => {
  assert.equal(getUser({ body: { id: "u-123" } } as Request), "u-123");
});
test("invalid id is rejected", () => {
  assert.throws(() => getUser({ body: { id: 123 } } as unknown as Request), /id must be string/);
});
test("full request fields are observed", () => {
  assert.equal(auditRequest({ body: { id: "u-123" }, method: "GET", headers: { "x-trace": "trace-7" } }), "GET:trace-7:u-123");
});
'''
after=before.replace('import { getUser, auditRequest, type Request }','import { fromPartial, fromAny, fromExact } from "@total-typescript/shoehorn";\nimport { getUser, auditRequest }').replace('getUser({ body: { id: "u-123" } } as Request)','getUser(fromPartial({ body: { id: "u-123" } }))').replace('getUser({ body: { id: 123 } } as unknown as Request)','getUser(fromAny({ body: { id: 123 } }))').replace('auditRequest({ body: { id: "u-123" }, method: "GET", headers: { "x-trace": "trace-7" } })','auditRequest(fromExact({ body: { id: "u-123" }, method: "GET", headers: { "x-trace": "trace-7" } }))')
(r/'before/request.test.ts').write_text(before); (r/'proposed/request.test.ts').write_text(after)
(r/'migration.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/request.test.ts',tofile='b/request.test.ts')))
# Inspect the registry tarball as data; never install/run package scripts or create node_modules.
meta=json.load(urllib.request.urlopen('https://registry.npmjs.org/@total-typescript%2fshoehorn/0.1.2'))
meta_evidence={k:meta.get(k) for k in ['name','version','types','exports','scripts','dist','repository']}
(r/'evidence/published-package-metadata.json').write_text(json.dumps(meta_evidence,indent=2)+'\n')
data=urllib.request.urlopen(meta['dist']['tarball']).read()
assert hashlib.sha1(data).hexdigest()==meta['dist']['shasum']
with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tar:
    decl=tar.extractfile('package/dist/index.d.ts').read().decode()
(r/'evidence/published-index.d.ts.txt').write_text(decl)
checks={'package_version':'0.1.2','registry_sha1_matched':True,'exports_found':{name:name in decl for name in ['fromPartial','fromAny','fromExact']},'all_helpers_test_only':True,'production_sha256_before':hashlib.sha256(production.encode()).hexdigest(),'production_sha256_after':hashlib.sha256((r/'proposed/request.ts').read_bytes()).hexdigest(),'package_installation':'not performed','proposed_typecheck':'unavailable: TypeScript and local project dependencies absent','proposed_test':'unavailable: shoehorn not installed','negative_mutation':'unavailable: migrated test cannot run against real shoehorn without installation'}
(r/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
# Run the exact project tests before/after to expose the true availability.
commands=[(['node','--experimental-strip-types','--test','request.test.ts'],r/'before','before-test'),(['node','--experimental-strip-types','--test','request.test.ts'],r/'proposed','proposed-test'),(['npm','run','typecheck'],r,'typecheck')]
run=[]
for cmd,cwd,label in commands:
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    (r/'evidence'/f'{label}.txt').write_text(p.stdout+p.stderr)
    run.append({'command':cmd,'cwd':str(cwd),'exit':p.returncode,'output':f'evidence/{label}.txt'})
(r/'evidence/commands.json').write_text(json.dumps(run,indent=2)+'\n')
(r/'PLAN.md').write_text('''# Test fixture migration proposal
Owner: lets-migrate, coordinated test-only refactor; lets-build owns an eventual real-project work-unit commit. No dependencies installed and no real project files modified.

Consumer map: request.test.ts passes the partial valid request to getUser, the intentionally invalid numeric id to the same public function, and all fields to auditRequest. getUser reads only body.id; auditRequest reads method, x-trace and body.id. No wire/stored data/mixed-deployment consumer is present in this fixture. The unchanged request.ts hash is recorded in checks.json.

Before/after migration.diff replaces the one partial `as Request` with fromPartial, the negative `as unknown as Request` with fromAny (id remains number 123, assertion remains throws), and wraps the complete request with fromExact. The intended result type is contextually inferred by the original function parameter. Helpers remain in the test. A pre-existing typed builder would be retained; none exists in this supplied fixture.

Package manager evidence: fixture packageManager, package-lock and CI all choose npm; fixture lock is a minimal inventory, not an installable complete lock. Requested package is @total-typescript/shoehorn 0.1.2. [Official API](https://github.com/total-typescript/shoehorn) and exact [published registry metadata](https://registry.npmjs.org/@total-typescript%2fshoehorn/0.1.2) support the helper exports; saved published declarations were read from its integrity-checked tarball, never installed or executed. GitHub v0.1.2 source URL returned 404; the published tarball is the exact-version evidence.

Next work, only after dependency addition is authorized: inspect exact package lifecycle scripts/transitives; use the pinned npm scripts-disabled dependency policy, add a development dependency plus generated authoritative lockfile, then apply the test-only diff as one green batch. Do not hand-edit a production lock from this fixture. Verify npm run typecheck and npm test with the real package, then remove the getUser validation only in a disposable copy and require the unchanged negative test to fail. Restore the validation afterward. Run the real repository closure checks and return evidence to build for commit. Reverting this test diff and the owned dependency/lock change is the recovery; no data backfill is involved. Removal gate: zero obsolete casts in the requested file, compiler/affected tests green and mutation proves negative-test sensitivity.

Current result: proposal prepared; successful fixture pre-migration runtime tests do not prove migrated tests compile or pass. Actual after-test fails on missing @total-typescript/shoehorn and actual typecheck fails on missing tsc. Those are unavailable required checks, not a broken API finding and not a pass. Mutation of the migrated negative path was not performed because the test cannot run with the real missing package. Full real-project compatibility remains unverified.
''')
print(json.dumps({'case':2,'version':meta['version'],'commands':run,'exports':checks['exports_found']}))
