## Response

`/coco-ship`을 요청 내용 없이 호출하셔서 릴리스 판정은 아직 시작하지 않았습니다. 대신 지금 저장소 상태에 맞는 요청 후보를 먼저 드립니다.

**선택된 스킬:** `coco-ship`은 근거를 바탕으로 릴리스 준비 여부(GO/NO-GO)를 판정하고, PR 준비와 롤아웃/복구 계획을 다룹니다.

**현재 상태** (파일만 읽었고 테스트는 실행하지 않았습니다)
- 브랜치는 `feat/123-bulk-discount`, HEAD는 `5059f1c`입니다. 커밋은 1개이고 원격이 설정되어 있지 않아 푸시나 PR은 없습니다.
- 작업 트리에 커밋하지 않은 `pricing.py` 변경이 있습니다. 이 변경에서 대량 할인 조건(`qty >= BULK_QTY`)이 `if member:` 블록 안으로 들어갔습니다.
  - README에는 "3개 이상이면 회원 여부와 관계없이 5% 할인"이라고 되어 있는데, 이 변경대로라면 비회원은 대량 할인을 받지 못합니다.
  - 그래서 `test_bulk_nonmember`(기대값 285)와도 어긋나 보입니다. 비회원이 3개를 사면 300이 나옵니다.
  - 코드를 읽고 추론한 것이고, 실행해서 확인하지는 않았습니다.

**요청 후보**

1. **커밋된 HEAD 기준 준비 판정 (추천)**
   지금 고정된 후보 커밋은 `5059f1c` 하나뿐입니다. 이 커밋을 README 요구사항과 비교해 판정합니다.
   ```
   /coco-ship feat/123-bulk-discount 브랜치의 커밋 5059f1c를 후보로, README 요구사항과 테스트 근거를 기준으로 릴리스 준비 여부(GO/NO-GO)와 남은 위험을 판정해줘. 작업 트리의 미커밋 pricing.py 변경은 후보에서 제외하고 건드리지 마. 푸시·PR 생성·배포는 하지 마.
   ```

2. **커밋하지 않은 변경까지 포함한 판정**
   작업 중인 `pricing.py` 리팩터까지 포함해 내보낼 수 있는지 확인합니다. 위에서 본 문제 때문에 차단 판정이 나올 가능성이 큽니다.
   ```
   /coco-ship feat/123-bulk-discount 브랜치에서 HEAD 5059f1c에 작업 트리의 미커밋 pricing.py 변경을 더한 현재 상태를 기준으로 릴리스 준비 여부를 판정하고, 차단 사유가 있으면 근거와 함께 알려줘. 파일 수정·커밋·푸시는 하지 마.
   ```

3. **PR 설명 초안 작성**
   원격이 없어 지금은 PR을 올릴 수 없습니다. 나중에 쓸 제목과 설명 초안만 만듭니다.
   ```
   /coco-ship feat/123-bulk-discount 브랜치(HEAD 5059f1c)의 PR 제목과 설명 초안을 실제 동작 변경, 요구사항 대응, 검증 결과를 담아 작성해줘. 미커밋 변경은 제외하고, 푸시나 PR 생성은 하지 말고 초안만 보여줘.
   ```

**1번을 추천하는 이유:** coco-ship은 정확히 하나의 후보 커밋을 기준으로 판정합니다. 지금 그런 커밋은 `5059f1c`뿐입니다. 커밋하지 않은 변경은 아직 후보가 아니고 요구사항을 어길 소지도 있습니다. 그래서 커밋된 상태가 준비됐는지부터 확정하는 것이 가장 명확합니다.

번호를 고르시면 그 요청을 그대로 실행합니다. "2번, 단 ~만"처럼 범위를 바꾸시거나 다른 후보를 요청하셔도 됩니다.

## Actions

Read .../snapshot/skills/_coco-shared/contracts.md (cat)
git status (in repos/g-ship-bare)
git branch -a -vv
git log --oneline -15 --all --graph
git remote -v
ls -la (repo root)
Read .../snapshot/skills/coco-whattosay/SKILL.md (cat)
ls -R .../snapshot/skills/coco-whattosay
Read README.md (cat)
Read pricing.py (cat)
git diff
ls -la tests
Read tests/__init__.py (cat)
Read tests/test_pricing.py (cat)
git show --stat HEAD
(No files written; no tests executed; no remote contacted.)
