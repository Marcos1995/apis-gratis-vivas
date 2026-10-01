# Graph Report - apis-gratis-vivas  (2026-10-01)

## Corpus Check
- 17 files · ~134,752 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .mdc 2, (none) 1)

## Summary
- 87 nodes · 96 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2a7b44ce`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- build.py
- Web design
- Debug
- Contexto del proyecto
- Verify (UI)
- Agent rules
- Build judgments with Laya
- Laya
- Review
- Project
- fetch.py
- DECISIONES.md

## God Nodes (most connected - your core abstractions)
1. `main()` - 11 edges
2. `Web design` - 8 edges
3. `Debug` - 6 edges
4. `Contexto del proyecto` - 6 edges
5. `build()` - 5 edges
6. `Verify (UI)` - 4 edges
7. `esc()` - 3 edges
8. `page()` - 3 edges
9. `assign_slugs()` - 3 edges
10. `load_json()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (14 total, 3 thin omitted)

### Community 0 - "build.py"
Cohesion: 0.20
Nodes (13): build(), esc(), page(), Genera el sitio estatico en _site/ desde project.json + data/items.json. Copia…, validate(), write(), datetime, html (+5 more)

### Community 1 - "Web design"
Cohesion: 0.22
Nodes (8): 0. Brief (30 s, don't ask the user), 1. Style = `DESIGN.md`, 2. Tokens (pick, don't invent), 3. Layout recipes, 4. Starter CSS (adapt; delete what you don't use), 5. Build rules, 6. Before HECHO, Web design

### Community 2 - "Debug"
Cohesion: 0.29
Nodes (6): 1. Root cause, 2. Compare, 3. Hypothesis, 4. Fix, Debug, Red flags → back to step 1

### Community 3 - "Contexto del proyecto"
Cohesion: 0.29
Nodes (6): Comandos utiles, Contexto del proyecto, Estado, Notas para el agente, Produccion, Stack

### Community 4 - "Verify (UI)"
Cohesion: 0.40
Nodes (4): 1. Screenshots, 2. Look, 3. Fix and repeat, Verify (UI)

### Community 5 - "Agent rules"
Cohesion: 0.50
Nodes (3): Agent rules, Flujo, Think → Simple → Surgical → Verify (Karpathy)

### Community 6 - "Build judgments with Laya"
Cohesion: 0.50
Nodes (3): Build judgments with Laya, Call, Design

### Community 7 - "Laya"
Cohesion: 0.50
Nodes (3): Laya, Reply (decision-only requests), Steps

### Community 8 - "Review"
Cohesion: 0.50
Nodes (3): Check, Do, Review

### Community 9 - "Project"
Cohesion: 0.50
Nodes (3): Docs, Project, Setup

### Community 10 - "fetch.py"
Cohesion: 0.16
Nodes (20): concurrent_futures, assign_slugs(), dump(), get_text(), load_json(), main(), parse_readme(), probe() (+12 more)

## Knowledge Gaps
- **31 isolated node(s):** `1. Root cause`, `2. Compare`, `3. Hypothesis`, `4. Fix`, `Red flags → back to step 1` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 52 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `1. Root cause`, `2. Compare`, `3. Hypothesis` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._