**coco-verify — 간단 설명**

**목적:** 실제 앱·API·CLI의 동작과 안전성 주장을 실행 증거로 확인합니다.

**사용 시점:** 기능 동작, 변경 영향, 안전성 가정을 검증하거나 검증 도구·형식 증명을 만들고 유지할 때 사용합니다.

**입력:** 검증할 주장, 정확한 대상 버전, 실행 환경과 대표 입력이 필요합니다.

**진행 방식:** 주장과 판정 신호를 정하고 실제 코드를 실행한 뒤, 영향 범위와 핵심 가정을 확인합니다.

**결과:** 주장별 증거표, 대상 버전, 통과 조건, 실패 사항, 미입증 가정과 다음 최소 검증을 제공합니다.

**예시:** `$coco-verify 로그인 API가 잘못된 비밀번호를 거부하는지 실제 요청으로 확인해줘.`

**주의:** 필수 도구·환경이 없으면 검증 불가로 보고하며, 단위 테스트 통과나 추상 모델의 증명으로 실제 동작 검증을 대신하지 않고 독자적으로 커밋·배포하지 않습니다.

**출처:** [coco-verify 원문](/private/tmp/coco-guidance-compaction-muorgx4u/english-behavior/skills/coco-verify/SKILL.md), [공통 설명 형식](/private/tmp/coco-guidance-compaction-muorgx4u/english-behavior/skills/coco-tellmeskill/references/explanation-format.md)
