#!/usr/bin/env python3
"""ElevenLabs TTS 생성기 — state/.env에서 키 읽어 음성 파일 생성."""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

CWD = Path("/Users/kein/Projects/lee-eunwoo")
SESSION_ENV = CWD / "session" / ".env"
VOICE_ROOT = CWD / "voice-message"


def load_env() -> dict:
    path = SESSION_ENV
    if not path.exists():
        raise RuntimeError("env file not found")
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip()] = v.strip()
    return values


def clean_text(text: str) -> str:
    text = re.sub(r"ㅋ+|ㅎ+", "", text)
    text = text.replace("..", ".").replace("~", "")
    return re.sub(r"\s+", " ", text).strip()


def synthesize(text: str, output_path: Path, env: dict) -> None:
    api_key = env.get("ELEVENLABS_API_KEY")
    voice_id = env.get("ELEVENLABS_VOICE_ID")
    if not api_key or not voice_id:
        raise RuntimeError("missing ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    payload = {
        "text": clean_text(text),
        "model_id": "eleven_multilingual_v2",
        "language_code": "ko",
        "voice_settings": {
            "stability": float(env.get("ELEVENLABS_STABILITY", "0.45")),
            "similarity_boost": float(env.get("ELEVENLABS_SIMILARITY_BOOST", "0.80")),
            "style": float(env.get("ELEVENLABS_STYLE", "0.20")),
            "use_speaker_boost": env.get("ELEVENLABS_USE_SPEAKER_BOOST", "true").lower() == "true",
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            output_path.write_bytes(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"elevenlabs_http_{exc.code}: {body[:400]}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--label", default="voice")
    args = parser.parse_args()
    env = load_env()
    now = datetime.now().astimezone()
    date_dir = VOICE_ROOT / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^0-9A-Za-z가-힣]+", "_", args.label.strip())[:30] or "voice"
    filename = f"{now.strftime('%H%M%S')}_{slug}.mp3"
    output_path = date_dir / filename
    synthesize(args.text, output_path, env)
    print(json.dumps({"ok": True, "path": str(output_path), "size_bytes": output_path.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
