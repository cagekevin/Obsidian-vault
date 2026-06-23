---
type: source
title: "5 Agent Skill Design Patterns"
source_url: "https://x.com/GoogleCloudTech/status/2033953579824758855"
fetched: 2026-06-23
tags:
  - source
  - agent-skills
  - design-patterns
  - adk
status: ingested
related:
  - "[[Agent Skill Design Patterns]]"
---

# 5 Agent Skill Design Patterns

> Source: `Clippings/raw/5 Agent Skill设计模式.md` — Twitter/X thread by Google Cloud Tech, Chinese translation via CSDN

A set of 5 standardized design patterns for organizing Agent skills (SKILL.md format), derived from Google Cloud, Anthropic, and Vercel internal practices. The patterns address the problem of how to structure skill logic beyond just the file format standard.

## Key Takeaways

1. **Progressive Disclosure** — Skills load in layers: metadata first, then full instructions, then references/assets on demand. This is the foundational mechanism behind all 5 patterns.

2. **5 Patterns:**
   - **Tool Wrapper** — packages domain knowledge into on-demand skills (e.g., FastAPI best practices)
   - **Generator** — enforces consistent output structure via templates and style guides
   - **Reviewer** — separates "what to check" from "how to check" for scalable evaluation
   - **Inversion** — agent interviews the user first instead of guessing and generating
   - **Pipeline** — multi-step workflow with explicit checkpoints and gates

3. **Patterns are composable**, not mutually exclusive. A pipeline can embed a reviewer at the final step; a generator can start with inversion to collect variables.

4. **The real problem solved**: modularity, reusability, and reliability. System prompts are flat and fragile; structured skills with proper patterns are maintainable and less prone to drift.

## Core Concepts Extracted

- [[Agent Skill Design Patterns]] — the full set of 5 patterns
- Progressive Disclosure (skill loading mechanism)
- Tool Wrapper pattern
- Generator pattern
- Reviewer pattern
- Inversion pattern
- Pipeline pattern

## Source Details

- Original publisher: Google Cloud Tech
- Platform: Twitter/X
- Publication date: ~March 2026
- Authors: Shubham Saboo, Lavini Gam (per Chinese translation attribution)
- Related: ADK (Agent Development Kit) by Google Cloud
