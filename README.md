# ai-human-maker

AI human character base project. Define a character via `character.json`, provide face references and a voice guide, and get a fully operational AI companion over Telegram.

Built on the same infrastructure as [woong-bb](https://github.com/Kein-chronicle/woong-bb-project).

---

## Concept

```
character.json
  → identity (name, age, gender, language)
  → profession (job type, workplace, schedule, work outfit)
  → relationship (type, dynamic)
  → personality (tone, traits, voice guide path)
  → appearance (hair, build, face reference dir)
  → content_levels (work/commute/home rules)

+ face reference images
+ voice guide markdown
+ Telegram bot token
  ↓
AI human that texts, shares selfies, follows daily routines
```

## Branch Strategy

- `main` — base infrastructure, no specific character
- `character/{name}` — each character gets its own branch

To create a new character:
```bash
git checkout -b character/your-character-name
cp character.example.json character.json
# edit character.json
# add face reference images to characters/{call_name}/references/curated/
# add voice guide to characters/{call_name}/profile/voice_guide.md
```

---

## Setup

### 1. Configure environment
```bash
cp .env.example session/.env
# Fill in TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, etc.
```

### 2. Configure character
```bash
cp character.example.json character.json
# Edit character.json — fill in identity, profession, personality, etc.
```

### 3. Add face references
Place 3–5 clear face photos (front-facing, no hat/glasses) in:
```
characters/{call_name}/references/curated/
```

### 4. Add voice guide (optional but recommended)
Create `characters/{call_name}/profile/voice_guide.md` describing:
- Speech patterns, endings, expressions to use/avoid
- Example responses at different emotional states

### 5. Run
```bash
# Start the Telegram bridge
bun bin/codex-telegram-bridge

# The bridge calls the worker automatically on each incoming message
```

---

## Character Config Reference

See `character.example.json` for all available fields.

Key fields:

| Field | Description |
|---|---|
| `identity.name` | Full name |
| `identity.call_name` | Nickname / how user calls them |
| `identity.gender` | `"female"` / `"male"` / `"nonbinary"` |
| `identity.language` | `"ko"` / `"en"` / etc. |
| `identity.user_address` | How they address the user (`"오빠"`, `"you"`, etc.) |
| `profession.work_activities` | Activity IDs that count as "at work" (content level 1) |
| `profession.work_outfit_description` | Text description of work uniform for image generation |
| `content_levels.rules` | Numeric content levels per context (1–3) |
| `appearance.face_reference_dir` | Directory with face reference photos |
| `personality.voice_guide_path` | Path to voice guide markdown |

---

## How Content Levels Work

| Level | Context | Image behavior |
|---|---|---|
| 1 | Work hours | Conservative — work outfit, professional setting |
| 2 | Commuting | Semi-expressive — casual outfit, outdoor selfie |
| 3 | Home / evening | Expressive — loungewear, indoor warmth |

Context is determined by `current_activity` in the snapshot + `profession.work_activities` in character config.

---

## Directory Structure

```
ai-human-maker/
├── bin/
│   ├── codex-telegram-worker       ← Character-config-driven prompt builder
│   └── codex-telegram-bridge-base  ← Telegram polling bridge (adapt per deployment)
├── characters/
│   └── {call_name}/
│       ├── references/curated/     ← Face reference images (jpg/png)
│       └── profile/
│           └── voice_guide.md      ← Speech pattern guide
├── state/
│   ├── templates/                  ← Template state files (copy to state/ on first run)
│   └── daily_schedule_state.json   ← Auto-generated daily schedule
├── scripts/
│   └── send_telegram_photo.py      ← Photo send helper
├── session/                        ← Runtime state (gitignored)
│   ├── .env                        ← Your secrets (gitignored)
│   └── codex-session.{name}.id     ← Active session ID
├── character.json                  ← Your character (gitignored or branch-specific)
├── character.example.json          ← Template
└── .env.example                    ← Env template
```
