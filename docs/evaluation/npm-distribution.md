# npm 배포 준비 검증

- 날짜: 2026-10-19.
- 작업 브랜치: `feat/npm-distribution`, 기준 커밋: `1f0f370`.
- 별도 작업 공간: `/private/tmp/coco-npm-distribution`. 기존 `feat/coco-whattosay` 작업은 변경하지 않았다.
- 실행 환경: macOS, Node.js `v22.23.2`, npm `10.9.8`, Python `3.9.6`.
- 초기 준비 시점에는 npm 계정명이 없어 임시 값 `@coco-placeholder/coco-skills`와 `private: true`로 registry 게시를 차단했다.

## 초기 준비 실행 결과

| 확인 | 명령 또는 관찰 | 결과 |
|---|---|---|
| 출처·체크섬·전체 스킬 참조 | `python3 scripts/validate.py` | passed: 26 skills |
| 전체 회귀 검사 | `python3 -m unittest discover -s tests -v` (`prepack`의 `npm test`에서 실행) | passed: 32 tests, skipped 0 |
| npm 배포 파일 생성 | `npm pack --pack-destination dist --cache /private/tmp/coco-npm-cache --offline --silent` | passed: prepack 검증·전체 테스트 후 아카이브 생성 |
| 아카이브 구성 | `dist/coco-placeholder-coco-skills-0.1.0.tgz` | 3,503,740 bytes, 432 files, 26 skill entrypoints |
| 저장소 밖에서 실행 | 테스트가 빈 작업 폴더와 임시 npm cache를 사용해 오프라인 `npm exec --package=<tgz> -- coco-skills install` 실행 | passed: 실제 설치 및 설치 후 검증 |
| npx의 패키지 실행 파일 추론 | 오프라인 `npm exec -- file:<tgz> install --dry-run` | passed: `coco-skills`를 자동 선택, 설치 경로 생성 없음 |
| 파일 보호 | 재설치·외부 스킬 충돌·개인 수정·추가 파일·심볼릭 링크 테스트 | passed: npm 경유 설치와 기존 Python 설치기 검사 |
| Python 선택 및 실패 | 자동 탐색·명시 실행 파일·없는 실행 파일·Python 없는 도움말 | passed: 실패 코드는 CLI로 전달되고 부분 설치 없음 |
| 설치 경로 | 한글·공백 경로, 명시 `--dest`, `CODEX_HOME` | passed |
| 변경 자체 검토 | CLI·배포 허용 목록·아카이브·테스트·문서, `git diff --check` | passed: 작성자 자체 검토, 독립 에이전트 검토는 수행하지 않음 |
| 공개 게시 준비 상태 | `npm whoami --registry=https://registry.npmjs.org --fetch-retries=0 --fetch-timeout=10000` | unavailable: ENEEDAUTH, npm 로그인 필요 |
| 실제 공개 게시·registry 설치 | npm 계정명과 로그인 미확정 | unavailable: 게시하지 않음 |

로컬 `.tgz`의 경로를 npm exec의 첫 인자로 사용할 때는 `file:`를 붙인다. npm 10은 파일 경로만 전달하면 그 파일을 실행 명령으로 취급할 수 있다. 명시적 `--package=<tgz> -- coco-skills` 방식도 실제 설치 테스트에서 확인했다.

Linux·Windows에서의 실제 실행은 아직 검증하지 않았다. Windows Python 런처 탐색은 구현되어 있지만 이 macOS 실행 결과를 다른 운영체제의 통과 근거로 사용하지 않는다. npm registry에서 다운로드·설치가 된다는 주장은 첫 공개 게시 후 별도 확인이 필요하다.

## 0.1.0 공개 게시 후보

사용자가 npm 계정 `thisis-joe`와 공개 게시를 확정했다. 후보 커밋은 `e4ac918`이며, 패키지명은 `@thisis-joe/coco-skills`, 버전은 `0.1.0`이다. 해당 커밋에서 임시 이름과 `private` 설정을 제거했다.

- `python3 scripts/validate.py`: passed, 26 skills.
- `npm pack --pack-destination dist --cache /private/tmp/coco-npm-cache --offline --silent`: passed. prepack에서 전체 32개 테스트를 다시 실행했고 모두 통과했다.
- 정확한 게시 파일: `dist/thisis-joe-coco-skills-0.1.0.tgz`, 3,503,572 bytes, 432 files.
- SHA-256: `a1702a4f0c7e60dbf11ec77d5fb1fdc4472caf5f86c2f927def6e140f636b863`.
- npm integrity: `sha512-9MBDctCgMcX53QcNl+kLsTl0H4hmQL/x7lMXoB4oZ2Ou2AFcqSop/Jl5AHzZyZhPWIKqJzozRgR68hZ37/9/Yg==`.
- `npm view @thisis-joe/coco-skills version dist.integrity --registry=https://registry.npmjs.org`: E404. 조회 시점에 기존 공개 패키지는 없었다.
- `npm publish ./dist/thisis-joe-coco-skills-0.1.0.tgz --dry-run --json --ignore-scripts --offline`: passed. 공개 저장소의 `latest`에 게시할 이름·버전·파일 수·integrity를 확인했다.
- `npm login --registry=https://registry.npmjs.org --auth-type=web`: 브라우저 인증을 시작했고 사용자의 완료를 기다리는 중이다. 실제 게시와 registry에서의 다운로드·설치는 아직 수행하지 않았다.

인증이 끝나면 `npm whoami`가 `thisis-joe`인지 확인하고 위 아카이브를 게시한다. 게시 응답을 받지 못한 경우 같은 버전을 바로 다시 올리지 말고 registry의 버전과 integrity부터 비교한다. 공개 다운로드 검증에는 인증 정보가 없는 임시 npm 설정·캐시와 별도 설치 경로를 사용한다.

## 인증 완료 후 게시 시도

- 2026-10-19: `npm login`이 종료 코드 0과 `Logged in on https://registry.npmjs.org/.`를 반환했다. 브라우저의 인증 계정은 `thisis-joe`로 확인했다.
- 아카이브 SHA-256을 다시 확인했고 위 게시 후보의 해시와 일치했다. 코드와 게시 파일은 변경하지 않았다.
- 허용된 registry 조회 `npm view @thisis-joe/coco-skills@0.1.0 ...`는 E404를 반환했다.
- `npm whoami`와 정확한 아카이브의 `npm publish ... --access public --tag latest`는 현재 제한된 실행 환경에서 `ENOTFOUND registry.npmjs.org`로 실패했다. 승인 요청이 비활성화되어 해당 명령의 네트워크 접근을 확대할 수 없었다.
- 실제 공개 게시와 익명 다운로드·설치 확인은 아직 완료되지 않았다. 사용자 터미널에서 아카이브를 게시하거나 해당 명령의 네트워크 접근이 허용된 뒤 이어서 확인해야 한다.

## 공개 게시 확인

2026-10-19 14:05 UTC에 공개 registry 조회가 성공했다. 패키지 `@thisis-joe/coco-skills`의 버전과 `latest`는 모두 `0.1.0`이다. 사용자 터미널의 첫 게시 시도는 2FA 요구로 E403이었고, 이후 사용자가 인증 설정과 게시를 진행한 결과를 registry에서 확인했다. 현재 상태는 공개 게시 완료다.

- 패키지 페이지: <https://www.npmjs.com/package/@thisis-joe/coco-skills>.
- 공개 tarball: <https://registry.npmjs.org/@thisis-joe/coco-skills/-/coco-skills-0.1.0.tgz>.
- 비어 있는 `user.npmrc`와 `global.npmrc`, 별도 캐시를 사용한 `npm view`도 버전 `0.1.0`, `latest` `0.1.0`을 반환했다. npm 로그인 정보 없이 공개 메타데이터에 접근할 수 있다.
- registry의 SHA-512 integrity는 위의 검증한 게시 후보와 정확히 같다. 공개 파일과 설치 검증에 사용한 로컬 아카이브가 동일하다.
- 새 환경 `/private/tmp/coco-public-verify.fnjqln`에서 registry 패키지를 지정한 익명 `npm exec`는 실행 환경의 네트워크 제한으로 ENOTFOUND가 발생했다. 따라서 새 다운로드부터 이어지는 전체 설치가 통과했다고 주장하지 않는다.
- 같은 임시 환경에서 정확히 일치하는 로컬 아카이브를 오프라인 `npm exec --package=<tgz> -- coco-skills install --dest <temp>/installed`로 설치했다. 결과는 `installed`, 26 skills, 84 files다.
- 설치가 끝난 후 `python3 scripts/validate.py --installed <temp>/installed`가 26 skills, 84 files를 확인했다.
- 종료 검사 `python3 scripts/validate.py`와 `python3 -m unittest discover -s tests -v`도 다시 통과했다. 전체 32개 테스트, skipped 0이다.

사용자 설치 명령은 `npx --yes @thisis-joe/coco-skills@latest install`이다. 이 확인은 npm 공개 게시와 설치 아카이브의 동작을 대상으로 하며 Git 원격 브랜치 게시·병합을 수행했다는 뜻은 아니다. 공개 아카이브는 변경하지 않았다.
