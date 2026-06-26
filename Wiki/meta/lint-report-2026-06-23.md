---
type: meta
title: "Lint Report 2026-06-23"
created: 2026-06-23
updated: 2026-06-23
tags: [meta, lint]
status: developing
---

# Lint Report: 2026-06-23

## Summary
- Pages scanned: 30 (6 concepts new, 14 concepts original, 7 entities original, 5 entities new, 6 sources new, 1 source original, index/hot/log)
- Issues found: 6
- Auto-fixed: 0
- Needs review: 6

## 1. Orphan Pages — 0 found
All 30 pages have at least one inbound wikilink. The newly created pages are well-connected through index, log, hot, and cross-references.

## 2. Dead Links — 1 found
- `Wiki/index.md` references `[[SVG Diagram Style Guide]]` in the concepts listing, but this page has **zero inbound links from any other wiki page** (only linked from index.md itself). This is a one-way index entry — it exists but nothing else in the wiki references it.

## 3. Stale Claims — 0 found
No contradictions detected. The new Local LLM Deployment ecosystem pages are self-consistent and don't conflict with existing Knowledge Management pages.

## 4. Missing Pages — 1 found
- **"Codex长期记忆系统"** — referenced in `.raw/raw-20260621-CodexClaude记忆管理.txt` as processed target, and mentioned in `Daily Notes/2026-06-21.md`, but no corresponding page exists in `Wiki/`. This was likely created by a previous AI session but not synced to this vault. Recommend: create stub or remove the `<!-- processed:` reference.
- **"LLM-Wiki框架"** — same situation. Referenced in `.raw/raw-20260403-Karpathy-LLM-Wiki-Gist.txt` as processed target, but no page exists. The content has been covered by `[[LLM Wiki Pattern]]` and existing Knowledge Management pages.

## 5. Missing Cross-References — 1 found
- `[[SVG Diagram Style Guide]]` in `Wiki/concepts/` has no `related:` field in its frontmatter linking it to any other concept. It's isolated from the rest of the wiki's concept graph (only reachable via index.md).

## 6. Frontmatter Gaps — 3 found
The following pages are **missing required frontmatter fields** (`complexity`, `status`, `tags`):

| Page | Missing Fields |
|------|---------------|
| `concepts/Persistent Wiki Artifact.md` | `complexity`, `domain`, `status`, `tags` |
| `concepts/Source-First Synthesis.md` | `complexity`, `domain`, `status`, `tags` |
| `concepts/Query-Time Retrieval.md` | `complexity`, `domain`, `status`, `tags` |

Also notable: `entities/Claude SEO.md` is typed as `entity` but lacks `entity_type` and `role` fields (has `created`/`updated`/`tags` only).

## 7. Empty Sections — 0 found
All pages have substantive content.

## 8. Stale Index Entries — 0 found
All entries in `Wiki/index.md` point to existing pages.

## 9. Address Validation — Skipped
DragonScale addresses not in use for this vault. No `address:` fields present on post-rollout pages (only `DragonScale Memory.md` has `address: c-000001` from import — this is a legacy carryover and not validated).

## 10. Semantic Tiling — Skipped
Requires `nomic-embed-text` model via Ollama. Not configured on this environment.

---

## Recommendations

### HIGH (consider fixing)
1. **Frontmatter gaps** — `Persistent Wiki Artifact.md`, `Source-First Synthesis.md`, `Query-Time Retrieval.md` lack `complexity`, `domain`, `status`, `tags`. These are developing concepts that were imported without complete frontmatter.
2. **Missing pages from previous ingest** — `Codex长期记忆系统` and `LLM-Wiki框架` were referenced as ingest targets but never actually synced to this vault. Either create stub pages or update the `<!-- processed:` markers.

### MEDIUM (nice to have)
3. **`SVG Diagram Style Guide`** — orphan-by-design? It's only accessible through index.md. Consider adding `related:` links or removing from index if it's an internal reference.
4. **`Claude SEO` entity** — missing `entity_type` and `role` fields.

### LOW
5. **Cross-linking opportunity**: The new Local LLM Deployment concepts could reference `[[Claude Code Local Setup]]` from `[[Ollama]]`'s existing mentions — already done, good connectivity.
