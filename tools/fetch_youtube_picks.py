#!/usr/bin/env python3
"""
실제 YouTube 영상 검색 후 오늘의 picks를 state/daily_youtube_picks.json에 저장.
generate_daily_schedule.py에서 호출됨.
응우(이은우, 33세, 변호사) 캐릭터 취향 기반.
"""
import json, subprocess, datetime, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT, "state", "daily_youtube_picks.json")

# 여자친구한테 "이거 봐봐" 하고 보낼 만한 콘텐츠만
SHARE_QUERIES = [
    # 웃긴/재밌는
    ("웃긴영상", "피식대학 최신 영상"),
    ("웃긴영상", "빠니보틀 웃긴 여행 영상"),
    ("웃긴영상", "침착맨 웃긴 장면 클립"),
    ("웃긴영상", "숏박스 최신 쇼츠"),
    # 귀여운/동물
    ("귀여운", "고양이 강아지 귀여운 영상 쇼츠"),
    ("귀여운", "아기 동물 귀여운 쇼츠"),
    # 감성 맛집/카페 (같이 가보자)
    ("맛집", "서울 뜨는 맛집 리뷰 2025"),
    ("맛집", "서울 감성 카페 브이로그 2025"),
    ("맛집", "요즘 핫한 팝업스토어 서울"),
    # 공감
    ("공감", "30대 직장인 공감 영상"),
    ("공감", "연애 공감 웃긴 쇼츠"),
    # 재밌는 콘텐츠
    ("예능", "유퀴즈 명장면 클립 웃긴"),
    ("예능", "나혼자산다 재밌는 클립"),
]

# 혼자 보는 것 (공유 안 함, 보고있다고 언급만 가능)
SOLO_QUERIES = [
    ("시사경제", "슈카월드 최신"),
    ("스포츠", "KBO 야구 하이라이트"),
    ("스포츠", "NBA 쇼츠 명장면"),
    ("예능", "유퀴즈 클립"),
    ("다큐", "역사 다큐"),
]

PROACTIVE_TEMPLATES = [
    "수정아 이거 봐봐 ㅋㅋ 진짜 웃겨 → {url}",
    "이거 보다가 생각났어. 수정이도 좋아할 것 같아서 → {url}",
    "야 이거 봤어? {title} ㅋㅋ",
    "이거 같이 보고 싶어서 → {url}",
    "방금 이거 보면서 수정이 생각났어 → {url}",
    "{title} 이거 꼭 봐봐 ㅋㅋ",
]

def search_youtube(query: str, max_results: int = 3) -> list:
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--print", "%(title)s\t%(url)s\t%(channel)s\t%(duration)s",
                f"ytsearch{max_results}:{query}",
                "--no-warnings",
                "--quiet",
            ],
            capture_output=True, text=True, timeout=20
        )
        picks = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            title = parts[0].strip()
            url = parts[1].strip()
            channel = parts[2].strip() if len(parts) > 2 else ""
            duration_s = float(parts[3]) if len(parts) > 3 and parts[3].replace(".", "").isdigit() else 0
            if duration_s and (duration_s < 30 or duration_s > 3600):
                continue
            is_shorts = duration_s > 0 and duration_s <= 65
            picks.append({
                "title": title,
                "url": url,
                "channel": channel,
                "duration_s": int(duration_s),
                "is_shorts": is_shorts,
            })
        return picks
    except Exception:
        return []


def run():
    today = datetime.date.today().isoformat()
    random.seed(int(today.replace("-", "")))

    # 공유용 영상 (수정이한테 보내는 것)
    selected_share = random.sample(SHARE_QUERIES, min(4, len(SHARE_QUERIES)))
    share_picks = []
    for category, query in selected_share:
        results = search_youtube(query, max_results=2)
        for r in results:
            r["category"] = category
            r["shareable"] = True
            tmpl = random.choice(PROACTIVE_TEMPLATES)
            r["proactive_hint"] = tmpl.format(title=r["title"], url=r["url"])
            share_picks.append(r)

    # 혼자 보는 영상 (언급만 가능, 링크 공유 없음)
    selected_solo = random.sample(SOLO_QUERIES, min(2, len(SOLO_QUERIES)))
    solo_picks = []
    for category, query in selected_solo:
        results = search_youtube(query, max_results=1)
        for r in results:
            r["category"] = category
            r["shareable"] = False
            r["proactive_hint"] = f"나 {r['title']} 보고 있어"
            solo_picks.append(r)

    all_picks = share_picks[:5] + solo_picks[:2]
    random.shuffle(all_picks)

    output = {
        "date": today,
        "character": "eunwoo",
        "picks": all_picks,
        "share_picks": share_picks[:5],
        "solo_picks": solo_picks[:2],
        "generated_at": datetime.datetime.now().isoformat(),
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[youtube_picks] {len(all_picks)} videos fetched → {OUTPUT_PATH}")


if __name__ == "__main__":
    run()
