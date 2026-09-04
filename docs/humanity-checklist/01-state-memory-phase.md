# 01. 상태/기억/감각 단계 체크리스트

## 목표

응우의 현재 상태, 감정 여운, 상대 상태, 생활 리듬, 감각 디테일을 먼저 안정화한다.

## 대상 파일

- `state/recent_conversation_memory.json`
- `state/mood_residue_state.json`
- `state/counterpart_state_memory.json`
- `state/chat_length_policy.json`
- `state/random_event_pool.json`
- `state/time_micro_detail_pool.json`
- `state/phone_notification_pool.json`
- 필요 시:
  - `state/inside_jokes_and_memories.json`
  - `state/user_conversation_state.json`
  - `state/reply_variance_state.json`

## 이번 단계에서 볼 항목

### A. 최근 대화 기억

- 직전 대화 행동/감정/분위기가 다음 응답에 이어질 수 있게 정리돼 있는가
- 너무 요약문처럼만 저장되지 않는가

### B. 감정 여운

- 기분 좋음, 멍함, 걱정, 서운함 같은 상태가 짧게 남는 구조가 있는가
- 대화가 끝날 때마다 감정이 초기화되지 않는가

### C. 상대 상태 추적

- 사용자의 피곤함, 바쁨, 예민함, 애정 필요 상태가 반영되는가
- 단순 메모가 아니라 응답 톤 결정에 쓸 수 있는 구조인가

### D. 생활 리듬

- 캘리그라피 작가의 현재 리듬이 상태로 잡혀 있는가
- 작업 중 / 작업 직후 / 쉬는 중 / 외출 중 같은 구분이 가능한가

### E. 감각 디테일

- 손끝, 종이, 잉크, 작업대 조명 같은 디테일이 자연스럽게 섞일 수 있는가

### F. 알림/사소한 사건

- DM, 커미션 문의, 재료 배송, 인스타 반응 같은 현재 생활 이벤트가 살아 있는가

## 단계 진행 프로세스

1. 기존 수정 대상 확인
2. 미비사항 검토
3. 상태 파일 수정
4. 구조 충돌 여부 확인
5. 문서 업데이트
6. 다음 단계 이월 작성

## 다음 단계로 넘길 가능성이 큰 항목

- worker에서 실제로 이 상태를 읽도록 반영해야 하는 부분
- proactive 문구에 현재 상태를 반영해야 하는 부분

---

## 실행 결과 (2026-06-02)

### 완료 상태
- [완료] A. recent_conversation_memory: items 빈 배열이나 schema/decay_policy/worker 참조 구조 정상. 런타임 채워짐.
- [완료] B. mood_residue_state: carry_ratio, residue_label, update_rule 구조 정상. worker가 mood_timeline 변경 시 함께 업데이트하도록 명시됨.
- [수정] C. counterpart_state_memory: common_state_keys에서 `commuting` 제거, `need_affection`과 `sensitive_or_stressed` 추가. update_rule에서 "이동 중" 제거하고 "감정 필요" 추가.
- [완료] D. chat_length_policy: time_defaults 키 이름이 work_ 형식이나 rules 내용은 "업무 중 / 작업 집중 중이면" 으로 캘리그라피 문맥 반영됨. 불규칙성 허용은 worker buildHumanLikenessSection에서 강제함.
- [완료] E. random_event_pool: 잉크 사러 문구점, 캘리그라피 연습, 커미션 등 캘리그라피 이벤트 16개 충분.
- [완료] F. time_micro_detail_pool: 잉크 냄새, 붓질 소리, 손끝 잉크 마른 느낌 등 작업 감각 디테일 충분.
- [완료] G. phone_notification_pool: 커미션 DM, 종이 배송, 인스타 반응 등 캘리그라피 생활 알림 충분.

### 남은 것
- 없음 (C 수정 완료)

### 다음 단계 이월 메모
- worker가 counterpart_state_memory의 need_affection 상태를 톤 조절에 반영하는지 2단계에서 확인

