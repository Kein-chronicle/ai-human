#!/usr/bin/env python3
"""오늘 대화 내용을 기반으로 daily_diary_state.json 부트스트랩 엔트리 생성."""
import json
from datetime import datetime, timedelta
from pathlib import Path

CWD = Path("/Users/kein/Projects/lee-eunwoo")
DIARY_PATH = CWD / "state" / "daily_diary_state.json"
MSGS_DIR = CWD / "messages"
TZ = 9


def kst_now():
    return datetime.utcnow() + timedelta(hours=TZ)


def main():
    now = kst_now()
    today = now.date().isoformat()

    diary = json.loads(DIARY_PATH.read_text()) if DIARY_PATH.exists() else {}

    if diary.get("today") == today and diary.get("today_written"):
        print(f"[diary] {today} already written, skipping")
        return

    msg_file = MSGS_DIR / f"{today}.jsonl"
    total_msgs = 0
    if msg_file.exists():
        total_msgs = sum(1 for line in msg_file.open(encoding="utf-8") if line.strip())

    diary.update({
        "today": today,
        "today_written": False,
        "today_message_count": total_msgs,
        "generated_at": now.isoformat() + "+09:00",
        "fill_status": "bootstrap_pending",
    })
    DIARY_PATH.write_text(json.dumps(diary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[diary] {today} bootstrap created ({total_msgs} messages today)")


if __name__ == "__main__":
    main()
