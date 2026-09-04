#!/usr/bin/env python3
"""
컨텐츠 트래커 초기 시딩 — YouTube 채널 영상 전체 수집 및 저장.
최초 1회만 실행. 이후는 check_user_social.py가 신규 추가만 관리.
"""
import json, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
TRACKER_PATH = STATE / "content_tracker.json"
USER_ID_PATH = STATE / "user_identity.json"
KST = timezone(timedelta(hours=9))


def now_kst():
    return datetime.now(KST).isoformat(timespec="seconds")


def fetch_youtube_videos(handle: str, max_items: int = 100) -> list:
    print(f"[seed] YouTube {handle} 영상 수집 중...")
    url = f"https://www.youtube.com/{handle}/videos"
    result = subprocess.run(
        ["yt-dlp", "--dump-json", f"--playlist-items", f"1-{max_items}",
         "--no-download", "--quiet", url],
        capture_output=True, text=True, timeout=120
    )
    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            v = json.loads(line)
            videos.append({
                "id": v.get("id", ""),
                "title": v.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={v.get('id','')}",
                "upload_date": v.get("upload_date", ""),
                "duration": v.get("duration_string", ""),
                "stats": {
                    "view_count": v.get("view_count", 0) or 0,
                    "like_count": v.get("like_count", 0) or 0,
                    "comment_count": v.get("comment_count", 0) or 0,
                },
                "last_checked": now_kst(),
                "seeded_at": now_kst(),
                "spike_notified": False,
            })
        except Exception:
            pass
    return videos


def main():
    user_id = json.loads(USER_ID_PATH.read_text()) if USER_ID_PATH.exists() else {}
    social = user_id.get("social_media", {})
    yt = social.get("youtube", {})

    tracker = {"youtube": [], "instagram": [], "last_seeded": now_kst()}

    # YouTube 시딩
    if yt.get("handle"):
        videos = fetch_youtube_videos(yt["handle"])
        tracker["youtube"] = videos
        print(f"[seed] YouTube {len(videos)}개 영상 저장 완료")
        for v in videos[:5]:
            print(f"  {v['upload_date']}: {v['title'][:40]} (조회수 {v['stats']['view_count']:,})")

    TRACKER_PATH.write_text(json.dumps(tracker, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[seed] content_tracker.json 저장 완료")


if __name__ == "__main__":
    main()
