---
name: Red Create Prototyp Project
description: Initialisiert das Product Development Framework (red) im aktuellen Projekt – kopiert alle Commands und richtet die Projektstruktur ein
---

Du richtest das Product Development Framework für dieses Projekt ein.

## Was du tust

**Schritt 1 – Prüfe ob das Framework schon installiert ist:**

```bash
ls .claude/commands/ 2>/dev/null | grep -E "sparring|dev-setup|requirements|ia-ux|solution-architect|developer|qa-engineer"
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
mkdir -p bugs
mkdir -p docs
# Codeverzeichnis NUR anlegen wenn noch kein project-config.md existiert:
# (sonst ist das Codeverzeichnis bereits konfiguriert und möglicherweise anders als "projekt/")
[ ! -f project-config.md ] && mkdir -p projekt
```

**Schritt 3a – Nur fehlende Dateien kopieren** (Modus: "Nur fehlende"):

```bash
# cp -n = no-clobber: überspringt Dateien die bereits existieren
cp -n ~/.claude/templates/red-create-prototyp-project/commands/workflow.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/sparring.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/dev-setup.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/user-research.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/requirements.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/ia-ux.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/solution-architect.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/developer.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/qa-engineer.md .claude/commands/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/
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
cp ~/.claude/templates/red-create-prototyp-project/commands/workflow.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/sparring.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/dev-setup.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/user-research.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/requirements.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/ia-ux.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/solution-architect.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/developer.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/commands/qa-engineer.md .claude/commands/
cp ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/
```

**Schritt 4 – Empfohlene Skills prüfen:**

Das Framework ruft folgende Skills auf, wenn sie installiert sind. Teile dem User mit, welche fehlen:

```typescript
// Prüfe ob Skills verfügbar sind – nenne fehlende beim Namen
```

| Skill | Genutzt von | Priorität |
|-------|-------------|-----------|
| `ui-ux-pro-max` | `/ia-ux`, `ux-reviewer` | Kern – stark empfohlen |
| `frontend-design` | `frontend-developer` | Kern – stark empfohlen |
| `neon-postgres` | `backend-developer` | Nur bei Neon-Stack |
| `atlassian:spec-to-backlog` | `/requirements` | Optional – bei Jira-Nutzung |
| `atlassian:triage-issue` | `/qa-engineer` | Optional – bei Jira-Nutzung |

**Fehlende Kern-Skills:** Weise den User explizit darauf hin. Agents laufen ohne Skills, aber mit reduzierter Qualität.
**Fehlende optionale Skills:** Kurz erwähnen, nicht blockieren.

---

**Schritt 5 – Bestätigung:**

Zeige dem User welche Commands installiert wurden und erkläre den nächsten Schritt:

```
✅ Product Development Framework installiert

Verfügbare Commands:
/workflow           → Pipeline-Status, offene Bugs, letztes Release
/sparring           → Idee schärfen + PRD erstellen
/dev-setup          → Projekt scaffolden, Git + GitHub einrichten
/user-research      → Research-Fragen, Personas, Problem Statement
/requirements       → Feature Specs (IEEE/IREB)
/ia-ux              → IA/UX-Entscheidungen (nutzt: ui-ux-pro-max)
/solution-architect → Tech-Design + Security
/developer          → Implementierung, orchestriert Agents parallel bei Full-Stack
/qa-engineer        → Tests + UX-Review parallel, Bug-Reports, Production-Ready

Sub-Agents (.claude/agents/ – automatisch gestartet):
frontend-developer  → Frontend-Implementierung (nutzt: frontend-design)
backend-developer   → Backend-Implementierung (nutzt: neon-postgres bei Neon-Stack)
qa-engineer         → Technisches QA-Review
ux-reviewer         → UX-Review (nutzt: ui-ux-pro-max)

Starte mit: /sparring

Nach einer Pause: /workflow   → zeigt Projektstatus und empfiehlt nächsten Schritt
```
