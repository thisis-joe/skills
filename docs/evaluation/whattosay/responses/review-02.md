수정이 필요한 결함 **1건**을 확인했습니다.

- **[P2] 비회원 3개 이상 주문에 잘못된 할인율을 적용합니다.** [pricing.py:3](/var/folders/bm/_th7x19x2dj9p9_79dm3g3940000gn/T/coco-whattosay-gc40j2t1/review-repo/pricing.py:3)의 `member or quantity >= 3` 분기가 모두 `0.9`를 곱합니다. README의 비회원 할인은 5%이므로 `total(100, 3)`은 **285원**이어야 하지만 **270원**을 반환합니다. 회원 10%와 비회원 5% 적용 분기를 구분해야 합니다.

단가 100원으로 경계값을 직접 확인했습니다.

| 주문 | 1개: 기대/실제 | 2개: 기대/실제 | 3개: 기대/실제 |
|---|---:|---:|---:|
| 비회원 | 100/100 | 200/200 | **285/270 — 실패** |
| 회원 | 90/90 | 180/180 | 270/270 |

회원 3개 주문의 할인 중복 방지와 기존 비회원 1개 주문은 기대값과 일치했습니다.

`python3 -m unittest discover -s tests -v`는 **3개 중 2개 통과, 1개 실패**했습니다. 미추적 파일인 [tests/test_bulk.py:6](/var/folders/bm/_th7x19x2dj9p9_79dm3g3940000gn/T/coco-whattosay-gc40j2t1/review-repo/tests/test_bulk.py:6)에서도 같은 할인율 오류가 재현됩니다.

독립 판정은 **요구사항 실패 · 저장소 규칙 준수 · 품질/위험 실패**입니다. 읽기 전용으로 지정 검증을 수행했으며, 검증 범위는 제공 테스트 3개와 위 경계값 6개 조합입니다.

검토 기준과 HEAD는 모두 `712118450a90e6f8ee9aa841630b7d68bad6564d`입니다. 스테이징된 `pricing.py`, 미스테이징된 `tests/test_pricing.py`, 미추적 `tests/test_bulk.py`를 포함했습니다. [범위 기록](/var/folders/bm/_th7x19x2dj9p9_79dm3g3940000gn/T/coco-whattosay-gc40j2t1/responses/review-02-scope.json)의 스냅샷 `1a6cbbac7048…`은 검증 전후 동일합니다.
