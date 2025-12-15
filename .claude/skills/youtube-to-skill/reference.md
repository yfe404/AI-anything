# The Deep Knowledge: What Makes Skills Actually Work

This document contains the understanding you MUST have before generating any skill. Read it completely.

---

## The Fundamental Truth

**A skill is not documentation. A skill is a tool that the agent uses to help users.**

When you create a skill from a YouTube video, you are NOT:
- Transcribing what someone said
- Summarizing video content
- Creating notes about a topic

You ARE:
- Building a capability the agent can invoke
- Creating actionable instructions the agent follows
- Extending what the agent can do for users

---

## How the agent Discovers and Uses Skills

Understanding this mechanism is critical:

### 1. The Description is a Classifier

```yaml
description: "Extract text from PDFs, fill forms, merge documents. Use when working with PDF files."
```

the agent reads ALL skill descriptions when deciding how to help a user. The description is not for humans — it's for the agent's decision-making.

**What happens:**
1. User says: "I need to get text out of this PDF"
2. the agent scans all skill descriptions
3. the agent matches "get text" + "PDF" → activates the skill
4. the agent then reads the full SKILL.md

**If your description doesn't contain trigger words, the agent will never find your skill.**

### 2. Trigger Words Must Match User Language

Users don't speak formally. They say:
- "How do I..." / "Can you help me..."
- "I need to..." / "I want to..."
- Platform names: "Docker", "React", "AWS"
- Actions: "deploy", "fix", "set up", "create"

Your description must contain these natural phrases.

**Bad:** `description: "Containerization workflow management"`
**Good:** `description: "Build and deploy Docker containers. Use when user needs to dockerize an app, create Dockerfile, or run containers."`

### 3. One Skill = One Capability

the agent gets confused when skills try to do everything.

**Bad:** A skill that covers "React, Vue, Angular, and Svelte components"
**Good:** Separate skills for each, or one focused on "frontend component patterns"

**The test:** Can you describe what this skill does in one sentence without using "and"?

---

## The Transformation Problem

The #1 failure mode when converting videos to skills:

### Video Content is Narrative

Videos are designed for humans watching sequentially:
- "So what we're going to do here is..."
- "The cool thing about this approach is..."
- "Now, you might be wondering why..."
- "Let me show you what happens when..."

### Skills Must Be Imperative

Skills are designed for the agent to execute:
- Step 1: Run `command`
- Step 2: Edit `file` to add...
- If X, then Y
- Warning: Don't do Z because...

### The Transformation Map

| Video Pattern | Skill Pattern |
|--------------|---------------|
| "So basically..." | *(delete entirely)* |
| "What you want to do is run..." | `bash command` |
| "The way this works is..." | Brief explanation, then steps |
| "I like to..." | "Recommended approach:" (if validated) |
| "Make sure you..." | "**Prerequisites:**" or "**⚠️ Warning:**" |
| "If you get this error..." | "**Troubleshooting:**" section |
| "The important thing here is..." | "**Key point:**" callout |
| "Let me show you..." | Concrete example with code |
| Rambling explanation | Bullet points |
| 10-minute walkthrough | Numbered steps |

---

## The Quality Checklist

Before finalizing any generated skill, verify:

### Description Quality
- [ ] Contains action verbs users would say ("deploy", "create", "fix")
- [ ] Mentions specific technologies by name
- [ ] Includes "Use when..." phrase listing 3-4 concrete scenarios
- [ ] Under 1024 characters
- [ ] No jargon users wouldn't use
- [ ] Covers both the technology AND the problem it solves (e.g., "off-grid messaging" not just "LoRa")

### Instructions Quality
- [ ] Every step is actionable (the agent can do it)
- [ ] Commands are complete (can be copy-pasted)
- [ ] Code examples are runnable
- [ ] No assumptions about "obvious" context
- [ ] Error cases are handled

### Voice Quality
- [ ] No "so", "basically", "gonna", "wanna"
- [ ] No "what we're doing here is"
- [ ] No first person ("I like to...")
- [ ] No rhetorical questions
- [ ] Professional, direct tone

### Structure Quality
- [ ] Clear sections with headers
- [ ] Prerequisites before instructions (with verification commands)
- [ ] Warnings before dangerous steps (hardware safety, data loss)
- [ ] Decision tables when multiple approaches exist
- [ ] Troubleshooting at the end with specific error messages
- [ ] Sources/references documented with links

---

## The Enrichment Decision

When you find a video's content can be enhanced with current documentation:

### When to Enrich
- API has changed since video
- Video skips edge cases docs cover
- Official docs have better examples
- Security best practices have evolved

### When NOT to Enrich
- Video approach is intentionally simplified
- Adding docs would bloat the skill
- User explicitly wants video-only content
- Docs are for different use case

### How to Enrich Well
1. Use Context7 to fetch relevant docs
2. Integrate naturally — don't just append
3. Note what came from video vs docs
4. Keep the skill focused (don't scope-creep)

---

## Common Mistakes and Fixes

### Mistake 1: The Info Dump
```markdown
# Bad: Just facts, no actions
Docker is a containerization platform that allows you to package applications
with their dependencies. It uses images and containers. Images are templates
and containers are running instances...
```

```markdown
# Good: Actionable instructions
## Create a Docker Container

1. Create `Dockerfile` in project root:
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   CMD ["npm", "start"]
   ```

2. Build the image:
   ```bash
   docker build -t myapp .
   ```

3. Run the container:
   ```bash
   docker run -p 3000:3000 myapp
   ```
```

### Mistake 2: The Vague Instruction
```markdown
# Bad: What does "set up" mean?
Set up your environment properly before starting.
```

```markdown
# Good: Specific steps
## Prerequisites

1. Install Node.js 20+: `brew install node` (macOS) or `winget install OpenJS.NodeJS` (Windows)
2. Verify installation: `node --version` (should show v20.x.x)
3. Install dependencies: `npm install`
```

### Mistake 3: Missing Context
```markdown
# Bad: Assumes knowledge
Run the migration command to update the schema.
```

```markdown
# Good: Complete context
Run the database migration:
```bash
npx prisma migrate dev --name init
```

This creates the `prisma/migrations/` folder and applies the schema from `prisma/schema.prisma` to your database.

**If you see "database does not exist":** Run `createdb myapp_dev` first.
```

### Mistake 4: Wrong Audience
```markdown
# Bad: Written for video viewer
As you can see on screen, we're clicking the deploy button...
```

```markdown
# Good: Written for the agent to execute
Deploy to Vercel:
```bash
vercel deploy --prod
```
When prompted, select:
- Project name: (use default or specify)
- Framework: Next.js
- Root directory: ./
```

---

## The Source Attribution Rule

Every generated skill MUST include:

```markdown
## Source

Generated from: [Video Title](youtube-url)
- Channel: <channel name>
- Published: <date>
- Verified against: <current docs date>

**Updates applied:**
- <what was updated from original video>
```

This is not optional. Users need to know the provenance.

---

## Final Test

Before delivering a skill, ask yourself:

1. **"If I gave this to the agent with no other context, could it help a user?"**
   - If no → Instructions aren't complete enough

2. **"Would the agent find this skill when a user asks for help with X?"**
   - If no → Description doesn't have right trigger words

3. **"Is there any 'video narrator' voice left?"**
   - If yes → Transform those sections

4. **"Is every piece of information still accurate today?"**
   - If unsure → Verify with Context7 or WebSearch

5. **"Does this skill try to do too many things?"**
   - If yes → Split into multiple skills
