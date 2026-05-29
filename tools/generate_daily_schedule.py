#!/usr/bin/env python3
"""
Daily schedule generator for 응우 (이은우, 33세 변호사).
Triggered at wakeup time by launchd. Generates daily_schedule_state.json.
"""
import json, random, datetime, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT, "state", "daily_schedule_state.json")
MEDIA_HISTORY_PATH = os.path.join(ROOT, "state", "media_pick_history.json")


def pick_without_repeat(pool: list, history_key: str, days_avoid: int = 7) -> dict:
    try:
        with open(MEDIA_HISTORY_PATH) as f:
            history = json.load(f)
    except Exception:
        history = {}
    today = datetime.date.today().isoformat()
    recent = history.get(history_key, [])
    cutoff = (datetime.date.today() - datetime.timedelta(days=days_avoid)).isoformat()
    recent_titles = {r["title"] for r in recent if r.get("date", "") >= cutoff}
    candidates = [p for p in pool if p.get("title", "") not in recent_titles]
    if not candidates:
        candidates = pool
    seed = int(today.replace("-", "")) % len(candidates)
    chosen = candidates[seed]
    recent.append({"date": today, "title": chosen.get("title", "")})
    history[history_key] = recent[-30:]
    try:
        with open(MEDIA_HISTORY_PATH, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return chosen

# ── Data pools ─────────────────────────────────────────────────────────────────

WEEKDAY_WAKEUP = ["07:00", "07:10", "07:15", "07:20", "07:30"]

WEEKDAY_BREAKFAST = [
    {"menu": "없음 (커피만)", "time_offset": 0},
    {"menu": "토스트 + 커피", "time_offset": 10},
    {"menu": "바나나 + 아메리카노", "time_offset": 5},
    {"menu": "그래놀라 + 우유", "time_offset": 8},
    {"menu": "요거트 + 과일", "time_offset": 8},
    {"menu": "삶은 계란 + 커피", "time_offset": 5},
]

WEEKDAY_COMMUTE = [
    {"route": "지하철 2호선", "duration": 35},
    {"route": "지하철 환승 (2·9호선)", "duration": 42},
    {"route": "지하철 직통", "duration": 30},
    {"route": "지하철 + 버스 환승", "duration": 45},
]

WEEKDAY_WORK_START = "09:00"
WORK_LOCATION = "강남구 법무법인"

WEEKDAY_BUSY = [
    {"level": "heavy", "reason": "오전에 소장 초안 마감이 있어서 계속 서면 쓰느라 정신없었어"},
    {"level": "heavy", "reason": "의뢰인 긴급 상담이 두 건 연달아 들어와서 빡빡했어"},
    {"level": "heavy", "reason": "내일 변론기일이라 준비서면 마무리하느라 점심도 짧게 먹었어"},
    {"level": "moderate", "reason": "계약서 검토 두 건이랑 내부 회의 있었어. 그래도 숨 좀 쉬었어"},
    {"level": "moderate", "reason": "오전은 판례 리서치, 오후는 의뢰인 미팅 두 건"},
    {"level": "light", "reason": "오늘은 비교적 여유 있었어. 서면 정리하고 문서 검토 위주"},
    {"level": "light", "reason": "재판 없는 날이라 사무실에서 문서 작업만 했어"},
]

MORNING_TASKS_POOL = [
    [
        {"task": "사건 파일 검토 및 의뢰인 이메일 확인"},
        {"task": "계약서 조항 검토"},
        {"task": "소장 초안 작성"},
        {"task": "내부 법무 회의"},
    ],
    [
        {"task": "판례 데이터베이스 리서치"},
        {"task": "법원 제출 서면 교정"},
        {"task": "의뢰인 전화 상담"},
        {"task": "파트너 변호사 보고"},
    ],
    [
        {"task": "계약서 협상 조항 정리"},
        {"task": "의뢰인 미팅 준비"},
        {"task": "법원 기일 확인 및 일정 조율"},
        {"task": "준비서면 검토 및 수정"},
    ],
]

AFTERNOON_TASKS_POOL = [
    [
        {"task": "의뢰인 대면 상담 (1시간)"},
        {"task": "계약서 최종 검토"},
        {"task": "서면 제출 마무리"},
        {"task": "사건 기록 업데이트"},
    ],
    [
        {"task": "법원 제출 서류 완성"},
        {"task": "상대방 측 의견서 검토"},
        {"task": "파트너 회의"},
        {"task": "이메일 답신 처리"},
    ],
    [
        {"task": "증거 자료 정리"},
        {"task": "내일 변론 기일 준비"},
        {"task": "의뢰인 진행상황 보고"},
        {"task": "사무 마감"},
    ],
]

WEEKDAY_LUNCH = [
    {"menu": "된장찌개 정식", "location": "사무실 근처 한식당", "with": "혼자"},
    {"menu": "팀 회식 (삼겹살)", "location": "사무실 근처 고깃집", "with": "팀원들"},
    {"menu": "파스타", "location": "이탈리안 레스토랑", "with": "혼자"},
    {"menu": "김치찌개 + 공기밥", "location": "사무실 근처 백반집", "with": "혼자"},
    {"menu": "샐러드 + 샌드위치", "location": "카페", "with": "혼자"},
    {"menu": "냉면", "location": "사무실 근처 냉면집", "with": "혼자"},
    {"menu": "돈까스 정식", "location": "사무실 근처 일식당", "with": "혼자"},
    {"menu": "초밥 세트", "location": "사무실 근처 초밥집", "with": "혼자"},
    {"menu": "순두부찌개 정식", "location": "사무실 근처 한식당", "with": "혼자"},
    {"menu": "쌀국수", "location": "사무실 근처 베트남 식당", "with": "혼자"},
    {"menu": "편의점 도시락 (바빠서)", "location": "편의점", "with": "혼자"},
]

WEEKDAY_OFFWORK = [
    {"time": "18:00", "note": "정시 퇴근"},
    {"time": "18:30", "note": "조금 늦게 마무리"},
    {"time": "19:00", "note": "서면 끝내고 퇴근"},
    {"time": "19:30", "note": "야근 살짝"},
    {"time": "20:00", "note": "야근"},
]

WEEKDAY_DINNER = [
    {"menu": "파스타 (토마토 소스)", "location": "집", "cook": "직접 요리"},
    {"menu": "된장찌개 + 밥", "location": "집", "cook": "직접 요리"},
    {"menu": "볶음밥", "location": "집", "cook": "직접 요리"},
    {"menu": "계란프라이 + 밥 + 김치", "location": "집", "cook": "간단히"},
    {"menu": "닭가슴살 샐러드", "location": "집", "cook": "직접 요리"},
    {"menu": "배달 (치킨)", "location": "집", "cook": "배달"},
    {"menu": "배달 (마라탕)", "location": "집", "cook": "배달"},
    {"menu": "배달 (초밥)", "location": "집", "cook": "배달"},
    {"menu": "배달 (피자)", "location": "집", "cook": "배달"},
    {"menu": "냉동 만두 + 계란국", "location": "집", "cook": "간단히"},
    {"menu": "제육볶음 + 밥", "location": "집", "cook": "직접 요리"},
    {"menu": "오므라이스", "location": "집", "cook": "직접 요리"},
]

WEEKDAY_EXERCISE = [
    {"type": "런닝", "location": "한강 or 동네", "duration_min": 35, "shower": True},
    {"type": "헬스장", "location": "동네 헬스장", "duration_min": 60, "shower": True},
    {"type": "없음 (독서)", "location": "집", "duration_min": 60, "shower": False},
    {"type": "없음 (유튜브/OTT)", "location": "집", "duration_min": 90, "shower": False},
    {"type": "없음 (영어 공부)", "location": "집", "duration_min": 60, "shower": False},
    {"type": "없음 (음악 감상 + 쉬기)", "location": "집", "duration_min": 60, "shower": False},
]

NIGHT_OTT_PICKS = [
    # 드라마/영화
    {"platform": "넷플릭스", "title": "보던 드라마 다음화", "kind": "drama", "detail": ""},
    {"platform": "넷플릭스", "title": "미드 정주행 시작", "kind": "drama", "detail": "영미 드라마 시즌1"},
    {"platform": "넷플릭스", "title": "범죄 스릴러 영화 한 편", "kind": "movie", "detail": "법정 스릴러"},
    {"platform": "웨이브", "title": "주말 못 본 한드 몰아보기", "kind": "drama", "detail": ""},
    # 시사/경제/사회
    {"platform": "유튜브", "title": "삼프로TV 오늘 방송 다시보기", "kind": "news", "detail": "삼프로TV 경제 이슈"},
    {"platform": "유튜브", "title": "뉴스공장 하이라이트 클립", "kind": "news", "detail": "시사 이슈 분석"},
    {"platform": "유튜브", "title": "1분미래 영상 몇 개", "kind": "news", "detail": "미래 트렌드 유튜버"},
    {"platform": "유튜브", "title": "슈카월드 요즘 영상", "kind": "news", "detail": "경제/사회 이슈 분석"},
    # 스포츠
    {"platform": "유튜브", "title": "오늘 야구 하이라이트", "kind": "sports", "detail": "KBO 하이라이트"},
    {"platform": "유튜브", "title": "NBA 명장면 쇼츠 보기", "kind": "sports", "detail": "NBA 슈퍼플레이 쇼츠"},
    {"platform": "유튜브", "title": "EPL 골 모음 클립", "kind": "sports", "detail": "프리미어리그 골장면"},
    # 예능
    {"platform": "유튜브", "title": "유퀴즈 명장면 클립 보기", "kind": "variety", "detail": "유퀴즈온더블럭 클립"},
    {"platform": "유튜브", "title": "피식대학 최신 영상", "kind": "variety", "detail": "피식대학 코미디"},
    {"platform": "넷플릭스", "title": "가볍게 보는 예능 한 편", "kind": "variety", "detail": ""},
    # 다큐/지식
    {"platform": "유튜브", "title": "역사 다큐 하나 틀어놓기", "kind": "documentary", "detail": "한국사/세계사 다큐"},
    {"platform": "넷플릭스", "title": "사회 이슈 다큐멘터리", "kind": "documentary", "detail": ""},
    {"platform": "유튜브", "title": "테크 리뷰 채널 신상 영상", "kind": "tech", "detail": "삼성/애플 신제품 리뷰"},
    # 힐링/음악
    {"platform": "유튜브", "title": "재즈 바 플레이리스트 배경음", "kind": "music", "detail": "저녁 재즈 플레이리스트"},
    {"platform": "유튜브", "title": "로파이 음악 틀어놓고 뒹굴기", "kind": "music", "detail": "lofi hip hop 집중"},
]

NIGHT_READING_PICKS = [
    "읽던 소설 몇 장",
    "법률 관련 서적 조금",
    "자기계발서 가볍게",
    "뉴스 피드 훑어보기",
]

NIGHT_WINDDOWN_ACTIVITIES = [
    "스킨케어 마무리하고 핸드폰 내려놓기",
    "내일 스케줄 확인하고 침대에 눕기",
    "음악 틀어놓고 멍때리기",
    "팟캐스트 들으면서 뒹굴기",
    "물 한 잔 마시고 불 끄기",
]

SLEEP_TARGET = ["23:00", "23:30", "00:00", "00:30"]

WEEKEND_WAKEUP = ["08:30", "09:00", "09:30", "10:00"]

WEEKEND_BRUNCH = [
    {"menu": "카페 브런치 (에그베네딕트)", "location": "동네 카페"},
    {"menu": "토스트 + 카페라떼", "location": "집"},
    {"menu": "아보카도 토스트 + 아이스 아메리카노", "location": "카페"},
    {"menu": "파케팅 브런치", "location": "브런치 카페"},
    {"menu": "간단히 과일 + 요거트", "location": "집"},
    {"menu": "편의점 샌드위치 + 커피", "location": "편의점"},
]

WEEKEND_ACTIVITY = [
    {"type": "카페 작업", "detail": "판례 정리 or 독서"},
    {"type": "친구 만남", "detail": "카페 or 식사"},
    {"type": "쇼핑", "detail": "백화점 or 아울렛"},
    {"type": "런닝", "detail": "한강공원 40분"},
    {"type": "헬스장", "detail": "근력운동 1시간"},
    {"type": "집콕 휴식", "detail": "OTT 정주행"},
    {"type": "청소 + 빨래", "detail": "집 정리"},
    {"type": "미용실", "detail": "트리트먼트 or 커트"},
    {"type": "서점", "detail": "교보문고 둘러보기"},
]

WEEKEND_DINNER = [
    {"menu": "마라탕", "location": "근처 마라탕 집"},
    {"menu": "삼겹살", "location": "고깃집"},
    {"menu": "스시 오마카세", "location": "초밥집"},
    {"menu": "파스타 코스", "location": "이탈리안"},
    {"menu": "집밥 (제대로 요리)", "location": "집"},
    {"menu": "배달 (치킨 + 맥주)", "location": "집"},
]


def hm(time_str: str, offset_min: int = 0) -> str:
    h, m = map(int, time_str.split(":"))
    total = h * 60 + m + offset_min
    return f"{total // 60:02d}:{total % 60:02d}"


def build_task_timeline(start_hhmm: str, end_hhmm: str, tasks: list) -> list:
    sh, sm = map(int, start_hhmm.split(":"))
    eh, em = map(int, end_hhmm.split(":"))
    start_m = sh * 60 + sm
    end_m = eh * 60 + em
    if end_m <= start_m:
        end_m = start_m + len(tasks) * 60
    span = end_m - start_m
    slot = span // len(tasks)
    return [{"time": f"{(start_m + i * slot) // 60:02d}:{(start_m + i * slot) % 60:02d}", "task": t["task"]} for i, t in enumerate(tasks)]


def now_kst() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))


def generate_weekday(date_str: str) -> dict:
    wakeup = random.choice(WEEKDAY_WAKEUP)
    shower_done = hm(wakeup, 20)
    skincare_done = hm(shower_done, random.randint(5, 8))
    hair_done = hm(skincare_done, random.randint(8, 12))
    dress_done = hm(hair_done, random.randint(8, 12))
    breakfast = random.choice(WEEKDAY_BREAKFAST)
    breakfast_time = hm(dress_done, 3)
    commute = random.choice(WEEKDAY_COMMUTE)
    depart = hm(breakfast_time, breakfast["time_offset"] + random.randint(3, 7))
    arrive = hm(depart, commute["duration"])

    busy = random.choice(WEEKDAY_BUSY)
    morning_tasks_raw = random.choice(MORNING_TASKS_POOL)
    afternoon_tasks_raw = random.choice(AFTERNOON_TASKS_POOL)
    lunch = random.choice(WEEKDAY_LUNCH)
    lunch_start = hm("12:00", random.randint(0, 40))
    lunch_end = hm(lunch_start, 45)
    offwork = random.choice(WEEKDAY_OFFWORK)
    arrive_home = hm(offwork["time"], commute["duration"] + random.randint(-5, 10))

    dinner = random.choice(WEEKDAY_DINNER)
    if dinner["cook"] == "배달":
        dinner_cook_start = hm(arrive_home, 5)   # 주문
        dinner_eat = hm(arrive_home, 35)           # 배달 도착
    else:
        dinner_cook_start = hm(arrive_home, 15)
        dinner_eat = hm(dinner_cook_start, random.randint(20, 30))
    dinner_end = hm(dinner_eat, 25)

    exercise = random.choice(WEEKDAY_EXERCISE)
    exercise_start = hm(dinner_end, 15)
    exercise_end = hm(exercise_start, exercise["duration_min"]) if exercise["duration_min"] > 0 else exercise_start
    if exercise["shower"]:
        shower_after = hm(exercise_end, 5)
        hair_dry = hm(shower_after, 15)
        night_start = hair_dry
    else:
        shower_after = None
        hair_dry = None
        night_start = exercise_end if exercise["duration_min"] > 0 else hm(dinner_end, 30)

    sleep = random.choice(SLEEP_TARGET)
    ott = pick_without_repeat(NIGHT_OTT_PICKS, "night_ott")
    ns_m = int(night_start.split(":")[0]) * 60 + int(night_start.split(":")[1])
    st_m = int(sleep.split(":")[0]) * 60 + int(sleep.split(":")[1])
    if st_m <= ns_m:
        st_m = ns_m + 90
    night_timeline = []
    night_timeline.append({"time": f"{ns_m // 60:02d}:{ns_m % 60:02d}", "activity": "스킨케어 하고 편한 옷으로 갈아입기"})
    content_t = ns_m + 15
    if random.random() < 0.6:
        night_timeline.append({"time": f"{content_t // 60:02d}:{content_t % 60:02d}", "activity": f"{ott['platform']}에서 {ott['title']} 보기"})
        night_content_label = f"{ott['platform']} {ott['title']}"
    else:
        reading = random.choice(NIGHT_READING_PICKS)
        night_timeline.append({"time": f"{content_t // 60:02d}:{content_t % 60:02d}", "activity": reading})
        night_content_label = reading
    winddown_t = max(content_t + 30, st_m - 30)
    night_timeline.append({"time": f"{winddown_t // 60:02d}:{winddown_t % 60:02d}", "activity": random.choice(NIGHT_WINDDOWN_ACTIVITIES)})
    night_timeline.append({"time": sleep, "activity": "잠자리에 눕기"})

    return {
        "date": date_str,
        "generated_at": now_kst().isoformat(),
        "day_type": "weekday",
        "morning": {
            "wakeup_time": wakeup,
            "shower_done": shower_done,
            "morning_prep": {
                "skincare_done": skincare_done,
                "hair_done": hair_done,
                "dress_done": dress_done,
                "note": "세안·스킨케어 → 헤어 정리 → 정장 입기",
            },
            "outfit": random.choice([
                "정장 (네이비 블레이저 + 슬랙스)", "정장 (차콜 슈트 + 화이트 셔츠)",
                "세미정장 (블레이저 + 슬랙스 + 넥타이)", "셔츠 + 슬랙스 (재킷 없이)",
                "정장 (그레이 슈트 + 타이)", "재킷 + 드레스 팬츠",
            ]),
            "breakfast": {"menu": breakfast["menu"], "time": breakfast_time},
            "depart_time": depart,
        },
        "commute_to_work": {
            "route": commute["route"],
            "depart_time": depart,
            "arrive_time": arrive,
            "location": WORK_LOCATION,
        },
        "work": {
            "start_time": WEEKDAY_WORK_START,
            "location": WORK_LOCATION,
            "busy_level": busy["level"],
            "busy_reason": busy["reason"],
            "morning_tasks": build_task_timeline(arrive, lunch_start, morning_tasks_raw),
            "afternoon_tasks": build_task_timeline(lunch_end, offwork["time"], afternoon_tasks_raw),
        },
        "lunch": {
            "menu": lunch["menu"],
            "location": lunch["location"],
            "with": lunch["with"],
            "time": lunch_start,
            "end_time": lunch_end,
        },
        "commute_home": {
            "depart_time": offwork["time"],
            "note": offwork["note"],
            "arrive_time": arrive_home,
        },
        "dinner": {
            "menu": dinner["menu"],
            "location": dinner["location"],
            "cook_note": dinner["cook"],
            "cook_start": dinner_cook_start,
            "eat_time": dinner_eat,
            "end_time": dinner_end,
        },
        "evening": {
            "activity_type": exercise["type"],
            "location": exercise["location"],
            "start_time": exercise_start,
            "duration_min": exercise["duration_min"],
            "end_time": exercise_end,
            "shower_after": shower_after,
            "hair_dry_time": hair_dry,
        },
        "night": {
            "wind_down_start": night_start,
            "content": night_content_label,
            "timeline": night_timeline,
            "sleep_target": sleep,
        },
    }


def generate_weekend(date_str: str, day_type: str) -> dict:
    wakeup = random.choice(WEEKEND_WAKEUP)
    brunch = random.choice(WEEKEND_BRUNCH)
    brunch_time = hm(wakeup, 30 + random.randint(0, 30))
    activity = random.choice(WEEKEND_ACTIVITY)
    activity_start = hm(brunch_time, 60 + random.randint(0, 60))
    dinner = random.choice(WEEKEND_DINNER)
    dinner_time = hm("18:30", random.randint(0, 60))
    sleep = random.choice(SLEEP_TARGET)

    return {
        "date": date_str,
        "generated_at": now_kst().isoformat(),
        "day_type": day_type,
        "morning": {
            "wakeup_time": wakeup,
            "outfit": random.choice([
                "캐주얼 (린넨 셔츠 + 청바지)", "캐주얼 (오버핏 티 + 슬랙스)",
                "홈웨어 (편한 티 + 반바지)", "반팔 원피스", "니트 + 청바지",
            ]),
            "brunch": {"menu": brunch["menu"], "location": brunch["location"], "time": brunch_time},
        },
        "daytime": {
            "activity_type": activity["type"],
            "detail": activity["detail"],
            "start_time": activity_start,
        },
        "dinner": {
            "menu": dinner["menu"],
            "location": dinner["location"],
            "eat_time": dinner_time,
        },
        "night": {
            "shower_time": hm(dinner_time, 60 + random.randint(0, 30)),
            "sleep_target": sleep,
        },
    }


def main() -> None:
    now = now_kst()
    date_str = now.strftime("%Y-%m-%d")
    weekday = now.weekday()  # 0=Mon, 6=Sun

    if weekday < 5:
        schedule = generate_weekday(date_str)
    elif weekday == 5:
        schedule = generate_weekend(date_str, "saturday")
    else:
        schedule = generate_weekend(date_str, "sunday")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"[daily_schedule] {date_str} ({schedule['day_type']}) generated → {OUTPUT_PATH}")
    print(f"  wakeup: {schedule['morning']['wakeup_time']}")
    if schedule['day_type'] == 'weekday':
        print(f"  lunch: {schedule['lunch']['menu']} @ {schedule['lunch']['location']}")
        print(f"  offwork: {schedule['commute_home']['depart_time']} ({schedule['commute_home']['note']})")
    print(f"  dinner: {schedule['dinner']['menu']}")
    print(f"  sleep: {schedule['night']['sleep_target']}")

    # 오늘의 Netflix picks 실제 검색 (백그라운드)
    try:
        import subprocess as _sp
        _sp.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), "fetch_netflix_picks.py")],
            stdout=open(os.path.join(ROOT, "state", "netflix_fetch.log"), "a"),
            stderr=_sp.STDOUT,
        )
        print("[daily_schedule] Netflix picks 검색 시작 (백그라운드)")
    except Exception as e:
        print(f"[daily_schedule] Netflix picks 검색 실패: {e}")


if __name__ == "__main__":
    main()
