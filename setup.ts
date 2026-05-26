#!/usr/bin/env bun
// =============================================================================
// ai-human-maker — Interactive Setup
// Usage: bun setup.ts
// =============================================================================

import { existsSync, mkdirSync, writeFileSync, readdirSync, chmodSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";
import { spawnSync } from "node:child_process";

const ROOT = import.meta.dir;

// =============================================================================
// UTILS
// =============================================================================

const RESET = "\x1b[0m";
const BOLD = "\x1b[1m";
const CYAN = "\x1b[36m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const RED = "\x1b[31m";
const DIM = "\x1b[2m";

const print = (s: string) => process.stdout.write(s + "\n");
const printBold = (s: string) => print(BOLD + s + RESET);
const printGreen = (s: string) => print(GREEN + "✓ " + s + RESET);
const printYellow = (s: string) => print(YELLOW + "⚠ " + s + RESET);
const printRed = (s: string) => print(RED + "✗ " + s + RESET);
const printDim = (s: string) => print(DIM + s + RESET);
const printSection = (n: number, total: number, title: string) => {
  print("");
  print(CYAN + BOLD + `[${n}/${total}] ${title}` + RESET);
};

async function ask(prompt: string, defaultVal = ""): Promise<string> {
  const hint = defaultVal ? DIM + ` (${defaultVal})` + RESET : "";
  process.stdout.write(`  ${prompt}${hint}: `);
  for await (const line of console) {
    const val = line.trim();
    return val || defaultVal;
  }
  return defaultVal;
}

async function askChoice(prompt: string, choices: string[], defaultVal = ""): Promise<string> {
  const hint = choices.map((c) => (c === defaultVal ? BOLD + c + RESET : c)).join("/");
  process.stdout.write(`  ${prompt} [${hint}]: `);
  for await (const line of console) {
    const val = line.trim().toLowerCase();
    if (!val && defaultVal) return defaultVal;
    if (choices.map((c) => c.toLowerCase()).includes(val)) return val;
    process.stdout.write(`  ${prompt} [${hint}]: `);
  }
  return defaultVal;
}

async function askSecret(prompt: string): Promise<string> {
  process.stdout.write(`  ${prompt}: `);
  for await (const line of console) {
    return line.trim();
  }
  return "";
}

async function pressEnter(prompt: string): Promise<void> {
  process.stdout.write(`  ${prompt} [Enter] `);
  for await (const _line of console) break;
}

// =============================================================================
// VALIDATION
// =============================================================================

function checkCodex(): boolean {
  const codexBin = process.env.CODEX_BIN ?? "codex";
  const result = spawnSync(codexBin, ["--version"], { encoding: "utf8" });
  return result.status === 0;
}

async function checkTelegramToken(token: string): Promise<boolean> {
  try {
    const res = await fetch(`https://api.telegram.org/bot${token}/getMe`);
    const body = await res.json() as any;
    return body.ok === true;
  } catch {
    return false;
  }
}

function countFaceRefs(dir: string): number {
  if (!existsSync(dir)) return 0;
  return readdirSync(dir).filter((f) => /\.(jpg|jpeg|png)$/i.test(f)).length;
}

// =============================================================================
// BUST SIZE LABEL
// =============================================================================

const BUST_OPTIONS = ["flat", "small", "small-medium", "medium", "medium-large", "large", "very-large"];
const BUST_PROMPT_MAP: Record<string, string> = {
  "flat": "flat chest",
  "small": "small bust",
  "small-medium": "small to medium bust",
  "medium": "medium bust",
  "medium-large": "medium to large bust",
  "large": "large bust",
  "very-large": "very large bust, voluptuous",
};

// =============================================================================
// MAIN SETUP
// =============================================================================

async function main() {
  print("");
  printBold("═══════════════════════════════════════");
  printBold("   ai-human-maker — Character Setup    ");
  printBold("═══════════════════════════════════════");
  print("");
  printDim("This will create your character.json and session/.env");
  printDim("You can re-run this anytime to update settings.");
  print("");

  // ── PREREQUISITES ────────────────────────────────────────────────────────

  printBold("Checking prerequisites...");
  if (checkCodex()) {
    printGreen("Claude Code (codex) installed and accessible");
  } else {
    printRed("Claude Code (codex) not found. Install from https://claude.ai/download");
    printDim("Or set CODEX_BIN env to the full path.");
    process.exit(1);
  }
  print("");

  const TOTAL = 7;

  // ── [1] IDENTITY ─────────────────────────────────────────────────────────

  printSection(1, TOTAL, "Identity");
  const name = await ask("Full name");
  const callName = await ask("Nickname / how user calls them", name);
  const age = await ask("Age", "22");
  const gender = await askChoice("Gender", ["female", "male", "nonbinary"], "female");
  const nationality = await ask("Nationality", "Korean");
  const language = await ask("Language code (ko / en / ja / ...)", "ko");
  const userAddress = await ask("How they address the user (오빠 / 언니 / you / ...)", gender === "female" ? "오빠" : "you");

  // ── [2] PROFESSION ───────────────────────────────────────────────────────

  printSection(2, TOTAL, "Profession");
  const profType = await ask("Job type (nurse / student / office_worker / cafe_staff / ...)");
  const workplace = await ask("Workplace type (hospital / office / cafe / school / ...)");
  const hasUniformStr = await askChoice("Do they wear a work uniform?", ["yes", "no"], "no");
  const hasUniform = hasUniformStr === "yes";

  let workOutfitDescription = "";
  if (hasUniform) {
    workOutfitDescription = await ask("Describe the work uniform (for image generation)");
  }

  print("");
  printDim("Work activities are schedule IDs that mean 'currently at work'.");
  printDim("Default: morning_shift, lunch_break, afternoon_shift");
  printDim("Leave blank to use defaults, or comma-separate custom IDs.");
  const workActivitiesInput = await ask("Work activity IDs", "morning_shift,lunch_break,afternoon_shift");
  const workActivities = workActivitiesInput.split(",").map((s) => s.trim()).filter(Boolean);

  // ── [3] RELATIONSHIP & PERSONALITY ──────────────────────────────────────

  printSection(3, TOTAL, "Relationship & Personality");
  const relType = await ask("Relationship to user (girlfriend / boyfriend / friend / sibling / ...)", "friend");
  const relDynamic = await ask("Dynamic (affectionate_playful / cool_calm / bubbly / tsundere / ...)", "affectionate_playful");

  const tone = await ask("Personality tone (warm_playful / cool_calm / shy_sweet / direct / ...)", "warm_playful");
  const traitsInput = await ask("Key traits, comma-separated (affectionate, curious, caring, ...)", "affectionate,curious,caring");
  const traits = traitsInput.split(",").map((s) => s.trim()).filter(Boolean);

  // ── [4] APPEARANCE ───────────────────────────────────────────────────────

  printSection(4, TOTAL, "Appearance");
  printDim("Used in image generation prompts.");
  const hair = await ask("Hair description (long dark wavy / short blonde bob / ...)", "long dark hair");
  const height = await ask("Height (163cm / 5'4\" / ...)", "165cm");
  const weight = await ask("Weight (50kg / 110lb / ...)", "");
  const build = await ask("Body build (slim / athletic / curvy / petite / average)", "slim");

  let bust = "";
  if (gender === "female") {
    print("");
    print(`  Bust size options: ${BUST_OPTIONS.join(" / ")}`);
    bust = await askChoice("Bust size", BUST_OPTIONS, "small-medium");
  }

  const style = await ask("Fashion style (feminine_casual / streetwear / minimal / preppy / ...)", "casual");

  // ── [5] CONTENT LEVELS ───────────────────────────────────────────────────

  printSection(5, TOTAL, "Content Levels");
  printDim("1 = conservative (work), 2 = semi-expressive (commuting), 3 = expressive (home/evening)");
  const lvlWork = await ask("Content level during work", "1");
  const lvlCommute = await ask("Content level while commuting", "2");
  const lvlHome = await ask("Content level at home / evening", "3");

  // ── [6] API KEYS ─────────────────────────────────────────────────────────

  printSection(6, TOTAL, "API Keys & Credentials");
  const telegramToken = await askSecret("Telegram Bot Token (from @BotFather)");

  print("");
  printDim("ElevenLabs is optional. Skip to disable voice messages.");
  const elevenLabsKey = await askSecret("ElevenLabs API key (Enter to skip)");
  let elevenLabsVoiceId = "";
  if (elevenLabsKey) {
    elevenLabsVoiceId = await askSecret("ElevenLabs Voice ID");
  }

  // ── [7] FACE REFERENCES ──────────────────────────────────────────────────

  printSection(7, TOTAL, "Face Reference Images");
  const refDir = join(ROOT, "characters", callName, "references", "curated");
  mkdirSync(refDir, { recursive: true });
  mkdirSync(join(ROOT, "characters", callName, "profile"), { recursive: true });

  print("");
  print(`  Place 3–5 clear face photos (front-facing, no glasses/hat) in:`);
  print(`  ${BOLD}${refDir}${RESET}`);
  print("");
  printDim("Tips: natural light, varied expressions, no heavy filters");
  await pressEnter("Press Enter once photos are placed...");

  const refCount = countFaceRefs(refDir);
  if (refCount === 0) {
    printYellow("No face reference images found. Image generation will have inconsistent faces.");
    printYellow(`Add photos to: ${refDir}`);
  } else if (refCount < 3) {
    printYellow(`Only ${refCount} face reference(s) found. 3–5 recommended.`);
  } else {
    printGreen(`${refCount} face reference image(s) found`);
  }

  // ── GENERATE FILES ───────────────────────────────────────────────────────

  print("");
  printBold("Generating files...");

  // character.json
  const character = {
    _generated_by: "ai-human-maker setup.ts",
    identity: { name, call_name: callName, age: parseInt(age) || age, gender, nationality, language, user_address: userAddress },
    profession: {
      type: profType,
      workplace,
      schedule_type: "shift_work",
      has_uniform: hasUniform,
      work_activities: workActivities,
      ...(hasUniform ? { work_outfit_description: workOutfitDescription } : {}),
    },
    relationship: { type: relType, dynamic: relDynamic, closeness: "high" },
    personality: {
      tone,
      base_traits: traits,
      speech_style: language === "ko" ? "casual_korean" : "casual",
      emoji_usage: "moderate_varied",
      voice_guide_path: `characters/${callName}/profile/voice_guide.md`,
    },
    appearance: {
      hair,
      height,
      ...(weight ? { weight } : {}),
      build,
      ...(gender === "female" && bust ? { bust } : {}),
      style,
      face_reference_dir: `characters/${callName}/references/curated`,
    },
    content_levels: {
      description: "1=conservative, 2=semi-expressive, 3=expressive",
      rules: {
        work_activities: parseInt(lvlWork) || 1,
        commuting: parseInt(lvlCommute) || 2,
        home_evening: parseInt(lvlHome) || 3,
        default: parseInt(lvlHome) || 3,
      },
    },
    telegram: { session_dir: "session", bot_token_env: "TELEGRAM_BOT_TOKEN" },
    codex: { model: null, session_file: `session/codex-session.${callName.toLowerCase()}.id`, state_dir: "state" },
    image_generation: {
      enabled: true,
      face_refs_count: 5,
      banned_from_image_flags: ["outfit_samples"],
      send_script: "scripts/send_telegram_photo.py",
    },
  };

  writeFileSync(join(ROOT, "character.json"), JSON.stringify(character, null, 2));
  printGreen("character.json created");

  // session/.env
  mkdirSync(join(ROOT, "session"), { recursive: true });
  const envLines = [
    `TELEGRAM_BOT_TOKEN=${telegramToken}`,
    elevenLabsKey ? `ELEVENLABS_API_KEY=${elevenLabsKey}` : "# ELEVENLABS_API_KEY=",
    elevenLabsVoiceId ? `ELEVENLABS_VOICE_ID=${elevenLabsVoiceId}` : "# ELEVENLABS_VOICE_ID=",
  ];
  writeFileSync(join(ROOT, "session", ".env"), envLines.join("\n") + "\n", { mode: 0o600 });
  printGreen("session/.env created");

  // voice_guide.md stub (if not exists)
  const voiceGuidePath = join(ROOT, "characters", callName, "profile", "voice_guide.md");
  if (!existsSync(voiceGuidePath)) {
    writeFileSync(voiceGuidePath, [
      `# Voice Guide: ${name} (${callName})`,
      "",
      "## Speech style",
      `- Tone: ${tone}`,
      `- Traits: ${traits.join(", ")}`,
      `- Language: ${language}`,
      "",
      "## Add your character's specific speech patterns below",
      "- Key expressions they use",
      "- Sentence endings they prefer",
      "- How they react to compliments, jokes, requests",
      "",
      "## Example responses",
      "**When greeted:**",
      "> (add example)",
      "",
    ].join("\n"));
    printGreen("characters/" + callName + "/profile/voice_guide.md stub created");
    printYellow("  → Edit this file to define speech patterns (optional but recommended)");
  }

  // launchd plist
  const plistLabel = `com.ai-human.${callName.toLowerCase().replace(/[^a-z0-9]/g, "-")}`;
  const plistName = `${plistLabel}.plist`;
  const launchAgentsDir = join(homedir(), "Library", "LaunchAgents");
  const plistPath = join(launchAgentsDir, plistName);
  const bridgeBin = resolve(ROOT, "bin", "codex-telegram-bridge-base");
  const bunBin = spawnSync("which", ["bun"], { encoding: "utf8" }).stdout?.trim() || "/opt/homebrew/bin/bun";
  const plistXml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${plistLabel}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${bunBin}</string>
    <string>run</string>
    <string>${bridgeBin}</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>AI_HUMAN_ROOT</key>
    <string>${ROOT}</string>
    <key>CHARACTER_CONFIG</key>
    <string>${join(ROOT, "character.json")}</string>
    <key>AI_HUMAN_STATE_DIR</key>
    <string>${join(ROOT, "session")}</string>
    <key>AI_HUMAN_CWD</key>
    <string>${ROOT}</string>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
  </dict>
  <key>WorkingDirectory</key>
  <string>${ROOT}</string>
  <key>RunAtLoad</key>
  <false/>
  <key>KeepAlive</key>
  <true/>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>StandardOutPath</key>
  <string>${join(ROOT, "session", "bridge.stdout.log")}</string>
  <key>StandardErrorPath</key>
  <string>${join(ROOT, "session", "bridge.stderr.log")}</string>
</dict>
</plist>
`;
  mkdirSync(launchAgentsDir, { recursive: true });
  writeFileSync(plistPath, plistXml);
  printGreen(`launchd plist: ${plistPath}`);

  // botctl script
  const botctlPath = join(ROOT, "botctl");
  const botctlScript = `#!/usr/bin/env bash
# botctl — manage ${name} (${callName}) AI human process
LABEL="${plistLabel}"
PLIST="${plistPath}"

case "\$1" in
  start)
    launchctl load "\$PLIST" && echo "Started \$LABEL"
    ;;
  stop)
    launchctl unload "\$PLIST" && echo "Stopped \$LABEL"
    ;;
  restart)
    launchctl unload "\$PLIST" 2>/dev/null; sleep 1
    launchctl load "\$PLIST" && echo "Restarted \$LABEL"
    ;;
  status)
    result=$(launchctl list | grep "\$LABEL")
    if [ -n "\$result" ]; then
      echo "RUNNING: \$result"
    else
      echo "STOPPED: \$LABEL not loaded"
    fi
    ;;
  logs)
    tail -f "${join(ROOT, "session", "bridge.stderr.log")}"
    ;;
  *)
    echo "Usage: botctl {start|stop|restart|status|logs}"
    exit 1
    ;;
esac
`;
  writeFileSync(botctlPath, botctlScript);
  chmodSync(botctlPath, 0o755);
  printGreen("botctl script created");

  // ── VALIDATION ───────────────────────────────────────────────────────────

  print("");
  printBold("Validating setup...");

  if (telegramToken) {
    const ok = await checkTelegramToken(telegramToken);
    ok ? printGreen("Telegram bot token valid") : printRed("Telegram bot token invalid — check @BotFather");
  }

  if (elevenLabsKey && elevenLabsVoiceId) {
    printGreen("ElevenLabs configured — voice messages enabled");
  } else {
    printDim("ElevenLabs not configured — voice requests will get a fallback reply");
  }

  // ── DONE ─────────────────────────────────────────────────────────────────

  print("");
  printBold("═══════════════════════════════════════");
  printGreen(`Setup complete! Character: ${name} (${callName})`);
  printBold("═══════════════════════════════════════");
  print("");
  print("Next steps:");
  let step = 1;
  print(`  ${step++}. ${DIM}(optional)${RESET} Edit voice guide: characters/${callName}/profile/voice_guide.md`);
  if (refCount < 3) {
    print(`  ${step++}. Add face reference photos: ${refDir}`);
  }
  print("");
  print("Start / stop:");
  printBold(`  ./botctl start    # load & run`);
  printBold(`  ./botctl stop     # stop`);
  printBold(`  ./botctl status   # check running`);
  printBold(`  ./botctl logs     # tail stderr log`);
  print("");
  print("Monitor all instances:");
  printDim("  launchctl list | grep com.ai-human");
  print("");
}

main().catch((err) => {
  console.error(RED + "Setup failed: " + err?.message + RESET);
  process.exit(1);
});
