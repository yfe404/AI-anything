# Good vs Bad Skill Generation: Examples

Learn from these contrasting examples to understand what makes skills effective.

---

## Example 1: Docker Tutorial Video

### The Video Transcript (excerpt)

> "Hey everyone! So today we're going to be looking at Docker, which is super cool. Basically, Docker lets you containerize your applications, which is really neat. So what you want to do is, first, you're going to create a file called Dockerfile - no extension, just Dockerfile. And in there, you're going to put... let me show you on my screen... FROM node:14, because we're using Node.js for this example. Pretty simple, right? Then you do WORKDIR /app, and this just sets up where your code is going to live inside the container. Cool, so next..."

---

### ❌ BAD: Transcription-Style Skill

```markdown
---
name: docker-containers
description: Learn about Docker containerization
---

# Docker Containers

Docker is a containerization platform that lets you containerize your applications.

## What Docker Does

Docker is super cool and lets you containerize your apps. Basically, it creates containers
which is really neat for deployment.

## Getting Started

So what you want to do is first create a file called Dockerfile. No extension, just Dockerfile.
And in there you're going to put FROM node:14 because we're using Node.js for this example.
Pretty simple, right?

Then you do WORKDIR /app and this just sets up where your code is going to live inside the container.

## Next Steps

Next you would add your other Docker commands...
```

**Why it fails:**
- Description has no trigger words ("deploy", "containerize", "create Dockerfile")
- Keeps video narrator voice ("super cool", "basically", "right?")
- Not actionable (the agent can't execute "you're going to put")
- Incomplete (trails off with "...")
- Uses outdated Node 14

---

### ✅ GOOD: Transformed Skill

```markdown
---
name: docker-nodejs
description: Containerize Node.js applications with Docker. Use when user needs to create a Dockerfile, build Docker images, or deploy Node.js apps in containers.
---

# Dockerize Node.js Applications

Create production-ready Docker containers for Node.js applications.

## Source

Generated from: [Docker Tutorial for Beginners](https://youtube.com/watch?v=example)
- **Channel:** TechChannel
- **Published:** 2022-03-15
- **Verified:** 2024-12-15 against Docker and Node.js documentation

**Updates applied:**
- Node.js base image updated from node:14 to node:20-alpine (LTS)
- Added multi-stage build for smaller production images
- Added security best practices from Docker docs

## Prerequisites

- [ ] Docker installed: `docker --version` (should show 20.x+)
- [ ] Node.js project with `package.json`

## Instructions

### Step 1: Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "index.js"]
```

### Step 2: Build the Image

```bash
docker build -t myapp:latest .
```

Expected output: `Successfully tagged myapp:latest`

### Step 3: Run the Container

```bash
docker run -p 3000:3000 myapp:latest
```

Your app is now accessible at `http://localhost:3000`

## Troubleshooting

### "npm ci" fails with permission errors

**Cause:** Running as root with strict permissions

**Solution:** Add before npm ci:
```dockerfile
RUN chown -R node:node /app
USER node
```

## Reference

| Command | Description |
|---------|-------------|
| `docker build -t name .` | Build image from Dockerfile |
| `docker run -p HOST:CONTAINER image` | Run container with port mapping |
| `docker ps` | List running containers |
| `docker logs CONTAINER` | View container logs |

## See Also

- [Official Docker Node.js Guide](https://docs.docker.com/language/nodejs/)
```

**Why it works:**
- Description contains trigger words users say
- No narrator voice — professional and direct
- Every step is executable (complete commands)
- Updated to current versions with explanation
- Includes troubleshooting for common issues
- Source attribution with modification notes

---

## Example 2: React Hooks Tutorial

### The Video Transcript (excerpt)

> "Alright so useEffect is probably one of the most confusing hooks when you're first learning React. I remember when I was learning this I was like, what is going on? But basically, useEffect is for side effects - things like fetching data, setting up subscriptions, that kind of thing. So let me show you how it works. You import it from React, and then inside your component you call useEffect and pass it a function. Like useEffect(() => { // do something }). Now the tricky part is the dependency array..."

---

### ❌ BAD: Confusing, Narrative-Style

```markdown
---
name: react-hooks
description: Understanding React hooks
---

# React Hooks

## useEffect

useEffect is probably one of the most confusing hooks when you're first learning React.
Basically useEffect is for side effects - things like fetching data, setting up subscriptions.

You import it from React and then inside your component you call useEffect and pass it a function.

The tricky part is the dependency array...
```

**Why it fails:**
- Vague description (won't trigger on "fetch data in React")
- Keeps confusion framing from video
- Incomplete ("tricky part is...")
- No actual code examples
- Doesn't teach, just summarizes

---

### ✅ GOOD: Actionable Patterns

```markdown
---
name: react-useeffect-data-fetching
description: Fetch data in React components using useEffect. Use when user needs to load API data, handle async operations in React, or set up data fetching with loading states.
---

# Data Fetching with useEffect

Fetch data from APIs in React functional components with proper loading and error states.

## Source

Generated from: [React Hooks Tutorial](https://youtube.com/watch?v=example)
- **Channel:** ReactMaster
- **Published:** 2023-01-20
- **Verified:** 2024-12-15 against React 18 documentation

**Updates applied:**
- Added AbortController for cleanup (React 18 strict mode)
- Added error boundary pattern from React docs

## Prerequisites

- [ ] React 18+ project
- [ ] Basic understanding of async/await

## Instructions

### Pattern 1: Basic Data Fetching

```tsx
import { useState, useEffect } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchUser() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal
        });
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();
        setUser(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err as Error);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchUser();

    return () => controller.abort(); // Cleanup on unmount or userId change
  }, [userId]); // Re-run when userId changes

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return null;

  return <div>{user.name}</div>;
}
```

### Pattern 2: With Custom Hook (Reusable)

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData)
      .catch(err => {
        if (err.name !== 'AbortError') setError(err);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// Usage
function MyComponent() {
  const { data, loading, error } = useFetch<User[]>('/api/users');
  // ...
}
```

## Dependency Array Rules

| Array | Behavior |
|-------|----------|
| `[]` | Run once on mount |
| `[dep]` | Run on mount + when `dep` changes |
| No array | Run on every render (usually wrong) |

## Troubleshooting

### "React Hook useEffect has a missing dependency"

**Cause:** ESLint detected a variable used in effect but not in deps array

**Solution:** Either add to deps array or wrap in useCallback:
```tsx
const fetchData = useCallback(() => { ... }, []);
useEffect(() => { fetchData(); }, [fetchData]);
```

### Effect runs twice in development

**Cause:** React 18 Strict Mode intentionally double-invokes effects

**Solution:** This is expected. Ensure your cleanup function works correctly.
The AbortController pattern above handles this properly.

## See Also

- [React useEffect Documentation](https://react.dev/reference/react/useEffect)
```

**Why it works:**
- Specific description with trigger words ("fetch data", "API", "async")
- Complete, copy-paste-ready code
- Multiple patterns for different needs
- Explains the "why" concisely (dependency array table)
- Addresses real issues (Strict Mode double-invoke)
- Updated for React 18

---

## The Transformation Checklist

When converting video content, verify:

| Check | Question |
|-------|----------|
| ✅ Trigger words | Would the agent find this if user says "help me fetch data in React"? |
| ✅ Complete code | Can this code be pasted and run without modification? |
| ✅ No narrator | Is there any "so basically", "let me show you", "pretty cool"? |
| ✅ Current | Have I verified versions against current docs? |
| ✅ Actionable | Can the agent follow each step without watching the video? |
| ✅ Troubleshooting | Did I include common errors from the video + current issues? |
