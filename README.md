# red · Create Prototyp Project

Ein KI-gestütztes Product Development Framework für [Claude Code](https://claude.ai/code) – von der vagen Idee bis zum getesteten Prototyp, mit Human-in-the-Loop an jedem Schritt.

---

## Was ist das?

Eine Sammlung von Claude Code Commands und Agents, die eine vollständige Produktentwicklungs-Pipeline abbilden. Du arbeitest mit natürlicher Sprache – Claude führt die Pipeline aus, du triffst die Entscheidungen.

```
/red:proto-sparring     → Idee schärfen → PRD
/red:proto-dev-setup    → Tech-Stack wählen, Projekt scaffolden, Git/GitHub einrichten
/red:proto-research     → Problem Statement Map + Personas
/red:proto-requirements → Feature Specs (User Stories, Acceptance Criteria, Edge Cases)
/red:proto-flows        → Screen-Inventar + verbindliche Transition-Tabelle
/red:proto-ux           → UX-Entscheidungen pro Feature – DS-konform, Transitions aus /flows
/red:proto-architect    → Technisches Design + Security + Test-Setup
/red:proto-dev          → Implementierung (Frontend + Backend, parallel falls nötig)
/red:proto-qa           → Tests, Accessibility, Security, Bug-Loop bis Production-Ready
```

Jeder Command ist eigenständig – du kannst an jedem Punkt einsteigen oder aufhören. Die Commands bauen aber aufeinander auf: jeder liest den Output des vorherigen und ergänzt die gemeinsamen Artefakte.

---

## Voraussetzungen

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installiert und eingerichtet
- [`gh` CLI](https://cli.github.com/) (nur für GitHub-Setup in `/red:proto-dev-setup`)
- Node.js, Python oder ähnliches – je nach gewähltem Tech-Stack

---

## Installation

### Option A – npx Installer (empfohlen)

Einmalig ausführen. Der Installer fragt interaktiv ob global oder lokal:

```bash
npx red-proto@latest
```

> **Update:** Einfach denselben Befehl erneut ausführen – der Installer erkennt bestehende Installationen und fragt was zu tun ist.

### Option B – Manuell via Git

```bash
git clone https://github.com/eltuctuc/red-create-prototyp-project.git ~/.claude/templates/red-create-prototyp-project && \
cp ~/.claude/templates/red-create-prototyp-project/commands/red\:proto.md ~/.claude/commands/
```

---

### Framework in ein Projekt einrichten

Nach der Installation (Option A oder B) in Claude Code:

```bash
mkdir mein-projekt && cd mein-projekt
claude
```

Dann in Claude Code:

```
/red:proto
```

Das kopiert alle Commands und Agents in `.claude/commands/` und `.claude/agents/` des Projekts, legt die Verzeichnisstruktur an und richtet das neutrale Design System ein.

### Schritt 3 – Loslegen

```
/red:proto-sparring
```

---

## Was wird installiert?

Nach dem Setup hat dein Projekt folgende Struktur:

```
./
  .claude/
    commands/          ← Alle Pipeline-Commands (red:proto-sparring, red:proto-dev, ...)
    agents/            ← Sub-Agents (frontend-developer, ux-reviewer, ...)
  design-system/       ← Neutrales Design System (Tokens, Komponenten, Patterns)
    tokens/            ← Farben, Typografie, Spacing, Shadows, Motion
    components/        ← Button, Input, Card, ...
    patterns/          ← Navigation, Formulare, Feedback, Datendarstellung
    screens/           ← Platzhalter für Figma-Exports
  features/            ← Akkumulatives Feature-File (alle Agents ergänzen hier)
  flows/               ← Screen-Inventar + verbindliche Transition-Tabellen
  research/            ← User Research Ergebnisse
  bugs/                ← Bug-Reports (werden nicht gelöscht, sondern zu -fixed.md)
  docs/                ← Produktfähigkeiten + Release-Historie
  prd.md               ← Product Requirements Document (erstellt von /red:proto-sparring)
  project-config.md    ← Tech-Stack, Pfade, Versionierung
```

Details zu allen File-Formaten: [ARTIFACT_SCHEMA.md](./ARTIFACT_SCHEMA.md)

---

## Das Design System

Das Framework bringt ein **neutrales Design System** mit – als Ausgangspunkt, keine Pflicht. Du kannst es schrittweise befüllen oder durch ein bestehendes ersetzen.

**Drei Zustände pro Komponente:**

| Status | Bedeutung |
|--------|-----------|
| `DS-konform` | Implementiert nach Spec – keine Anpassung nötig |
| `Tokens-Build` | Nutzt DS-Tokens, aber keine fertige Komponente vorhanden – Agent baut selbst |
| `Hypothesen-Test` | Bewusstes Abweichen – UX-Entscheidung mit Begründung |

Der `frontend-developer` Agent liest die Design-System-Specs bevor er implementiert und meldet fehlende Komponenten zurück, statt still zu improvisieren.

---

## Empfohlene Skills

Das Framework läuft ohne zusätzliche Skills, nutzt sie aber wenn vorhanden:

| Skill | Genutzt von | Effekt |
|-------|-------------|--------|
| `ui-ux-pro-max` | `/red:proto-ux`, `ux-reviewer` Agent | Deutlich bessere UX-Qualität |
| `frontend-design` | `frontend-developer` Agent | Bessere Component-Implementierung |
| `neon-postgres` | `backend-developer` Agent | Nur bei Neon-Datenbankstack |
| `atlassian:spec-to-backlog` | `/red:proto-requirements` | Direkt in Jira schreiben |

Skills werden in Claude Code unter **Einstellungen → Skills** installiert.

---

## Framework-Philosophie

**Human-in-the-Loop:** Kein Agent geht alleine weiter – jeder Schritt braucht eine explizite Bestätigung.

**Akkumulativ statt überschreibend:** Jeder Agent ergänzt seinen Abschnitt im Feature-File, bestehende Abschnitte bleiben erhalten.

**Flows als Navigationsvertrag:** `/red:proto-flows` erstellt eine verbindliche Transition-Tabelle, die UX und Developer als gemeinsame Quelle der Wahrheit nutzen. Undokumentierte Transitions werden gemeldet, nicht stillschweigend implementiert.

**Audit-Trail:** Bugs werden nicht gelöscht, sondern zu `-fixed.md` umbenannt.

**SemVer:** Automatisches Versioning – PATCH bei Bug-Fixes, MINOR bei neuen Features, MAJOR bei intentionalem Release.

---

## Lizenz

MIT
