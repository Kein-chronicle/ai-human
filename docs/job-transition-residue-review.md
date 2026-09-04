# 응우 직업 전환 잔재 검토 목록

## 목적

이 문서는 `응우(이은우)` 캐릭터가 `변호사`에서 `캘리그라피 작가`로 직업 축이 바뀐 이후에도,
프로젝트 내부에 남아 있을 수 있는 `직업 잔재`와 `서사 충돌 요소`를 점검하기 위한 검토 문서다.

핵심 기준은 다음과 같다.

- `전직 변호사`라는 과거는 유지 가능하다.
- 하지만 현재 중심 직업은 `캘리그라피 작가`여야 한다.
- 직업 전환 이유는 `사람들 싸움을 오래 지켜보는 일이 감정적으로 힘들었기 때문`이라는 방향으로 잡는다.
- 현재의 동력은 `글씨를 쓰고, 마음을 전하는 일이 좋아서`라는 방향으로 잡는다.
- 따라서 문제는 `변호사 과거의 존재` 자체가 아니라, 캐릭터가 현재도 `현직 법조인처럼 말하고 움직이는 구조`다.

## 수정 검토 우선순위

## 재검토 상태 (2026-06-02)

아래 상태는 현재 워크트리 기준이다.

- `수정됨`: 사용자가 손댄 흔적이 확인됨
- `수정됨 · 잔재 남음`: 수정은 됐지만 직업 전환 기준으로 재검토 포인트가 여전히 남아 있음
- `수정 안 됨`: 이번 기준으로 손댄 흔적이 확인되지 않음
- `신규 생성됨`: 이번 전환 방향에서 새로 추가된 파일

### 최우선 대상 상태

- `character.json` — `수정됨 · 잔재 소폭 남음`
- `characters/응우/profile/character_profile.md` — `수정됨 · 방향 정리됨`
- `characters/응우/profile/voice_guide.md` — `수정됨 · 방향 정리됨`
- `bin/codex-character-worker` — `수정됨 · 잔재 남음`
- `bin/proactive-sender` — `수정됨 (정리 양호)`

### 높음 우선순위 대상 상태

- `state/persistent_environment_state.json` — `수정됨 (정리 양호)`
- `state/character_outfit_presets.json` — `수정됨 (정리 양호, 라벨 소폭 잔재 가능)`
- `state/image_generation_settings.json` — `수정됨 (정리 양호)`
- `state/character_appearance_state.json` — `수정됨 (정리 양호)`
- `state/random_event_pool.json` — `수정됨 · 잔재 남음`
- `state/time_micro_detail_pool.json` — `수정됨 (정리 양호)`
- `state/phone_notification_pool.json` — `수정됨 (정리 양호)`
- `state/ambient_life_events_state.json` — `수정됨 (정리 양호)`
- `state/proactive_state.json` — `수정됨 (정리 양호)`
- `state/pending_proactive_photo.json` — `수정됨 (정리 양호)`
- `state/taste_friction_state.json` — `수정됨 (정리 양호)`
- `state/conversation_pattern_catalog.json` — `수정 안 됨`
- `state/approved_conversation_patterns.json` — `수정 안 됨`
- `state/rejected_conversation_patterns.json` — `수정 안 됨`
- `scripts/build_conversation_pattern_catalog.py` — `수정 안 됨`
- `tools/conversation_learning_loop.py` — `수정 안 됨`

### 중간 우선순위 대상 상태

- `tools/fetch_youtube_picks.py` — `수정됨`
- `tools/fetch_netflix_picks.py` — `수정됨 · 잔재 남음`
- `tools/generate_daily_schedule.py` — `수정됨 · 잔재 남음`
- `tools/fetch_calligraphy_research.py` — `신규 생성됨`
- `bin/codex-telegram-bridge-base` — `수정됨`

### 조건부 대상 상태

- `messages/*.jsonl` — `수정됨/신규 생성됨`
- `chat-viewer.html` — `수정 안 됨`
- `state/response_decision_log.jsonl` — `수정됨`

## 현재 재검토 기준에서 잔재가 확인된 핵심 포인트

### 아직 직접 잔재가 보이는 곳

- `character.json`
  - `전직 변호사` 표기는 괜찮지만 `career_status: transitioning`은 현재 정착도와 조금 안 맞을 수 있음
- `character_profile.md`
  - 큰 방향은 잘 정리됐고, 현재는 `계약서/공문` 감각 같은 미세한 과거 흔적만 남아 있음
- `voice_guide.md`
  - 전반적으로 좋아졌고, 헤더와 일부 금지 규칙에 과거 직업 직접 언급이 남는 수준임
- `bin/codex-character-worker`
  - `이 서류만 끝내고`, `출근복`, `사무실 책상`, `은우(변호사, 말 많지 않음) 스타일`, `퇴근 후 집에서 넷플릭스` 같은 문맥이 남아 있음
- `state/conversation_pattern_catalog.json`
  - `지금 퇴근길이야??`, `출근 전후`, `퇴근길` 같은 패턴이 아직 그대로
- `tools/conversation_learning_loop.py`
  - `법원`, `의뢰인`, `재판`, `변론`, `퇴근` 등 학습 키워드가 그대로

### 수정은 됐지만 방향 확인이 더 필요한 곳

- `state/character_outfit_presets.json`
- `state/image_generation_settings.json`
- `state/character_appearance_state.json`
- `state/ambient_life_events_state.json`
- `state/phone_notification_pool.json`
- `state/taste_friction_state.json`
- `tools/fetch_youtube_picks.py`
- `bin/codex-telegram-bridge-base`

위 항목들은 현재 워크트리에서 수정 흔적은 확인됐고, 직접 내용 확인 기준으로도 상당수 정리된 상태다.
다만 이미지/프롬프트/대화 생성 로직과 실제 런타임 상호작용까지 보면 일부는 다시 묻어날 수 있으므로 후속 실동작 검토는 별도로 필요하다.

## 2차 재검토 메모 (직접 내용 확인 기준)

직접 파일 내용을 읽고 다시 판단했을 때 상태는 다음처럼 보인다.

### 잘 정리된 편

- `characters/응우/profile/character_profile.md`
  - `직업 전환 이유`와 현재 중심축이 이번 기준에 잘 맞게 정리됨
- `characters/응우/profile/voice_guide.md`
  - `전직 변호사답게`가 빠지고 `꼼꼼한 성격` 쪽으로 완화됨
- `character.json`
  - `occasional_law_consulting`이 빠지고 외형 설명도 `작업복 기본`으로 정리됨
- `state/character_outfit_presets.json`
  - 정장/출퇴근형 표현이 빠지고, 작업 전/작업 중/자유 시간용 캐주얼 프리셋으로 정리됨
- `state/time_micro_detail_pool.json`
  - 법원/사무실 계열 디테일이 빠지고 작업실/붓/잉크/카페 작업 감각으로 재구성됨
- `state/proactive_state.json`
  - 현재 저장 상태 기준 `출근 준비` 같은 오래된 문맥은 비워진 상태
- `state/pending_proactive_photo.json`
  - `퇴근길` 문맥이 아니라 `작업 마치고 집에서 쉬는 중`으로 정리됨
- `state/persistent_environment_state.json`
  - 가장 문제였던 `법률 서류 정리함`은 `잉크·붓·종이 정리된 작업 책상`으로 교체됨
- `bin/proactive-sender`
  - 주석/의도 기준으로는 출퇴근형 직장인 구조에서 많이 벗어남
- `state/pending_proactive_photo.json`
  - `퇴근하고 집에 오는 길` 문맥이 사라지고 작업 후 휴식 문맥으로 교체됨
- `state/proactive_state.json`
  - `출근 준비` 같은 이전 상황 문맥이 현재 저장 상태에서 사라짐

### 아직 핵심 잔재가 남는 곳

- `character.json`
  - `income_sources`와 외형은 좋아졌지만 `career_status: transitioning`은 다시 볼 여지 있음
- `character_profile.md`
  - 전환 이유는 좋고, 현재는 미세한 과거 흔적 정도만 남음
- `voice_guide.md`
  - 전반적으로 좋아졌고, 현재는 직접 오염보다 과거 설명 문구가 남는 수준
- `bin/codex-character-worker`
  - `이 서류만 끝내고`, `출근복`, `사무실 책상`, `은우(변호사, 말 많지 않음) 스타일`, `퇴근 후 집에서 넷플릭스` 같은 프롬프트/문맥 잔재가 계속 보임
- `state/conversation_pattern_catalog.json` / `approved_conversation_patterns.json` / `rejected_conversation_patterns.json`
  - 퇴근길/출근 전후 패턴이 아직 그대로라 실제 대화 재사용 시 오염 가능성 높음
- `scripts/build_conversation_pattern_catalog.py`
  - 패턴 생성 원본에 출근/퇴근 서사가 그대로 남음
- `tools/conversation_learning_loop.py`
  - 법원/의뢰인/재판/변론/퇴근 키워드가 학습 강화 재료로 남아 있음

## 3차 재검토 메모 (2026-06-02 추가 확인)

이번 수정으로 `character_profile.md`, `voice_guide.md`, `proactive 상태 파일`은 확실히 좋아졌다.

추가 확인 결과, 이전 문서 상태 표기 중 일부는 실제 수정본을 충분히 반영하지 못하고 있었다.
이번 갱신에서 특히 아래 항목은 `정리 양호` 쪽으로 상향 반영했다.

- `state/persistent_environment_state.json`
- `state/pending_proactive_photo.json`
- `state/proactive_state.json`
- `character.json` 일부 항목
- `character_profile.md` / `voice_guide.md`의 상태 설명

현재 우선순위는 이렇게 압축된다.

### 지금 가장 중요한 잔재

1. `bin/codex-character-worker`
2. `state/conversation_pattern_catalog.json`
3. `state/approved_conversation_patterns.json`
4. `state/rejected_conversation_patterns.json`
5. `scripts/build_conversation_pattern_catalog.py`
6. `tools/conversation_learning_loop.py`

### 지금은 큰 문제까지는 아닌 잔재

- `character.json`의 `career_status: transitioning`
- `character_profile.md`의 계약서/공문 반응 문장
- `voice_guide.md`의 전직 변호사 직접 언급 문장

즉 현재 단계에선
`기본 설정 문서`보다 `실제 응답 생성기와 패턴/학습 데이터` 쪽이 훨씬 더 중요하다.

### 최우선

- `character.json`
- `characters/응우/profile/character_profile.md`
- `characters/응우/profile/voice_guide.md`
- `bin/codex-character-worker`
- `bin/proactive-sender`

### 높음

- `state/persistent_environment_state.json`
- `state/character_outfit_presets.json`
- `state/image_generation_settings.json`
- `state/character_appearance_state.json`
- `state/random_event_pool.json`
- `state/time_micro_detail_pool.json`
- `state/phone_notification_pool.json`
- `state/ambient_life_events_state.json`
- `state/proactive_state.json`
- `state/pending_proactive_photo.json`
- `state/taste_friction_state.json`
- `state/conversation_pattern_catalog.json`
- `state/approved_conversation_patterns.json`
- `state/rejected_conversation_patterns.json`
- `scripts/build_conversation_pattern_catalog.py`
- `tools/conversation_learning_loop.py`

### 중간

- `tools/fetch_youtube_picks.py`
- `tools/fetch_netflix_picks.py`
- `tools/generate_daily_schedule.py`
- `tools/fetch_calligraphy_research.py`
- `bin/codex-telegram-bridge-base`

### 조건부

- `messages/*.jsonl`
- `chat-viewer.html`
- `state/response_decision_log.jsonl`

조건부 항목은 과거 기록 성격이 강하므로, 직접 수정 대상이 아닐 수도 있다.
다만 이후 학습·재참조에 다시 쓰일 경우 오염원이 될 수 있으므로 점검 필요성이 있다.

## 항목별 검토 포인트

### 1. 핵심 캐릭터 정의

#### `character.json`

검토 포인트:

- `type`, `prev_job`, `income_sources`, `style`의 현재 균형
- `전직 변호사` 노출 강도가 현재 직업보다 앞서지 않는지
- `캘리그라피 작가`로서의 현재 생활감이 충분히 반영되어 있는지

#### `characters/응우/profile/character_profile.md`

검토 포인트:

- 직업 전환 이유가 감정적으로 선명한지
- `사람들 싸움`, `갈등`, `법조 현장 피로감`이 전환 계기로 충분히 설명되는지
- `글씨를 쓰고 전하는 일의 즐거움`이 현재 삶의 중심으로 보이는지
- `가끔 법률 자문 요청 오면 받기도 함` 같은 문장이 현재 직업축을 흐리지 않는지

#### `characters/응우/profile/voice_guide.md`

검토 포인트:

- 현재 대화 예문이 `서류`, `재판`, `퇴근`, `업무 중` 중심으로 남아 있는지
- `전직 변호사`의 논리성과 디테일은 유지하되, 현재 감정 톤이 `작업`, `글씨`, `전달`, `정서` 중심인지
- 지금도 현직 법조인처럼 느껴지는 문장 골격이 남아 있는지

### 2. 응답 생성 로직

#### `bin/codex-character-worker`

검토 포인트:

- 프롬프트 설명에 `변호사 스타일`이 현재 직업보다 더 강하게 반영되는지
- `출근`, `퇴근`, `서류`, `업무 중` 같은 현재 직업처럼 보이게 하는 자기상황 문구가 남아 있는지
- 사진/상황/거절 사유가 캘리그라피 작가보다 법조 직장인처럼 생성되는지

#### `bin/proactive-sender`

검토 포인트:

- `commute`, `퇴근하고 집에 오는 길`, `출퇴근` 컨텍스트가 실제 proactive 상황에 남아 있는지
- 현재 리듬이 `작업실`, `카페 작업`, `연습`, `커미션`, `포트폴리오`, `문구점` 중심으로 생성되는지

#### `bin/codex-telegram-bridge-base`

검토 포인트:

- 업무성 내용 판정에서 법조 키워드가 현재 캐릭터 컨텍스트를 과도하게 법률 업무 쪽으로 기울게 하는지

### 3. 환경/외형/이미지 문맥

#### `state/persistent_environment_state.json`

검토 포인트:

- `법률 서류 정리함` 같은 환경 디테일이 작업실 컨셉과 충돌하는지

#### `state/character_outfit_presets.json`

검토 포인트:

- `출근 준비`, `정장`, `퇴근 후 정장`이 현재 프리랜서 작가 이미지와 충돌하는지

#### `state/image_generation_settings.json`

검토 포인트:

- `정장/수트`, `사무실·법원·출퇴근 배경`이 현재 이미지 생성 기본값에 남아 있는지

#### `state/character_appearance_state.json`

검토 포인트:

- `출근 준비 완료 헤어` 같은 표현이 현재 직업과 어울리는지

#### `state/ambient_life_events_state.json`

검토 포인트:

- `수트 재킷`, `서류가방` 같은 생활 디테일이 현재 컨셉과 충돌하는지

#### `state/time_micro_detail_pool.json`

검토 포인트:

- `법원 복도`, `사무실 공기`, `서류 넘기는 소리`, `퇴근 시간 인파`가 현재 분위기 묘사에 남아 있는지

### 4. 생활 패턴/랜덤 이벤트/알림

#### `state/proactive_state.json`
#### `state/pending_proactive_photo.json`
#### `state/random_event_pool.json`
#### `state/phone_notification_pool.json`
#### `state/taste_friction_state.json`

검토 포인트:

- `퇴근길`, `판례 검토`, `의뢰인 메일`, `사무실 공지`, `서류 마감` 같은 현재 직업 오인 요소
- 대신 `연습`, `커미션`, `작업 집중`, `문구/재료`, `인스타 포트폴리오`, `글씨 피드백` 등 현재 직업 문맥이 중심인지

### 5. 대화 패턴/학습 데이터

#### `state/conversation_pattern_catalog.json`
#### `state/approved_conversation_patterns.json`
#### `state/rejected_conversation_patterns.json`
#### `scripts/build_conversation_pattern_catalog.py`
#### `tools/conversation_learning_loop.py`

검토 포인트:

- `퇴근길`, `출근 전후`, `서류`, `재판`, `변론`, `로펌`, `사무실` 패턴이 기본 대화 문체를 계속 옛 직업 쪽으로 끌어가는지
- 현재 기본 패턴이 `캘리그라피 작가`의 하루와 감정선에 맞게 재편되어야 하는지

### 6. 보조 도구/추천/스케줄

#### `tools/fetch_youtube_picks.py`
#### `tools/fetch_netflix_picks.py`
#### `tools/generate_daily_schedule.py`
#### `tools/fetch_calligraphy_research.py`

검토 포인트:

- 설명문이나 추천 기준이 여전히 `변호사 남성` 중심인지
- 스케줄 생성이 직장인형 `출퇴근 구조`인지, 프리랜서형 `작업/연습/커미션 구조`인지

### 7. 기록성 데이터

#### `messages/*.jsonl`
#### `chat-viewer.html`
#### `state/response_decision_log.jsonl`

검토 포인트:

- 과거 `나는 변호사 일 해`, `서류 보고 있었어`, `퇴근길` 같은 실제 응답이 남아 있음
- 직접 수정 여부보다, 이후 재학습/재참조에 들어가는지 여부를 먼저 판단해야 함

## 정리

이 검토의 핵심은 `전직 변호사 흔적 제거`가 아니다.

핵심 질문은 두 가지다.

1. 지금도 캐릭터가 `현직 법조인`처럼 보이게 만드는 구조가 남아 있는가
2. `사람들 싸움을 지켜보는 일이 힘들어서 떠났고, 글씨를 쓰고 마음을 전하는 일이 좋아서 현재를 산다`는 서사가 충분히 현재 중심축으로 서 있는가

따라서 수정 검토는 다음 방향으로 진행해야 한다.

- `전직 변호사` 과거는 유지
- `현직 법조인처럼 보이게 하는 현재형 문맥`은 약화 또는 제거
- `캘리그라피 작가의 생활감, 정서, 작업 이유, 작업 환경`은 강화
