---
type: concept
title: "Agent Skill Design Patterns"
complexity: intermediate
domain: agent-engineering
aliases:
  - "Skill Design Patterns"
  - "5 Agent Skill Patterns"
  - "ADK Skill Patterns"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - agent-engineering
  - skills
  - design-patterns
status: developing
related:
  - "[[LLM Wiki Pattern]]"
  - "[[DragonScale Memory]]"
  - "[[5 Agent Skill Design Patterns]]"
  - "[[concepts/_index]]"
sources:
  - "[[5 Agent Skill Design Patterns]]"
---

# Agent Skill Design Patterns

Five standardized patterns for structuring Agent skill logic (SKILL.md format), identified from Google Cloud, Anthropic, and Vercel internal practices. They go beyond the file format standard to address how skill logic should be organized internally.

Origin: Google Cloud Tech (Twitter/X), March 2026.

---

## Foundational Mechanism: Progressive Disclosure

Skills don't load all at once. They load in three layers:

1. **Metadata only** (~50 tokens) — name + description, loaded at startup
2. **Full instructions** (2000-5000 tokens) — loaded when user request matches the skill description
3. **References & assets** — loaded on-demand during execution, only when needed

This means you can distribute knowledge across many files, and the agent only fetches what it actually needs. This is why patterns like Tool Wrapper and Reviewer put detailed knowledge in `references/` instead of the main instruction file.

---

## The 5 Patterns

### 1. Tool Wrapper

**What it solves**: Packaging domain-specific knowledge so agents can apply it on-demand without bloating the system prompt.

**How it works**: Encapsulate library best practices, team conventions, or domain expertise into a skill. The main instruction tells the agent *when* and *how* to use the knowledge; the detailed knowledge lives in `references/` files loaded only when needed.

**Example**: A FastAPI expert skill that loads `references/conventions.md` only when reviewing code.

**When to use**: When your skill is essentially answering "how to correctly do X".

---

### 2. Generator

**What it solves**: Inconsistent output structure — sometimes summaries are included, sometimes not; heading levels vary; format drifts over time.

**How it works**: Output templates in `assets/`, style guides in `references/`, and the instruction acts as a project manager: read template → read style guide → collect missing variables from user → fill in the blanks.

**Key design choice**: Actively ask the user for missing information instead of letting the agent guess. This prevents hallucinated filler content.

**When to use**: API docs, standardized commit messages, project READMEs, weekly reports — any scenario where format matters more than content.

---

### 3. Reviewer

**What it solves**: Code review prompts grow longer and more fragile as you add rules; updating one rule risks breaking others.

**How it works**: Separate "what to check" from "how to check it". Evaluation criteria live in `references/review-checklist.md` (modular, easy to update). The instruction only describes the review process: load checklist → read code → apply each rule → generate structured report with severity levels.

**Scalability benefit**: Swap the checklist file (Python style → OWASP security) and you get a completely different reviewer — without changing the SKILL.md instruction at all.

**When to use**: Automated PR reviews, pre-human-review machine checks, security scanning, document quality assessment.

---

### 4. Inversion

**What it solves**: Agents love to guess and generate immediately. Give them a vague request and they'll fill in all blanks with assumptions, delivering a seemingly complete result that's actually off-target.

**How it works**: The agent becomes the interviewer. It asks structured questions in phases, and only starts working after all information is collected. The key is a hard gate instruction: "Do not begin building or designing until all phases are complete."

**Phase structure**: Typically 2-3 phases (problem discovery → technical constraints → synthesis), each with specific questions.

**When to use**: Project planning, architecture design, requirements analysis — any task where incomplete information leads to poor results.

---

### 5. Pipeline

**What it solves**: Complex multi-step tasks where the agent might skip steps or proceed with bad intermediate results.

**How it works**: The instruction itself is the workflow definition. Explicit sequential steps with hard checkpoints (gates) between them. Each step only loads the reference files it needs, keeping the context window clean.

**Key feature**: Diamond gates — explicit conditions that must be met before proceeding to the next step. Often includes human confirmation at critical junctions to prevent the agent from continuing with flawed intermediate output.

**When to use**: Multi-step document generation, code refactoring pipelines, data processing workflows — any task with multiple steps that must run in order with confirmation points.

---

## How to Choose

| Question | Pattern |
|----------|---------|
| Apply domain knowledge to user input? | **Tool Wrapper** |
| Generate consistently structured output? | **Generator** |
| Systematically evaluate something? | **Reviewer** |
| Need lots of context that users don't volunteer? | **Inversion** |
| Multiple sequential steps with checkpoints? | **Pipeline** |

**Patterns are composable**, not mutually exclusive. A pipeline can embed a reviewer at the final step; a generator can start with inversion to collect template variables. Composition is the norm, not the exception.

---

## Why This Matters

System prompts are flat, fragile, and hard to maintain. All content exists in context simultaneously, causing interference. Updates in one place can break other behaviors. And they're not reusable across projects.

Structured skills with proper patterns provide:
- **Separation of concerns** — instructions, knowledge, and templates live in different places
- **On-demand loading** — progressive disclosure keeps context windows clean
- **Reusability** — skills work across tools and projects

This isn't just engineering neatness — it affects agent reliability. A clearly structured skill is less likely to drift; a knowledge-layered skill is less likely to forget critical instructions in long contexts.

Choosing the right design pattern is choosing how much uncertainty you're willing to tolerate in agent behavior.

---

## Connections

See [[LLM Wiki Pattern]] for another pattern of structured knowledge management.
See [[DragonScale Memory]] for advanced memory structuring patterns.
See [[5 Agent Skill Design Patterns]] for the original source.
