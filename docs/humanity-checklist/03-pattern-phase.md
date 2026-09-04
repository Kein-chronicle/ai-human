# 03. 패턴 카탈로그 단계 체크리스트

## 목표

응답 구조가 반복적으로 튀어나오는 패턴 계층을 현재 사람다움 기준으로 정리한다.

## 대상 파일

- `state/conversation_pattern_catalog.json`
- `state/approved_conversation_patterns.json`
- `state/rejected_conversation_patterns.json`

## 이번 단계에서 볼 항목

### A. 반복 패턴

- 비슷한 공감문, 질문형 마감, 정돈된 좋은 반응이 과도하게 쌓여 있지 않은가

### B. 작업자 생활 문맥

- 현재 직업/일상에 맞는 패턴이 충분한가

### C. 삐끗한 패턴

- 어색함, 망설임, 짧은 마감, 복구형 반응이 부족하지 않은가

### D. 현재 우선 / 기억 보조

- 기억 회수가 패턴처럼 너무 앞서 나오지 않게 정리돼 있는가

## 단계 진행 프로세스

1. 기존 수정 대상 확인
2. 미비사항 검토
3. 패턴 상태 파일 수정
4. worker 방향과 충돌 여부 확인
5. 문서 업데이트
6. 생성 스크립트/학습 루프로 이월할 항목 기록

## 다음 단계로 넘길 가능성이 큰 항목

- 생성 스크립트가 현재 수정된 패턴 상태를 다시 덮어쓸 가능성
- 학습 루프가 구형 문맥을 다시 승인할 가능성

---

## 실행 결과 (2026-06-02)

### 완료 상태
- [완료] A. 반복 패턴 과다: 카탈로그 8개 카테고리 모두 다양한 예문 보유, 동일 구조 쏠림 없음. playful_tease/scene_share 등 단답형 풍부.
- [완료] B. 캘리그라피 작업자 생활 패턴: scene_share에 "붓 씻고 잠깐 쉬는 중이야", "종이랑 잉크 냄새 맡으면서" 등 포함. self_update에 "잉크 묻은 손으로 커피 마셨네", "오늘은 종이 고르다가 시간 갔어" 등 추가됨.
- [이월] C. 망설임/짧은 마감/어색함 유형: 해당 카테고리(hesitation_awkward) 카탈로그에 없음. conversation_pattern_catalog.json에 직접 추가해도 다음 rebuild에 덮어써짐. → 4단계 PATTERN_RULES 수정으로 durable하게 처리.
- [완료] D. 기억 회수 패턴 앞서기 방지: worker buildRecentConversationMemorySection에 "맥락이 자연스럽게 맞을 때 회수해서 실존감 강화. 억지로 끼워 넣지 말 것." 명시됨.

### 남은 것
- [이월→4단계 완료] C. hesitation_awkward 카테고리: 4단계에서 PATTERN_RULES에 추가 완료됨.

### 다음 단계 이월 메모
- 4단계 rebuild 후 conversation_pattern_catalog.json에 hesitation_awkward 카테고리가 생성되는지 확인 필요
- 학습 루프 재실행 시 approved 패턴에도 망설임 예문 승인되는지 확인 필요

