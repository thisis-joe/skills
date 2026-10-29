"""Check that load-bearing upstream techniques stay reachable in active COCO text.

Package validation proves files and links exist. These checks pin the specific
rules a source-fidelity audit found missing or unreachable: concrete advanced
triggers, the verify core loading rule, pstack's two-fix premise rule, Addy
Osmani's stop signals, and Matt Pocock's full-frontier grill mode. Wording
checks are structural evidence only; they do not prove agent behavior.
"""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VAGUE_POINTER = 'only when the task needs their additional procedure'
ADVANCED_LINK = '](../_coco-shared/advanced/'
COMMON_SIGNALS_LINK = '](../_coco-shared/contracts.md#stop-signals)'
ADDY_TABLES = ('## Common Rationalizations', '## Red Flags')

# Each trigger term must appear in the entrypoint's loading sentence and its
# target must still exist: `file.md#Heading` (level-two/three heading) or a
# module file. Renaming a mode or dropping its trigger therefore fails here.
TRIGGERS = {
    'automate': [
        ('ci/deployment', 'automate-ci.md'),
        ('sustained execution', 'automate-sustained.md'),
        ('webhook/bot work', 'automate-webhook.md'),
        ('report intake', 'automate-intake-setup.md'),
        ('manual setup wizards', 'automate-wizard.md'),
        ('workflow specifications', 'automate-specification.md'),
    ],
    'build': [
        ('resuming interrupted work', 'build.md#Resume the actual task'),
        ('strengthened work', 'build.md#Choose a proportionate path'),
        ('domain data or state shape', 'build.md#Name the shape first'),
        ('repeatable mechanical edits', 'build.md#Repeatable edits and migrations'),
        ('typescript surface', 'build.md#TypeScript condition'),
        ('concurrent or delegated execution', 'build.md#Optional concurrent execution'),
    ],
    'clarify': [
        ('focused interview', 'clarify.md#Focused interview'),
        ('divergent ideas', 'clarify.md#Divergent-to-convergent refinement'),
        ('grill or stress-test', 'clarify.md#Grill mode'),
        ('domain term', 'clarify.md#Domain modeling'),
    ],
    'context': [
        ('task pickup', 'context.md#Task pickup'),
        ('current-chat catchup', 'context.md#Current-chat catchup'),
        ('cross-chat recall', 'context.md#Cross-chat recall'),
        ('portable handoff', 'context.md#Portable handoff and phase boundaries'),
        ('decision log', 'context.md#Decision run logs'),
        ('domain-language maintenance', 'context.md#Domain-language maintenance'),
        ('profile-only', 'context.md#Profile-only workstyle capture'),
        ('worktree or simulator cleanup', 'context.md#Conditional owned worktree and simulator cleanup'),
    ],
    'debug': [
        ('red signal', 'debug.md#Construct a red-capable feedback loop'),
        ('bisection', 'debug.md#Minimize without changing the bug'),
        ('premise', 'debug.md#Test competing causes'),
        ('existing pr or commit fix', 'debug.md#Existing-fix verification'),
        ('captured-artifact', 'debug.md#Performance and captured-artifact diagnosis'),
        ('report intake', 'debug.md#Automated report intake condition'),
    ],
    'design': [
        ('public api contract', 'design.md#Public contracts and retry safety'),
        ('idempotent', 'design.md#Public contracts and retry safety'),
        ('type-discipline', 'design.md#Type discipline'),
        ('deepening shallow modules', 'design.md#Deep interfaces and dependency strategy'),
        ('architecture opportunity survey', 'design.md#Architecture opportunity survey'),
        ('structurally different alternatives', 'design.md#Alternatives and synthesis'),
        ('disposable prototype', 'design.md#Disposable prototype mode'),
        ('package-boundary', 'design.md#Optional TypeScript package-boundary recipe'),
    ],
    'docs': [
        ('default skeletons', 'docs.md#Default skeletons'),
        ('drift audit', 'docs.md#Drift audit'),
        ('adr or glossary', 'docs.md#Decision records and domain language'),
        ('agent-facing instructions', 'docs.md#Agent-facing instructions and reusable recipes'),
        ('async discovery questionnaire', 'docs.md#Async discovery questionnaire'),
        ('course-exercise scaffolding', 'docs.md#Conditional course-exercise scaffolding'),
        ('writing collaboration', 'docs.md#Experimental writing collaboration'),
    ],
    'frontend': [
        ('new screen or open visual direction', 'frontend.md#Establish the design contract'),
        ('optimistic updates', 'frontend.md#Component and state design'),
        ('accessibility verification', 'frontend.md#Interaction and accessibility verification'),
        ('runtime finish gate', 'frontend.md#Runtime and finish gate'),
        ('visual parity', 'frontend.md#Conditional visual parity'),
        ('missing browser capability', 'frontend.md#Inputs and modes'),
    ],
    'migrate': [
        ('independently deployed consumers', 'migrate.md#Choose the mode'),
        ('production schema or data change', 'migrate.md#Production schema sequence'),
        ('destructive phase or recovery plan', 'migrate.md#Recovery and destructive phase'),
        ('integration-only branch', 'migrate.md#Expand and migrate'),
        ('typescript test-fixture migration', 'migrate.md#Conditional TypeScript fixture migration'),
    ],
    'observe': [
        ('opaque failure path', 'observe.md#Inputs and modes'),
        ('cardinality', 'observe.md#Metrics and cardinality'),
        ('distributed tracing', 'observe.md#Tracing'),
        ('alert or runbook review', 'observe.md#Alerts and runbooks'),
        ('verification of the telemetry itself', 'observe.md#Test the telemetry itself'),
        ('unavailable sink', 'observe.md#Inputs and modes'),
    ],
    'performance': [
        ('adoption-deciding benchmark', 'performance.md#Controlled experiment and decision'),
        ('query-plan', 'performance.md#Measure the actual bottleneck'),
        ('one-run ballpark', 'performance.md#Inputs and modes'),
        ('source-only inspection', 'performance.md#Inputs and modes'),
        ('sustained tuning', 'performance.md#Conditional sustained tuning'),
    ],
    'plan': [
        ('wide mechanical migration', 'plan.md#Wide mechanical migrations'),
        ('whole-spec integration', 'plan.md#Whole-spec integration and optional concurrency'),
        ('decision map', 'plan.md#Decision-map mode for large uncertainty'),
        ('bespoke investigation', 'plan.md#Bespoke investigation mode'),
    ],
    'askme': [
        ('version-specific api facts', 'research.md#API facts and documentation'),
        ('runtime mechanism', 'research.md#Runtime mechanism and ownership'),
        ('historical rationale', 'research.md#Historical rationale and defensive code'),
        ('bounded multi-source investigation', 'research.md#Input and selection'),
        ('claim-confidence', 'research.md#Claim confidence'),
        ('cited findings artifact', 'research.md#Artifact and completion'),
    ],
    'retro': [
        ('session retrospective', 'retro.md#Reconstruct the outcome'),
        ('recurring mistake class', 'retro.md#Recurring-error prevention procedure'),
        ('maintained instructions', 'retro.md#Reflection into maintained procedures'),
        ('work-environment audit', 'retro.md#Examine the environment'),
    ],
    'review': [
        ('review-scope collector', 'review.md#Freeze the actual scope'),
        ('dependency or lockfile', 'review.md#Dependency changes'),
        ('safety facts', 'review.md#Impact and safety-fact mode'),
        ('adversarial review', 'review.md#Bounded adversarial mode'),
        ('automated review comments', 'review.md#Automated-review comment triage'),
        ('suppressions', 'review.md#Comments and constraints condition'),
    ],
    'security': [
        ('full threat pass', 'security.md#Threat model before controls'),
        ('install scripts', 'security.md#Dependency script gate'),
        ('user-influenced urls', 'security.md#Server fetches and destructive paths'),
        ('model output', 'security.md#AI and runtime effects'),
        ('personal-data', 'security.md#Secrets and personal data'),
        ('git command guard', 'security.md#Conditional Git command guard setup'),
    ],
    'ship': [
        ('version preparation', 'ship.md#PR and version preparation'),
        ('dependent pr stack', 'ship.md#Conditional dependent PR stack'),
        ('error-budget', 'ship.md#Rollout and SLO budget gate'),
        ('post-deploy proof', 'ship.md#Rollback and post-deploy proof'),
        ('pr supervision', 'ship.md#Conditional PR supervision modes'),
    ],
    'simplify': [
        ('structural responsibility change', 'simplify.md#Inputs and conditional modes'),
        ('legacy internal api', 'simplify.md#Migrate callers before deleting legacy APIs'),
        ('purpose or history is unclear', 'simplify.md#Establish what must remain true'),
        ('codemod', 'simplify.md#Choose a concrete simplification'),
    ],
    'spec': [
        ('capability map', 'spec.md#Conditional capability decomposition'),
        ('revision of an existing agreement', 'spec.md#Input and mode'),
        ('project guidance', 'spec.md#Project guidance and constraints'),
        ('measurable acceptance', 'spec.md#Test seams and validation'),
        ('tracker publication', 'spec.md#Save and hand off'),
    ],
    'start': [
        ('standing quality bar', 'start.md#Establish a standing bar'),
        ('quality-floor', 'start.md#Quality floor'),
        ('ratchets', 'start.md#Ratchets and checking cost'),
        ('package-manager signals', 'start.md#Discover before asking'),
        ('pstack playbook', 'start.md#Former pstack playbook coverage'),
    ],
    'triage': [
        ('label and state mapping', 'triage.md#Canonical roles and discovery'),
        ('agent or human brief', 'triage.md#Durable agent and human briefs'),
        ('already-built', 'triage.md#Rejection, duplicates and already-built behavior'),
        ('automated intake', 'triage.md#Configured automated intake: fail-closed preflight'),
    ],
    'verify': [
        ('standing-quality audits', 'verify-quality-audit.md'),
        ('runtime-helper', 'verify-runtime-create.md'),
        ('formal-verification', 'verify-formal-create.md'),
        ('workflow experiments', 'verify-experiments.md'),
        ('pre-commit setup', 'verify-pre-commit.md'),
    ],
}

VERIFY_CORE_ENTRY = (
    'Read the [verification core](../_coco-shared/advanced/verify.md) before driving a UI, browser, '
    'live service, account or persistent state, designing behavioral checks',
    'once read, the whole core applies even if no mode matches',
)
AUTOMATE_CORE_ENTRY = (
    'Read the [automation core](../_coco-shared/advanced/automate.md) before preparing or changing '
    'anything that runs on a schedule or trigger, runs unattended, retries, or writes externally',
    'once read, the whole core applies even if no mode matches',
)
CORE_ROUTER = 'Once loaded, apply the entire core even without module matches.'
# Both routers' cores must load wherever their rules matter, not only on a module match.
CORE_LOADING = {'verify': VERIFY_CORE_ENTRY, 'automate': AUTOMATE_CORE_ENTRY}

PREMISE_ENTRY = ('two fixes sharing one premise fail the same gate', 'before any third fix',
                 '](../_coco-shared/advanced/debug.md#test-competing-causes)')
PREMISE_RULE = ('When two fixes sharing a premise fail the same gate, write and test that premise '
                'before trying a third', 'would differ if it were false',
                'trace one why deeper')

GRILL_MECHANICS = (
    'Ask the whole frontier in one round',
    'belongs to a later round',
    'Number each question',
    'recommended answer',
    'Word each question so "yes" accepts that recommendation',
    'A pending lookup blocks only the questions downstream of it',
    'End only when the frontier is empty',
    'the user confirms the shared understanding',
    'Do not act on the result before that confirmation',
)


def sections(text, level='##'):
    """Map each heading at `level` to its body up to the next same-level heading."""
    pattern = re.compile(r'^%s ([^\n]+)\n' % level, re.MULTILINE)
    matches = list(pattern.finditer(text))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1).strip()] = text[match.end():end]
    return result


def headings(text):
    return {line.split(' ', 1)[1].strip() for line in text.splitlines()
            if re.match(r'^#{2,3} ', line)}


def bullets(body):
    return [line for line in body.splitlines() if line.startswith('- ')]


def loading_sentence(text):
    """The entrypoint paragraph that decides when advanced guidance is read."""
    for paragraph in text.split('\n\n'):
        if ADVANCED_LINK in paragraph:
            return paragraph
    return ''


def addy_table_families(root):
    """Families whose Addy sources carry rationalization or red-flag tables."""
    coverage = json.loads((root / 'sources/coverage.json').read_text(encoding='utf-8'))
    family = {(row['author'], row['path']): row for row in coverage['entries']}
    found = {}
    for source in sorted((root / 'sources/addy/skills').glob('*/SKILL.md.source')):
        if any(marker in source.read_text(encoding='utf-8') for marker in ADDY_TABLES):
            row = family[('addy', 'skills/%s/SKILL.md' % source.parent.name)]
            found[source.parent.name] = row
    return found


def inspect_source_fidelity(root=ROOT):
    root = Path(root)
    skills = root / 'skills'
    advanced = skills / '_coco-shared/advanced'
    failures = []

    def fail(code, detail):
        failures.append((code, detail))

    def entry(name):
        return (skills / ('coco-' + name) / 'SKILL.md').read_text(encoding='utf-8')

    # 1. Advanced reachability: no vague pointer; named triggers with live targets.
    for path in sorted(skills.glob('coco-*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        if VAGUE_POINTER in text:
            fail('vague-advanced-pointer', path.parent.name)
        sentence = loading_sentence(text)
        if sentence and 'check for' not in sentence:
            fail('advanced-trigger-missing', path.parent.name)
        name = path.parent.name[len('coco-'):]
        if sentence and name not in TRIGGERS:
            fail('advanced-trigger-unmapped', path.parent.name)
    for name, pairs in TRIGGERS.items():
        sentence = loading_sentence(entry(name)).lower()
        for term, target in pairs:
            if term not in sentence:
                fail('advanced-trigger-term', '%s: %s' % (name, term))
            filename, _, heading = target.partition('#')
            module = advanced / filename
            if not module.is_file():
                fail('advanced-trigger-target', '%s: %s' % (name, target))
            elif heading and heading not in headings(module.read_text(encoding='utf-8')):
                fail('advanced-trigger-target', '%s: %s' % (name, target))

    # 2. Split-router cores load where their rules matter and apply once loaded.
    for name, phrases in CORE_LOADING.items():
        sentence = loading_sentence(entry(name))
        for phrase in phrases:
            if phrase not in sentence:
                fail('core-entry', '%s: %s' % (name, phrase))
        selection = sections((advanced / (name + '.md')).read_text(encoding='utf-8')).get('Mode selection', '')
        if CORE_ROUTER not in selection:
            fail('core-router', name)

    # 3. pstack attack-the-premise is routed from the debug procedure.
    procedure = sections(entry('debug')).get('Procedure and output', '')
    step = next((line for line in procedure.splitlines() if line.startswith('6. ')), '')
    for phrase in PREMISE_ENTRY:
        if phrase not in step:
            fail('premise-route', phrase)
    causes = sections((advanced / 'debug.md').read_text(encoding='utf-8')).get('Test competing causes', '')
    for phrase in PREMISE_RULE:
        if phrase not in causes:
            fail('premise-rule', phrase)

    # 4. Addy's rationalization/red-flag tables survive as stop signals.
    contract = sections((skills / '_coco-shared/contracts.md').read_text(encoding='utf-8'))
    if len(bullets(contract.get('Stop signals', ''))) < 5:
        fail('common-stop-signals', 'contracts.md')
    for source, row in sorted(addy_table_families(root).items()):
        name = row['family']
        body = sections(entry(name)).get('Stop signals', '')
        if len(bullets(body)) < 3:
            fail('family-stop-signals', '%s (from %s)' % (name, source))
        if COMMON_SIGNALS_LINK not in body:
            fail('family-stop-signals-link', name)
        reference = 'skills/coco-%s/SKILL.md#stop-signals' % name
        if reference not in row['implemented_references']:
            fail('stop-signals-coverage', '%s: %s' % (source, reference))
    decisions = (skills / '_coco-shared/decisions.md').read_text(encoding='utf-8')
    if 'Addy rationalization and red-flag tables' not in decisions:
        fail('stop-signals-decision', 'decisions.md')

    # 5. Matt's grilling keeps its mechanics in an explicit, discoverable mode.
    clarify = (advanced / 'clarify.md').read_text(encoding='utf-8')
    grill = sections(clarify).get('Grill mode', '')
    for phrase in GRILL_MECHANICS:
        if phrase not in grill:
            fail('grill-mechanics', phrase)
    if '| Grill mode |' not in sections(clarify).get('Select a conditional mode', ''):
        fail('grill-selection', 'clarify.md mode table')
    if 'Ask one focused question' not in sections(clarify).get('Focused interview', ''):
        fail('focused-default', 'clarify.md')
    description = next((line for line in entry('clarify').splitlines()
                        if line.startswith('description: ')), '')
    for word in ('grilled', 'stress-tested'):
        if word not in description:
            fail('grill-discovery', word)
    if '](../_coco-shared/advanced/clarify.md#grill-mode)' not in entry('clarify'):
        fail('grill-route', 'coco-clarify procedure')
    if 'Matt full-frontier grilling' not in decisions:
        fail('grill-decision', 'decisions.md')

    # 6. A repeated heading splits one mode into competing rule sets, and its
    # anchor silently resolves to the first copy only.
    for path in sorted(skills.rglob('*.md')):
        seen = set()
        for line in path.read_text(encoding='utf-8').splitlines():
            if re.match(r'^#{1,6} ', line):
                if line in seen:
                    fail('duplicate-heading', '%s: %s' % (path.relative_to(skills), line))
                seen.add(line)
    return failures


class SourceFidelityTests(unittest.TestCase):
    def assert_clean(self, root=ROOT):
        failures = inspect_source_fidelity(root)
        self.assertEqual(failures, [], '\n'.join('%s: %s' % item for item in failures))

    def isolated_package(self):
        self.assert_clean()
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        shutil.copytree(ROOT / 'skills', root / 'skills')
        shutil.copytree(ROOT / 'sources/addy', root / 'sources/addy')
        shutil.copy2(ROOT / 'sources/coverage.json', root / 'sources/coverage.json')
        self.assert_clean(root)
        return root

    def assert_detected(self, root, code):
        failures = inspect_source_fidelity(root)
        self.assertIn(code, [kind for kind, _ in failures], failures)

    def edit(self, path, old, new):
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text, 'Fixture must contain the text this mutation changes')
        path.write_text(text.replace(old, new), encoding='utf-8')

    def test_active_text_retains_audited_source_rules(self):
        self.assert_clean()

    def test_every_addy_table_maps_to_a_family_with_stop_signals(self):
        found = addy_table_families(ROOT)
        self.assertEqual(len(found), 24)
        self.assertEqual(len({row['family'] for row in found.values()}), 20)
        self.assertNotIn('using-agent-skills', found)

    def test_vague_advanced_pointer_is_detected(self):
        root = self.isolated_package()
        path = root / 'skills/coco-design/SKILL.md'
        sentence = loading_sentence(path.read_text(encoding='utf-8'))
        self.edit(path, sentence, 'Read the [common contract](../_coco-shared/contracts.md) before acting. '
                  'Load [advanced modes](../_coco-shared/advanced/design.md) ' + VAGUE_POINTER + '.')
        self.assert_detected(root, 'vague-advanced-pointer')
        self.assert_detected(root, 'advanced-trigger-term')

    def test_renamed_mode_without_trigger_update_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/_coco-shared/advanced/debug.md',
                  '## Existing-fix verification', '## Patch confirmation')
        self.assert_detected(root, 'advanced-trigger-target')

    def test_conditional_only_verify_core_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/coco-verify/SKILL.md', VERIFY_CORE_ENTRY[0], 'Read the core when needed')
        self.assert_detected(root, 'core-entry')

    def test_conditional_only_automate_core_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/coco-automate/SKILL.md', AUTOMATE_CORE_ENTRY[0], 'Read the core when needed')
        self.assert_detected(root, 'core-entry')

    def test_unqualified_core_claim_in_router_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/_coco-shared/advanced/automate.md', CORE_ROUTER,
                  'Apply the common contract and entire core even without matches.')
        self.assert_detected(root, 'core-router')

    def test_unrouted_premise_rule_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/coco-debug/SKILL.md', PREMISE_ENTRY[0], 'a fix fails')
        self.assert_detected(root, 'premise-route')

    def test_dropped_family_stop_signals_are_detected(self):
        root = self.isolated_package()
        path = root / 'skills/coco-security/SKILL.md'
        text = path.read_text(encoding='utf-8')
        path.write_text(text[:text.index('\n## Stop signals')] + '\n', encoding='utf-8')
        self.assert_detected(root, 'family-stop-signals')

    def test_softened_grill_mode_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/_coco-shared/advanced/clarify.md',
                  GRILL_MECHANICS[0], 'Ask one question at a time')
        self.assert_detected(root, 'grill-mechanics')

    def test_repeated_mode_heading_is_detected(self):
        root = self.isolated_package()
        path = root / 'skills/_coco-shared/advanced/frontend.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n## Conditional visual parity\n\nCompeting copy.\n')
        self.assert_detected(root, 'duplicate-heading')

    def test_undiscoverable_grill_mode_is_detected(self):
        root = self.isolated_package()
        self.edit(root / 'skills/coco-clarify/SKILL.md',
                  ', or when the user wants a plan, decision or idea grilled or stress-tested', '')
        self.assert_detected(root, 'grill-discovery')


if __name__ == '__main__':
    unittest.main()


class TilAdoptionTests(unittest.TestCase):
    def test_teaching_override_keeps_frozen_rules_and_current_owner(self):
        rows = json.loads((ROOT / 'sources/coverage.json').read_text())['entries']
        teaching = [r for r in rows if r['family'] == 'til']
        self.assertEqual(len(teaching), 3)
        for row in teaching:
            self.assertTrue(row['essential_rules'])
            self.assertIn('no longer adopted', row['team_override'])
            self.assertIn('skills/coco-til/SKILL.md', row['implemented_references'])
        self.assertFalse((ROOT / 'skills/_coco-shared/advanced/learn.md').exists())
