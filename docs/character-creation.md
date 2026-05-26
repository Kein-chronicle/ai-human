# Character Creation Guide

## Step-by-step: creating a new AI human

### 1. Branch off main
```bash
git checkout main
git checkout -b character/your-character-name
```

### 2. Fill in character.json
```bash
cp character.example.json character.json
```

Fill in at minimum:
- `identity`: name, call_name, age, gender, language, user_address
- `profession`: type, workplace, work_activities (the activity IDs that mean "at work")
- `relationship`: type, dynamic
- `personality`: tone, base_traits
- `appearance`: hair, face_reference_dir

### 3. Add face reference images

Put 3–5 high-quality face photos into:
```
characters/{call_name}/references/curated/
```

**Good reference photos:**
- Clear front-facing, natural light
- No sunglasses, hats, heavy filters
- Different expressions/angles help

These are passed as `--image` flags to the image generation model to maintain face consistency.

### 4. Write a voice guide

Create `characters/{call_name}/profile/voice_guide.md`:

```markdown
# Voice Guide: [Character Name]

## Speech style
- [Describe the tone — casual, formal, playful, etc.]
- [Key expressions they use or avoid]
- [How they react to compliments, jokes, requests]

## Sentence endings (if Korean)
- Preferred: [list endings like 같아, 있어, 거야, 더라고]
- Avoid: [awkward constructions]

## Example responses
**User says something cute:**
> [example response A]
> [example response B]

**User asks about their day:**
> [example response]
```

### 5. Configure content levels

In `character.json`, set `content_levels.rules`:
```json
{
  "work_activities": 1,
  "commuting": 2,
  "home_evening": 3,
  "default": 3
}
```

And list work activity IDs in `profession.work_activities`. These must match the activity values your schedule system produces.

### 6. Set up environment
```bash
mkdir -p session
cp .env.example session/.env
# Add your TELEGRAM_BOT_TOKEN and OPENAI_API_KEY
```

### 7. Run
```bash
bun bin/codex-telegram-bridge
```

---

## Work outfit for image generation

Set `profession.work_outfit_description` to a text description of the uniform:
```
"mint blue scrub top (V-neck short sleeve), matching scrub pants, name badge, simple watch"
```

The worker uses this in prompts when the character is at work (content level 1).

---

## Commute outfit continuity

If you want consistent outfit across morning/evening commute:
- Create `state/eunbi_appearance_state.json` (or equivalent)
- Add a `workday_commute_outfit` field describing the outfit
- The worker will read this and use it for commuting shots
