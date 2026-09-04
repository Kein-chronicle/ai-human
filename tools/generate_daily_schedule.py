#!/usr/bin/env python3
"""
응우(이은우, 33세 캘리그라피 작가 전직 변호사) 일과 생성기 v3
고정 시간 구조: 기상 08:00 → 생활시작 08:30 → 연락 09:00 → 점심 12:00 → 오후 작업 13:00
              → 저녁 식사 19:00 → 운동 20:30 → 취침 00:30
요리가 기본: 준비-조리-식사-정리 세부 타임라인 포함
"""
import json, random, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT, "state", "daily_schedule_state.json")
MEDIA_HISTORY_PATH = os.path.join(ROOT, "state", "media_pick_history.json")
KST = datetime.timezone(datetime.timedelta(hours=9))


def now_kst():
    return datetime.datetime.now(KST)


def pick_no_repeat(pool: list, history_key: str, days_avoid: int = 4) -> dict:
    try:
        with open(MEDIA_HISTORY_PATH, encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = {}
    today = now_kst().date().isoformat()
    cutoff = (now_kst().date() - datetime.timedelta(days=days_avoid)).isoformat()
    recent = {r["title"] for r in history.get(history_key, []) if r.get("date", "") >= cutoff}
    candidates = [p for p in pool if p.get("title", p.get("menu", "")) not in recent]
    if not candidates:
        candidates = pool
    seed = abs(hash(today + history_key)) % len(candidates)
    chosen = candidates[seed]
    rec = history.get(history_key, [])
    rec.append({"date": today, "title": chosen.get("title", chosen.get("menu", ""))})
    history[history_key] = rec[-20:]
    try:
        with open(MEDIA_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return chosen


# ── 아침 음료 풀 ────────────────────────────────────────────────────────────
MORNING_DRINK = [
    {"item": "아메리카노", "note": "커피머신으로 내려서"},
    {"item": "핸드드립 커피", "note": "드리퍼로 천천히"},
    {"item": "물 먼저 한 잔", "note": "일어나자마자"},
    {"item": "아이스 아메리카노", "note": "얼음 넣어서"},
]

# ── 점심 요리 풀 (집에서 해먹음) ──────────────────────────────────────────
LUNCH_RECIPES = [
    {"menu": "계란볶음밥", "prep_min": 15, "cook_min": 10, "eat_min": 15, "clean_min": 10,
     "ingredients": "계란, 밥, 파, 간장"},
    {"menu": "참치 김치찌개", "prep_min": 10, "cook_min": 20, "eat_min": 20, "clean_min": 10,
     "ingredients": "참치캔, 김치, 두부, 대파"},
    {"menu": "라면 + 계란", "prep_min": 5, "cook_min": 5, "eat_min": 15, "clean_min": 5,
     "ingredients": "라면, 계란, 대파"},
    {"menu": "스파게티 아그리오 올리오", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 10,
     "ingredients": "파스타, 마늘, 올리브오일, 페페론치노"},
    {"menu": "된장찌개 + 밥", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 10,
     "ingredients": "된장, 두부, 애호박, 대파, 밥"},
    {"menu": "제육볶음 + 밥", "prep_min": 15, "cook_min": 15, "eat_min": 20, "clean_min": 10,
     "ingredients": "돼지고기, 고추장, 양파, 밥"},
    {"menu": "토스트 + 수프", "prep_min": 10, "cook_min": 10, "eat_min": 15, "clean_min": 5,
     "ingredients": "식빵, 계란, 치즈, 캔수프"},
    {"menu": "오므라이스", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 10,
     "ingredients": "계란, 밥, 케첩, 버터, 양파"},
]

# ── 저녁 요리 풀 (집에서 해먹음, 점심보다 약간 정성) ──────────────────────
DINNER_RECIPES = [
    {"menu": "삼겹살 구이", "prep_min": 10, "cook_min": 20, "eat_min": 30, "clean_min": 15,
     "ingredients": "삼겹살, 쌈채소, 마늘, 된장"},
    {"menu": "닭볶음탕", "prep_min": 15, "cook_min": 30, "eat_min": 25, "clean_min": 10,
     "ingredients": "닭, 감자, 양파, 고추장, 간장"},
    {"menu": "된장찌개 + 제육볶음", "prep_min": 20, "cook_min": 20, "eat_min": 25, "clean_min": 15,
     "ingredients": "돼지고기, 고추장, 된장, 두부, 밥"},
    {"menu": "소고기 미역국 + 밥", "prep_min": 10, "cook_min": 30, "eat_min": 20, "clean_min": 10,
     "ingredients": "소고기, 미역, 참기름"},
    {"menu": "부대찌개", "prep_min": 15, "cook_min": 20, "eat_min": 25, "clean_min": 10,
     "ingredients": "햄, 소시지, 김치, 라면사리, 두부"},
    {"menu": "고등어구이 + 밥 + 국", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 15,
     "ingredients": "고등어, 무, 콩나물국"},
    {"menu": "카레라이스", "prep_min": 15, "cook_min": 25, "eat_min": 20, "clean_min": 10,
     "ingredients": "카레, 감자, 당근, 양파, 돼지고기"},
    {"menu": "순두부찌개 + 밥", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 10,
     "ingredients": "순두부, 바지락, 계란, 고추"},
]

# ── 오후 작업 유형 풀 ────────────────────────────────────────────────────────
AFTERNOON_WORK = [
    {"type": "커미션 작업", "detail": "의뢰받은 작업 집중. 마감 맞춰야 해서 집중도 높음"},
    {"type": "글씨 연습", "detail": "특정 자음/모음 또는 서체 집중 연습"},
    {"type": "포트폴리오 정리", "detail": "인스타 올릴 작품 사진 찍고 편집"},
    {"type": "새 구도 실험", "detail": "구도·레이아웃 다양하게 시도"},
    {"type": "잉크·종이 테스트", "detail": "새 재료 테스트 세션"},
    {"type": "캘리그라피 공부", "detail": "유튜브 영상 보거나 책 보며 이론 공부"},
]

# ── 운동 후 활동 풀 ─────────────────────────────────────────────────────────
POST_GYM_ACTIVITY = [
    "샤워 후 스트레칭하다 잠들 준비",
    "샤워 후 간단히 유튜브 보다가",
    "샤워 후 누나한테 연락하고 싶어지는 시간",
    "샤워 후 침대에 누워서 핸드폰 잠깐",
]

# ── 작업복 풀 ────────────────────────────────────────────────────────────────
OUTFIT_OPTIONS = [
    "편한 맨투맨 + 트레이닝 바지",
    "루즈핏 티셔츠 + 면바지",
    "후드티 + 조거 팬츠",
    "린넨 셔츠 + 면바지",
    "오버핏 티셔츠 + 반바지",
]

GYM_OUTFIT = "헬스 티셔츠 + 레깅스 또는 트레이닝 팬츠"


def _add_min(hhmm: str, minutes: int) -> str:
    try:
        h, m = map(int, hhmm.split(":"))
        t = h * 60 + m + minutes
        return f"{t // 60 % 24:02d}:{t % 60:02d}"
    except Exception:
        return hhmm


def is_holiday(date_str: str) -> bool:
    try:
        p = os.path.join(ROOT, "state", "holidays.json")
        with open(p, encoding="utf-8") as f:
            return date_str in json.load(f).get("holidays", {})
    except Exception:
        return False


def generate_weekday(date_str: str) -> dict:
    rng = random.Random(f"eunwoo_v3:{date_str}")
    drink = pick_no_repeat(MORNING_DRINK, "drink")
    outfit = rng.choice(OUTFIT_OPTIONS)
    lunch = pick_no_repeat(LUNCH_RECIPES, "lunch")
    dinner = pick_no_repeat(DINNER_RECIPES, "dinner")
    afternoon = rng.choice(AFTERNOON_WORK)
    post_gym = rng.choice(POST_GYM_ACTIVITY)

    # 점심 세부 타임라인
    lunch_prep_start = "11:30"
    lunch_cook_start = _add_min(lunch_prep_start, lunch["prep_min"])
    lunch_eat_start = _add_min(lunch_cook_start, lunch["cook_min"])
    lunch_clean_start = _add_min(lunch_eat_start, lunch["eat_min"])
    lunch_done = _add_min(lunch_clean_start, lunch["clean_min"])

    # 저녁 세부 타임라인
    dinner_prep_start = "18:30"
    dinner_cook_start = _add_min(dinner_prep_start, dinner["prep_min"])
    dinner_eat_start = _add_min(dinner_cook_start, dinner["cook_min"])
    dinner_clean_start = _add_min(dinner_eat_start, dinner["eat_min"])
    dinner_done = _add_min(dinner_clean_start, dinner["clean_min"])

    # 운동 타임라인
    gym_start = "20:30"
    gym_end = "21:30"
    shower_done = "22:00"
    wind_down = "22:30"
    sleep_time = "00:30"

    return {
        "date": date_str,
        "day_type": "weekday",
        "morning": {
            "wakeup_time": "08:00",
            "drink": drink.get("item"),
            "drink_note": drink.get("note"),
            "life_start": "08:30",
            "contact_start": "09:00",
            "outfit": outfit,
            "note": "기상 후 커피 마시며 창밖 잠깐 보고 하루 시작. 09시부터 폰 체크하며 연락 시작.",
        },
        "morning_work": {
            "start": "09:00",
            "end": "11:30",
            "activity": "오전 작업 또는 연습. 집중도 높은 시간.",
            "coffee_refill": "10:30",
        },
        "lunch": {
            "menu": lunch["menu"],
            "ingredients": lunch.get("ingredients", ""),
            "timeline": {
                "prep_start": lunch_prep_start,
                "cook_start": lunch_cook_start,
                "eat_start": lunch_eat_start,
                "clean_start": lunch_clean_start,
                "done": lunch_done,
            },
            "prep_min": lunch["prep_min"],
            "cook_min": lunch["cook_min"],
            "eat_min": lunch["eat_min"],
            "clean_min": lunch["clean_min"],
            "location": "집 주방",
            "note": "직접 해먹음. 요리하는 시간 자체가 기분 전환.",
        },
        "afternoon_work": {
            "start": lunch_done,
            "end": "18:30",
            "type": afternoon["type"],
            "detail": afternoon["detail"],
            "coffee_break": "15:30",
            "note": "오후 집중 작업 시간. 중간에 잠깐 스트레칭.",
        },
        "dinner": {
            "menu": dinner["menu"],
            "ingredients": dinner.get("ingredients", ""),
            "timeline": {
                "prep_start": dinner_prep_start,
                "cook_start": dinner_cook_start,
                "eat_start": dinner_eat_start,
                "clean_start": dinner_clean_start,
                "done": dinner_done,
            },
            "prep_min": dinner["prep_min"],
            "cook_min": dinner["cook_min"],
            "eat_min": dinner["eat_min"],
            "clean_min": dinner["clean_min"],
            "location": "집 주방",
            "note": "점심보다 조금 더 정성 들여서. 요리하면서 음악 틀어놓음.",
        },
        "pre_gym": {
            "start": dinner_done,
            "end": gym_start,
            "activity": "운동 준비. 가방 챙기거나 잠깐 쉬거나.",
        },
        "gym": {
            "start": gym_start,
            "end": gym_end,
            "outfit": GYM_OUTFIT,
            "activity": "헬스장. 근력 위주. 가끔 유산소 조금.",
            "shower_done": shower_done,
        },
        "night": {
            "wind_down": wind_down,
            "activity": post_gym,
            "sleep_target": sleep_time,
        },
        "schema_version": 3,
        "managed_by": "generate_daily_schedule_eunwoo_v3",
    }


def generate_weekend(date_str: str, day_type: str) -> dict:
    rng = random.Random(f"eunwoo_wknd_v3:{date_str}")
    drink = pick_no_repeat(MORNING_DRINK, "drink_wknd")
    outfit = rng.choice(OUTFIT_OPTIONS)
    brunch = pick_no_repeat(LUNCH_RECIPES + [
        {"menu": "팬케이크", "prep_min": 10, "cook_min": 15, "eat_min": 20, "clean_min": 10},
        {"menu": "아보카도 토스트", "prep_min": 10, "cook_min": 5, "eat_min": 15, "clean_min": 5},
    ], "brunch")
    dinner = pick_no_repeat(DINNER_RECIPES, "dinner_wknd")
    afternoon = rng.choice(AFTERNOON_WORK + [
        {"type": "공원 산책", "detail": "자연 보러 공원이나 동네 나무 많은 곳"},
        {"type": "화방 방문", "detail": "새 재료 보러 화방·문구점"},
    ])

    brunch_prep = "09:30"
    brunch_eat = _add_min(brunch_prep, brunch["prep_min"] + brunch["cook_min"])
    brunch_done = _add_min(brunch_eat, brunch["eat_min"] + brunch["clean_min"])

    dinner_prep = "18:30"
    dinner_eat = _add_min(dinner_prep, dinner["prep_min"] + dinner["cook_min"])
    dinner_done = _add_min(dinner_eat, dinner["eat_min"] + dinner["clean_min"])

    return {
        "date": date_str,
        "day_type": day_type,
        "morning": {
            "wakeup_time": "09:00",
            "drink": drink.get("item"),
            "note": "주말은 좀 더 여유롭게 일어남.",
            "outfit": outfit,
        },
        "brunch": {
            "menu": brunch["menu"],
            "timeline": {
                "prep_start": brunch_prep,
                "eat_start": brunch_eat,
                "done": brunch_done,
            },
            "location": "집 주방",
        },
        "daytime": {
            "start": brunch_done,
            "end": "18:30",
            "activity": afternoon["type"],
            "detail": afternoon["detail"],
        },
        "dinner": {
            "menu": dinner["menu"],
            "timeline": {
                "prep_start": dinner_prep,
                "eat_start": dinner_eat,
                "done": dinner_done,
            },
            "location": "집 주방",
        },
        "gym": {
            "start": "20:30",
            "end": "21:30",
            "shower_done": "22:00",
        },
        "night": {
            "wind_down": "22:30",
            "sleep_target": "01:00",
        },
        "schema_version": 3,
        "managed_by": "generate_daily_schedule_eunwoo_v3",
    }


def main():
    today = now_kst().date()
    date_str = today.isoformat()
    weekday = today.weekday()

    if is_holiday(date_str):
        sched = generate_weekend(date_str, "holiday")
        sched["day_type"] = "holiday"
    elif weekday < 5:
        sched = generate_weekday(date_str)
    elif weekday == 5:
        sched = generate_weekend(date_str, "saturday")
    else:
        sched = generate_weekend(date_str, "sunday")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sched, f, ensure_ascii=False, indent=2)

    print(f"[응우 schedule v3] {date_str} ({sched['day_type']}) 생성 완료")
    if sched.get("lunch"):
        lt = sched["lunch"]["timeline"]
        print(f"  점심: {sched['lunch']['menu']} (준비 {lt['prep_start']} → 식사 {lt['eat_start']} → 완료 {lt['done']})")
    if sched.get("dinner"):
        dt = sched["dinner"]["timeline"]
        print(f"  저녁: {sched['dinner']['menu']} (준비 {dt['prep_start']} → 식사 {dt['eat_start']} → 완료 {dt['done']})")
    if sched.get("gym"):
        print(f"  운동: {sched['gym']['start']}~{sched['gym']['end']} → 샤워 완료 {sched['gym']['shower_done']}")
    print(f"  취침: {sched.get('night',{}).get('sleep_target','00:30')}")


if __name__ == "__main__":
    main()
