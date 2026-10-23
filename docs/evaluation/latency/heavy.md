# 무거운 네 스킬의 대기 시간 진단

[1차 진단](README.md)은 push, merge, ship, start, updateskill, docs를 다뤘고, coco-build, coco-review, coco-debug, coco-verify는 실제 사용 기록이 없어 남겨 두었습니다. 이 문서는 2026-10-22에 이 네 스킬을 같은 예제에서 스킬 미사용 실행과 비교해, 늘어난 시간을 어떤 지시문이 만들었는지와 세 원저자(Addy Osmani, Matt Pocock, pstack)가 실제로 무엇을 요구하는지 대조한 근거입니다. 조정 후 동작 확인은 [결과 기록](heavy-results.md)에 있습니다.

지시문 위치는 조정 전 `main`(d2d848d)의 `skills/` 기준 줄 번호이고, 원저자 위치는 `sources/` 아래 원본(`.source` 생략)의 줄 번호입니다.

## 방법

| 조사 | 대상 | 방식 |
|---|---|---|
| 기준 측정 | 과제 5개 × (스킬 사용 / 미사용) 각 1회 | 같은 예제를 새로 복제해 실행. 시간은 에이전트가 처음과 마지막에 찍은 `date +%s` 차이 |
| 판정 | 과제마다 판정 에이전트 1명 | 실행 폴더에서 테스트를 다시 돌리고, 보고한 주장과 심은 결함을 직접 재현. 어느 쪽이 스킬인지 알고 판정함 |
| 기록 분석 | 스킬 실행 5건과 미사용 실행 5건의 에이전트 기록 | 모델 호출 수(메시지 id 기준), 도구 시간, 단계 순서, 읽은 문서. 각 구간을 그 구간을 시킨 지시문과 연결 |
| 원저자 대조 | 네 계열에 연결된 원본 32개(`sources/coverage.json`) | 비용마다 원저자가 요구하는 문장을 찾고, 없으면 "원저자 없음" |

예제는 Python 3.9 표준 라이브러리만 쓰는 저장소 4개입니다.

- notes-app: JSON 메모 API. 심은 결함 없음.
- notes-paging: notes-app에 페이지·검색 커밋을 더하고 논리 결함 3개를 심음. 마지막 페이지가 마지막 메모를 빠뜨림, 검색이 대소문자를 구분함, PUT이 `updated_at`을 갱신하지 않음.
- ml-lab: 로지스틱 회귀 학습. 심은 결함 없음.
- ml-bug: ml-lab에 결함 2개를 심음. 분할 전에 전체 데이터로 표준화 통계를 구함(누수), 분할에 시드가 없음(정확도 테스트가 약 26~30% 확률로 실패).

보안 결함은 심지 않았습니다. 스킬 실행은 Skill 도구로 전역 설치본을 불렀고, 네 SKILL.md와 공용 파일이 `main`과 바이트 단위로 같음을 확인했습니다.

측정 지시문이 "사용한 다른 COCO 스킬"을 결과에 적게 했습니다. 그래서 review 결과의 "COCO skills used" 절과 verify 결과의 사용 절차 공개 문단은 스킬이 아니라 측정 지시문이 만든 것입니다. 아래 비용 목록에서는 뺐습니다.

## 결과 1. 차이는 build와 debug에 몰려 있다

| 과제 | 스킬 | 미사용 | 모델 호출 | 도구 시간 | 판정 |
|---|---:|---:|---|---|---|
| build: 로그인 기능 (notes-app) | 838초 | 464초 | 50 vs 25 | 208초 vs 52초 | 스킬 우세(보안) |
| build: 조기 종료 (ml-lab) | 379초 | 316초 | 37 vs 24 | 25초 vs 15초 | 미사용 우세 |
| debug: 누수와 시드 없는 분할 (ml-bug) | 489초 | 338초 | 34 vs 22 | 88초 vs 56초 | 무승부, 둘 다 두 결함 수정 |
| verify: 페이지 주장 (notes-paging) | 102초 | 79초 | 16 vs 15 | 16초 vs 9초 | 무승부, 둘 다 3/3 |
| review: 페이지 커밋 (notes-paging) | 129초 | 71초 | 15 vs 10 | 10초 vs 14초 | 무승부, 둘 다 3/3 |

- 1차 진단과 같이 대부분은 모델 호출 수입니다. 다만 build 로그인 과제는 예외로, 늘어난 374초 중 약 150초가 도구 시간이었습니다. 600,000회 PBKDF2를 그대로 쓴 테스트 묶음(한 번에 7~14초)을 슬라이스마다 다시 돌렸기 때문입니다.
- 거짓 지적은 양쪽 모두 0건입니다.

## 결과 2. 결함을 실제로 잡은 단계

비용을 줄이기 전에, 기준 측정에서 결과를 바꾼 단계부터 확인했습니다. 이 단계들은 유지합니다.

| 단계 | 근거 |
|---|---|
| build 중 coco-security 위협 점검 | 로그인·가입이 `application/json`이 아니면 415(로그인 CSRF 차단), 쿠키 헤더를 직접 파싱해 잘못된 이웃 쿠키와 CVE-2024-7592의 이차 시간 지연을 피함. 미사용 실행은 둘 다 놓침 |
| build의 커밋 전 자기 검토 | 전체 diff를 다시 읽다가 "쿠키 없는 로그아웃도 삭제 쿠키를 보냄(다른 사이트가 로그아웃시킬 수 있음)"을 찾아, 실패 테스트부터 쓰고 고침. 미사용 실행은 놓침 |
| 실패를 먼저 확인하는 테스트(red→green) | 모든 스킬 실행이 각 슬라이스의 의도한 실패를 확인함. debug 두 실행 모두 새 테스트가 원래 코드에서 실패함 |
| 실제 서버·CLI 실행 점검 | verify·review 모두 실서버에서 세 결함을 재현함 |
| 간헐 결함의 실패율 측정 | debug가 실패율(21/100)을 재고 수정 후 0/100을 보임 |
| 세 축 판정 분리 | 결과를 바꾼 사례는 없지만 결정 기록상 유지 규칙("Separate axes versus one ranked finding list") |

## 결과 3. 비용, 원인 지시문, 원저자 요구

### coco-build

| 측정한 비용 | 원인 지시문 | 원저자 요구 | 조치 |
|---|---|---|---|
| 느린 테스트를 슬라이스마다 반복(로그인: 도구 208초 vs 52초, 테스트 한 번 7~14초 vs 3초) | `coco-build/SKILL.md:35` 슬라이스 반복만 있고 반복 범위·속도 기준이 없음 | Matt `implement/SKILL.md:13` "single test files regularly, and the full test suite once at the end". Addy `test-driven-development/SKILL.md:146` "most tests should be small and fast". 해시 반복 횟수를 테스트에서 낮추라는 문장은 원저자 없음 | 반복 중에는 슬라이스의 테스트 파일만, 전체는 마무리에 한 번. 의도적으로 느린 값(해시 반복, sleep, timeout)은 매개변수로 낮추고 운영값 확인 하나는 유지(팀 추가) |
| 첫 실행에서 통과한 테스트마다 변이 확인(로그인 5개, 조기 종료 6개) | `coco-build/SKILL.md:48` 중단 신호 "see it fail for the intended reason" | Addy `test-driven-development/SKILL.md:379` 첫 통과는 경고 신호. Addy `code-review-and-quality/SKILL.md:164` 변이는 리뷰당 하나. pstack `principle-test-behavior-not-implementation/SKILL.md:11` "imagined edits". 테스트마다 실행하는 변이는 원저자 없음 | 경고 신호는 유지하고, 해당 테스트를 마무리에 scratch 실행 한 번으로 묶어 확인 |
| 리뷰 절차 전체 수행: review.md·coco-review 읽기, 범위 수집기 소스를 두 번에 나눠 읽고 두 번 실행(약 20초, 결과 변화 없음) | `coco-build/SKILL.md:37` 수집기 필수, `advanced/build.md:49` "Obtain the required review" 링크 | Matt `implement/SKILL.md:15` 커밋 전 리뷰 한 번. Addy `build.md`는 작업마다 리뷰 단계가 없음. pstack은 설계가 논쟁적일 때만. 스냅샷·해시는 원저자 없음(Matt `code-review/SKILL.md:21`은 diff 명령 하나) | 자기 검토는 유지(실제 결함을 찾음). 범위는 `git status --porcelain --untracked-files=all`과 `git diff <base>`로 잡고, 강화 작업과 의존성·공유 계약 변경만 리뷰 모드와 수집기(처음부터 강화 작업이면 고급 build 문서와 함께 읽음), 새 문맥·요청된 리뷰는 coco-review |
| curl 구동 스크립트와 증거 파일 작성 | `contracts.md:19` "artifact pointer", 검증 핵심 `advanced/verify.md:33` "Keep ... evidence together" | Addy `references/definition-of-done.md:23` 실행 확인 필요. Matt `diagnosing-bugs/SKILL.md:27` curl로 충분. pstack `principle-prove-it-works/SKILL.md:22` "Commit it only for large or complex work" | 실행 점검은 유지. 일회성 확인은 명령과 출력이 증거, 다시 돌려야 할 때만 파일 |
| 검증 핵심 문서 읽기 | `advanced/build.md:95`의 verify 링크 | 원저자 없음 | UI, 브라우저, 계정, 지속 상태를 일회용 로컬 예제 밖에서 다룰 때만 읽음 |
| 기준 측정 1회에서 조기 종료가 기본 데이터에서 한 번도 작동하지 않음. 테스트가 기본 데이터에서 항상 참이었고, 스킬은 고치지 않고 공개만 함. 조정 전후 비교에서는 네 실행 모두 작동시켜, 지시문 탓이라기보다 실행 간 편차로 봄 | 인수 점검이 "실행했다"만 요구하고 새 동작이 실제로 일어났는지는 묻지 않음 | pstack `principle-test-behavior-not-implementation/SKILL.md:13` "If the test still passes, it proves nothing". Matt `tdd/SKILL.md:31` 구성상 통과하는 테스트 금지 | 시간 비용 없는 안전망: 새 동작이 기본·실제 입력에서 일어남을 인수 점검이 보여야 하고, 아니면 미충족 |
| "no task tracker", "independence degraded" 보고 | `coco-build/SKILL.md:41` 반환 항목, `contracts.md:39` "report degraded review when independence/tools are unavailable" | 원저자 없음 | 해당 없는 항목은 생략. 독립 리뷰가 필요했는데 못 한 경우만 보고 |
| Jira 형식 브랜치 이름과 `git check-ref-format`(약 10초) | `coco-build/SKILL.md:13-30` | 원저자 없음(팀 규칙) | 바꾸지 않음. 아래 "바꾸지 않은 것" 참조 |

### coco-debug

| 측정한 비용 | 원인 지시문 | 원저자 요구 | 조치 |
|---|---|---|---|
| 수정 단계에서 build로 넘기며 문서 4개(coco-build, build.md, review.md, verify.md)를 더 읽고 build 절차(브랜치, 범위 수집기, 자기 검토) 수행 | `coco-debug/SKILL.md:20` "hand the verified fix to the build owner", `advanced/debug.md:66,73` | Matt `diagnosing-bugs/SKILL.md:126` "Apply the fix." Addy `debugging-and-error-recovery` 4단계에서 바로 수정. 둘 다 그 자리에서 고침 | 원인과 실패 테스트를 debug가 확정한 수정은 표준 build 작업. coco-build 진입 문서만 따르고 고급 문서는 나열된 조건일 때만 |
| 코드로 이미 배제되는 가설(학습·데이터 생성의 결정성) 실험, 시드 고정 실험, 400개 데이터셋 낙관도 측정(도구 32초 포함 약 90초). 수정 내용은 바뀌지 않음 | `advanced/debug.md:52-53` "Record eliminated hypotheses", "Confirm the surviving mechanism in runtime evidence" | Matt `diagnosing-bugs/SKILL.md:90` 가설 3~5개, `:102` 실험마다 예측 하나. pstack 버그 수정 절차(`poteto-mode/playbooks/bug-fix.md:8`)는 가장 많이 줄이는 분할부터. 가설마다 실험하라는 원저자 없음 | 코드나 최근 diff가 배제하는 가설은 근거 줄을 인용. 가설이 갈리면 실험 중단. 수정이 의존하지 않는 효과 크기는 재지 않음 |
| 100회 반복을 수정 전후 두 번, 중간 커밋에서 30회 더 | `advanced/debug.md:34` 실패율 측정(횟수 기준 없음) | Matt `diagnosing-bugs/SKILL.md:51` "Loop the trigger 100×"는 재현율을 높이는 방법이지 통과 기준이 아님 | 실패율 p에 맞춰 횟수를 정함. n회 연속 통과의 우연 확률 (1-p)^n, 30%면 13회로 1% 미만. 관련 변경 뒤에만 다시 실행 |
| Jira 규칙 앞에서 브랜치 이름 고민 | `coco-build/SKILL.md:26` 없는 정보는 묻게 함 | 원저자 없음 | 바꾸지 않음 |

### coco-review

| 측정한 비용 | 원인 지시문 | 원저자 요구 | 조치 |
|---|---|---|---|
| `HEAD~1..HEAD`처럼 정확한 범위인데 범위 수집기를 실행하고 그 소스(60~200줄)를 읽음 | `coco-review/SKILL.md:15` "Run the review-scope collector ... use a direct Git diff for an exact revision range"가 둘 다 하라는 뜻으로 읽힘. `advanced/review.md:17` "separately" | Matt `code-review/SKILL.md:21` diff 명령 하나. Addy `.claude/commands/review.md:7` "staged or recent commits". 스냅샷은 원저자 없음 | 정확한 범위는 `git diff <range>`와 `git status --porcelain`이 범위. 수집기는 merge-base·미커밋 범위에만 쓰고, 출력 형식을 적어 소스를 읽지 않게 함 |
| 세 축 판정 표, Limitations 절 | `coco-review/SKILL.md:22` 반환 항목 "remaining limitations", `:19` "Report degraded independence", `advanced/review.md:117` | Matt `code-review/SKILL.md:78` 두 축을 따로 제시. Addy `code-review-and-quality/SKILL.md:193` "a few high-conviction comments beat a long list", 판정은 하나. Limitations 절은 원저자 없음 | 결과 먼저(심각도 순), 판정은 축마다 한 줄, 판정의 쓰임을 바꾸는 한계만 |

### coco-verify

| 측정한 비용 | 원인 지시문 | 원저자 요구 | 조치 |
|---|---|---|---|
| 147줄 구동 스크립트 작성(약 35초). 즉석 요청이 놓친 것을 찾지 못함 | `contracts.md:19`, 검증 핵심 `advanced/verify.md:33` | pstack `create-verification-skill/SKILL.md:3-4`는 사용자가 부를 때만. `principle-prove-it-works/SKILL.md:22` 큰 작업만 커밋 | 일회성 확인은 즉석 명령과 출력이 증거. 요청, 재실행 필요, 실행 도우미 모드일 때만 스크립트 |
| 9행 판정표. 판정자는 요청한 주장과 1:1인 보고를 더 읽기 쉽다고 봄 | `coco-verify/SKILL.md:22` "claim-to-evidence matrix" | 원저자 없음 | 요청한 주장마다 판정 하나 |
| 공용 계약과 검증 핵심 읽기, 모드 표 확인 | `coco-verify/SKILL.md:11` | - | 바꾸지 않음. 실서버 점검 전 핵심 읽기는 `tests/test_source_fidelity.py`가 고정한 안전 규칙이고, 한 번에 읽으면 호출이 늘지 않음 |

## 결과 4. 원저자들은 더 짧지만, 더 느슨하지는 않다

| 계열 | 원저자 핵심 문서(단어) | COCO 조정 전 상시 읽기(단어) |
|---|---|---|
| build | Matt implement 103, Addy build 명령 612 | coco-build 797 + 공용 계약 1,187, 실제로는 build.md 1,319, review.md 1,396, verify.md 750을 더 읽음 |
| review | Matt code-review 1,086, Addy code-review-and-quality 3,334 | coco-review 488 + 계약 1,187 + review.md 1,396 |
| debug | Matt diagnosing-bugs 1,427, Addy debugging 1,690 | coco-debug 457 + 계약 1,187 + debug.md 1,403, 수정 시 build 계열 문서 추가 |

- 원저자 셋 모두 실패를 먼저 보는 테스트, 실행 확인, 실패할 수 있는 테스트를 요구합니다. 이 요구는 COCO에서도 그대로 둡니다.
- COCO가 더한 것은 대부분 절차의 겉입니다. 범위 스냅샷과 해시, 테스트마다 실행하는 변이, 슬라이스별 기록, 구동 스크립트와 증거 파일, 세 판정 표와 Limitations 절, 수정 단계의 문서 이관이 여기에 해당하며, 원저자 원본에는 없습니다.
- Addy는 생략 기준이 가장 분명합니다(`using-agent-skills/SKILL.md:164` "Not every task needs every skill"). Matt의 implement에는 "작은 작업이면" 같은 기준이 없지만, 문서 자체가 103단어입니다.

## 판단

### 바꾼 것

각 항목은 `skills/_coco-shared/decisions.md`의 행에 기록했고, 원저자에서 온 규칙을 완화한 경우 `sources/coverage.json`의 adaptation에 덧붙였습니다.

| 결정 기록 행 | 바뀐 문서 |
|---|---|
| Build loop cost versus red-to-green evidence | `coco-build/SKILL.md` 2·4단계와 중단 신호 |
| Build self-review versus the full review procedure on every task | `coco-build/SKILL.md` 4단계, `advanced/build.md` 슬라이스 8단계·마무리 1단계, `contracts.md` 독립성 보고 |
| Debug fix handoff versus reading build's whole procedure | `coco-debug/SKILL.md` 3·6단계, `advanced/debug.md` 반복 횟수와 build 이관 |
| Review scope and report shape versus exact-range reviews | `coco-review/SKILL.md` 1·5단계와 반환, `advanced/review.md` 범위·반환 |
| Verification drivers versus one-off checks | `coco-verify/SKILL.md` 2단계와 반환 |

진입 문서는 46~138단어 늘었습니다. 대신 build와 debug의 일반 경로에서 review.md(1,396단어), verify.md(750단어), 수집기 소스 읽기가 빠지도록 했습니다. 실제로 읽은 문서는 [결과 기록](heavy-results.md)에서 확인합니다.

### 바꾸지 않은 것

| 대상 | 이유 |
|---|---|
| 동작 하나마다 실패→통과 슬라이스 | Matt `tdd/SKILL.md:36`, Addy `test-driven-development/SKILL.md:51`의 공통 규칙이고 결정 기록 첫 행. 슬라이스 수가 호출 수를 늘리지만, 테스트 속도 조치로 슬라이스당 비용을 줄임 |
| coco-security 위협 점검 경로 | 측정한 보안 이점 3개가 모두 여기서 나옴 |
| 자기 검토 자체 | 실제 결함(교차 사이트 로그아웃)을 찾음 |
| 안전 계열의 "or is unclear" 고급 문서 읽기 | 1차 진단의 판단 유지 |
| verify·automate 핵심 문서의 운영 절 | `tests/test_context_loading.py`가 원문 그대로 보존을 확인함. 모드 선택 절도 4,500자 한도(현재 4,490자)에 묶여 문장을 더하지 않음 |
| Jira 형식 브랜치 이름 | 팀이 정한 규칙이고 원저자 근거가 없어 이 조정의 판단 범위 밖. 티켓 없는 debug 수정에서 이름 고민과 질문이 생긴다는 측정은 팀에 넘김 |

## 한계

- 기준 측정은 과제마다 1회이고, 판정자는 어느 쪽이 스킬인지 알았습니다. 조정 전후 비교는 사본을 가리고 2회씩 실행했습니다([결과 기록](heavy-results.md)).
- 생각 내용이 가려져 있어, 긴 공백(예: 위협 점검 뒤 58초)이 무엇에 쓰였는지는 앞뒤 도구 호출로 추정했습니다.
- 예제는 작은 Python 저장소 4개뿐입니다. TypeScript 조건, 동시 실행, 의존성 변경 리뷰는 측정하지 않았습니다.
- 정상 사용에서는 사람이 중간에 답하거나 Jira를 읽을 수 있습니다. 측정은 "묻지 말고 판단하라"는 조건에서 했습니다.
