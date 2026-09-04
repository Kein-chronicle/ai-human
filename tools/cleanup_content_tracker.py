#!/usr/bin/env python3
"""
컨텐츠 트래커 일일 정리 — 오래되고 활동 없는 영상은 자연스럽게 제거.
정책:
- 활성 추적: 최근 30일 이내 업로드 + 최근 7일 이내 스파이크 있던 것
- 30~90일: 조회수 100 이상이면 유지, 아니면 제거
- 90일 이상: 조회수 500 이상이면 유지, 아니면 제거
- 180일 이상: 조회수 2000 이상 or 댓글 50개 이상이 아니면 제거
"""
import json
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER_PATH = ROOT / "state" / "content_tracker.json"
KST = timezone(timedelta(hours=9))


def days_since_upload(upload_date_str: str) -> int:
    try:
        upload = datetime.strptime(upload_date_str, "%Y%m%d").date()
        return (date.today() - upload).days
    except Exception:
        return 9999


def should_keep(v: dict) -> tuple[bool, str]:
    days = days_since_upload(v.get("upload_date", ""))
    views = v.get("stats", {}).get("view_count", 0) or 0
    comments = v.get("stats", {}).get("comment_count", 0) or 0
    spike_notified = v.get("spike_notified", False)
    
    # 최근 30일: 무조건 유지
    if days <= 30:
        return True, "최근 30일"
    # 스파이크 알림 보낸 건 60일 더 유지
    if spike_notified and days <= 90:
        return True, "스파이크 기록"
    # 30~90일: 조회수 100 이상
    if days <= 90 and views >= 100:
        return True, f"조회수 {views:,}"
    # 90~180일: 조회수 500 이상
    if days <= 180 and views >= 500:
        return True, f"조회수 {views:,}"
    # 180일 이상: 조회수 2000 or 댓글 50
    if days > 180 and (views >= 2000 or comments >= 50):
        return True, f"조회수/댓글 높음"
    
    return False, f"{days}일 경과, 조회수 {views:,}"


def run():
    if not TRACKER_PATH.exists():
        print("[cleanup] tracker 파일 없음")
        return
    
    tracker = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))
    yt_list = tracker.get("youtube", [])
    
    kept = []
    removed = []
    for v in yt_list:
        keep, reason = should_keep(v)
        if keep:
            kept.append(v)
        else:
            removed.append((v.get("title", "")[:30], reason))
    
    tracker["youtube"] = kept
    tracker["last_cleanup"] = datetime.now(KST).isoformat(timespec="seconds")
    tracker["active_count"] = len(kept)
    
    TRACKER_PATH.write_text(json.dumps(tracker, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"[cleanup] 정리 완료: {len(yt_list)}개 → {len(kept)}개 유지, {len(removed)}개 제거")
    for title, reason in removed[:5]:
        print(f"  제거: {title} ({reason})")


if __name__ == "__main__":
    run()
