#!/usr/bin/env python3
"""
수정이 소셜미디어 새 게시물 체크 및 프로액티브 선톡 트리거.
YouTube(@famtv6339), Instagram(kind770) 새 게시물 감지.
"""
import json, subprocess, os, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
USER_ID_PATH = STATE / "user_identity.json"
SOCIAL_STATE_PATH = STATE / "user_social_state.json"
KST = timezone(timedelta(hours=9))


def now_kst():
    return datetime.now(KST)


def load_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(p: Path, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def check_youtube(handle: str, last_id) :
    """yt-dlp로 최신 영상 1개 가져오기"""
    try:
        url = f"https://www.youtube.com/{handle}/videos"
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--playlist-items", "1", "--no-download", "--quiet", url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        v = json.loads(result.stdout.strip().split("\n")[0])
        vid = v.get("id", "")
        if not vid or vid == last_id:
            return None  # 새 영상 없음
        return {
            "platform": "youtube",
            "id": vid,
            "title": v.get("title", ""),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "thumbnail": v.get("thumbnail", ""),
            "view_count": v.get("view_count", 0),
            "like_count": v.get("like_count", 0),
            "comment_count": v.get("comment_count", 0),
            "upload_date": v.get("upload_date", ""),
            "description": (v.get("description", "") or "")[:200],
            "duration": v.get("duration_string", ""),
        }
    except Exception as e:
        print(f"[youtube] error: {e}", file=sys.stderr)
        return None


def check_instagram(handle: str, last_id) :
    """Instagram 최신 게시물 체크 (공개 계정 기준 웹 스크래핑)"""
    try:
        ig_script = str(Path(__file__).resolve().parent / "_ig_fetch.py")
        result = subprocess.run(
            ["python3", ig_script, handle],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0 or not result.stdout.strip() or result.stdout.strip() == "none":
            return None
        post = json.loads(result.stdout.strip())
        pid = post.get("id", "")
        if not pid or pid == last_id:
            return None
        shortcode = post.get("shortcode", "")
        return {
            "platform": "instagram",
            "id": pid,
            "url": f"https://www.instagram.com/p/{shortcode}/",
            "caption": post.get("caption", ""),
            "like_count": post.get("likes", 0),
            "comment_count": post.get("comments", 0),
            "timestamp": post.get("timestamp", 0),
        }
    except Exception as e:
        print(f"[instagram] error: {e}", file=sys.stderr)
        return None


def build_proactive_hint(new_post: dict) -> str:
    platform = new_post.get("platform", "")
    if platform == "youtube":
        title = new_post.get("title", "")
        views = new_post.get("view_count", 0)
        likes = new_post.get("like_count", 0)
        url = new_post.get("url", "")
        dur = new_post.get("duration", "")
        return (
            f"누나가 유튜브에 새 영상을 올렸어. "
            f"제목: '{title}' ({dur}). "
            f"조회수 {views:,}회, 좋아요 {likes:,}개. "
            f"링크: {url}. "
            f"영상 내용 파악하고 감성적·기술적으로 자연스럽게 반응해줘. 캘리그라피 관련이면 더 집중해서. "
            f"조회수/좋아요 언급도 자연스럽게 섞어줘. "
            f"누나한테 직접 말 거는 선톡으로."
        )
    elif platform == "instagram":
        caption = new_post.get("caption", "")[:100]
        likes = new_post.get("like_count", 0)
        comments = new_post.get("comment_count", 0)
        url = new_post.get("url", "")
        return (
            f"누나가 인스타그램에 새 게시물을 올렸어. "
            f"캡션: '{caption}'. "
            f"좋아요 {likes:,}개, 댓글 {comments:,}개. "
            f"링크: {url}. "
            f"게시물 내용 파악하고 자연스럽게 반응해줘. 잘 된 점 언급하고 좋아요/댓글 수도 자연스럽게 섞어줘. "
            f"누나한테 직접 말 거는 선톡으로."
        )
    return ""


def trigger_proactive(hint: str):
    """응우 character worker에 선톡 트리거"""
    import json as _json
    bun = str(Path.home() / ".bun/bin/bun")
    worker = str(ROOT / "bin/codex-character-worker")
    stateDir = str(ROOT / "session")
    payload = _json.dumps({
        "proactive": True,
        "intent": "social_media_new_post",
        "situation": hint,
        "userName": "누나",
    }, ensure_ascii=False)
    try:
        result = subprocess.run(
            [bun, worker], input=payload, capture_output=True, text=True, timeout=120,
            env={**os.environ, "CODEX_TELEGRAM_CWD": str(ROOT), "CODEX_TELEGRAM_STATE_DIR": stateDir}
        )
        if result.returncode == 0:
            data = _json.loads(result.stdout or "{}")
            answer = (data.get("answer") or "").strip()
            if answer:
                # 텔레그램 발송
                token_path = Path(stateDir) / ".env"
                token = None
                if token_path.exists():
                    for line in token_path.read_text().split("\n"):
                        if line.startswith("TELEGRAM_BOT_TOKEN="):
                            token = line.split("=", 1)[1].strip()
                access_path = Path(stateDir) / "access.json"
                chat_id = None
                if access_path.exists():
                    acc = _json.loads(access_path.read_text())
                    chat_id = (acc.get("allowFrom") or [None])[0]
                if token and chat_id:
                    import urllib.request, urllib.parse
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    data_bytes = urllib.parse.urlencode({"chat_id": chat_id, "text": answer}).encode()
                    urllib.request.urlopen(url, data_bytes, timeout=10)
                    print(f"[social] 발송 완료: {answer[:60]}")
                    return True
    except Exception as e:
        print(f"[social] proactive 실패: {e}", file=sys.stderr)
    return False




def check_existing_spikes() -> list:
    """기존 트래킹 영상들 스탯 업데이트 후 스파이크 감지"""
    tracker_path = STATE / "content_tracker.json"
    try:
        tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    
    spikes = []
    now = now_kst().isoformat(timespec="seconds")
    
    for v in tracker.get("youtube", []):
        vid = v.get("id", "")
        if not vid:
            continue
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download", "--quiet",
                 f"https://www.youtube.com/watch?v={vid}"],
                capture_output=True, text=True, timeout=20
            )
            if result.returncode != 0 or not result.stdout.strip():
                continue
            new_data = json.loads(result.stdout.strip())
            old_views = v["stats"].get("view_count", 0)
            new_views = new_data.get("view_count", 0) or 0
            old_comments = v["stats"].get("comment_count", 0) or 0
            new_comments = new_data.get("comment_count", 0) or 0
            old_likes = v["stats"].get("like_count", 0) or 0
            new_likes = new_data.get("like_count", 0) or 0
            
            spike_reason = []
            if old_views > 10 and new_views - old_views >= max(20, old_views * 0.15):
                spike_reason.append(f"조회수 {old_views:,} → {new_views:,} (+{new_views-old_views:,})")
            if old_comments is not None and new_comments - (old_comments or 0) >= 3:
                spike_reason.append(f"댓글 {old_comments} → {new_comments} (+{new_comments-(old_comments or 0)})")
            
            if spike_reason and not v.get("spike_notified"):
                spikes.append({
                    "platform": "youtube",
                    "id": vid,
                    "title": v.get("title", ""),
                    "url": v.get("url", ""),
                    "spike_reason": spike_reason,
                    "new_stats": {"view_count": new_views, "like_count": new_likes, "comment_count": new_comments},
                })
                v["spike_notified"] = True
            
            # 스탯 업데이트
            v["stats"] = {"view_count": new_views, "like_count": new_likes, "comment_count": new_comments}
            v["last_checked"] = now
        except Exception:
            pass
    
    # 저장
    tracker_path.write_text(json.dumps(tracker, ensure_ascii=False, indent=2), encoding="utf-8")
    return spikes


def build_spike_hint(spike: dict) -> str:
    title = spike.get("title", "")
    reasons = " / ".join(spike.get("spike_reason", []))
    stats = spike.get("new_stats", {})
    url = spike.get("url", "")
    return (
        f"누나 유튜브 영상 '{title}'에서 반응이 올라오고 있어. "
        f"{reasons}. "
        f"현재 조회수 {stats.get('view_count',0):,}회, 좋아요 {stats.get('like_count',0):,}개. "
        f"링크: {url}. "
        f"영상 내용 파악하고 자연스럽게 '이 영상 반응 좋은 것 같던데' 하면서 말 걸어줘. "
        f"조회수/댓글 증가 자연스럽게 언급하고, 잘 된 점 이야기해줘."
    )


def run():
    user_id = load_json(USER_ID_PATH, {})
    social = user_id.get("social_media", {})
    state = load_json(SOCIAL_STATE_PATH, {})

    yt = social.get("youtube", {})
    ig = social.get("instagram", {})

    found_new = []
    
    # 기존 영상 스파이크 체크 (30분마다 체크하지만 너무 많으면 부하 → 랜덤 5개만)
    import random
    tracker_path = STATE / "content_tracker.json"
    if tracker_path.exists():
        tracker = load_json(tracker_path, {})
        yt_list = tracker.get("youtube", [])
        # 조회수 10 이상인 영상 중 랜덤 5개 샘플링
        candidates = [v for v in yt_list if v.get("stats", {}).get("view_count", 0) >= 10]
        sample = random.sample(candidates, min(5, len(candidates)))
        for v in sample:
            tracker_items = {vv["id"]: vv for vv in yt_list}
        # 실제로는 check_existing_spikes 호출
        spikes = check_existing_spikes()
        for spike in spikes:
            hint = build_spike_hint(spike)
            if hint:
                print(f"[spike] 감지: {spike.get('title','')[:30]}")
                trigger_proactive(hint)

    # YouTube 체크
    if yt.get("handle"):
        last_yt = state.get("youtube_last_id")
        new_yt = check_youtube(yt["handle"], last_yt)
        if new_yt:
            found_new.append(new_yt)
            state["youtube_last_id"] = new_yt["id"]
            state["youtube_last_checked"] = now_kst().isoformat(timespec="seconds")
            print(f"[youtube] 새 영상: {new_yt['title']}")
        else:
            state["youtube_last_checked"] = now_kst().isoformat(timespec="seconds")
            print(f"[youtube] 새 영상 없음")

    # Instagram 체크
    if ig.get("handle"):
        last_ig = state.get("instagram_last_id")
        new_ig = check_instagram(ig["handle"], last_ig)
        if new_ig:
            found_new.append(new_ig)
            state["instagram_last_id"] = new_ig["id"]
            state["instagram_last_checked"] = now_kst().isoformat(timespec="seconds")
            print(f"[instagram] 새 게시물 발견")
        else:
            state["instagram_last_checked"] = now_kst().isoformat(timespec="seconds")
            print(f"[instagram] 새 게시물 없음")

    save_json(SOCIAL_STATE_PATH, state)

    # 새 게시물 있으면 선톡 트리거
    for post in found_new:
        hint = build_proactive_hint(post)
        if hint:
            trigger_proactive(hint)


if __name__ == "__main__":
    run()
