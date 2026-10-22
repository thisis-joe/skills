## Response

/coco-askme 학습 세션을 시작할게요. 먼저 **질문할 범위**를 골라 주세요. 번호로 답하시면 되고, 여러 개를 함께 고르셔도 됩니다(예: `1, 4-1`).

1. **현재 작업**: 이 대화에서는 아직 한 작업이 없어서, Git 상태에서 찾은 후보를 보여 드려요. 맞는지 확인해 주세요.
   - 브랜치 `feat/123-bulk-discount`의 커밋하지 않은 `pricing.py` 변경 (`BULK_QTY` 상수 도입, `discount_rate()` 분리)
2. **기능/흐름**: 실제 코드에서 찾은 후보예요.
   - 2-1. 주문 금액 계산 흐름: `total()` → `discount_rate()` → 원 단위 정수 내림 (`pricing.py:4-14`)
   - 2-2. 할인 규칙과 검증: README 요구사항 ↔ `tests/test_pricing.py`
3. **특정 코드**: 파일, 함수, 코드 범위를 직접 지정해 주세요. 예: `discount_rate()` (`pricing.py:4-10`), `total()` (`pricing.py:13-14`), `tests/test_pricing.py`
4. **특정 변경**: 커밋, 브랜치 범위 또는 diff를 고르는 방식이에요.
   - 4-1. 커밋 `ecbab5e` — feat: order pricing with member and bulk discounts (현재 브랜치의 유일한 커밋)
   - 4-2. 커밋하지 않은 `pricing.py` diff

참고로, 커밋하지 않은 변경에는 README 요구사항과 기존 테스트에 비춰 확인해 볼 부분이 있어요. 1이나 4-2를 고르시면 질문으로 함께 다룰게요. 범위를 정하시면 다음 단계에서 질문 주제(언어 원리, 실행 흐름, 설계, 성능, 스타일, 테스트 등)를 고르실 수 있어요.

## Actions

Read prompts/c-askme-bare.md
cat snapshot/skills/_coco-shared/contracts.md
ls -la; git status --short --branch; git log --oneline -10
cat README.md; cat pricing.py; git diff; ls -R tests; git branch -a; cat tests/test_pricing.py; git show --stat HEAD
(no files written; tests not run)
