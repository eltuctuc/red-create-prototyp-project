---
name: Dev-QA-Loop
description: Orchestriert automatische /red-proto:dev → /red-proto:qa Zyklen für ein Feature, bis keine offenen Bugs über der Fix-Schwelle mehr existieren
---

Du bist Orchestrator für den Dev-QA-Loop. Du spawnst in jeder Iteration zwei Subagenten (Dev und QA), die jeweils die Phasen aus `commands/red-proto/dev.md` bzw. `commands/red-proto/qa.md` autonom abarbeiten. Die eigentliche Implementierung und das Review passieren in den Subagenten – du koordinierst nur die Iterationen und die Risikobewertung.

**Wichtig:**
- Dieser Command erwartet einen **Write-fähigen Kontext** – die Subagenten committen Code und legen Bug-Files an. Wenn Bash/Write-Permissions restriktiv sind, scheitern die Agents stumm.
- `/red-proto:dev` und `/red-proto:qa` bleiben als eigenständige Commands nutzbar – dieser Loop ruft sie **nicht** direkt auf, sondern lässt Subagenten die jeweilige Command-Datei als Playbook abarbeiten. Vorteil: der Haupt-Context bleibt über viele Iterationen schlank.

## Konflikt-Check (Pflicht – vor allen Phasen)

Führe die Prüfung aus `.claude/red-proto/templates/conflict-check.md` aus. Bei Konflikt: stoppe sofort mit der dort dokumentierten Meldung – keine Subagenten spawnen. Der Konflikt wird vom User außerhalb dieses Commands gelöst.

## Phase 0: Feature-ID bestimmen

```bash
# Argument normalisieren (feat-2, 2, FEAT-2 → alle werden zu FEAT-2)
# Aus dem Aufruf-Argument oder – falls nicht gegeben – Nachfrage:
ls features/FEAT-*.md 2>/dev/null
```

Falls keine ID: Liste zeigen, `AskUserQuestion` mit Feature-Auswahl.

**Guards:**
- `features/FEAT-[N]-*.md` muss existieren → sonst stopp: "Feature-Spec fehlt. Zuerst `/red-proto:requirements` ausführen."
- `## 3. Technisches Design` muss in der Spec sein → sonst Hinweis: "Tech-Design fehlt. Zuerst `/red-proto:architect FEAT-[N]`."

## Phase 0b: Loop-Log initialisieren

```bash
mkdir -p context
LOG="context/FEAT-[N]-loop.log"
```

Wenn `$LOG` bereits existiert: lies ihn ein, du setzt einen früheren Loop fort. Extrahiere die letzte genutzte `threshold`, die letzte `iteration`-Nummer und die Historie für die Risk-Berechnung.

Wenn nicht: lege den Log neu an mit YAML-Header:

```markdown
---
feature: FEAT-[N]
started: [ISO-Datum]
threshold: (noch nicht gesetzt)
---

# Dev-QA-Loop Log FEAT-[N]
```

## Phase 1: Dev-Subagent spawnen

Spawnt einen Subagent im **autonomen Modus** (siehe `.claude/red-proto/CONVENTIONS.md` → „Autonomer Modus"). Der Subagent arbeitet `dev.md` ab und kennt alle Standard-Regeln.

```typescript
Agent({
  description: "FEAT-[N] Dev-Implementation (Loop-Iteration [K])",
  prompt: `Du bist Dev-Orchestrator für FEAT-[N], Loop-Iteration [K]. Arbeite die Phasen
  aus .claude/commands/red-proto/dev.md autonom ab (siehe "Autonomer Modus" in
  .claude/red-proto/CONVENTIONS.md). Arbeitsverzeichnis aus project-config.md.

  Gib danach ausschließlich zurück:

  DEV_RESULT:
  status: success | failed
  commit: <git commit hash oder "keiner">
  changed_files: <Anzahl>
  notes: <max 2 Sätze, nur bei Ungewöhnlichem>`
})
```

Auf Ergebnis warten. Bei `status: failed`: Loop pausieren, Fehlerdetails anzeigen, auf Nutzer warten.

## Phase 2: QA-Subagent spawnen

Analog im autonomen Modus. Zusätzliche Anweisung: QA soll **alle** Bugs finden, unabhängig vom Schweregrad – die Fix-Schwelle verwaltet der Loop-Orchestrator selbst (Phase 3), nicht die qa.md.

```typescript
Agent({
  description: "FEAT-[N] QA-Review (Loop-Iteration [K])",
  prompt: `Du bist QA-Orchestrator für FEAT-[N], Loop-Iteration [K]. Arbeite die Phasen
  aus .claude/commands/red-proto/qa.md autonom ab (siehe "Autonomer Modus" in
  .claude/red-proto/CONVENTIONS.md). Finde alle Bugs, unabhängig vom Schweregrad –
  die Fix-Schwelle verwaltet der Loop-Orchestrator, nicht qa.md.

  Gib danach ausschließlich zurück:

  QA_RESULT:
  status: success | failed
  bugs_total: <Gesamtzahl offener Bugs>
  critical: <Anzahl>
  high: <Anzahl>
  medium: <Anzahl>
  low: <Anzahl>
  bug_ids: <kommagetrennte Liste aller offenen Bug-IDs, oder "keine">
  notes: <max 2 Sätze, nur bei Ungewöhnlichem>`
})
```

Auf Ergebnis warten. Bei `status: failed`: Loop pausieren.

**Wichtig:** Die QA-Zahlen sind orientierend – der Orchestrator liest gleich die Bug-Files selbst neu ein (Phase 4).

## Phase 3: Fix-Schwelle festlegen (nur erste Iteration)

Nur wenn `threshold` im Log noch nicht gesetzt ist:

Ermittle den letzten genutzten Schwellenwert aus anderen Features zur Vorschlag-Anzeige:

```bash
LAST_THRESHOLD=$(ls context/FEAT-*-loop.log 2>/dev/null \
  | xargs -I{} grep -h "^threshold:" {} 2>/dev/null \
  | grep -v "noch nicht gesetzt" \
  | tail -1 \
  | sed 's/^threshold: //')
```

```typescript
AskUserQuestion({
  questions: [
    {
      question: "QA-Runde abgeschlossen. Bis zu welchem Schweregrad sollen Bugs automatisch gefixt werden?",
      header: "Fix-Schwelle",
      options: [
        { label: "Critical", description: "Nur kritische Blocker fixen" },
        { label: "Critical + High", description: "Default für Prototypen" },
        // Wenn LAST_THRESHOLD gesetzt und nicht Default:
        { label: "Wie beim letzten Feature ([LAST_THRESHOLD])", description: "Konsistenz über Features hinweg" },
        { label: "Critical + High + Medium", description: "Strenger – für MVP-nahe Prototypen" }
      ],
      multiSelect: false
    }
  ]
})
```

Default-Highlight: "Critical + High" (medium-Level, der pragmatische Standard für Prototypen). Wenn `LAST_THRESHOLD` identisch wäre, entfällt die „Wie beim letzten Feature"-Option.

Speichere die Wahl im Log-Header:

```
threshold: critical,high
```

**Nie wieder fragen.** Auch bei späteren Iterationen desselben Loops.

## Phase 4: Bugs einlesen und Risiko berechnen

```bash
# Strikter Regex – verhindert, dass FEAT-1 auch FEAT-10 matcht:
ls bugs/ | grep -E "^BUG-FEAT[N]-" | grep -v "\-fixed"
```

Lies pro Bug-File das `severity`- und `status`-Feld. Ermittle für die aktuelle Iteration:

- `bugs_above`: Anzahl offener Bugs, deren Severity im Schwellenwert-Set liegt
- `bug_ids`: Set dieser Bug-IDs
- `new_ids`: IDs in `bug_ids`, die in der Vor-Iteration noch nicht existierten
- `recurring_ids`: IDs, die in einer früheren Iteration als `-fixed` markiert waren, jetzt aber wieder offen

**Risk-Berechnung als priorisierte Regelliste** (oberste matchende Regel gewinnt):

| Priorität | Bedingung | Risiko |
|-----------|-----------|--------|
| 1 | `recurring_ids` nicht leer | HIGH |
| 2 | `bugs_above` ≥ Voreiteration UND ≥ Vor-Voreiteration (2× keine Abnahme) | HIGH |
| 3 | `bugs_above` == Voreiteration (1× keine Abnahme) | MEDIUM |
| 4 | `new_ids` nicht leer | MEDIUM |
| 5 | `bugs_above` < Voreiteration | LOW |
| 6 | erste Iteration (keine Voreiteration) | LOW |

**Wichtig:** Sobald eine Regel matcht, ist das Risiko festgelegt – keine Kombination.

Append zur Loop-Log:

```markdown
## Iteration [K]

- bugs_above: [X]
- delta: [+/-Y vs. Iteration K-1]
- new_ids: [IDs oder –]
- recurring_ids: [IDs oder –]
- risk: [LOW | MEDIUM | HIGH]
- dev_commit: [hash aus DEV_RESULT]
- qa_commit: [hash oder –]
```

## Phase 5: Entscheidungslogik

| Situation | Aktion |
|-----------|--------|
| `bugs_above == 0` | → Phase 7 (Abschluss) |
| Bugs vorhanden, Risk LOW oder MEDIUM | → Phase 6 Statuszeile, dann zurück zu Phase 1 |
| Bugs vorhanden, Risk HIGH, 1× in Folge | → Phase 6 Statuszeile mit Warnung, dann zurück zu Phase 1 |
| Bugs vorhanden, Risk HIGH, 2× in Folge | → Phase 5a Exit anbieten |

### Phase 5a – Exit anbieten

```typescript
AskUserQuestion({
  questions: [
    {
      question: "🔴 Risiko Endlosschleife: 2 Iterationen ohne Fortschritt bei Bugs über Schwelle. Aktuelle Situation: [bugs_above] offen, neu: [new_ids oder keine], wiederkehrend: [recurring_ids oder keine]. Wie weiter?",
      header: "Loop-Exit",
      options: [
        { label: "Weiter – Risiko akzeptieren", description: "HIGH-Zähler wird zurückgesetzt" },
        { label: "Stoppen – Abschlussbericht", description: "Offene Bugs werden gelistet" }
      ],
      multiSelect: false
    }
  ]
})
```

Bei „Weiter": HIGH-Zähler im Log zurücksetzen, dann Phase 6 → Phase 1.
Bei „Stoppen": Phase 7.

## Phase 6: Iterationsstatus melden

Einzeiler im Chat:

```
Iteration [K] – Bugs über Schwelle: [X] ([±Y]) | Neu: [n] | Wiederkehrend: [r] | Risiko: [LOW|MEDIUM|HIGH]
```

Bei MEDIUM/HIGH: Bug-IDs der Anomalie anhängen (welche sind neu / welche wiederkehrend).

Dann automatisch zurück zu Phase 1. **Keine Rückfrage.**

## Phase 7: Abschlussbericht

```
✓ FEAT-[N] implementiert und QA-geprüft nach [K] Iteration(en).

Ergebnis: [Alle Ziel-Bugs behoben | Manuell abgebrochen]
Fix-Schwelle: [critical | critical,high | critical,high,medium]

Verbleibende offene Bugs unter Schwelle:
- [Bug-ID]: [Titel] (Severity: X)
(oder: keine)

Iterations-Verlauf:
[K] | Bugs: [X] | Risiko: [LOW|MEDIUM|HIGH]
...

Log: context/FEAT-[N]-loop.log

Hinweis: Die Abnahme-Screens (falls vorhanden in features/FEAT-[N]-*/screens/)
wurden nicht automatisch verändert. Wenn du die visuelle Umsetzung nochmal
prüfen willst: Code direkt anschauen oder /red-proto:preview FEAT-[N] erneut
aufrufen, falls du neue Abnahme-Screens brauchst.

Hinweis zum alten Skill: Es gab zuvor ein gleichnamiges Claude-Code-Skill in
~/.claude/skills/red-proto-dev-qa-loop/. Dieses wird durch diesen Command
ersetzt – du kannst es lokal löschen.
```

Log final schreiben und committen:

```bash
git add context/FEAT-[N]-loop.log
git commit -q -m "docs: FEAT-[N] dev-qa-loop abgeschlossen nach [K] Iteration(en)" && git push -q
```

## Wichtige Regeln

- Fix-Schwelle **genau einmal** pro Feature abfragen (erste Iteration), Log-Header speichert Entscheidung
- Exit nur **anbieten**, nie erzwingen
- Nach jeder QA-Runde Bugs **neu einlesen** – nie auf alter Zählung aufbauen
- Dateien mit `-fixed.md` ignorieren; nur offene Bugs zählen
- Subagent-Prompts niemals modifizieren, die Format-Strings (DEV_RESULT, QA_RESULT) sind der einzige Kanal
- Keine visuelle Prüfung der Screens – der Loop respektiert das Prototyp-Prinzip (Pixel-Perfektion ist nicht das Ziel)

## Checklist

- [ ] Feature-ID normalisiert und Guards bestanden
- [ ] Loop-Log in `context/` angelegt oder fortgesetzt
- [ ] Pro Iteration: Dev-Subagent + QA-Subagent, Ergebnis-Format geparst
- [ ] Fix-Schwelle einmalig erfragt, im Log verankert
- [ ] Bug-Regex strikt auf Feature-ID (kein FEAT-1/FEAT-10-Kollisions-Problem)
- [ ] Risk-Berechnung mit priorisierter Regelliste, oberste Regel gewinnt
- [ ] Iterationsstatus nach jeder Runde ausgegeben
- [ ] Abschlussbericht mit Log-Verweis und Screens/Skill-Hinweisen
