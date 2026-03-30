---
name: Red Create Prototyp Project
description: Initialisiert das Product Development Framework (red) im aktuellen Projekt – kopiert alle Commands und richtet die Projektstruktur ein
---

Du richtest das Product Development Framework für dieses Projekt ein.

## Was du tust

**Schritt 1 – Prüfe ob das Framework schon installiert ist:**

```bash
ls .claude/commands/ 2>/dev/null | grep -E "sparring|dev-setup|requirements|ux-design|solution-architect|developer|qa-engineer"
ls .claude/agents/ 2>/dev/null
cat project-config.md 2>/dev/null | grep "Codeverzeichnis"
```

**Wenn Commands bereits vorhanden sind**, frage mit AskUserQuestion:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Das Framework ist bereits installiert. Was möchtest du tun?",
      header: "Setup-Modus",
      options: [
        {
          label: "Nur fehlende Dateien hinzufügen",
          description: "Bestehende Commands/Agents werden NICHT überschrieben – sicher für laufende Projekte"
        },
        {
          label: "Alle Commands + Agents auf neueste Version aktualisieren",
          description: "Überschreibt lokale Anpassungen an Commands und Agents – Projektdaten (features/, prd.md etc.) bleiben erhalten"
        },
        {
          label: "Abbrechen",
          description: "Nichts ändern"
        }
      ],
      multiSelect: false
    }
  ]
})
```

Bei "Abbrechen": sofort stoppen.

**Schritt 2 – Verzeichnisse anlegen:**

```bash
mkdir -p .claude/commands
mkdir -p .claude/agents
mkdir -p research
mkdir -p features
mkdir -p flows
mkdir -p bugs
mkdir -p docs
mkdir -p design-system/tokens
mkdir -p design-system/components
mkdir -p design-system/patterns
mkdir -p design-system/screens
# Codeverzeichnis NUR anlegen wenn noch kein project-config.md existiert:
# (sonst ist das Codeverzeichnis bereits konfiguriert und möglicherweise anders als "projekt/")
[ ! -f project-config.md ] && mkdir -p projekt
```

**Schritt 3a – Nur fehlende Dateien kopieren** (Modus: "Nur fehlende"):

```bash
# cp -n = no-clobber: überspringt Dateien die bereits existieren
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-workflow.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-sparring.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-dev-setup.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-research.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-requirements.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-flows.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-ux.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-architect.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-dev.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red:proto-qa.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/

# Design System Templates kopieren (nur wenn noch nicht vorhanden)
cp -rn ~/.claude/templates/red-create-prototyp-project/design-system/ ./
```

Zeige danach welche Dateien bereits existiert haben (übersprungen) und welche neu hinzugefügt wurden:
```bash
# Überprüfen welche Dateien tatsächlich existieren:
ls .claude/commands/
ls .claude/agents/
```

**Schritt 3b – Alle aktualisieren** (Modus: "Aktualisieren"):

Warnung ausgeben: "Commands und Agents werden mit der Template-Version überschrieben. Projektdaten (prd.md, features/, research/, bugs/, docs/) bleiben vollständig erhalten."

```bash
# Ohne -n: überschreibt bestehende Dateien
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-workflow.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-sparring.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-dev-setup.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-research.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-requirements.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-flows.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-ux.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-architect.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-dev.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/red:proto-qa.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/

# Design System Templates aktualisieren
cp -r ~/.claude/templates/red-create-prototyp-project/design-system/ ./
```

**Schritt 4 – Empfohlene Skills prüfen:**

Das Framework ruft folgende Skills auf, wenn sie installiert sind. Teile dem User mit, welche fehlen:

```typescript
// Prüfe ob Skills verfügbar sind – nenne fehlende beim Namen
```

| Skill | Genutzt von | Priorität |
|-------|-------------|-----------|
| `ui-ux-pro-max` | `/red:proto-ux`, `ux-reviewer` | Kern – stark empfohlen |
| `frontend-design` | `frontend-developer` | Kern – stark empfohlen |
| `neon-postgres` | `backend-developer` | Nur bei Neon-Stack |
| `atlassian:spec-to-backlog` | `/red:proto-requirements` | Optional – bei Jira-Nutzung |
| `atlassian:triage-issue` | `/red:proto-qa` | Optional – bei Jira-Nutzung |

**Fehlende Kern-Skills:** Weise den User explizit darauf hin. Agents laufen ohne Skills, aber mit reduzierter Qualität.
**Fehlende optionale Skills:** Kurz erwähnen, nicht blockieren.

---

**Schritt 5 – Bestätigung:**

Zeige dem User welche Commands installiert wurden und erkläre den nächsten Schritt:

```
✅ Product Development Framework installiert

Verfügbare Commands:
/red:proto-workflow           → Pipeline-Status, offene Bugs, letztes Release
/red:proto-sparring           → Idee schärfen + PRD erstellen
/red:proto-dev-setup          → Projekt scaffolden, Git + GitHub einrichten
/red:proto-research      → Research-Fragen, Personas, Problem Statement
/red:proto-requirements       → Feature Specs (IEEE/IREB)
/red:proto-ux          → UX-Design-Entscheidungen, DS-konform (nutzt: ui-ux-pro-max)
/red:proto-architect → Tech-Design + Security
/red:proto-dev          → Implementierung, orchestriert Agents parallel bei Full-Stack
/red:proto-qa        → Tests + UX-Review parallel, Bug-Reports, Production-Ready

Sub-Agents (.claude/agents/ – automatisch gestartet):
frontend-developer  → Frontend-Implementierung (nutzt: frontend-design)
backend-developer   → Backend-Implementierung (nutzt: neon-postgres bei Neon-Stack)
qa-engineer         → Technisches QA-Review
ux-reviewer         → UX-Review (nutzt: ui-ux-pro-max)

Starte mit: /red:proto-sparring

Nach einer Pause: /red:proto-workflow   → zeigt Projektstatus und empfiehlt nächsten Schritt
```
