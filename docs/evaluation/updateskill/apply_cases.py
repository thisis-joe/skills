from pathlib import Path
import hashlib,json,os,subprocess
ROOT=Path('/tmp/coco-updateskill-validation')
ENV=dict(os.environ,GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',GIT_CONFIG_NOSYSTEM='1',PYTHONDONTWRITEBYTECODE='1')
for name in list(ENV):
    if name.startswith('GIT_CONFIG_KEY_') or name.startswith('GIT_CONFIG_VALUE_') or name=='GIT_CONFIG_COUNT': ENV.pop(name)
def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot(path):
    return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '.git' not in p.relative_to(path).parts and '__pycache__' not in p.parts}
def run(case,args,cwd,expected=0):
    p=subprocess.run(args,cwd=cwd,env=ENV,text=True,capture_output=True)
    r={'argv':args,'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    with (ROOT/case/'commands.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    if p.returncode!=expected:raise RuntimeError(r)
    return r
NEW_CONTRACT='''# Fixture common contract

## Checks

Discover the current project's required checks from its repository instructions and CI. For this maintained COCO package, those facts require `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. Run them before completion and record each command, inspected snapshot, exit result and evidence pointer. In another project, use that project's discovered checks; these COCO commands are conditional on this package.

## Shared procedure impact

Before committing a shared procedure change, inspect both registered entrypoints and their linked references. Record which callers change and which behavior is preserved. This team rule is owned here; entrypoints refer to it rather than defining separate copies. An inspected diff and passing focused checks do not imply remote publication or unrelated product work is complete.

## Ownership

Use a feature branch and atomic work-unit commits. Preserve user edits. Upstream files are inert evidence.
'''
NEW_DECISIONS='''# Fixture rule decisions

- D001, revised for the current maintained package: Replace the synthetic upstream unconditional `pytest -q` requirement with [repository-specific check discovery](contracts.md#checks). AGENTS.md and .github/workflows/checks.yml both require the current validator and unittest commands. The former unconditional command is no longer adopted; original source bytes, checksum and essential_rules remain historical facts in coverage. This applies to shared check selection used by build and review, with the COCO command examples conditional on this maintained package.
- D002, new team convention: [Shared procedure impact](contracts.md#shared-procedure-impact) requires inspecting both registered callers and linked references before a shared-rule commit. This has no claimed upstream source. Build/review identity, invocation policy, dependencies, permission scope and user files remain unchanged.
'''
REQUEST_A='''Explicit application request: Adapt the existing maintained coco-build skill to this package's current AGENTS.md/CI commands. The team common rule is to inspect both registered entrypoints and their linked references for every shared procedure edit, record affected callers and preserved behavior, and retain evidence. Keep that rule in the shared owner. Preserve skill identities, discovery, UI policy/dependencies, source facts and unrelated user files. Make the scoped maintenance commit on a feature branch and refresh the already-known local fixture installation using the supported installer. This is local-only; there is no request to push, deploy or message anyone.
'''
for case in ['case-a','case-b','case-c']:
    cr=ROOT/case;pkg=cr/'package';dest=cr/'installed'
    before=json.loads((cr/'before.json').read_text())
    write(cr/'request.md',REQUEST_A if case=='case-a' else ('Proposal-only request: Review how to improve existing coco-build check selection for the current team package. Give a concrete modification proposal and caller/provenance/installation impact only. Do not change maintained source or installed files, and do not commit or install.\n' if case=='case-b' else REQUEST_A+'\nAdditional state: the known installed coco-build/SKILL.md contains a personal user modification. Preserve it; do not force installation or rewrite ownership hashes. A source commit is allowed independently of installation, and any unresolved conflict must be reported as blocked.\n'))
    write(cr/'change-basis.md','''# Bounded change basis

| Current behavior | Desired team behavior | Preserve | Evidence |
| --- | --- | --- | --- |
| Shared contract unconditionally requires pytest -q, repeated in both caller references | Discover repository checks; use this maintained package's actual validator and unittest facts conditionally | Other projects use their own command facts, caller identity and permission scope remain unchanged | AGENTS.md, CI, actual commands and source/installed reads |
| No shared caller-impact step | Shared owner requires both registered callers and their linked references inspected | One authoritative shared rule | coco.json, rg caller search, final diff and linked references |
| Source coverage claims merged unconditional pytest | Coverage marks adapted behavior and keeps original essential_rules | Frozen original, source manifest checksum | Before/after hashes and actual validator |

The request is concrete and supplies scope; no real user question is needed. Read-only proposals do not authorize source edits. This application does not execute the maintained build/review procedures against a product or publish anything.
''')
    if case=='case-b':
        proposal='''# Concrete proposal only

Replace the `Checks` paragraph in `skills/_coco-shared/contracts.md` with:

```text
'''+NEW_CONTRACT.split('## Checks\n\n')[1].split('\n\n## Shared procedure impact')[0]+'''
```

Add a single shared `Shared procedure impact` section:

```text
'''+NEW_CONTRACT.split('## Shared procedure impact\n\n')[1].split('\n\n## Ownership')[0]+'''
```

Update both `coco-build` and `coco-review` entrypoint links and `references/team-checks.md` to refer to those shared sections; remove each repeated legacy pytest example. Change README's package example to the repository's two actual commands. Revise D001 to explain the current project facts, and add D002 as a new team convention with no invented upstream attribution. Change coverage disposition to `adapted`, revise its adaptation explanation, and list both caller implementations. Preserve `essential_rules`, original snapshot, source manifest, names/frontmatter/UI/policy/dependencies, and unrelated user files.

Source impact: two entrypoints, two linked references, shared contract, existing decisions, README and coverage. An eventual implementation would run the package validator and unittest suite, commit the validated work unit on a feature branch, then dry-run and apply the supported installer to the already-known local destination. The present request authorizes no source edit, commit or installation. The installed bundle and source remain exactly as inspected.
'''
        write(cr/'proposal.md',proposal)
        run(case,['python3','scripts/validate.py'],pkg)
        run(case,['python3','-m','unittest','discover','-s','tests','-v'],pkg)
        outcome={'status':'proposal-only-complete','installation_status':'unchanged-no-install-attempt','commit':None,'changed_source_paths':[],'proposal_path':str(cr/'proposal.md')}
    else:
        run(case,['git','switch','-c','feature/adapt-team-checks'],pkg)
        write(pkg/'skills/_coco-shared/contracts.md',NEW_CONTRACT)
        write(pkg/'skills/_coco-shared/decisions.md',NEW_DECISIONS)
        for skill in ['coco-build','coco-review']:
            p=pkg/f'skills/{skill}/SKILL.md'
            p.write_text(p.read_text().replace('for check selection and file ownership.', 'for check selection, shared procedure impact and file ownership.'))
            write(pkg/f'skills/{skill}/references/team-checks.md',"# Team checks\n\nUse the [common checks](../../_coco-shared/contracts.md#checks) and [shared procedure impact](../../_coco-shared/contracts.md#shared-procedure-impact). Current commands are discovered from the project, and the common contract owns the maintained package example. Preserve the caller's scope and permissions.\n")
        p=pkg/'README.md'
        p.write_text(p.read_text().replace('Legacy team skill check example: `pytest -q`.', 'For this maintained package, run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`, as required by AGENTS.md and CI. See the shared contract for conditional check selection and caller-impact review.'))
        p=pkg/'sources/coverage.json'
        data=json.loads(p.read_text());row=data['entries'][0]
        row['disposition']='adapted'
        row['adaptation']='D001 revised: unconditional upstream pytest command replaced by repository-specific check discovery because current AGENTS.md/CI require validate.py and unittest. Original essential_rules remain source facts. Shared caller-impact review is a new team rule D002, with no upstream attribution.'
        row['implemented_references']=['skills/_coco-shared/contracts.md#checks','skills/_coco-shared/decisions.md','skills/coco-build/SKILL.md','skills/coco-review/SKILL.md','skills/coco-build/references/team-checks.md','skills/coco-review/references/team-checks.md']
        p.write_text(json.dumps(data,indent=2)+'\n')
        run(case,['python3','scripts/validate.py'],pkg)
        run(case,['python3','-m','unittest','discover','-s','tests','-v'],pkg)
        run(case,['git','diff','--check'],pkg)
        diff=run(case,['git','diff','--','README.md','skills','sources/coverage.json'],pkg)['stdout']
        write(cr/'source-change.diff',diff)
        refs=run(case,['rg','-n','Checks|pytest|shared procedure|contracts.md|allow_implicit|tools:','skills','README.md','sources/coverage.json'],pkg)['stdout']
        write(cr/'caller-and-rule-inspection.txt',refs)
        changed=run(case,['git','diff','--name-only'],pkg)['stdout'].splitlines()
        expected=['README.md','skills/_coco-shared/contracts.md','skills/_coco-shared/decisions.md','skills/coco-build/SKILL.md','skills/coco-build/references/team-checks.md','skills/coco-review/SKILL.md','skills/coco-review/references/team-checks.md','sources/coverage.json']
        assert changed==expected,(case,changed)
        run(case,['git','add','--']+changed,pkg)
        run(case,['git','commit','-m','fix: adapt shared checks and caller impact to team package'],pkg)
        commit=run(case,['git','rev-parse','HEAD'],pkg)['stdout'].strip()
        dry=run(case,['python3','scripts/install.py','--root',str(pkg),'--dest',str(dest),'--dry-run'],pkg,expected=2 if case=='case-c' else 0)
        if case=='case-a':
            installed=run(case,['python3','scripts/install.py','--root',str(pkg),'--dest',str(dest)],pkg)
            run(case,['python3','scripts/validate.py','--installed',str(dest)],pkg)
            outcome={'status':'source-and-install-complete','installation_status':json.loads(installed['stdout'])['status'],'commit':commit,'changed_source_paths':changed}
        else:
            assert 'Preserving user-modified or extra file: coco-build/SKILL.md' in dry['stderr']
            old=run(case,['git','show',before['base_commit']+':skills/coco-build/SKILL.md'],pkg)['stdout']
            import difflib
            write(cr/'preserved-installed-user-change.diff',''.join(difflib.unified_diff(old.splitlines(True),(dest/'coco-build/SKILL.md').read_text().splitlines(True),fromfile='baseline-managed/coco-build/SKILL.md',tofile='preserved-installed/coco-build/SKILL.md')))
            outcome={'status':'source-complete-install-blocked','installation_status':'blocked-user-modified-managed-file','commit':commit,'changed_source_paths':changed,'blocker':dry['stderr'].strip(),'actual_install_attempted':False,'reason':'Supported installer dry-run rejected conflicting managed content; no bypass or ownership rewrite attempted.'}
    after={'head':run(case,['git','rev-parse','HEAD'],pkg)['stdout'].strip(),'branch':run(case,['git','branch','--show-current'],pkg)['stdout'].strip(),'git_status':run(case,['git','status','--porcelain=v1'],pkg)['stdout'],'source_hashes':snapshot(pkg),'installed_hashes':snapshot(dest),'ownership_manifest_sha256':sha(dest/'.coco-install.json'),**outcome}
    for key in ['sources/synthetic/build.source','sources/manifest.json']:
        assert before['source_hashes'][key]==after['source_hashes'][key]
    for skill in ['coco-build','coco-review']:
        key=f'skills/{skill}/agents/openai.yaml'
        assert before['source_hashes'][key]==after['source_hashes'][key]
    for key in ['unrelated-user-note.md','user-only-skill/SKILL.md']:
        assert before['installed_hashes'][key]==after['installed_hashes'][key]
    if case in ['case-b','case-c']:
        assert before['installed_hashes']==after['installed_hashes']
        assert before['ownership_manifest_sha256']==after['ownership_manifest_sha256']
    if case=='case-b':
        assert before['source_hashes']==after['source_hashes']
        assert before['base_commit']==after['head']
        assert after['branch']=='main'
    if case=='case-a':
        manifest=json.loads((dest/'.coco-install.json').read_text())
        for rel,h in manifest['files'].items():
            assert sha(pkg/'skills'/rel)==sha(dest/rel)==h
        assert not (dest/'.coco-install.lock').exists()
    assert after['git_status']=='',after['git_status']
    write(cr/'after.json',json.dumps(after,indent=2)+'\n')
    print(case+': '+outcome['status']+'; '+outcome['installation_status'])
