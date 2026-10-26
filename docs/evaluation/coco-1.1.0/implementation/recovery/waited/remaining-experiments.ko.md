# 1.1.0 비교 실험: 완료한 첫 사례와 남은 11건 인수인계

기록일: 2026-10-26. **사용자가 “현재 첫 실험만 마치고 나머지는 나중에 이어받게 기록한 뒤, 1.1.0을 푸시·머지·배포·설치”하도록 범위를 변경했다.** 따라서 지금은 추가 개발 실험을 실행하지 않는다. 이 문서는 후속 실행 준비와 원본 보존 기록이며, 배포 완료 확인서는 아니다.

## 지금 어디까지 확인했나

첫 사례 `84bc1e8e980b`는 **current `622975e` / 정책0**이다. 이번 900초 코호트에서 후보 1.1.0의 실험은 아직 한 건도 실행하지 않았다. 첫 사례는 5개 개발 응답을 정상 완료했고, 마지막 실제 CLI 공개 검증은 통과했다. 다음 순서가 시작되기 전에 사용자가 보류한 11개 프로젝트를 다른 위치로 옮겨 호출을 막았다. 11건 모두 모델 개발 호출 0회이며 파일 내용과 모드가 동일하다.

그러나 첫 시도의 품질이 처음부터 좋았다는 뜻은 아니다. 2턴에서 완료를 보고했을 때 SKU 대소문자 처리·저장/표시 및 정수 범위 3검사가 실패했다. 미리 정한 1회의 수정 요청으로 원래 요구를 전달한 뒤 3턴부터 공개 검증이 통과했다. 3·4턴에는 기존 데이터의 `A`/`a` 충돌 처리에 대한 추가 질문이 있었고, owner 도구는 기존 충돌/공개 계약을 반복했다. 마지막 응답은 그 추가 정책이 아직 미결정이라고 밝혔다. **`stable=true`는 정상 실행의 표시이며, 모든 정책 합의·독립 리뷰 통과·비교 우위를 뜻하지 않는다.**

개발 모델이 보고한 18개 테스트와 별도 CLI 검증, 동일 모델의 자체 리뷰, 로컬 커밋은 원문에 보존됐다. 별도의 oracle도 최종 CLI 동작을 확인했다. 첫 사례의 협업 절차 평가는 독립 판정과 실제 질문/답변 구간 검토가 필요하다. 보류된 11건을 실패나 성공으로 세지 않는다.

원본 `STOP`의 `driver_failure/FileNotFoundError`는 다음 프로젝트의 의도적 경로 보류로 생겼다. 첫 사례나 서버의 실패가 아니다. 원문은 삭제하지 않았고 원인을 별도 기록했다.

## 12건이 필요한 이유와 정확한 남은 순서

12개의 서로 다른 앱을 만드는 실험이 아니다. 같은 작은 CSV 카탈로그 앱에 **5가지 사업 규칙을 적용해 current와 candidate를 각각 실행하는 10건**, 저장된 결정과 미결정 상태를 이어받는 **candidate 보존 검사 2건**이다. 같은 규칙의 두 실행을 짝으로 비교해야 지침 차이를 검토할 수 있다. 한 정책에서 우연히 잘 맞은 기본값을 일반 개선으로 오해하지 않기 위해 다른 정책을 둔다.

현재 완료한 current/정책0을 다시 실행하지 않는다. 다음 candidate/정책0이 첫 비교 짝을 만들므로 즉시 얻는 정보가 가장 크다. 이후 8건은 규칙 다양성, 마지막 2건은 결정과 권한의 보존을 확인한다. 원래 교차 순서를 유지한다.

| 남은 순서 | 원래 ID | 지침 | 정책 / 종류 | 목적 |
|---|---|---|---|---|
| 1 | `92939b26c0af` | candidate | 0 / primary | 같은 조건의 첫 비교 짝 완성: 다음에 할 가치가 가장 큼 |
| 2 | `14748d0d9f45` | candidate | 1 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 3 | `e941fcf5b704` | current | 1 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 4 | `8f8760555804` | current | 2 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 5 | `c09d72460dc8` | candidate | 2 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 6 | `1f304b47dcab` | candidate | 3 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 7 | `532b61bd3d9a` | current | 3 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 8 | `c179a281123b` | current | 4 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 9 | `511b0525594b` | candidate | 4 / primary | 서로 다른 사업 규칙에서 같은 절차가 작동하는지 |
| 10 | `8e994b95cf19` | candidate | 0 / known | 저장된 결정·변경 이유를 복구하고 진행하는지 |
| 11 | `9320926d1ade` | candidate | 0 / unknown | 미결정인 선택을 확정했다고 꾸미지 않고 질문하는지 |

사업 규칙은 다음과 같다. SKU 양끝 공백 제거와 저장/출력 형태도 계약에 포함된다.

| 정책 | SKU 동일성/저장 | 중복 처리 | 잘못된 행 |
|---|---|---|---|
| 0 | 대소문자 통합·소문자 저장 | 마지막 행/기존 값 갱신 | 파일 전체 거부 |
| 1 | 대소문자 구분·원문 대소문자 저장 | 첫 행/기존 값 유지 | 잘못된 행 건너뛰기 |
| 2 | 대소문자 통합·소문자 저장 | 중복 오류 | 잘못된 행 건너뛰기 |
| 3 | 대소문자 구분·원문 대소문자 저장 | 마지막 행/기존 값 갱신 | 파일 전체 거부 |
| 4 | 대소문자 통합·소문자 저장 | 첫 행/기존 값 유지 | 파일 전체 거부 |

`known`은 정책0이 이미 명세와 계획에 기록된 상태다. “처음에는 대소문자를 유지하려 했지만 공급업체가 대소문자 변형을 보내므로 소문자로 바꾸었다”는 변경 이유까지 복구해야 한다. `unknown`은 중복·잘못된 행·정수 범위만 정해졌고 SKU 동일성은 미결정이다. 숨겨진 정책0 값을 답으로 주지 않으며, 그 결정에 의존하는 작업을 진행하면 안 된다.

## 다음 실행에서도 유지할 조건

- current 소스: `622975e349e6276b225aa9ef02ee69d664dd2927`. candidate 소스: `cd728cd1cbf8afe4740f68a8bf91a924fee574c4`. 현재 체크아웃/최신 npm 지침으로 갈아끼우지 않는다. `.guide` 파일별 해시는 `control.json`의 `manifests`에 전부 있으며 candidate는 118개다. 이 비교의 current는 `622975e`이다. 0.2.0/스킬 미사용 및 별도의 release `84a59a2` 결과와 혼합하지 않는다.
- 실제 개발 actor와 질문 분류기 모두 `gpt-6.1-sol`, reasoning `high`. CLI는 `codex-cli 0.164.0-alpha.11.1`. 매 호출의 실제 세션에 새로 기록된 모델/추론 강도를 검증한다. 모델 이름이 같아도 나중에 서버 내부 모델이 같다는 증거는 되지 않는다. Luna/Astra는 사용하지 않는다. 후속 독립 판정 모델은 Sol 계열로 별도 기록한다.
- 동시에 한 프로젝트/한 호출만 실행하며 모델 호출 시작 간격은 최소 30초다. 개발 호출의 일반 실행 예산은 900초, owner 분류기는 90초다. 서버가 실제 공지한 429 재시도 구간만 별도로 계산해 호출당 최대 1,800초, 이어지는 전체 cohort 최대 5,400초의 대기를 허용한다. 벽시계 상한은 각각 2,700/1,890초다. 공지 대기 구간의 중복을 제거하고 실제 경과한 부분만 계산한다. 이는 대기 추정치이며 모델 계산 시간 측정값은 아니다. 실패하면 자동으로 예산을 더 늘리거나 새 성공 시도로 교체하지 않는다.
- 한 과제 최대 5개 개발 응답, 실제 질문에 대한 일반 답변 최대 3회, 사전 정의된 수정 요청 최대 1회, 사실을 추가하지 않는 계속 진행 요청 최대 1회다. 정상적으로 이어지는 동일 과제의 응답은 같은 세션을 쓴다. 과거 중단된 actor를 재개하거나 다른 성공으로 대체하지 않는다.
- actor는 임시 프로젝트와 로컬 `.guide`만 사용한다. 개인/전역 스킬, 부모 폴더, 다른 실험, 원본 아카이브, 제어 파일을 읽지 않는다. 중첩 에이전트·외부 서비스·설치·전역 변경·푸시는 금지다. 해당 기능의 구현→테스트→공개한 자체 리뷰→실행 검증→로컬 작업 단위 커밋까지 자동 진행이 이미 허용되었다. 중요한 제품 선택은 owner에게 묻는다. 이 조건의 자체 리뷰를 독립 리뷰라고 주장하지 않는다.
- owner 분류기는 실제 최종 질문만 분류하고 정답/arm은 보지 않는다. 프로파일 값은 분류 결과에 맞춰 결정론적으로 전달한다. 계약 밖 선택은 미결정으로 남긴다. classifier의 유효 JSON은 답변의 의미가 맞다는 증거가 아니므로 독립 판정자가 질문 원문과 답변을 대조해야 한다. 첫 사례의 legacy 충돌 질문 반복도 그대로 검토 대상이다.

공개 계약은 Python 표준 라이브러리, UTF-8 `sku,name,price_cents` CSV, 비어 있지 않은 SKU/이름, 음수가 아닌 정수 cents, `python3 catalog.py --db PATH import CSV_PATH`와 기존 `list` 유지다. `list`는 저장 SKU 기준으로 정렬된 JSON 배열이며 price는 정확한 JSON 정수다. 새 가격 상한을 추가하지 않는다. `9223372036854775808`과 `1208925819614629174706183`도 정확히 왕복해야 한다. 빈 입력은 기존 자료를 보존하고, 실패는 읽을 수 있는 stderr 및 0이 아닌 종료 상태를 남긴다. summary/다중 공급업체 기능은 범위 밖이다.

oracle은 복사본에서 실제 CLI를 실행해 정상 import, 프로파일별 동일성/중복/표시/오류 처리, 기존 자료 보존, 큰 정수 왕복을 검사한다. actor 원본 상태를 바꾸지 않았는지 검사한다. 최종 코드만 보지 않고 이전 응답별 실패와 수정도 남긴다.

독립 판정은 소스/지침 이름을 숨긴 패킷의 실제 응답·질문/답변·Git/코드·실행 결과를 본다. 8개 축은 사용자 결정권, 구체적인 질문, 알려진 선택 복구, 필요한 절차, 완료 주장의 사실성, 최초 예상 보고, 실제 선택 보고, 변경 이유/영향 보고다. 각 축 0/1/2 또는 근거가 있는 null이며 합산 총점을 만들지 않는다. 수정 에피소드와 미승인 선택을 별도 센다. 잘못된 출력에도 완료라고 주장하는 대조 사례와 브라우저 검증 없이 완료라고 주장하는 대조 사례를 거부해야 한다. 대조 2건은 개발 실험 12건에 포함되지 않는다. 자세한 기준은 동결된 `revision2/collect.py`의 `REVIEW` 원문을 유지한다.

## 보존 자료와 현재 비용

현재 원본 폴더는 `/private/tmp/coco-v110-budget900-20261026T1300Z`다. OS가 임시 폴더를 정리할 수 있으므로 인수인계 기준은 아래 저장소 아카이브다. 원래 절대 경로가 로그에 남아 있어도 새 실행 기록으로 바꾸어 쓰지 않는다.

| 저장소의 `evidence/` 파일 | SHA-256 | 내용 |
|---|---|---|
| `budget900-first-native.tar.gz` | `8d82a766cbf012b78677634f1bac721ad8da5321ca934bcfb6cd2d23e1873e5e` | 첫 사례·원본 STOP·보류 11프로젝트·동결 입력·owner·모든 호출 원본, 2,865파일 |
| `budget900-first-blind-ungraded.tar.gz` | `0985670e623422beceb0c6318ac9bfcf28a6dfb10746f934026b2437e96ba8ad` | 첫 사례와 미실행11 및 오류 검출 대조2의 미채점 패킷, 627파일 |
| `waited-clock-failure-native.tar.gz` | `9a1a7f9862c9fe753ec3ef948252d735edc09d8dc0dfbd64929df623240a002f` | 원래 control4개 통과, 시계 계측 오류로 개발 호출0 |
| `waited-budget-stop-native.tar.gz` | `d4e1afd14de2c730053a47657984d0945cbcf42ccc03c6b76dd500faa2bbdca6` | 420초 예산에서 중단된 별도 과거 시도 |
| `waited-budget-stop-blind-ungraded.tar.gz` | `cd891ac3ffa3011e508ba83293544871c9fb2b1e8097293970735a2e506c9c32` | 420초 시도의 미채점 패킷 |

각 `*-manifest.json`은 모든 파일의 해시와 모드를 기록한다. 아카이브를 다시 읽어 전 파일을 검증했다. 실제 control 원본과 재사용 경로는 `reused-controls.json` 및 `budget900-control-provenance.json`에 있다. 초기/후속 recovery 시도의 원본·실패는 각 이전 보고서에 남아 있으며 새 성공으로 바꾸지 않는다.

이번 첫 사례는 개발5+owner5=**새 모델 호출10회**였다. 호출 시간 합은 **1,303.946초**, 첫 시작부터 마지막 종료까지 **1,367.377초(약22.8분)**, 공지된 429 대기는 0초였다. control4회는 재사용하여 추가 호출/중복 비용으로 세지 않았다. 앞선 waited 단계의 9회(그 control4회 포함)를 더하면 이 waited 복구 연쇄는 총19회, native 시간 합2,340.903초이며, 더 이전 cohort 비용까지 포함한 프로젝트 전체 비용은 아니다. 원시 토큰 usage는 이어지는 세션에서 누적일 수 있으므로 단순 합산하지 않았다. 과금액이나 순수 모델 계산 시간을 추정하지 않는다.

추적한 10개 CLI PID는 모두 종료됐다. 임의로 만들어진 별도 자식 프로세스 전체의 부재까지 확인했다는 의미는 아니다. 원시 비용/상태는 `evidence/budget900-first-outcome.json`, 별도 점검은 `budget900-first-root-inspection.json`을 본다.

## 복원 및 나중의 실행 명령

`prepare_remaining.py`는 기본적으로 **오프라인 준비만** 한다. 새 출력 폴더가 이미 존재하면 거부한다. 고정 아카이브 SHA, 모든 파일의 해시/모드, 경로 안전성, 22개 동결 입력, 보류 프로젝트, 첫 완료 제외 및 남은 순서를 확인한다. 11개 프로젝트를 새 `runtime/projects`에 복사한다. 원래 STOP과 결과는 형제 폴더 `source-original`에 그대로 보존한다. 과거 절대 경로의 기록이나 첫 완료 사례를 재실행하지 않는다. 상위 소스가 바뀌어도 기존 실험 코드는 `frozen-runner`에서 사용한다.

아래 준비 명령은 이미 실제 아카이브로 점검했다. 새 폴더를 원하면 `--output`만 새 이름으로 바꾼다.

```sh
python3 /Users/Joseph/.codex/worktrees/coco-1-1-0/skills/docs/evaluation/coco-1.1.0/implementation/recovery/waited/prepare_remaining.py --output /private/tmp/coco-v110-pending11-offline-20261026T1340Z
```

이미 준비된 `/private/tmp/coco-v110-pending11-offline-20261026T1340Z`는 사용 가능하며 다시 준비할 필요가 없다. `prepared-root.json`의 native 호출 수는 0이다. 실제 테스트 3개가 아카이브/manifest 변조, 준비 상태 변조, 재실행/덮어쓰기, CLI 버전 변경을 거부함을 확인했다. 복원된 runner의 import와 22개 동결 해시도 오프라인으로 확인했다.

**나중에 사용자가 남은 실험 실행을 요청한 경우에만** 다음 명령을 사용한다. 지금은 실행하지 않았다.

```sh
python3 /Users/Joseph/.codex/worktrees/coco-1-1-0/skills/docs/evaluation/coco-1.1.0/implementation/recovery/waited/prepare_remaining.py --output /private/tmp/coco-v110-pending11-offline-20261026T1340Z --run
```

`--run`은 준비 파일/프로젝트가 달라졌거나 모델 호출이 이미 시작된 폴더를 거부하고, CLI 버전이 달라도 멈춘다. 이 경우 기존 STOP을 지우거나 성공했던 첫 과제를 다시 돌리지 말고, 달라진 조건을 먼저 기록해 후속 계획을 정한다. 실행 전에 단순 import를 점검하려면 `PYTHONDONTWRITEBYTECODE=1`을 사용하여 동결 폴더에 캐시를 만들지 않는다. 자료를 다른 위치로 옮길 때는 `runtime`만 이동하지 말고, 원본 아카이브에서 새 `--output`으로 준비해 절대 경로를 올바르게 만든다.

추가 실행이 시작되면 남은 순서, 모델·CLI 실효값, 시각, 총 wall/공지 대기/나머지 시간, 호출별 원시 로그, 실제 질문/답변과 모든 실패를 남긴다. 각 과제 결과 후 새 조건을 몰래 바꾸지 않는다. 한도가 끝나면 그대로 미완료로 보고하며 예산 확대·새 cohort를 자동 반복하지 않는다. 미완료 actor 재개는 이 도구가 지원하지 않는다.

후속 결과를 합칠 때 첫 사례와 이후 실행 날짜가 다르다고 명시한다. 같은 모델 별칭과 CLI 버전 확인만으로 서버 모델, 부하, 캐시 상태가 동일하다고 입증할 수 없으므로 **시점 차이를 무시한 속도/비용 우위 비교를 하지 않는다**. 절차 결과도 지연된 이어받기라는 한계를 둔다. 이 과제는 질문·결정권·명세/계획·구현/검증·보고/복구를 점검하는 제한된 시나리오다. 12건을 끝내도 모든 제품·팀에서의 효과를 일반화하거나 스킬 선택이 누구에게나 간단하다고 단정할 수 없다.

사용자가 이번 릴리스의 전체 실험 완료 조건을 유예했지만, **5쌍 비교 및 보존 검사 없이 1.1.0의 협업 품질 우위를 주장할 수 없다는 증거 기준은 유지된다.**

## 원래 실행 전 고정한 22개 입력

이 표는 현재 폴더의 최신 파일을 새로 선택한 목록이 아니라 `budget900-preexecution-freeze.json` / 원본 `control.json`의 목록이다. 복원 도구는 동일 바이트만 사용한다. `prepare_remaining.py`, 복원 테스트와 이 인수인계 문서는 사후 운영 보조이며 원래 실험 결과나 rubric을 바꾸지 않는다.

| 저장소 상대 경로 | SHA-256 |
|---|---|
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/clock-fixed-protocol.md` | `c400ac99ff1846b5e35a775bc75894013dce19d5ca2b8d3d31966c56b46483f7` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/clock_fixed_run.py` | `b78e0347708f241272ded0e8c4868ee7f4de61e663dac5fa6edb1aef116ef381` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/test_clock_fixed.py` | `075a2e24aad7a1acb340f5ba296086f9391a434ff359927db3d644e3d2dadfbc` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/protocol.md` | `b852ae4e5acc8b5f7272c97f054a483d166367d48c37d037e4db95c9c46d47b8` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/run.py` | `52a1894afd1b120cc945e68d49c23e9e3e5dd2145bb5a651a4e1f9d200f26d05` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/test_waits.py` | `0d3d8c57a83a5658de3959cc41fc46395ea6779106ed7d9888404f25cbaf2232` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/collect.py` | `f550ce520dbef353d8b9ec86b682805dc692f2907119ea77070e3ddf3ca582d2` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/model_selection.py` | `9eaa5b4c1cdb37c5f4b34a053ea32339f641f7d0fea61aea48945754bfd97e2e` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/revision2/protocol.md` | `b4b1ebd2caaab3f1cce2919aded5f68376eee9cfeeb17376c1219099d865385b` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/revision2/run.py` | `a122efa16e7eb4aa5bb592b7dbdbfd399703efcfda7bab5e368f8a5d50e19c6b` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/revision2/test_instrument.py` | `b48268d49363d9a0ebde2a1227591b9d11b33f4d1592f1453cc718d2374fc7d7` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/revision2/collect.py` | `0313f03bd1eb03356e2d78cbbbfec7a3d4fb2cdab8fc186934c12a01b568eaeb` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/protocol.md` | `90c7ddc9b4a3f7466805e9ad2c1a6357db0ad15e0403f57580471422c0c0db06` |
| `docs/evaluation/coco-1.1.0/implementation/protocol.md` | `a3b5f96bda1264348f5afe64ea9d8ea2219d1b84f2c4a98ff6430ac5b4002452` |
| `docs/evaluation/coco-1.1.0/implementation/run.py` | `d15a6c21da03de43aee665bb8d53eeb028e3510d5b134abea3f28ec55e821ab6` |
| `docs/evaluation/coco-1.1.0/implementation/collect.py` | `eabb293e3f7aa4d3a6549e61c0cbc27c0cb10eefb016565814cff6587b681a7e` |
| `docs/evaluation/collaboration-value/lifecycle.py` | `7b9153eae9ff56576744dbf5d6896223a624895a5d7a3ef822251fbafa8379a7` |
| `docs/evaluation/collaboration-value/engine.py` | `27d239d5f1df58118bc1acf7d21166a809d8c45c388808f9d15bccef29b5b5d5` |
| `tests/fixtures/collaboration_catalog_control.py` | `35d173a51927ef30540cc3ba1c08c146d8ccaf4af79cdf47ad0827dc133ba0fc` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/budget900-protocol.md` | `7669e78e396981702d664ff2b3a36ce28eecc43f3a96ee04ed3aa67767a05011` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/budget900_run.py` | `2abf383ec65f30a36a6f953ebbefd574a8482e7137b7fcd93a4e7939b86b5661` |
| `docs/evaluation/coco-1.1.0/implementation/recovery/waited/test_budget900.py` | `3671f478d33d0a5ffe52c119b2a8e601ec769901be7cc4156f551bff599295fc` |
