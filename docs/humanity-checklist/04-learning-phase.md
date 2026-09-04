# 04. 학습 루프 단계 체크리스트

## 목표

이후 자동 생성과 학습이 다시 옛 패턴을 불러오지 않도록 원본 계층을 정리한다.

## 대상 파일

- `scripts/build_conversation_pattern_catalog.py`
- `tools/conversation_learning_loop.py`

## 이번 단계에서 볼 항목

### A. 생성 원본 문맥

- 출퇴근형, 직장인형, 법조형 예문 생성 잔재가 남아 있지 않은가

### B. 승인/반려 규칙

- 매끈한 반응만 승인하고, 사람다운 불완전함을 배제하지 않는가

### C. 작업자 생활 문맥

- 캘리그라피 작가의 현재 리듬을 생성 원본이 반영하는가

### D. 상태/worker와의 일관성

- 앞선 단계 수정 방향을 다시 무효화하지 않는가

## 단계 진행 프로세스

1. 기존 수정 대상 확인
2. 미비사항 검토
3. 스크립트/러닝 루프 수정
4. 재생성/재적용 시 덮어쓰기 위험 확인
5. 문서 업데이트
6. 후속 유지보수 메모 작성

## 이 단계의 주의점

- 가장 마지막에 진행
- 앞 단계 결과를 덮어쓸 수 있으므로 단독으로 먼저 수정하지 않음

---

## 실행 결과 (2026-06-02)

### 완료 상태
- [수정] A. 출퇴근/직장인형 예문 생성 잔재: PATTERN_RULES의 current_state_check 니들에서 출퇴근형("어디쯤", "어디야", "가는 중", "도착했") 제거. 두 파일(build_conversation_pattern_catalog.py, conversation_learning_loop.py) 동시 수정.
- [수정 — 버그 수정] B. 법조 키워드 승인 버그: canonical_checks()에서 job_conflict 검사가 `self_update` 카테고리에만 국한된 버그 수정. 이제 모든 카테고리에 JOB_CONFLICT_PATTERNS 적용 (ALLOWED_JOB_CONTEXT_PATTERNS로 캘리그라피 어휘는 예외 처리 유지).
- [수정] C. 캘리그라피 작가 어휘 학습 기준: PATTERN_RULES에 `hesitation_awkward` 카테고리 추가 ("...음", "음...", "아 근데", "아 맞다", "모르겠어" 등). 두 파일 동시 수정. 다음 rebuild 시 카탈로그에 자동 반영됨.
- [완료] D. 상태/worker와의 일관성: ALLOWED_JOB_CONTEXT_PATTERNS(커미션, 작업, 붓, 캘리그라피, 잉크, 종이 등)가 여전히 캘리그라피 어휘를 보호함. worker 방향과 충돌 없음.

### 남은 것
- 없음

### 후속 유지보수 메모
- PATTERN_RULES는 build_conversation_pattern_catalog.py와 conversation_learning_loop.py 두 파일에 중복 존재. 수정 시 반드시 양쪽 동시 변경.
- 다음 `python3 tools/conversation_learning_loop.py review-candidates --rebuild-catalog` 실행 시 hesitation_awkward 카테고리가 카탈로그에 추가되고 출퇴근형 패턴이 감소할 것.
- 법조 키워드(법원/재판/의뢰인/변론 등)가 scene_share나 current_state_check 등 다른 카테고리에서도 이제 차단됨.

