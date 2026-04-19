---
name: Red Create Prototyp Project
description: Initialisiert das Product Development Framework (red) im aktuellen Projekt – kopiert alle Commands und richtet die Projektstruktur ein
---

Du richtest das Product Development Framework für dieses Projekt ein.

## Was du tust

**Schritt 1 – Prüfe ob das Framework schon installiert ist:**

```bash
ls .claude/commands/red-proto/ 2>/dev/null
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
mkdir -p .claude/commands/red-proto
mkdir -p .claude/agents
mkdir -p test-setup
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

**Schritt 2b – Terminal-Permissions einrichten (.claude/settings.json):**

Damit du nicht bei jedem Bash-, Git- oder Node-Befehl manuell zustimmen musst, werden die Permissions einmalig gesetzt.

**Wichtig:** Falls bereits eine `.claude/settings.json` existiert (z.B. durch MCP-Einstellungen), wird sie **erweitert**, nicht überschrieben.

```bash
if [ -f .claude/settings.json ]; then
  echo "settings.json existiert bereits – wird erweitert"
  cat .claude/settings.json
else
  echo "Keine settings.json vorhanden – wird neu erstellt"
fi
```

Wenn die Datei **nicht existiert**: erstelle `.claude/settings.json` mit folgendem Inhalt:

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": []
  }
}
```

Wenn die Datei **bereits existiert**: lies sie vollständig, prüfe ob ein `permissions`-Block vorhanden ist:
- Falls **kein** `permissions`-Block → füge ihn zum bestehenden JSON hinzu (JSON korrekt mergen, alle anderen Felder erhalten)
- Falls `permissions`-Block **bereits vorhanden** → nichts ändern, dem User mitteilen dass Permissions bereits konfiguriert sind

Zeige dem User danach den aktuellen Stand der settings.json:
```
✅ Terminal-Permissions gesetzt – du wirst nicht mehr bei jedem Befehl gefragt.
   Bash, Git, Read, Write und Edit sind für dieses Projekt vorab genehmigt.
   (Konfiguriert in .claude/settings.json – jederzeit anpassbar)
```

---

**Schritt 3a – Nur fehlende Dateien kopieren** (Modus: "Nur fehlende"):

```bash
# cp -n = no-clobber: überspringt Dateien die bereits existieren
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/workflow.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/sparring.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/dev-setup.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/test-setup.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/requirements.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/flows.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/ux.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/architect.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/preview.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/dev.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/commands/red-proto/qa.md .claude/commands/red-proto/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp -n ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/

# Design System Templates kopieren (nur wenn noch nicht vorhanden)
cp -rn ~/.claude/templates/red-create-prototyp-project/design-system/ ./

# Framework-Docs kopieren (Templates, SCAFFOLDING, CONVENTIONS) – ins .claude/red-proto/ Verzeichnis
mkdir -p .claude/red-proto
cp -rn ~/.claude/templates/red-create-prototyp-project/docs/ .claude/red-proto/
```

Verifiziere nach dem Kopieren dass alle kritischen Dateien wirklich angekommen sind:
```bash
# Pflicht-Check: diese Dateien müssen existieren
ls .claude/commands/red-proto/qa.md 2>/dev/null || echo "FEHLT: qa.md"
ls .claude/agents/qa-engineer.md 2>/dev/null || echo "FEHLT: qa-engineer.md"
ls .claude/red-proto/templates/bug-report.md 2>/dev/null || echo "FEHLT: bug-report.md (Bug-Template)"
ls .claude/red-proto/CONVENTIONS.md 2>/dev/null || echo "FEHLT: CONVENTIONS.md"
ls design-system/INDEX.md 2>/dev/null || echo "FEHLT: design-system/"
```

Wenn eine Datei als FEHLT gemeldet wird:
```
⚠️  [Dateiname] konnte nicht kopiert werden.
    Quelle: ~/.claude/templates/red-create-prototyp-project/ scheint unvollständig.
    Lösung: Führe `npx red-proto` erneut aus um das Framework neu zu installieren.
```

Zeige danach welche Dateien bereits existiert haben (übersprungen) und welche neu hinzugefügt wurden:
```bash
ls .claude/commands/red-proto/
ls .claude/agents/
```

**Schritt 3b – Alle aktualisieren** (Modus: "Aktualisieren"):

Warnung ausgeben: "Commands und Agents werden mit der Template-Version überschrieben. Projektdaten (prd.md, features/, test-setup/, bugs/, docs/) bleiben vollständig erhalten."

```bash
# Ohne -n: überschreibt bestehende Dateien
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/workflow.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/sparring.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/dev-setup.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/test-setup.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/requirements.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/flows.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/ux.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/architect.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/preview.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/dev.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/commands/red-proto/qa.md .claude/commands/red-proto/
cp ~/.claude/templates/red-create-prototyp-project/agents/frontend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/backend-developer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/qa-engineer.md .claude/agents/
cp ~/.claude/templates/red-create-prototyp-project/agents/ux-reviewer.md .claude/agents/

# Design System Templates aktualisieren
cp -r ~/.claude/templates/red-create-prototyp-project/design-system/ ./

# Framework-Docs aktualisieren (Templates, SCAFFOLDING, CONVENTIONS)
mkdir -p .claude/red-proto
cp -r ~/.claude/templates/red-create-prototyp-project/docs/ .claude/red-proto/
```

Verifiziere nach dem Kopieren:
```bash
ls .claude/commands/red-proto/qa.md 2>/dev/null || echo "FEHLT: qa.md"
ls .claude/agents/qa-engineer.md 2>/dev/null || echo "FEHLT: qa-engineer.md"
ls .claude/red-proto/templates/bug-report.md 2>/dev/null || echo "FEHLT: bug-report.md (Bug-Template)"
ls .claude/red-proto/CONVENTIONS.md 2>/dev/null || echo "FEHLT: CONVENTIONS.md"
ls design-system/INDEX.md 2>/dev/null || echo "FEHLT: design-system/"
```

Wenn eine Datei als FEHLT gemeldet wird:
```
⚠️  [Dateiname] konnte nicht kopiert werden.
    Quelle: ~/.claude/templates/red-create-prototyp-project/ scheint unvollständig.
    Lösung: Führe `npx red-proto` erneut aus um das Framework neu zu installieren.
```

**Schritt 4 – Empfohlene Skills prüfen:**

Das Framework ruft folgende Skills auf, wenn sie installiert sind. Teile dem User mit, welche fehlen:

```typescript
// Prüfe ob Skills verfügbar sind – nenne fehlende beim Namen
```

| Skill | Genutzt von | Priorität |
|-------|-------------|-----------|
| `ui-ux-pro-max` | `/red-proto:ux`, `ux-reviewer` | Kern – stark empfohlen |
| `frontend-design` | `frontend-developer` | Kern – stark empfohlen |
| `neon-postgres` | `backend-developer` | Nur bei Neon-Stack |
| `atlassian:spec-to-backlog` | `/red-proto:requirements` | Optional – bei Jira-Nutzung |
| `atlassian:triage-issue` | `/red-proto:qa` | Optional – bei Jira-Nutzung |

**Fehlende Kern-Skills:** Weise den User explizit darauf hin. Agents laufen ohne Skills, aber mit reduzierter Qualität.
**Fehlende optionale Skills:** Kurz erwähnen, nicht blockieren.

---

**Schritt 5 – Bestätigung:**

Zeige dem User welche Commands installiert wurden und erkläre den nächsten Schritt:

```
✅ Product Development Framework installiert

Verfügbare Commands:
/red-proto:workflow           → Pipeline-Status, offene Bugs, letztes Release
/red-proto:sparring           → Idee schärfen + PRD erstellen
/red-proto:dev-setup          → Projekt scaffolden, Git + GitHub einrichten
/red-proto:test-setup         → Personas + Test-Hypothesen für den Prototyp
/red-proto:requirements       → Feature Specs (IEEE/IREB)
/red-proto:ux                 → UX-Design-Entscheidungen, DS-konform (nutzt: ui-ux-pro-max)
/red-proto:architect          → Tech-Design + Security
/red-proto:preview            → Optional: Abnahme-Screens aus Spec, vor Dev begutachten
/red-proto:dev                → Implementierung, orchestriert Agents parallel bei Full-Stack
/red-proto:qa                 → Tests + UX-Review parallel, Bug-Reports, Production-Ready

Sub-Agents (.claude/agents/ – automatisch gestartet):
frontend-developer  → Frontend-Implementierung (nutzt: frontend-design)
backend-developer   → Backend-Implementierung (nutzt: neon-postgres bei Neon-Stack)
qa-engineer         → Technisches QA-Review
ux-reviewer         → UX-Review (nutzt: ui-ux-pro-max)

Starte mit: /red-proto:sparring

Nach einer Pause: /red-proto:workflow   → zeigt Projektstatus und empfiehlt nächsten Schritt
```
