#!/usr/bin/env python3
"""
지난 7일 messages/*.jsonl을 모아 주간 요약 bootstrap entry를 생성.
codex가 실제 요약 내용을 별도로 채운다.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

CWD = Path("/Users/kein/Projects/lee-eunwoo")
WCS = CWD / "state" / "weekly_conversation_summary.json"
MSGS_DIR = CWD / "messages"
TZ = 9


def kst_now():
    return datetime.utcnow() + timedelta(hours=TZ)


def main():
    now = kst_now()
    week_end = now.date()
    week_start = week_end - timedelta(days=6)
    iso_week = f"{week_start.isoformat()}_to_{week_end.isoformat()}"

    wcs = json.loads(WCS.read_text(encoding="utf-8")) if WCS.exists() else {}
    wcs.setdefault("weekly_summaries", [])
    wcs["last_generated_at"] = now.isoformat() + "+09:00"
    wcs["current_week_iso"] = iso_week

    existing = [s for s in wcs["weekly_summaries"] if s.get("week_start_iso") == week_start.isoformat()]
    if existing:
        print(f"week {iso_week} already exists, skipping")
        return

    msg_files = sorted(MSGS_DIR.glob("*.jsonl")) if MSGS_DIR.exists() else []
    recent_files = [f for f in msg_files if f.stem >= week_start.isoformat()]
    total_lines = 0
    for f in recent_files:
        try:
            total_lines += sum(1 for _ in f.open(encoding="utf-8"))
        except Exception:
            pass

    entry = {
        "week_start_iso": week_start.isoformat(),
        "week_end_iso": week_end.isoformat(),
        "generated_at": now.isoformat() + "+09:00",
        "raw_message_lines": total_lines,
        "message_file_count": len(recent_files),
        "key_events": [],
        "user_mood_arc": "",
        "main_topics": [],
        "user_disclosed_facts": [],
        "promises_or_plans": [],
        "outstanding_unresolved": [],
        "fill_status": "bootstrap_pending_codex_review",
        "raw_file_paths": [str(f) for f in recent_files],
    }
    wcs["weekly_summaries"].append(entry)
    wcs["weekly_summaries"] = wcs["weekly_summaries"][-4:]

    WCS.write_text(json.dumps(wcs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"bootstrap entry for {iso_week} created")


if __name__ == "__main__":
    main()
