# red · Create Prototyp Project

Ein KI-gestütztes Product Development Framework für [Claude Code](https://claude.ai/code) – von der vagen Idee bis zum getesteten Prototyp, mit Human-in-the-Loop an jedem Schritt.

## Was ist das?

Eine Sammlung von Claude Code Commands und Agents, die eine vollständige Produktentwicklungs-Pipeline abbilden:

```
/sparring              → Idee schärfen → PRD
/dev-setup             → Tech-Stack wählen, Projekt scaffolden, Git/GitHub einrichten
/user-research         → Problem Statement Map + Personas
/requirements          → Feature Specs (User Stories, Acceptance Criteria, Edge Cases)
/flows                 → Screen-Inventar + verbindliche Transition-Tabelle (nach allen Feature Specs)
/ux-design             → UX-Entscheidungen pro Feature – DS-konform, Transitions aus /flows
/solution-architect    → Technisches Design + Security + Test-Setup
/developer             → Implementierung (Frontend + Backend, parallel falls nötig)
/qa-engineer           → Tests, Accessibility, Security, Bug-Loop bis Production-Ready
```

Jeder Command ist eigenständig – du kannst an jedem Punkt einsteigen oder aufhören. Die Commands bauen aber aufeinander auf: jeder liest den Output des vorherigen und ergänzt die gemeinsamen Artefakte.

## Voraussetzungen

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installiert
- [`gh` CLI](https://cli.github.com/) (nur für GitHub-Setup in `/dev-setup`)
- Node.js, Python, Java etc. – je nach gewähltem Tech-Stack

## Installation

### 1. Bootstrap-Command global installieren

```bash
git clone https://github.com/eltuctuc/red-create-prototyp-project.git /tmp/red-framework && \
cp /tmp/red-framework/commands/red-create-prototyp-project.md ~/.claude/commands/ && \
rm -rf /tmp/red-framework
```

### 2. Framework in ein neues Projekt installieren

In deinem Projektverzeichnis:

```
/red-create-prototyp-project
```

Das kopiert alle Commands und Agents in `.claude/commands/` und `.claude/agents/` des Projekts. Danach stehen alle Pipeline-Commands lokal zur Verfügung.

### 3. Loslegen

```
/sparring
```

## Wie funktioniert es?

Alle Commands arbeiten mit denselben Artefakten im Projektverzeichnis:

```
./
  prd.md                     ← Product Requirements Document
  project-config.md          ← Tech-Stack, Pfade, Versionierung
  flows/                     ← Verbindliche Screen Transitions (erstellt von /flows)
  design-system/             ← Design-Vorgaben (Tokens, Komponenten, Patterns, Screens)
    tokens/                  ← Farben, Typografie, Spacing, Shadows, Motion
    components/              ← Komponenten-Specs (ein File pro Komponente)
    patterns/                ← UX-Patterns (Navigation, Formulare, Feedback, Datendarstellung)
    screens/                 ← Figma-Exports / Referenz-Screenshots
  research/                  ← User Research Ergebnisse
  features/FEAT-X.md         ← Akkumulatives Feature-File (alle Agents ergänzen)
  bugs/                      ← Bug-Reports (BUG-FEAT1-QA-001.md → -fixed.md nach Fix)
  docs/                      ← Produktfähigkeiten + Release-Historie
  [codeverzeichnis]/         ← Der eigentliche Code
```

Details zu allen File-Formaten: [ARTIFACT_SCHEMA.md](./ARTIFACT_SCHEMA.md)

## Framework-Philosophie

- **Human-in-the-Loop:** Kein Agent geht alleine weiter – jeder Schritt braucht eine explizite Bestätigung
- **Akkumulativ statt überschreibend:** Jeder Agent ergänzt seinen Abschnitt im Feature-File, bestehende Abschnitte bleiben erhalten
- **Audit-Trail:** Bugs werden nicht gelöscht, sondern zu `-fixed.md` umbenannt
- **Konfigurierbar:** Tech-Stack, Pfade und Team-Setup werden in `project-config.md` gespeichert und von allen Agents gelesen – kein Hardcoding
- **SemVer:** Automatisches Versioning – PATCH bei Bug-Fixes, MINOR bei neuen Features, MAJOR bei intentionalem Release

## Lizenz

MIT
