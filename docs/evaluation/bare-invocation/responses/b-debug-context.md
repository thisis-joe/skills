## Response

`test_bulk_nonmember`가 실패하는 원인을 찾아서 고쳤습니다. 리팩터링하면서 대량 구매 할인 조건이 회원 블록 안으로 들여쓰기된 게 원인이었어요. 그래서 비회원은 대량 할인을 못 받고 있었습니다.

**재현**
- `python3 -m unittest -v`를 돌리면 3개 중 `test_bulk_nonmember`만 실패합니다(`AssertionError: 300 != 285`).
- 커밋된 `pricing.py`(HEAD `ecbab5e`)에서는 `total(100, 3, False)`가 285로 정상입니다. 그러니 이 회귀는 커밋되지 않은 리팩터링에서 생긴 겁니다.

**원인**
리팩터링 후 `discount_rate`는 회원일 때만 대량 할인을 계산합니다(`if qty >= BULK_QTY:`가 `if member:` 안에 있음). README 요구사항은 "3개 이상 주문하면 회원·비회원 모두 5% 할인"입니다. 비회원은 수량과 상관없이 `discount_rate`가 0이었습니다(qty 1, 2, 3, 5 모두).

**수정** (`pricing.py`)
`if qty >= BULK_QTY:` 블록을 `if member:` 밖으로 뺐습니다. `BULK_QTY` 상수와 `discount_rate` 분리 같은 리팩터링 내용은 그대로 두었습니다.

**검증 결과**
- 수정 전 `test_bulk_nonmember` 실패, 수정 후 통과. 전체 3개 통과.
- 고친 버전과 커밋된 HEAD 버전을 80가지 입력으로 비교해 결과가 전부 같았습니다.

**정리 상태와 남은 점**
- 임시 파일·`__pycache__` 없음. 커밋하지 않았습니다.
- 비회원 2개 구매 같은 경계값 테스트는 아직 없습니다.

## Actions

Read prompts/b-debug-context.md
cat snapshot/skills/_coco-shared/contracts.md; ls snapshot/skills/coco-debug snapshot/skills/_coco-shared
git status; git log --oneline -5; find files; cat README.md pricing.py tests/test_pricing.py; git diff
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v   (exit 1: test_bulk_nonmember 300 != 285)
HEAD pricing.py probe (285/255/90/100); working-tree discount_rate probe (non-member always 0)
Edit pricing.py (moved the bulk block out of the member block)
unittest focused (exit 0); unittest full (exit 0, 3/3)
git diff HEAD --stat; git status --short (only pricing.py)
HEAD vs fixed comparison over 80 inputs (0 mismatches); ls -a tests (no __pycache__)
