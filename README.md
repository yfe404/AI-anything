# YouTube to Skill

**Transform YouTube tutorials into AI agent skills that actually work.**

## The Problem

### Video Knowledge is Trapped

YouTube contains millions of programming tutorials, but this knowledge is:

1. **Inaccessible to AI assistants** — AI agents cannot watch videos
2. **Time-consuming to extract** — A 10-minute video takes 10 minutes to watch
3. **Often outdated** — APIs change, libraries deprecate, best practices evolve
4. **Not actionable** — Narrative format ("so what we're gonna do...") ≠ executable instructions

### The Skill Quality Problem

AI agent skills extend an agent's capabilities. However, creating effective skills requires understanding:

- How agents discover skills (via description matching)
- The difference between narrative and imperative content
- Current state of mentioned technologies

Without this knowledge, generated skills are often:
- Never activated (poor descriptions)
- Unusable (incomplete instructions)
- Harmful (outdated information)

## The Solution

This skill automates the transformation pipeline:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EXTRACT   │────▶│  IDENTIFY   │────▶│   VERIFY    │────▶│  TRANSFORM  │────▶│  GENERATE   │
│  transcript │     │technologies │     │  up-to-date │     │   content   │     │    skill    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 1. Extract

Pulls transcripts from YouTube using captions API (with Whisper fallback):

```bash
python scripts/extract_youtube.py "https://youtube.com/watch?v=..."
```

**Output**: JSON with metadata (title, channel, date) and full transcript.

### 2. Identify

Scans transcript for technologies:
- Languages and versions
- Frameworks and libraries
- APIs and services
- CLI tools

### 3. Verify

**Videos get outdated. Skills must not.**

Uses available tools to verify current state:

| Source | Tool | Use Case |
|--------|------|----------|
| Library docs | Context7 MCP[^2] | React, Node.js, Python packages |
| General search | WebSearch | Tools, services, APIs |
| Specific docs | WebFetch | Official documentation URLs |

When outdated content is detected, the user is asked how to proceed:
- Update to current version
- Keep original with warnings
- Skip the section

### 4. Transform

Converts narrative video content to actionable skill instructions:

| Video Content | Skill Content |
|--------------|---------------|
| "So basically what we're doing..." | *(removed)* |
| "You want to run this command..." | ```bash\ncommand\n``` |
| "The important thing here is..." | **Prerequisites** section |
| "If you get this error..." | **Troubleshooting** section |

### 5. Generate

Produces a SKILL.md following the standard skill format:

```yaml
---
name: lowercase-with-hyphens
description: Action verb + what + when to use (max 1024 chars)
---
```

## File Structure

```
.claude/skills/youtube-to-skill/
├── SKILL.md                 # Main skill (174 lines)
│                            # - Workflow overview
│                            # - Tool integration (Context7, WebSearch)
│                            # - Quality checklist
│
├── reference.md             # Deep knowledge (289 lines)
│                            # - How agents discover skills
│                            # - Transformation patterns
│                            # - Common mistakes
│
├── templates/
│   └── skill_template.md    # Output template (94 lines)
│
├── scripts/
│   ├── extract_youtube.py   # Transcript extractor (337 lines)
│   └── requirements.txt     # Dependencies
│
└── examples/
    └── good_vs_bad.md       # Contrasting examples (354 lines)
```

**Total**: 1,250 lines of skill content

## Installation

### Option A: Project Skill

```bash
# Clone to your project
cp -r .claude/skills/youtube-to-skill /path/to/your/project/.claude/skills/
```

Available only in that project.

### Option B: Personal Skill (Recommended)

```bash
# Symlink to personal skills
ln -sf /path/to/youtube-to-skill ~/.claude/skills/youtube-to-skill

# Install dependencies
pip install youtube-transcript-api yt-dlp
```

Available in all projects. Restart your AI agent to load.

## Usage

Start a new session and request:

```
Create a skill from this YouTube video: https://youtube.com/watch?v=...
```

The agent will:
1. Extract the transcript
2. Identify technologies
3. Verify current state (ask about updates)
4. Ask about enrichment from official docs
5. Generate the skill
6. Ask where to save it

## Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| youtube-transcript-api | Caption extraction | `pip install youtube-transcript-api` |
| yt-dlp | Metadata + fallback | `pip install yt-dlp` |
| openai-whisper | Audio transcription (optional) | `pip install openai-whisper` |

## Limitations

- **Requires captions**: Videos without captions need Whisper (slower, requires GPU for speed)
- **English-focused**: Translation available but may reduce accuracy
- **Single video or playlist**: Does not process channel-wide content
- **Verification depends on tools**: Context7 coverage varies by library

## References

[^1]: AI Agent Skills — Packaged expertise that agents can discover and invoke based on description matching.

[^2]: Context7 MCP — Library documentation retrieval tool providing up-to-date API references and code examples.

---

**License**: MIT
