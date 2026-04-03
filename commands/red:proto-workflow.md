---
name: Workflow
description: Liest den echten Projektstatus und sagt dir exakt was als nächstes zu tun ist – starte hiermit nach jeder Pause
---

Du bist der Workflow-Navigator. Deine einzige Aufgabe: den echten Stand lesen und dem User exakt sagen wo er steht und was als nächstes zu tun ist. Kein Raten, kein Schätzen – alles aus den Dateien.

> **Nach jeder Session-Pause hier starten.** Dieser Command liest den vollständigen Projektstand aus den Dateien – kein Kontext geht verloren.

## Phase 1: Projektstand vollständig lesen

```bash
# Grundstruktur
cat prd.md 2>/dev/null | head -5 || echo "FEHLT"
cat project-config.md 2>/dev/null | grep -E "Projektname|Tech-Stack|Codeverzeichnis|Developer aufgeteilt" || echo "FEHLT"

# Alle Features: Fortschritt-Sektion + Draft-Status
for f in features/FEAT-*.md 2>/dev/null; do
  echo "=== $f ==="
  grep -E "^# |Status:|Aktueller Schritt:|Fix-Schwelle:" "$f" 2>/dev/null | head -5
done

# Offene Drafts in der Discovery Phase
echo "--- OFFENE DRAFTS ---"
grep -rl "status: draft" prd.md research/ features/ flows/ 2>/dev/null || echo "Keine offenen Drafts"

# Offene Bugs (nach Feature gruppiert)
ls bugs/ 2>/dev/null | grep -v "\-fixed" || echo "Keine offenen Bugs"

# Flows vorhanden?
cat flows/product-flows.md 2>/dev/null | head -3 || echo "FEHLT"

# Letztes Release
cat docs/releases.md 2>/dev/null | head -10 || echo "FEHLT"
```

## Phase 2: Status-Übersicht ausgeben

Zeige eine präzise Übersicht – alles aus den echten Dateiinhalten:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROJEKTSTATUS: [Projektname aus prd.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VORBEREITUNG
  [✅/⬜] PRD               prd.md
  [✅/⬜] Dev Setup          project-config.md
  [✅/⬜] User Research      research/

OFFENE DRAFTS  ⚠️
  [Liste offener Draft-Dateien oder: Keine – alles finalisiert ✅]

FEATURES
  FEAT-1: [Name] ──── Schritt: [Spec|UX|Tech|Dev|QA|Done]  Status: [Draft|Approved]
  FEAT-2: [Name] ──── Schritt: [...]  Status: [...]
  ...

OFFENE BUGS
  [Liste oder: Keine offenen Bugs ✅]

BUILD-LOOP STATUS
  Flows definiert:   [✅ Ja / ⬜ Nein]
  Features mit UX:   [X von Y]
  Features im Loop:  [welche sind bei Architect/Dev/QA/Done]

LETZTES RELEASE
  [Version + Datum oder: Noch kein Release]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wenn offene Drafts vorhanden sind: diese prominent anzeigen und als ersten nächsten Schritt empfehlen (vor allem anderen).

## Phase 2b: STATUS.md generieren

Nach der Übersicht im Chat immer eine `STATUS.md` im Projektstamm speichern als Snapshot:

```markdown
---
generated: true
---

# Projektstatus
> ⚠️ Automatisch generiert via /red:proto-workflow — [Datum + Uhrzeit]
> Nicht manuell bearbeiten. Immer /red:proto-workflow aufrufen um zu aktualisieren.

## Vorbereitung

| Artefakt | Datei | Status |
|---|---|---|
| PRD | prd.md | [✅ Approved / ⚠️ Draft / ❌ Fehlt] |
| Dev Setup | project-config.md | [✅ Vorhanden / ❌ Fehlt] |
| User Research | research/ | [✅ Approved / ⚠️ Draft / ❌ Fehlt] |
| Flows | flows/product-flows.md | [✅ Approved / ⚠️ Draft / ❌ Fehlt] |

## Features

| ID | Feature | Schritt | Status |
|---|---|---|---|
| FEAT-[X] | [Name] | [Spec\|UX\|Tech\|Dev\|QA\|Done] | [✅ Approved / ⚠️ Draft] |

## Offene Drafts

[Liste der Dateien mit status: draft – oder: Keine]
```

Status-Werte aus den Dateien lesen:
- YAML-Frontmatter `status: draft` → ⚠️ Draft
- YAML-Frontmatter `status: approved` → ✅ Approved
- Datei fehlt → ❌ Fehlt

## Phase 3: Nächsten Schritt exakt benennen

Wende diese Entscheidungslogik an – in dieser Reihenfolge:

**1. Noch kein PRD?**
→ `Starte mit /red:proto-sparring`

**2. PRD vorhanden, kein project-config.md?**
→ `Führe /red:proto-dev-setup aus`

**3. Dev-Setup vorhanden, offene Bugs aus früheren Features?**
→ `Offene Bugs gefunden: [Liste]. Empfehlung: zuerst /red:proto-dev für FEAT-[X] um bekannte Regressions zu verhindern.`

**4. Features fehlen oder nicht alle haben Status ≥ "Spec"?**
→ `Definiere Features mit /red:proto-requirements`

**5. Alle Features haben "Spec", aber kein Flows-Dokument?**
→ `Alle Feature-Specs vorhanden – jetzt /red:proto-flows ausführen (einmalig, vor UX)`

**6. Flows vorhanden, aber Features mit Status "Spec" (noch keine UX)?**
→ `Führe /red:proto-ux für FEAT-[X] aus`

**7. Features mit Status "UX", aber noch kein Tech-Design?**
→ `Führe /red:proto-architect für FEAT-[X] aus`

**8. Features mit Status "Tech", aber noch keine Implementierung?**
→ `Führe /red:proto-dev für FEAT-[X] aus`

**9. Features mit Status "Dev", aber noch kein QA?**
→ `Führe /red:proto-qa für FEAT-[X] aus`

**10. Features mit Status "QA" und offenen Bugs?**
→ `FEAT-[X] hat [N] offene Bugs. Führe /red:proto-dev für FEAT-[X] aus, dann erneut /red:proto-qa`

**11. Alle Features "Done", keine offenen Bugs?**
→ `Alle Features Production-Ready ✅. Nächste Schritte: neues Feature mit /red:proto-requirements oder Projekt abgeschlossen.`

Gib immer **einen** konkreten nächsten Schritt – nicht mehrere gleichwertige Optionen. Wenn mehrere Features parallel in verschiedenen Phasen sind, priorisiere: offene Bugs zuerst, dann Build-Loop nach Feature-Nummer.

## Phase 4: Feature-Detail auf Wunsch

Wenn der User nach einem spezifischen Feature fragt ("was ist offen in FEAT-2?"):

```bash
cat features/FEAT-[ID].md
ls bugs/ 2>/dev/null | grep "FEAT-[ID]"
```

Zeige: Was wurde bereits entschieden, was fehlt noch, welche Bugs sind offen.

## Sonderfall: Neues Projekt

Wenn noch gar nichts vorhanden ist:

```
Noch kein Projekt gestartet.

Die Pipeline im Überblick:
  1. /red:proto-sparring      → Idee → PRD
  2. /red:proto-dev-setup     → Tech-Stack + Scaffold + Git
  3. /red:proto-research      → Personas (optional)
  4. /red:proto-requirements  → Feature Specs (einmal pro Feature)
                                ↓ wenn ALLE Features Specs haben:
  5. /red:proto-flows         → Screen-Inventar + Transitions (einmalig)
  6. /red:proto-ux            → UX-Entscheidungen (einmal pro Feature)

  Dann pro Feature (Build-Loop):
  7. /red:proto-architect → 8. /red:proto-dev → 9. /red:proto-qa
     └── Bei Bugs: zurück zu /red:proto-dev → /red:proto-qa

Starte mit: /red:proto-sparring
```
