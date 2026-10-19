from pathlib import Path
import hashlib,json
ROOT=Path('/tmp/coco-updateskill-validation')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
initial=json.loads((ROOT/'instruction-source-hashes.before.json').read_text())
final={p:sha(Path(p)) for p in initial}
(ROOT/'instruction-source-hashes.after.json').write_text(json.dumps(final,indent=2)+'\n')
assert initial==final,'Instruction or tool source changed during bounded application'
results={'kind':'one bounded application','not_claimed':['benchmark','broad certification','independent behavioral review','external service execution'],'fixture_authorship':'self-authored temporary package, requests and checks','scope':'Three cases only; writes restricted to /tmp/coco-updateskill-validation; no repository/global/user-installation writes, external writes, real user questions or spawned agents.','git_isolation':{'GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_CONFIG_NOSYSTEM':'1','identity':'fixture-only local git config','hooks':'fixture-only core.hooksPath=/dev/null','HOME_or_CODEX_HOME_repurposed':False},'instruction_source_hashes_unchanged':initial==final,'instruction_hashes_before':str(ROOT/'instruction-source-hashes.before.json'),'instruction_hashes_after':str(ROOT/'instruction-source-hashes.after.json'),'setup_failure':{'status':'repaired','detail':'Initial fixture construction failed before creating the scripts/ directory. Recreated only the incomplete temp case-a fixture after fixing setup.py.','evidence':str(ROOT/'setup-repair.txt')},'cases':{}}
rows=[]
for case in ['case-a','case-b','case-c']:
    cr=ROOT/case;b=json.loads((cr/'before.json').read_text());a=json.loads((cr/'after.json').read_text())
    commands=[json.loads(s) for s in (cr/'commands.jsonl').read_text().splitlines()]
    checks=[]
    for c in commands:
        if c['argv'][0]=='python3':checks.append({'argv':c['argv'],'exit_code':c['exit_code'],'stdout':c['stdout'],'stderr':c['stderr']})
    preserved=['sources/synthetic/build.source','sources/manifest.json','skills/coco-build/agents/openai.yaml','skills/coco-review/agents/openai.yaml']
    assert all(b['source_hashes'][p]==a['source_hashes'][p] for p in preserved)
    userpaths=['unrelated-user-note.md','user-only-skill/SKILL.md']
    assert all(b['installed_hashes'][p]==a['installed_hashes'][p] for p in userpaths)
    tool_copy_hashes={f:sha(cr/'package'/'scripts'/f) for f in ['validate.py','install.py','package_utils.py']}
    assert all(tool_copy_hashes[f]==initial['/Users/Joseph/workspaces/skills/scripts/'+f] for f in tool_copy_hashes)
    summary={'status':a['status'],'source_location':str(cr/'package'),'installed_location':str(cr/'installed'),'branch':a['branch'],'base_commit':b['base_commit'],'head':a['head'],'work_unit_commit':a['commit'],'git_status':a['git_status'],'installation_status':a['installation_status'],'changed_source_paths':a['changed_source_paths'],'checks':checks,'expected_installer_rejection':case=='case-c','source_original_manifest_and_UI_preserved':True,'unrelated_user_hashes':{p:{'before':b['installed_hashes'][p],'after':a['installed_hashes'][p]} for p in userpaths},'source_original_hash':{'before':b['source_hashes']['sources/synthetic/build.source'],'after':a['source_hashes']['sources/synthetic/build.source']},'ownership_manifest_hash':{'before':b['ownership_manifest_sha256'],'after':a['ownership_manifest_sha256']},'tool_copy_hashes':tool_copy_hashes,'full_before_hashes':str(cr/'before.json'),'full_after_hashes':str(cr/'after.json'),'command_log':str(cr/'commands.jsonl'),'request':str(cr/'request.md'),'change_basis':str(cr/'change-basis.md'),'independent_review':{'status':'unavailable','reason':'Application constraint prohibited spawning agents; this is direct author inspection with self-authored fixtures.'},'external_service_behavior':{'status':'not-applicable','reason':'Local-only skill-maintenance scope.'}}
    if case=='case-a':
        summary['installed_managed_files_match_source']=all(a['source_hashes']['skills/'+p]==h for p,h in a['installed_hashes'].items() if p in json.loads((cr/'installed/.coco-install.json').read_text())['files'])
        summary['source_diff']=str(cr/'source-change.diff')
        summary['managed_installation_files']=8
    elif case=='case-b':
        summary['source_hashes_exactly_unchanged']=b['source_hashes']==a['source_hashes']
        summary['installed_hashes_exactly_unchanged']=b['installed_hashes']==a['installed_hashes']
        summary['proposal']=str(cr/'proposal.md')
        summary['installation_attempts_after_request']=0
        summary['note']='The install command in commands.jsonl is fixture setup before the proposal request, not an installation response to the proposal.'
    else:
        summary['installed_hashes_exactly_unchanged']=b['installed_hashes']==a['installed_hashes']
        summary['user_modified_managed_file_hash']={'path':'coco-build/SKILL.md','before':b['installed_hashes']['coco-build/SKILL.md'],'after':a['installed_hashes']['coco-build/SKILL.md']}
        summary['blocker']=a['blocker']
        summary['actual_install_attempted_after_failed_preflight']=False
        summary['conflict_diff']=str(cr/'preserved-installed-user-change.diff')
        summary['source_diff']=str(cr/'source-change.diff')
    results['cases'][case]=summary
    rows.append('| '+case.upper()+' | '+a['status']+' | '+(a['commit'][:12] if a['commit'] else 'none')+' | '+a['installation_status']+' |')
(ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
report='''# Bounded coco-updateskill application

One direct application to three self-authored temporary cases. This is not a benchmark, broad certification, or an independent behavioral evaluation. No author chat or other evaluation reports were read. All writes stayed under this temporary root. No real user question, agent spawn, remote push, deployment, service write, global install or maintained repository edit occurred.

## Instruction sources and fixture

Applied the maintained `skills/coco-updateskill/SKILL.md`, `references/team-update.md` and `_coco-shared/contracts.md` read from `/Users/Joseph/workspaces/skills`. Their starting/final hashes, plus the allowed installer/checker source hashes, are captured in `instruction-source-hashes.before.json` and `.after.json`; all are equal. Checker/installer copies in every fixture are byte-identical to those starting files.

Each fixture is a two-entrypoint maintained COCO package with registration/UI metadata, shared contract and existing decisions, a synthetic inert original plus manifest checksum and coverage facts, actual AGENTS.md/CI commands, three preservation/package unit tests, an owned local installation, an unrelated note and an unrelated personal skill. Git uses /dev/null global/system configuration and only fixture-local identity/hooks settings; HOME and CODEX_HOME are untouched.

## Results

| Case | Actual outcome | Work-unit commit | Installation |
| --- | --- | --- | --- |
'''+ '\n'.join(rows)+'''

A replaced universal pytest with discovered project checks, retaining conditional scope for other projects. The shared caller-impact rule lives once in the shared contract and is linked by both entrypoints and references. Exactly eight scoped maintenance files changed. Existing D001 explains why upstream behavior was adapted; D002 explicitly identifies the new team convention. Source bytes, source manifest checksum, original essential_rules, names/discovery/UI policy/dependencies remain intact. The supported dry-run and install succeeded. The installed validator passed for two skills/eight files; every managed installed file hash matches its source. Both unrelated user files were preserved.

B produced `case-b/proposal.md` with replacement rule text, explicit affected paths, provenance treatment and eventual check/install impact. Maintained-source and installed-file hashes, branch and HEAD remain exactly unchanged. No work-unit commit or installation was attempted for the proposal. Baseline installation in its log belongs to fixture setup, before this request.

C made the same validated scoped source change on a feature branch and committed it. The supported installer dry-run exited 2: `Preserving user-modified or extra file: coco-build/SKILL.md`. Installation remains blocked. No subsequent install, force operation or ownership-manifest rewrite was attempted. Every installed byte, including the personal managed-file edit and unrelated files, remains identical to its pre-update state. `case-c/preserved-installed-user-change.diff` preserves the exact user change. No supported conflict-resolution decision was available within the bounded request, so source completion and installation completion remain distinct.

## Actual checks and evidence

Each baseline and each applicable source result ran `python3 scripts/validate.py` (two skills, source checksums/coverage/references) and `python3 -m unittest discover -s tests -v` (three tests, all pass). A/C also passed `git diff --check` before an atomic commit. A used supported `install.py --root <fixture> --dest <fixture-install> --dry-run`, then the actual install and `validate.py --installed <fixture-install>`. C used the same supported preflight and preserved its expected rejection. Full argv/cwd/exit/output records are in each `commands.jsonl`; full source/installed SHA-256 maps are in each `before.json`/`after.json`. `results.json` supplies structured summaries and evidence paths.

Inspected final diffs and actual A installed contract, B proposal and unchanged hashes, and C user conflict diff and preflight output. Direct inspection confirms both caller links, single rule ownership, provenance distinction, clean worktrees and scoped commits. The fixture tests check package validity and preserved source/UI facts; they do not prove behavior across arbitrary projects or future requests. No independent reviewer or external-service behavior was claimed because the application constraint prohibited agents and the scope was local.

## Setup failure retained

Initial fixture setup failed because scripts/ had not been created before copying the allowed checker files. Fixed setup.py and recreated only the incomplete temporary case-a directory. This happened before baseline/application evidence; it is retained in `setup-repair.txt` and results.json and is not counted as a skill outcome. No checker was weakened or bypassed.
'''
(ROOT/'report.md').write_text(report)
print(json.dumps({'report':str(ROOT/'report.md'),'results':str(ROOT/'results.json'),'instructions_unchanged':True,'case_statuses':{c:r['status'] for c,r in results['cases'].items()}},indent=2))
