# COCO 공개 배포

## 1.3.0 source version

Version `1.3.0` replaces coco-learn with coco-til. Session capture selects at most three concepts per topic and stores notes in the primary checkout, including recorded separate-metadata configurations. The existing note schema and checker remain unchanged. The installer removes the managed old skill and installs the new identifier; update Codex and Claude separately. See [migration and verification](coco-1.3.0.md). Source preparation and Git merging do not imply npm publication; the registry commands below remain pinned to the previously published `1.2.0` until `1.3.0` publication is independently confirmed.

## 1.2.0 published release

Version `1.2.0` adds `coco-blog` as the thirtieth skill and corrects local-note release guidance to use the consumer project's actual publication schema. Existing skill identifiers, installer commands and source provenance remain unchanged. See [release notes](coco-1.2.0.md) for verification and limits. Version `1.2.0` is now published; fresh-cache downloads match the verified archive and both runtime project installs validate. Preparing source or an archive alone still does not establish publication. Upgrade and rollback use the same installer with an explicit destination and version; preserve personal edits when preflight reports a conflict.

## 설치 인터페이스

공개 npm 패키지명은 `@thisis-joe/coco-skills`이며, 실행 명령은 `coco-skills`다. 아래 registry 명령은 해당 버전의 게시가 끝난 뒤 사용할 수 있다. 준비한 코드나 로컬 `.tgz`만으로 npm 게시 완료를 의미하지 않는다.

Node.js 22 이상과 Python 3.9 이상이 필요하다. 설치 사용자는 npm 로그인이 필요하지 않다. Node.js/npm이 없는 환경에서는 저장소를 clone하고 Python 설치기를 직접 실행할 수 있다. npm 설치와 Python 직접 설치는 같은 설치기를 사용한다.

1.1.0은 요구사항 정리 → 구현 → 리뷰·검증 → 출시의 안내, 명세 하나에 한정된 단계 자동 진행, 구현 전과 새 제약 발견 시의 중요한 선택 확인, 처음 예상과 실제 결과의 보고를 추가한다. Jira 규칙은 실제 프로젝트에서 선택한 경우에만 적용하며 기존 스킬 이름 29개와 설치 인터페이스는 유지한다. [1.0.0 대비 구체적인 변경](https://github.com/thisis-joe/skills/blob/v1.1.0/docs/coco-1.0.0-to-1.1.0.md)을 참고한다. 모델 성능·실행 속도·사람의 학습 효과를 일괄적으로 보장하지 않는다.

운영 중인 Codex 수정판의 최근 기록 격리, 실제 병합 대상 검사, 요청문 전용 안내, 티켓 게시·접수 복구, 내부 테스트 정리 조건, Markdown 예제 판별도 함께 보존한다. 공개 1.0.0과 다르게 설치돼 있던 파일을 단순히 덮어써 이전 수정을 잃지 않도록, 해당 수정과 원래 회귀 검사를 통합한다. 새 버전의 설치·검증·되돌리기는 최종 아카이브로 확인한다.

1.0.0은 원본 기법 보강(스킬별 고급 절차 읽기 조건, 멈춤 신호, clarify grill 모드, debug 전제 재검증), `coco-document`를 나눈 `coco-docs`·`coco-learn` (now `coco-til`), PR/MR 머지 스킬 `coco-merge`를 포함한 영어 스킬 문서와 공통 자료를 Codex·Claude Code에 함께 배포한다. 요청 없이 이름만 호출한 스킬은 대화에서 할 일이 정해지지 않았으면 `coco-whattosay` 요청문 추천으로 시작하고, `coco-push`·`coco-merge`는 이름만 호출해도 현재 브랜치 기준으로 바로 실행한다. 설치기는 1.0.0부터 프로젝트별 설치(`--project`), 프로젝트 설치 시 기존 글로벌 설치 제거(`--remove-global`), 설치 제거 명령(`uninstall`)을 지원한다. 실행 시간도 줄였다. 보고는 결과부터 쓰고, `coco-start`는 다음 경로만 정하며, `coco-ship`은 배포가 아닌 PR 점검에서 롤아웃 계획 대신 되돌리는 방법을 한 줄로 적는다. `coco-updateskill`은 바뀐 파일에 맞춰 검증 범위를 정한다. bash, zsh, PowerShell, cmd 어디서든 동작하는 명령 작성 규칙도 추가했다. `coco-build`는 단계마다 해당 테스트 파일만 돌리고 전체 테스트는 마무리에 한 번 실행하며, `coco-debug`는 코드로 이미 배제된 가설을 다시 시험하지 않고, `coco-verify`는 일회성 확인을 즉석 명령으로 하며, `coco-review`는 정확한 커밋 범위를 `git diff`로 보고 지적부터 쓴다. 근거는 [실행 시간 진단](evaluation/latency/README.md)과 [무거운 스킬 진단](evaluation/latency/heavy.md)에 있다. 두 런타임은 같은 29개 스킬과 `_coco-shared`를 사용하며, `agents/openai.yaml`은 Codex용 표시 메타데이터다. 설치 대상 에이전트 자체의 설치·인증은 별도다.

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime codex --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime codex
npx --yes @thisis-joe/coco-skills@latest validate --installed "${CODEX_HOME:-$HOME/.codex}/skills"
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude
npx --yes @thisis-joe/coco-skills@latest validate --installed "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
```

`--runtime`은 `codex` 또는 `claude`이며, 생략하면 기존과 같이 `codex`다. 설치 위치는 세 가지다. `--project <폴더>`는 해당 프로젝트에만 설치하며, Claude Code는 `<폴더>/.claude/skills`, Codex는 `<폴더>/.agents/skills`를 사용한다. 여러 번 지정할 수 있다. `--global`은 모든 프로젝트에 적용되는 경로에 설치한다. Codex는 `~/.codex/skills`이고 `CODEX_HOME`을 설정했다면 그 아래 `skills`를 사용한다. Claude Code는 `~/.claude/skills` 또는 `CLAUDE_CONFIG_DIR` 아래 `skills`를 사용한다. `--dest`는 두 경로보다 우선한다. Windows에서도 설치 폴더를 직접 지정할 수 있다.

위치 옵션이 없으면 터미널 실행일 때 프로젝트 설치와 글로벌 설치 중 하나를 묻는다. 프로젝트 폴더의 기본값은 현재 폴더이며, 현재 폴더가 홈 폴더이면 기본값 없이 묻는다. 받을 수 없는 폴더는 설치를 멈추지 않고 다시 묻는다. 표준 입력이 터미널이 아니면 이전 버전과 같이 글로벌로 설치한다. 질문은 표준 오류로 출력하므로 표준 출력의 JSON 결과는 그대로 유지된다. 설치 대상이 둘 이상이면 결과는 JSON 배열이다.

프로젝트 설치, 기존 글로벌 설치 정리, 제거와 버전 고정은 다음과 같다. 두 런타임에 설치하려면 각각의 `install --runtime` 명령을 모두 실행한다.

```sh
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --project ./my-project --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --project ./my-project
npx --yes @thisis-joe/coco-skills@latest validate --installed ./my-project/.claude/skills
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --project ./my-project --remove-global
npx --yes @thisis-joe/coco-skills@latest uninstall --runtime claude --project ./my-project
npx --yes @thisis-joe/coco-skills@1.2.0 install --runtime codex --dest ./my-skills
```

`--project` 설치는 설치한 폴더와 설치 기록을 해당 저장소의 `.git/info/exclude`에 저장소 루트 기준 경로로 추가한다. 공유되는 `.gitignore`는 바꾸지 않는다. Git 저장소가 아니면 이 단계를 건너뛰고 `git_exclude`를 `null`로 반환한다. 홈 폴더나 글로벌 경로와 같은 위치는 프로젝트로 받지 않는다.

프로젝트 설치 시 글로벌 설치가 있으면 터미널에서는 제거 여부를 묻고, 그 밖의 환경에서는 `--remove-global`이 있을 때만 제거한다. 제거하지 않으면 경고를 출력한다. 제거 가능 여부는 어떤 파일도 쓰기 전에 확인하고, 실제 제거는 프로젝트 설치가 성공한 뒤에 한다. `uninstall`과 같은 절차로, 소유권 기록에 있고 해시가 그대로인 파일만 지운다. 관리 폴더에 수정·추가된 파일이 있으면 멈춘다.

설치 후 Codex에서는 새 대화나 스킬 새로고침 후 `$coco-start`, Claude Code에서는 해당 프로젝트의 새 세션에서 `/` 메뉴를 확인한 뒤 `/coco-start`를 호출한다. 설치 파일 검증과 클라이언트가 실제 스킬을 읽는 확인은 구분한다. 읽기 전용 요청인 `$coco-tellmeskill coco-build 간단 설명` 또는 `/coco-tellmeskill coco-build 간단 설명`으로 인식과 호출을 확인할 수 있다. 경로·호출은 [Claude Code 스킬 문서](https://code.claude.com/docs/en/skills), 설정 경로는 [설정 문서](https://code.claude.com/docs/en/settings)를 따른다. 로컬 Claude Code 설치는 claude.ai·Cowork용 업로드 배포를 제공하지 않는다.

업데이트는 `@latest install`을 다시 실행한다. 동일한 내용은 `unchanged`를 반환하고, 관리 중인 파일을 개인적으로 바꿨거나 같은 이름의 다른 스킬이 있으면 변경 전에 중단한다. 이전 버전으로 돌아가려면 원하는 버전을 지정해 같은 명령을 실행한다. 개인 수정으로 충돌하면 기존 파일을 먼저 보관하고 별도 경로에서 새 버전을 검토한다.

CLI는 `python3`, `python`, Windows의 `py -3` 순서로 Python을 찾는다. `COCO_PYTHON`을 설정하면 해당 실행 파일만 사용한다. 값에는 인자 없이 실행 파일 이름이나 경로를 넣는다. UTF-8 모드를 사용하므로 한국어 문서도 같은 인코딩으로 처리한다.

## 배포 구조와 선택 이유

`bin/coco-skills.cjs`는 Python 버전을 확인하고 기존 `scripts/install.py` 또는 `scripts/validate.py`를 실행한다. 런타임 옵션과 명시적 경로를 Python 설치기에 전달하고, 실제 설치는 한 번만 실행하며 종료 코드를 그대로 전달한다. 기본 경로 선택도 Python 설치기가 맡는다. npm 설치 후 자동으로 스킬 폴더를 수정하는 lifecycle hook은 없다. 사용자가 `install` 명령을 실행해야 스킬이 설치된다.

`uninstall` 명령은 같은 `install.py`에 `--uninstall`을 붙여 실행하므로 배포 파일 목록은 바뀌지 않는다.

프로젝트별 설치는 모든 프로젝트에 COCO를 노출하지 않으려는 팀 요구에서 나왔다. 이미 글로벌로 설치한 팀원도 다음 업데이트에서 고를 수 있어야 하므로, 설치 경로를 묻는 질문과 글로벌 설치 정리를 함께 제공한다. 글로벌 설치를 남겨 두면 선택이 무의미해진다. [Claude Code](https://code.claude.com/docs/en/skills)는 같은 이름의 스킬이 있으면 개인 폴더를 프로젝트보다 우선하고, [Codex](https://learn.chatgpt.com/docs/build-skills)는 같은 이름의 스킬을 합치지 않고 둘 다 보여 준다. 두 런타임 모두 세션을 시작한 폴더부터 저장소 루트까지의 프로젝트 스킬 폴더를 읽는다. Git 제외는 팀 저장소에 커밋되지 않는 `.git/info/exclude`를 사용해 각자 설치 여부를 정하게 했다. 비대화형 호출의 글로벌 기본값은 기존 스크립트 호환을 위해 유지했다.

기존 설치기를 재사용해 파일 소유권, 개인 수정 보호, 설치 잠금과 복구 절차를 한곳에 유지한다. Node.js 전용 설치기로 다시 작성하는 대안은 Python이 필요 없지만, 현재 검증한 설치 규칙을 두 언어로 관리하게 되어 선택하지 않았다. Python을 사용하는 기존 Git clone/ZIP 설치는 계속 지원한다.

`package.json`의 `files` 허용 목록에는 실행 CLI, 세 Python 파일, `coco.json`, 스킬·공통 자료, 라이선스·출처 고지, 출처의 체크섬과 `.source` 증거, 필요한 안내 문서만 포함한다. 평가용 저장소와 대화 기록, 테스트, 작업 지침, Git 메타데이터는 배포하지 않는다. 출처 자료는 npm 아카이브 안에 보존하지만 스킬 설치 경로에 복사하지 않는다. `sources/`는 계속 비활성 증거다.

## 게시자 절차

첫 게시는 npm 계정 `thisis-joe`로 로그인해 진행한다. `npm login`을 실행하면 브라우저 인증을 안내하며, 브라우저에서 계정 로그인과 인증을 마친다. `npm whoami`가 `thisis-joe`를 반환하는지 확인한 뒤 게시한다. 조직의 다른 게시자를 추가하는 경우에는 해당 scope에 대한 권한을 별도로 확인한다.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
mkdir -p dist
npm pack --pack-destination ./dist
npm login --registry=https://registry.npmjs.org
npm whoami --registry=https://registry.npmjs.org
npm publish --access public
```

`npm pack`과 소스 디렉터리에서 실행하는 `npm publish`는 `prepack`에서 필수 검사와 테스트를 다시 실행한다. 이름과 파일 구성을 공개 전 검토하려면 `npm publish --dry-run`을 사용한다. 이 동작은 registry에 게시하지 않는다.

테스트는 실제 npm 아카이브를 만들고 소스 저장소 밖에서 오프라인 `npm exec --package=<아카이브>`로 설치한다. 전체 출처·참조 검증, 두 런타임의 설치 후 검증과 기본 경로, 명시적 경로 우선순위, 재설치, 외부 파일 보호, 한글·공백 경로와 Python 부재도 확인한다. 프로젝트 설치 후 Git 상태가 깨끗한지, 글로벌 설치 정리와 `uninstall`이 CLI에서 Python까지 전달되는지도 확인한다. 질문 흐름, 하위 폴더 설치의 저장소 기준 제외 경로, 수정된 글로벌 설치의 쓰기 전 중단은 Python 테스트가 확인한다. Node.js/npm이 없는 Python 전용 개발 환경에서는 npm 전용 테스트를 `skipped`로 표시하므로, 배포자는 Node.js/npm이 있는 환경에서 검사해야 한다.

게시가 성공하면 아래 명령으로 registry 버전과 설치를 확인한다. 공개 패키지 게시와 Git 원격 게시 여부는 별개다.

```sh
npm view @thisis-joe/coco-skills version dist.integrity --registry=https://registry.npmjs.org
npx --yes @thisis-joe/coco-skills@latest install --runtime codex --dry-run
npx --yes @thisis-joe/coco-skills@latest install --runtime claude --dry-run
```

다음 버전은 기능·수정에 맞게 `npm version patch`, `minor` 또는 `major`로 올린 뒤 같은 절차로 게시한다. 같은 버전 번호는 재사용하지 않는다.

## 기준 문서

- [npm package.json의 bin·files·publishConfig](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)
- [npm exec와 npx](https://docs.npmjs.com/cli/v11/commands/npm-exec/)
- [공개 scoped 패키지 게시](https://docs.npmjs.com/creating-and-publishing-scoped-public-packages/)
- [npm login의 브라우저 인증](https://docs.npmjs.com/cli/v10/commands/npm-login/)
- [npm publish와 dry-run](https://docs.npmjs.com/cli/v11/commands/npm-publish/)
