#!/usr/bin/env python3
"""
Update specific fields in daily_schedule_state.json during conversation.

Usage:
  python3 update_daily_schedule.py <section> <key> <value> [--reason "..."]
  python3 update_daily_schedule.py --patch '{"dinner": {"menu": "삼겹살", "location": "고깃집"}}'
  python3 update_daily_schedule.py --show
  python3 update_daily_schedule.py --show-section dinner

Examples:
  python3 update_daily_schedule.py dinner menu "삼겹살" --reason "수정이랑 외식"
  python3 update_daily_schedule.py commute_home depart_time "20:00" --reason "야근"
  python3 update_daily_schedule.py night sleep_target "01:00"
  python3 update_daily_schedule.py morning outfit "편한 캐주얼"
"""
import json, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(ROOT, "state", "daily_schedule_state.json")


def load() -> dict:
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save(data: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("section", nargs="?")
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?")
    parser.add_argument("--reason", default="")
    parser.add_argument("--patch", default="")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--show-section", default="")
    args = parser.parse_args()

    data = load()

    if args.show:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if args.show_section:
        section = data.get(args.show_section, {})
        print(json.dumps(section, ensure_ascii=False, indent=2))
        return

    if args.patch:
        patch = json.loads(args.patch)
        for section, updates in patch.items():
            if section not in data:
                data[section] = {}
            if isinstance(updates, dict):
                data[section].update(updates)
            else:
                data[section] = updates
        save(data)
        print(f"[update_daily_schedule] patch applied: {list(patch.keys())}")
        return

    if not args.section or not args.key or args.value is None:
        parser.print_help()
        sys.exit(1)

    if args.section not in data:
        data[args.section] = {}

    try:
        value = json.loads(args.value)
    except Exception:
        value = args.value

    old = data[args.section].get(args.key)
    data[args.section][args.key] = value
    save(data)
    reason_str = f" (이유: {args.reason})" if args.reason else ""
    print(f"[update_daily_schedule] {args.section}.{args.key}: {repr(old)} → {repr(value)}{reason_str}")


if __name__ == "__main__":
    main()
