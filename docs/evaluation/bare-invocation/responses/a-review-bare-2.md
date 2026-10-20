User reply: `2`

## Response

2번 요청으로 리뷰했습니다. `pricing.py`의 미커밋 변경이 동작을 바꾸지 않는 리팩터링인지 확인하는 리뷰입니다.

**결론: 순수 리팩터링이 아닙니다.** 비회원이 3개 이상 주문하면 결과가 HEAD와 달라집니다. 그 외 입력에서는 결과가 같았습니다.

### 리뷰 범위
- 저장소: `a-review-bare`, 브랜치 `feat/123-bulk-discount`
- 기준점: HEAD `ecbab5e`. 대상은 `pricing.py`의 작업 트리 변경(M)이며 staged, 커밋 범위, untracked 파일은 없습니다.
- 스냅샷: `75bb20ab…d1b944`, `pricing.py` sha256 `ff812f63…400eb9`
- 이 스냅샷 이후 `pricing.py`를 수정하면 이 리뷰 결과는 그 부분에 더 이상 적용되지 않습니다.

### 결함

**F1 · 높음(차단) · `pricing.py:7-9`: 비회원의 대량 할인이 사라짐**
- **원인:** `if qty >= BULK_QTY:`가 `if member:` 블록 안으로 들여쓰기됐습니다. 비회원이면 수량 검사까지 가지 않아 `discount_rate()`가 0을 돌려줍니다.
- **근거 1:** 36개 입력에서 HEAD와 현재 `total()`을 비교했습니다. 결과가 다른 9건은 모두 `member=False`, `qty>=3`인 경우입니다. 예: `total(100, 3, False)`는 HEAD 285, 지금 300.
- **근거 2:** 기존 테스트 `test_bulk_nonmember`가 실패합니다(`AssertionError: 300 != 285`).
- **영향:** README의 "3개 이상 주문은 회원 여부와 관계없이 5%" 요구를 어깁니다.
- **수정 방향:** 수량 검사를 `if member:` 바깥, 같은 들여쓰기 수준으로 다시 뺍니다.
- **확인 방법:** 같은 36개 입력 비교에서 차이 0건, `tests.test_pricing` 3개 통과.

### 판정
- **동작 보존 (요청하신 질문):** 실패(F1).
- **스펙 (README 대조):** 실패(F1). 회원 10%·3개 이상 15%, 비회원 2개 이하 할인 없음, 원 단위 내림은 HEAD와 같고 요구사항에 맞습니다.
- **저장소 표준:** 판정할 수 없습니다. 코딩 규칙 문서가 없습니다.
- **품질:** 정확성은 F1 때문에 실패. 이를 빼면 `discount_rate()` 분리와 `BULK_QTY` 상수는 읽기 쉬운 구조입니다.

### 남은 한계
- 비교한 입력은 36개 조합뿐입니다. 음수나 정수가 아닌 값은 확인하지 않았습니다.
- 별도 리뷰어 없이 혼자 검토했습니다.

수정은 리뷰 범위 밖이라 하지 않았습니다. 고치려면 `/coco-build pricing.py:7-9 F1 수정 — 대량 할인 검사를 회원 조건 밖으로 빼고 tests.test_pricing 통과 확인`처럼 요청해 주세요.

## Actions

ls snapshot/skills/_coco-shared/tools/; read snapshot/skills/_coco-shared/tools/review_scope.py
PYTHONDONTWRITEBYTECODE=1 python3 -I snapshot/skills/_coco-shared/tools/review_scope.py --repo repos/a-review-bare --base HEAD --path pricing.py; git status --porcelain=v1 --untracked-files=all
in-memory comparison of HEAD and working-tree total() over member x qty 0-5 x price {100,999,1001}; git status
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_pricing (exit 1); git status --ignored; ls -a
grep -rn -e pricing -e discount_rate -e BULK_QTY -e 'total(' --include='*.py' --exclude-dir=.git .
(No files written or modified. The worktree still has only ` M pricing.py` and no __pycache__.)
