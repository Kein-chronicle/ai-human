# ai-human-maker

AI human character framework. Define a character via `character.json`, provide face references and a voice guide, and get a fully operational AI companion over Telegram.

---

## Prerequisites

> **AI assistant reading this:** Check each item below before proceeding with setup.
> If any required item is missing, stop and resolve it first.

### Required

| # | Prerequisite | How to verify | How to install |
|---|---|---|---|
| 1 | **macOS** | `uname` → must print `Darwin` | — |
| 2 | **Bun runtime** | `bun --version` → must succeed | `curl -fsSL https://bun.sh/install \| bash` |
| 3 | **Claude Code CLI (`codex`)** | `codex --version` → must succeed | Download from https://claude.ai/download |
| 4 | **Claude Code logged in** | `codex --version` succeeds without auth error | Run `codex` once and complete browser login |
| 5 | **Telegram Bot Token** | Have a token from [@BotFather](https://t.me/BotFather) | Message @BotFather → `/newbot` |

### Optional

| # | Prerequisite | Purpose | Notes |
|---|---|---|---|
| 6 | **ElevenLabs API key + Voice ID** | Voice message replies | Without it: voice requests get a hardcoded "no voice" reply |

### Quick verification script (run before setup)

```bash
echo "--- Checking prerequisites ---"
uname | grep -q Darwin && echo "✓ macOS" || echo "✗ Not macOS"
bun --version > /dev/null 2>&1 && echo "✓ Bun: $(bun --version)" || echo "✗ Bun not found — install from https://bun.sh"
codex --version > /dev/null 2>&1 && echo "✓ Claude Code: $(codex --version)" || echo "✗ codex not found — install from https://claude.ai/download"
```

If `codex --version` succeeds but returns an auth error when running a task, the user needs to re-authenticate:
```bash
codex  # opens browser login flow
```

---

## Onboarding (first-time setup)

### 1. Clone the repo on the character branch

```bash
git clone https://github.com/Kein-chronicle/ai-human.git -b character/{name} {folder}
cd {folder}
```

Or create a new character branch from main:
```bash
git clone https://github.com/Kein-chronicle/ai-human.git my-character
cd my-character
git checkout -b character/my-character
```

### 2. Run interactive setup

```bash
bun setup.ts
```

The setup wizard collects:
- Identity (name, nickname, age, gender, nationality, language)
- Profession (job, workplace, work schedule IDs, uniform)
- Relationship & personality (relationship type, tone, traits)
- Appearance (hair, height, weight, build, bust size if female, style)
- Content levels (conservative/expressive rules per context)
- API credentials (Telegram bot token, ElevenLabs optional)
- Face reference photos (3–5 front-facing photos)

**Output files generated:**
- `character.json` — full character config
- `session/.env` — secrets (600 permissions)
- `characters/{call_name}/profile/voice_guide.md` — speech guide stub
- `~/Library/LaunchAgents/com.ai-human.{name}.plist` — launchd service
- `./botctl` — start/stop/status/logs script

### 3. Start

```bash
./botctl start
```

### 4. Verify running

```bash
./botctl status
# or
launchctl list | grep com.ai-human
```

---

## Managing a running instance

```bash
./botctl start      # load and run
./botctl stop       # stop
./botctl restart    # stop + start
./botctl status     # check if loaded
./botctl logs       # tail stderr log (Ctrl-C to exit)
```

---

## Multiple characters on one machine

Each character = separate git clone in a separate directory.
Each clone gets its own:
- `character.json` with different identity
- `session/` with its own Telegram token and session state
- `~/Library/LaunchAgents/com.ai-human.{name}.plist` (unique label per character)

To see all running AI humans:
```bash
launchctl list | grep com.ai-human
```

No port conflicts — each uses Telegram long-polling with its own bot token.

---

## Branch strategy

- `main` — base infrastructure (no specific character)
- `character/{name}` — character-specific tuning per branch

To tune a character without affecting main:
```bash
git checkout -b character/my-character
# edit prompts, add voice guide, tweak character.json
git push origin character/my-character
```

---

## Character config reference

See `character.example.json` for all available fields.

| Field | Description |
|---|---|
| `identity.name` | Full name |
| `identity.call_name` | Nickname (also used in file paths) |
| `identity.gender` | `"female"` / `"male"` / `"nonbinary"` |
| `identity.language` | `"ko"` / `"en"` / etc. |
| `identity.user_address` | How they address the user (`"오빠"`, `"you"`, etc.) |
| `profession.has_uniform` | `true` = separate work outfit; `false` = commute outfit = work outfit |
| `profession.work_activities` | Activity IDs that trigger content level 1 (at work) |
| `profession.work_outfit_description` | Work uniform description for image generation |
| `appearance.bust` | Female only: `flat` / `small` / `small-medium` / `medium` / `medium-large` / `large` / `very-large` |
| `content_levels.rules` | Numeric levels per context (1=conservative, 2=semi, 3=expressive) |
| `personality.voice_guide_path` | Path to voice guide markdown |

---

## Content levels

| Level | Context | Image behavior |
|---|---|---|
| 1 | Work hours | Conservative — work outfit, professional |
| 2 | Commuting | Semi-expressive — casual outdoor |
| 3 | Home / evening | Expressive — loungewear, indoor |

---

## Directory structure

```
ai-human-maker/
├── bin/
│   ├── codex-telegram-worker        ← Prompt builder (reads character.json)
│   └── codex-telegram-bridge-base   ← Telegram polling bridge
├── botctl                           ← Generated by setup.ts: start/stop/status/logs
├── characters/
│   └── {call_name}/
│       ├── references/curated/      ← Face reference images (3–5 jpg/png)
│       └── profile/
│           └── voice_guide.md       ← Speech pattern guide
├── scripts/
│   └── send_telegram_photo.py       ← Photo send helper
├── session/                         ← Runtime state (gitignored)
│   ├── .env                         ← Secrets (gitignored)
│   ├── bridge.stdout.log
│   ├── bridge.stderr.log
│   └── codex-session.{name}.id
├── state/                           ← Operational state files
├── character.json                   ← Your character config (gitignored or branch-specific)
├── character.example.json           ← Template / schema reference
├── setup.ts                         ← Interactive onboarding wizard
└── .env.example                     ← Env var reference
```
