#!/usr/bin/env python3
"""
Netflix Korea 공식 YouTube 채널에서 현재 방영/인기 중인 콘텐츠를 추출.
state/daily_netflix_picks.json에 저장.
응우(이은우, 33세, 변호사) 캐릭터가 보고 있을 법한 콘텐츠 리스트.
"""
import json, subprocess, datetime, os, sys, re, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT, "state", "daily_netflix_picks.json")


def fetch_from_netflix_korea_channel() -> list:
    """Netflix Korea 공식 유튜브 채널에서 최신 콘텐츠 제목 추출."""
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--print", "%(title)s",
                "https://www.youtube.com/@NetflixKorea/videos",
                "--playlist-items", "1-20",
                "--no-warnings",
                "--quiet",
            ],
            capture_output=True, text=True, timeout=30
        )
        titles = []
        seen = set()
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            # 하이라이트/티저/캐스팅 비하인드에서 콘텐츠 제목 추출
            # 패턴: "제목 | [콘텐츠명] | 넷플릭스" or "[콘텐츠명] | 넷플릭스"
            m = re.search(r'[|｜]\s*([^\|｜]+)\s*[|｜]\s*넷플릭스', line)
            if m:
                content_title = m.group(1).strip()
                # 콘텐츠 제목이 아닌 메타 키워드 필터
                skip_kw = ["공식", "예고편", "티저", "캐스팅", "하이라이트", "주간", "TOP",
                           "소개", "비하인드", "현장", "인터뷰", "비교", "클립", "선공개",
                           "에피소드", "화", "시즌 예고", "리뷰", "반응"]
                if any(kw in content_title for kw in skip_kw):
                    continue
                # 3글자 미만이거나 숫자만이면 스킵
                if len(content_title) < 3:
                    continue
                if content_title and content_title not in seen:
                    seen.add(content_title)
                    titles.append(content_title)
        return titles
    except Exception as e:
        print(f"[netflix_fetch] channel error: {e}")
        return []


# 응우가 볼 법한 콘텐츠 취향 (fallback + 보정용)
# 변호사 30대 남성: 액션/SF/스릴러 선호, 법정 드라마는 거의 안 봄
EUNWOO_GENRE_PREFS = {
    "좋아함": ["액션", "SF", "스릴러", "다큐", "범죄"],
    "싫어함": ["법정드라마", "로맨스"],
    "중립": ["예능", "코미디"],
}

FALLBACK_POOL = [
    {"title": "멋진 신세계", "genre": "로맨스코미디", "platform": "Netflix"},
    {"title": "원더풀스", "genre": "히어로코미디", "platform": "Netflix"},
    {"title": "유재석 캠프", "genre": "예능", "platform": "Netflix"},
    {"title": "솔로지옥 시즌5", "genre": "예능연애", "platform": "Netflix"},
    {"title": "카지노 시즌2", "genre": "범죄스릴러", "platform": "Netflix"},
    {"title": "D.P. 시즌3", "genre": "사회드라마", "platform": "Netflix"},
]

MENTION_TEMPLATES = [
    "나 요즘 {title} 보고 있어",
    "{title} 재밌다는 거 들었어. 아직 안 봤어?",
    "{title} 봤어? 요즘 난리던데",
    "어제 {title} 보다 잤어 ㅋㅋ",
    "{title} 한번 봐봐. 생각보다 재밌어",
]


def run():
    today = datetime.date.today().isoformat()
    random.seed(int(today.replace("-", "")))

    # Netflix Korea 채널에서 현재 방영 중인 콘텐츠 제목 추출
    live_titles = fetch_from_netflix_korea_channel()
    print(f"[netflix_fetch] live titles: {live_titles}")

    picks = []
    for title in live_titles[:6]:
        mention = random.choice(MENTION_TEMPLATES).format(title=title)
        picks.append({
            "title": title,
            "platform": "Netflix",
            "source": "netflix_korea_channel",
            "mention_hint": mention,
            "shareable": True,
        })

    # live가 부족하면 fallback으로 보완
    if len(picks) < 3:
        for item in random.sample(FALLBACK_POOL, min(3, len(FALLBACK_POOL))):
            if item["title"] not in [p["title"] for p in picks]:
                mention = random.choice(MENTION_TEMPLATES).format(title=item["title"])
                item["mention_hint"] = mention
                item["shareable"] = True
                item["source"] = "fallback"
                picks.append(item)

    output = {
        "date": today,
        "character": "eunwoo",
        "picks": picks,
        "generated_at": datetime.datetime.now().isoformat(),
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[netflix_fetch] {len(picks)} titles saved → {OUTPUT_PATH}")


if __name__ == "__main__":
    run()
