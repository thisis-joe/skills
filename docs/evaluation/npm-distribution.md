# npm 배포 준비 검증

- 날짜: 2026-10-19.
- 작업 브랜치: `feat/npm-distribution`, 기준 커밋: `1f0f370`.
- 별도 작업 공간: `/private/tmp/coco-npm-distribution`. 기존 `feat/coco-whattosay` 작업은 변경하지 않았다.
- 실행 환경: macOS, Node.js `v22.23.2`, npm `10.9.8`, Python `3.9.6`.
- 패키지명은 npm 계정명 확정 전 임시 값 `@coco-placeholder/coco-skills`다. `private: true`로 registry 게시를 차단한다.

## 실행 결과

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
