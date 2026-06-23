---
type: entity
title: "Google ADK"
entity_type: tool
role: "Google's Agent Development Kit for building production AI agents"
first_mentioned: "[[5 Agent Skill Design Patterns]]"
created: 2026-06-23
updated: 2026-06-23
tags:
  - entity
  - tool
  - agent-engineering
status: developing
related:
  - "[[Agent Skill Design Patterns]]"
  - "[[5 Agent Skill Design Patterns]]"
sources:
  - "[[5 Agent Skill Design Patterns]]"
---

# Google ADK

Google's **Agent Development Kit (ADK)** — a framework for building production-grade AI agents with modular skills, multi-agent systems, and progressive disclosure.

## Overview

ADK provides the infrastructure for building, deploying, and monitoring AI agents. It implements the **Agent Skills specification** (agentskills.io), which has been adopted by over 30 agent tools including Claude Code, Gemini CLI, GitHub Copilot, Cursor, and JetBrains Junie.

## Key Components

### SkillToolset

The runtime API that equips agents with modular skills. Implements progressive disclosure through three auto-generated tools:
- `list_skills` — shows skill names and descriptions (L1, ~100 tokens each)
- `load_skill` — fetches full instructions (L2)
- `load_skill_resource` — loads reference files and templates on demand (L3)

### SKILL.md Format

Every skill follows the same directory layout:
```
skill-name/
├── SKILL.md ← YAML frontmatter + markdown instructions (required)
├── references/ ← style guides, checklists, conventions (optional)
├── assets/ ← templates and output formats (optional)
└── scripts/ ← executable scripts (optional)
```

### ADK Core Skills

Google publishes 6 official skills that teach coding agents how to write ADK code (all Tool Wrapper pattern):

| Skill | Purpose |
|-------|---------|
| `adk-dev-guide` | ADK architecture, agent types, tool definitions, callbacks |
| `adk-cheatsheet` | Quick-reference patterns for common ADK tasks |
| `adk-eval-guide` | Writing and running agent evaluations |
| `adk-deploy-guide` | Deploying ADK agents to Cloud Run and Vertex AI |
| `adk-observability-guide` | Tracing, logging, and monitoring ADK agents |
| `adk-scaffold` | Project scaffolding and directory structure |

## Ecosystem

- **skills.sh** — largest community marketplace (86,000+ installs)
- **Vercel** — official skills for React, Next.js, AI SDK
- **Supabase** — Postgres optimization skills
- **Anthropic** — production-grade document skills (86,500 stars)
- **30+ compatible agent tools** support the same SKILL.md format

## Skill Design Patterns

ADK skills follow 5 standardized design patterns:
1. **Tool Wrapper** — package library conventions into on-demand knowledge
2. **Generator** — produce structured output from templates
3. **Reviewer** — evaluate against checklists with severity grouping
4. **Inversion** — agent interviews the user before acting
5. **Pipeline** — multi-step workflow with gates and checkpoints

See [[Agent Skill Design Patterns]] for details.

## Installation

Core skills can be installed globally with:
```bash
npx skills add google/adk-docs -y -g
```

## Relevance

Directly relevant to Kevin's skills-main project — the same SKILL.md format and design patterns apply to both ADK and claude-obsidian skills. The Agent Skills specification enables cross-platform interoperability.
