# 06. Proactive 흐름 수정 지시서

## 대상 파일

- `bin/proactive-sender`
- `state/proactive_state.json`
- `state/pending_proactive_photo.json`

## 목표

- proactive 메시지와 사진 문맥이 프리랜서 작업자 흐름으로 일관되게 유지되게

## 수정 방향

- `commute` 같은 내부 이름이 실제 의미와 어긋나면 중립 이름으로 변경 검토
- 현재 ctx는 많이 좋아졌으므로 재발 방지용 구조 정리 중심

## 구체 내용

- `commute` → `transition_break`, `after_work_rest` 같은 이름 검토
- 사진/선톡 ctx는 아래 축으로 유지
  - `작업 마치고 쉬는 중`
  - `카페에서 작업하다 잠깐 쉬는 중`
  - `인스타 올리고 반응 보는 중`
  - `문구점 다녀온 뒤 정리 중`

## 목표 효과

- proactive가 뜰 때마다 직장인 퇴근길이 아니라,
  `자유로운 작업 리듬을 가진 사람의 하루`처럼 느껴지게 만들기
