---
source_url: https://x.com/GoogleCloudTech/status/2033953579824758855
source_reprint: https://lavinigam.com/posts/adk-skill-design-patterns/
fetched: 2026-06-23
---

# 5 Agent Skill Design Patterns Every ADK Developer Should Know

**Author:** Lavi Nigam
**Published:** March 7, 2026
**Source:** Google Cloud Tech (X/Twitter), republished on lavinigam.com

## Summary

Master 5 SKILL.md design patterns for Google ADK agents — Tool Wrapper, Generator, Reviewer, Inversion, Pipeline. Includes working code and a decision tree.

The Agent Skills standard has been adopted by over 30 agent tools — Claude Code, Gemini CLI, GitHub Copilot, Cursor, JetBrains Junie, and many more. Every skill follows the same directory layout:

```
skill-name/
├── SKILL.md ← YAML frontmatter + markdown instructions (required)
├── references/ ← style guides, checklists, conventions (optional)
├── assets/ ← templates and output formats (optional)
└── scripts/ ← executable scripts (optional)
```

## The 5 Patterns

### Pattern 1: Tool Wrapper — Teach the Agent a Library

A Tool Wrapper is an agent skill that packages a library or tool's conventions, best practices, and coding standards into on-demand knowledge the agent loads when working with that technology. It is the simplest SKILL.md pattern — instructions plus reference files, no templates or scripts.

**When to use:** When you want your agent to apply consistent, expert-level conventions for a specific library, SDK, or internal system.

**Examples:**
- Vercel `react-best-practices` — 40+ React and Next.js performance rules
- Supabase `supabase-postgres-best-practices` — Postgres optimization guidelines
- Google `gemini-api-dev` — official Tool Wrapper for the Gemini API
- Google `adk-core-skills` — 6 official ADK development skills

**Key insight:** The `description` field in frontmatter is the agent's search index — if it's vague, the agent won't activate the skill when it should.

### Pattern 2: Generator — Produce Structured Output

A Generator skill produces documents, reports, or configurations by filling a reusable template. It uses both optional directories: `assets/` holds the output template, and `references/` holds the style guide.

**When to use:** When the output needs to follow a fixed structure every time — consistency matters more than creativity.

**Examples:**
- Technical reports — Executive Summary, Methodology, Findings, Recommendations
- API documentation — every endpoint with same sections
- Commit messages — enforce Conventional Commits format
- ADK agent scaffolding — generate standard project structure

**Key insight:** Template enforces structure, style guide enforces quality. Swap either file to change the output without touching the instructions.

### Pattern 3: Reviewer — Evaluate Against a Standard

A Reviewer skill evaluates code, content, or artifacts against a checklist stored in `references/`, producing a scored findings report grouped by severity.

**When to use:** Anywhere a human reviewer works from a checklist.

**Examples:**
- Code review — catch bugs and style issues against team rules
- Security audit — run OWASP Top 10 checks
- Editorial review — check against house style guide
- ADK agent review — validate against team conventions

**Key insight:** Separating WHAT to check (the checklist file) from HOW to check (the review protocol in the instructions). Swap the checklist and you get a completely different review from the same skill structure.

### Pattern 4: Inversion — The Skill Interviews You

Inversion flips the typical agent interaction: instead of the user driving the conversation, the skill instructs the agent to ask structured questions through defined phases before producing any output.

**When to use:** Anywhere the agent needs context from the user before it can do useful work — prevents generating detailed plans based on assumptions instead of asking.

**Examples:**
- Requirements gathering — interview before producing technical design
- Diagnostic interviews — walk through troubleshooting checklist
- Configuration wizards — gather deployment preferences
- ADK agent design — interview before scaffolding

**Key insight:** The `DO NOT start building or designing until all phases are complete` instruction at the top is the critical gate — without it, agents tend to jump to conclusions after the first answer.

### Pattern 5: Pipeline — Enforce a Multi-Step Workflow

A Pipeline skill defines a sequential workflow where each step must complete before the next begins, with explicit gate conditions that prevent the agent from skipping validation.

**When to use:** Any multi-step process where steps have dependencies and order matters — if skipping a step would produce incorrect or unvalidated output.

**Examples:**
- Documentation generation — parse → generate docstrings (with approval) → assemble docs → quality check
- Data processing — validate input → transform → enrich → write output
- Deployment workflows — test → build → deploy to staging → smoke test → promote
- ADK agent onboarding — interview (Inversion) → scaffold (Generator) → validate (Reviewer)

**Key insight:** Gate conditions are the defining feature. "Do NOT proceed to Step 3 until the user confirms" prevents the agent from assembling output with unreviewed content.

## Choosing the Right Pattern

| Pattern | Use when… | Directories used | Complexity |
|---------|-----------|------------------|------------|
| **Tool Wrapper** | Agent needs expert knowledge about a specific library or tool | `references/` | Low |
| **Generator** | Output must follow a fixed template every time | `assets/` + `references/` | Medium |
| **Reviewer** | Code or content needs evaluation against a checklist | `references/` | Medium |
| **Inversion** | Agent must gather context from the user before acting | `assets/` | Medium — multi-turn |
| **Pipeline** | Workflow has ordered steps with validation gates between them | `references/` + `assets/` + `scripts/` | High |

**Patterns compose.** A Pipeline can include a Reviewer step. A Generator can use Inversion to gather inputs. A Tool Wrapper can be embedded as a reference file inside a Pipeline skill. Production systems typically combine 2-3 patterns.

## Decision Tree

```
Start
  ↓
Does the skill produce output?
  ├─ Yes → From a template?
  │         ├─ Yes → Generator
  │         └─ No → Tool Wrapper
  └─ No → Does it evaluate existing input?
            ├─ Yes → Reviewer
            └─ No → Needs user input first?
                      ├─ Yes → Inversion
                      └─ No → Has ordered steps?
                                ├─ Yes → Pipeline
                                └─ No → Tool Wrapper
```

## ADK Skills Ecosystem

- **skills.sh** — largest community marketplace (86,000+ installs)
- **google-gemini/gemini-skills** — Google's official Tool Wrapper skills
- **google/adk-docs/skills** — Google's official ADK development skills
- **vercel-labs/agent-skills** — Vercel's official skills (22K stars)
- **supabase/agent-skills** — Supabase's Postgres optimization skills
- **anthropics/skills** — production-grade document skills (86,500 stars)
- **VoltAgent/awesome-agent-skills** — curated collection

## ADK Core Skills

Google publishes 6 official skills that teach coding agents how to write ADK code:

| Skill | What It Teaches |
|-------|-----------------|
| `adk-dev-guide` | ADK architecture, agent types, tool definitions, callbacks |
| `adk-cheatsheet` | Quick-reference patterns for common ADK tasks |
| `adk-eval-guide` | Writing and running agent evaluations |
| `adk-deploy-guide` | Deploying ADK agents to Cloud Run and Vertex AI |
| `adk-observability-guide` | Tracing, logging, and monitoring ADK agents |
| `adk-scaffold` | Project scaffolding and directory structure |

These are all Tool Wrapper pattern skills.

## SkillToolset and Three Levels

ADK's `SkillToolset` implements progressive disclosure through three auto-generated tools:
- `list_skills` — shows skill names and descriptions (L1, ~100 tokens each)
- `load_skill` — fetches full instructions (L2)
- `load_skill_resource` — loads reference files and templates on demand (L3)

The agent pays ~100 tokens per skill at startup, then loads the rest only when needed.

## FAQ Highlights

- **Skills vs Tools:** Tools give agents the ability to take actions. Skills teach agents when and how to use those tools effectively.
- **How many skills?** No hard limit. At 50 skills, roughly 5,000-7,500 tokens of overhead per call.
- **Where to store?** Project-level (`<project>/.agents/skills/`) for team-shared. User-level (`~/.agents/skills/`) for personal.
- **Testing:** Create test cases in `evals/evals.json`, run with and without the skill, measure pass rate delta.
- **Start with:** Tool Wrapper — simplest pattern and most widely adopted.

## References

1. Official ADK documentation for SkillToolset and progressive disclosure
2. Agent Skills Specification — open standard defining SKILL.md format
3. SoK: Agentic Skills — arXiv paper (February 2026) identifying 7 system-level skill design patterns
4. skills.sh — community marketplace with 86,000+ total installs
