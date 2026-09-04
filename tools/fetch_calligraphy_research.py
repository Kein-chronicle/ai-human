#!/usr/bin/env python3
"""
캘리그라피 리서치 — 응우(이은우, 33세 캘리그라피 작가 전직 변호사)
매일 아침 캘리그라피 관련 유튜브 영상, 팁, 작가 정보를 검색해
state/calligraphy_research.json에 저장.
proactive-sender에서 읽어 수정이와의 대화에 활용.
"""
import json, subprocess, datetime, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT, "state", "calligraphy_research.json")
KST = datetime.timezone(datetime.timedelta(hours=9))


def now_kst():
    return datetime.datetime.now(KST)


# 수정이와 공유할 만한 캘리그라피 유튜브 검색 쿼리
SHARE_QUERIES = [
    ("캘리그라피", "캘리그라피 입문 초보 배우기"),
    ("캘리그라피", "한글 캘리그라피 기초 붓펜"),
    ("캘리그라피", "캘리그라피 감성 영상"),
    ("캘리그라피", "캘리그라피 작가 브이로그"),
    ("캘리그라피", "붓글씨 캘리그라피 쓰는 법"),
    ("캘리그라피", "캘리그라피 작품 만들기"),
    ("캘리그라피", "카드 편지 손글씨 캘리그라피"),
    ("캘리그라피", "웨딩 청첩장 캘리그라피 작업"),
    ("손글씨", "예쁜 손글씨 쓰는 법"),
    ("손글씨", "감성 손글씨 연습"),
]

# 혼자 보는 연습/공부용
SOLO_QUERIES = [
    ("캘리그라피", "캘리그라피 붓 종류 선택"),
    ("캘리그라피", "캘리그라피 잉크 종류 추천"),
    ("캘리그라피", "캘리그라피 구도 잡기"),
    ("캘리그라피", "캘리그라피 커미션 작업 과정"),
    ("캘리그라피", "한국 캘리그라피 작가 포트폴리오"),
]

# 오늘의 연습 주제 풀 (자기 연습 이야기)
PRACTICE_TOPICS = [
    {"topic": "곡선 획 연습", "note": "곡선이 자꾸 흔들려서 오늘은 그것만 집중해봄"},
    {"topic": "자음 자형 정리", "note": "ㅎ, ㄹ 같은 획이 많은 자음 집중 연습"},
    {"topic": "모음 균형 잡기", "note": "모음 비율이 자꾸 틀어져서 오늘은 눈금지에 연습"},
    {"topic": "압력 조절", "note": "붓 압력 세기에 따른 굵기 변화 컨트롤"},
    {"topic": "전체 단어 작업", "note": "단어 하나를 계속 써보면서 리듬감 찾기"},
    {"topic": "문장 구도 연습", "note": "한 줄 문장을 종이에 구도 잡아서 쓰기"},
    {"topic": "흘림체 입문", "note": "정자체만 하다가 흘림체 처음 시도"},
    {"topic": "서체 비교", "note": "같은 글자를 여러 서체로 써보며 차이 비교"},
    {"topic": "잉크 농도 테스트", "note": "물 비율 조절로 잉크 농도 변화 실험"},
    {"topic": "빠른 획 연습", "note": "너무 천천히 쓰는 습관 고치려고 속도 올려서 연습"},
]

# 공유할 팁/정보
TIPS = [
    "붓펜은 닥터그립이나 쿠레타케가 입문자한테 괜찮대. 나도 처음에 거기서 시작함.",
    "캘리그라피 유튜브 채널 중에 '손글씨연구소'가 기초 설명이 제일 쉽게 되어있더라고.",
    "하루 15분이라도 매일 쓰는 게 한 번에 두 시간 쓰는 것보다 낫다는 게 진짜인 것 같아.",
    "종이 질감이 생각보다 엄청 중요해. 화선지 계열이랑 일반 종이가 완전히 달라.",
    "유튜브 쇼츠로 캘리 영상 보면 감 잡는 데 도움 많이 돼. 짧은 거라도 보다 보면 눈이 익어.",
    "커미션 받을 때 고객이 원하는 느낌을 정확히 잡는 게 제일 어려운 부분 같아.",
    "붓 세척이 생각보다 중요함. 다 쓰고 바로 씻어야 잉크가 굳지 않아.",
    "문구점 가면 일본 붓펜이 다양한데 그것도 한번 써보면 재밌어.",
    "캘리그라피 인스타 계정 팔로하면 매일 좋은 작품 보면서 자극 받을 수 있어.",
    "글씨 쓸 때 호흡이 중요하다는 말이 처음엔 이해 안 됐는데 이제 좀 알 것 같아.",
]


def run_yt_search(query: str, max_results: int = 3) -> list:
    try:
        cmd = [
            "yt-dlp",
            f"ytsearch{max_results}:{query}",
            "--dump-json",
            "--flat-playlist",
            "--no-download",
            "--quiet",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        videos = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            try:
                v = json.loads(line)
                videos.append({
                    "title": v.get("title", ""),
                    "url": v.get("url", "") or f"https://www.youtube.com/watch?v={v.get('id','')}",
                    "channel": v.get("channel", v.get("uploader", "")),
                    "duration": v.get("duration_string", ""),
                })
            except Exception:
                pass
        return videos
    except Exception:
        return []


def main():
    today = now_kst().date().isoformat()
    rng = random.Random(today + "calli")

    # 오늘의 공유용 영상 검색
    share_query_cat, share_query = rng.choice(SHARE_QUERIES)
    share_videos = run_yt_search(share_query, 2)

    # 혼자 보는 연습 영상
    solo_query_cat, solo_query = rng.choice(SOLO_QUERIES)
    solo_videos = run_yt_search(solo_query, 2)

    # 오늘의 연습 주제
    practice = rng.choice(PRACTICE_TOPICS)

    # 오늘의 팁
    tip = rng.choice(TIPS)

    output = {
        "date": today,
        "generated_at": now_kst().isoformat(timespec="seconds"),
        "share": {
            "query": share_query,
            "category": share_query_cat,
            "videos": share_videos,
            "summary": f"오늘 찾아본 캘리그라피 영상: '{share_query}' 관련",
        },
        "solo_study": {
            "query": solo_query,
            "videos": solo_videos,
        },
        "today_practice": practice,
        "today_tip": tip,
        "share_ready": len(share_videos) > 0 or True,  # 항상 팁은 공유 가능
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"[calli_research] {today} 완료")
    print(f"  공유용 검색: {share_query} → {len(share_videos)}개 영상")
    print(f"  오늘 연습: {practice['topic']}")
    print(f"  팁: {tip[:50]}")


if __name__ == "__main__":
    main()
