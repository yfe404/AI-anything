---
name: youtube-to-skill
description: Transform YouTube videos or playlists into SKILL.md files. Use when user wants to create a skill from YouTube content, convert video tutorials into reusable agent workflows, learn from educational videos, or extract actionable knowledge from any YouTube URL.
---

# YouTube to Skill Transformer

Convert YouTube video content into effective, verified, up-to-date agent skills.

## ⚠️ Before You Generate ANY Skill

**You MUST read [reference.md](./reference.md) first.**

It contains the critical understanding of what makes skills actually work vs useless text files. Without this knowledge, you will create skills that the agent ignores.

---

## The Pipeline

```
EXTRACT ──▶ IDENTIFY ──▶ VERIFY ──▶ TRANSFORM ──▶ GENERATE
   │            │           │            │            │
transcript   tools &    current?     narrative    effective
 + meta      versions   enriched?    ──▶ action     skill
```

---

## Step 1: Extract Transcript

```bash
python .claude/skills/youtube-to-skill/scripts/extract_youtube.py "<URL>"
```

- Single videos: `youtube.com/watch?v=...` or `youtu.be/...`
- Playlists: `youtube.com/playlist?list=...`

Output: JSON with title, publish date, channel, and transcript.

**Note the publish date** — older videos need more verification.

---

## Step 2: Identify Technologies

Scan transcript and list ALL mentioned:

| Category | Examples |
|----------|----------|
| Languages | Python 3.9, TypeScript, Rust |
| Frameworks | React 18, Next.js 14, FastAPI |
| Libraries | axios, lodash, pandas |
| Tools | Docker, kubectl, terraform |
| Services | AWS S3, Stripe API, OpenAI |
| CLIs | npm, cargo, pip commands |

Create a verification checklist with version numbers if mentioned.

---

## Step 3: Verify & Update (CRITICAL)

**Videos get outdated. Your skill must not.**

### For Libraries/Frameworks → Use Context7 MCP

```
1. mcp__context7__resolve-library-id
   → Find the library ID (e.g., "react" → "/reactjs/react.dev")

2. mcp__context7__get-library-docs
   → Fetch current documentation for specific topics
   → Use mode='code' for API/examples, mode='info' for concepts
```

Example:
- Video mentions "React useEffect cleanup"
- Resolve: `/reactjs/react.dev`
- Fetch: topic="useEffect cleanup" mode="code"
- Compare video content with current docs

### For Tools/Services/APIs → Use WebSearch

```
WebSearch: "<tool name> documentation 2025" or "<api> breaking changes"
```

### When You Find Outdated Information

**STOP and ask the user:**

```
⚠️ Outdated content detected in video (published <date>):

[Library/Tool] v<old> → Current: v<new>

Breaking changes found:
• <specific change 1>
• <specific change 2>

How should I proceed?
A) Update to current version (recommended)
B) Keep original with deprecation warnings
C) Skip this section
```

### Ask About Enrichment

```
Would you like me to enrich this skill with current official documentation?

This would add:
• Updated API references from Context7
• Additional code examples
• Edge cases not covered in the video

[Yes / No / Ask me for each topic]
```

---

## Step 4: Transform Content

**This is where most skill generation fails.**

See [reference.md](./reference.md) for the deep understanding, but the core principle:

> **You are not transcribing. You are creating executable instructions.**

| ❌ Video Narration | ✅ Skill Instruction |
|-------------------|---------------------|
| "So what we're gonna do here is..." | *(delete)* |
| "You want to open your terminal and type..." | `bash -c "command"` |
| "The cool thing about this is..." | *(delete or convert to a note)* |
| "Make sure you don't forget to..." | **⚠️ Warning:** ... |
| "If you see this error..." | **Troubleshooting:** ... |
| "I usually structure it like..." | **Recommended structure:** |

**The test:** Can the agent follow these instructions without watching the video?

---

## Step 5: Generate the Skill

Use template: [templates/skill_template.md](./templates/skill_template.md)

### Pre-delivery Checklist

- [ ] **Description has trigger words** users actually say
- [ ] **One skill = one capability** (split if video covers multiple)
- [ ] **Instructions are executable** (commands, code, steps)
- [ ] **No narrator voice** ("so", "basically", "gonna")
- [ ] **Sources documented** (video URL + docs used)
- [ ] **Versions specified** for all tools/libraries

### Ask for Placement

```
Where should I save this skill?

A) .claude/skills/<name>/ — Project skill (shared via git)
B) ~/.claude/skills/<name>/ — Personal skill (your machine only)
```

---

## Available Tools Reference

| Need | Tool | Example |
|------|------|---------|
| Library docs | `mcp__context7__resolve-library-id` | Find React library ID |
| Library docs | `mcp__context7__get-library-docs` | Fetch React hooks docs |
| General search | `WebSearch` | "docker compose v2 migration" |
| Specific URL | `WebFetch` | Fetch a specific doc page |
