# COCO 공개 배포

## 설치 인터페이스

공개 npm 패키지명은 `@thisis-joe/coco-skills`이며, 실행 명령은 `coco-skills`다. 아래 registry 명령은 해당 버전의 게시가 끝난 뒤 사용할 수 있다. 준비한 코드나 로컬 `.tgz`만으로 npm 게시 완료를 의미하지 않는다.

Node.js 22 이상과 Python 3.9 이상이 필요하다. 설치 사용자는 npm 로그인이 필요하지 않다.

```sh
npx --yes @thisis-joe/coco-skills@latest install --dry-run
npx --yes @thisis-joe/coco-skills@latest install
npx --yes @thisis-joe/coco-skills@latest validate --installed "$HOME/.codex/skills"
```

기본 경로는 `~/.codex/skills`이고 `CODEX_HOME`을 설정했다면 그 아래 `skills`를 사용한다. `--dest`가 기본 경로보다 우선한다. Windows에서도 설치 폴더를 직접 지정할 수 있다.

```sh
npx --yes @thisis-joe/coco-skills@latest install --dest ./my-skills
npx --yes @thisis-joe/coco-skills@latest validate --installed ./my-skills
npx --yes @thisis-joe/coco-skills@0.1.0 install --dest ./my-skills
```

업데이트는 `@latest install`을 다시 실행한다. 동일한 내용은 `unchanged`를 반환하고, 관리 중인 파일을 개인적으로 바꿨거나 같은 이름의 다른 스킬이 있으면 변경 전에 중단한다. 이전 버전으로 돌아가려면 원하는 버전을 지정해 같은 명령을 실행한다. 개인 수정으로 충돌하면 기존 파일을 먼저 보관하고 별도 경로에서 새 버전을 검토한다.

CLI는 `python3`, `python`, Windows의 `py -3` 순서로 Python을 찾는다. `COCO_PYTHON`을 설정하면 해당 실행 파일만 사용한다. 값에는 인자 없이 실행 파일 이름이나 경로를 넣는다. UTF-8 모드를 사용하므로 한국어 문서도 같은 인코딩으로 처리한다.

## 배포 구조와 선택 이유

`bin/coco-skills.cjs`는 Python 버전을 확인하고 기존 `scripts/install.py` 또는 `scripts/validate.py`를 실행한다. 실제 설치는 한 번만 실행하고 종료 코드를 그대로 전달한다. npm 설치 후 자동으로 스킬 폴더를 수정하는 lifecycle hook은 없다. 사용자가 `install` 명령을 실행해야 스킬이 설치된다.

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

테스트는 실제 npm 아카이브를 만들고 소스 저장소 밖에서 오프라인 `npm exec --package=<아카이브>`로 설치한다. 전체 출처·참조 검증, 설치 후 검증, 재설치, 외부 파일 보호, 한글·공백 경로, Python 부재와 기본 경로 선택도 확인한다. Node.js/npm이 없는 Python 전용 개발 환경에서는 npm 전용 테스트를 `skipped`로 표시하므로, 배포자는 Node.js/npm이 있는 환경에서 검사해야 한다.

게시가 성공하면 아래 명령으로 registry 버전과 설치를 확인한다. 공개 패키지 게시와 Git 원격 게시 여부는 별개다.

```sh
npm view @thisis-joe/coco-skills version dist.integrity --registry=https://registry.npmjs.org
npx --yes @thisis-joe/coco-skills@latest install --dry-run
```

다음 버전은 기능·수정에 맞게 `npm version patch`, `minor` 또는 `major`로 올린 뒤 같은 절차로 게시한다. 같은 버전 번호는 재사용하지 않는다.

## 기준 문서

- [npm package.json의 bin·files·publishConfig](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)
- [npm exec와 npx](https://docs.npmjs.com/cli/v11/commands/npm-exec/)
- [공개 scoped 패키지 게시](https://docs.npmjs.com/creating-and-publishing-scoped-public-packages/)
- [npm login의 브라우저 인증](https://docs.npmjs.com/cli/v10/commands/npm-login/)
- [npm publish와 dry-run](https://docs.npmjs.com/cli/v11/commands/npm-publish/)
