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
grep -rl "status: draft" prd.md test-setup/ features/ flows/ 2>/dev/null || echo "Keine offenen Drafts"

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

LEGENDE
  ⬜  Noch nicht begonnen
  🔄  In Bearbeitung / In Prüfung (z.B. Draft, offene Bugs)
  ✅  Abgenommen / Freigegeben
  ✅⚠️ Abgenommen mit Known Issues

VORBEREITUNG
  [✅/🔄/⬜] PRD               prd.md
  [✅/🔄/⬜] Test-Setup         test-setup/
  [✅/🔄/⬜] Design-System      design-system/tokens/
  [✅/🔄/⬜] Dev Setup          project-config.md

OFFENE DRAFTS  ⚠️
  [Liste offener Draft-Dateien oder: Keine – alles finalisiert ✅]

FEATURES
  ID       Name          Spec  UX    Tech  Dev   QA
  FEAT-1   [Name]        ✅    ✅    ✅    ✅    🔄 2 High, 1 Medium offen
  FEAT-2   [Name]        ✅    🔄    ⬜    ⬜    ⬜
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
> ⚠️ Automatisch generiert via /red-proto:workflow — [Datum + Uhrzeit]
> Nicht manuell bearbeiten. Immer /red-proto:workflow aufrufen um zu aktualisieren.

## Legende

| Symbol | Bedeutung |
|---|---|
| ⬜ | Noch nicht begonnen |
| 🔄 | In Bearbeitung / In Prüfung (Draft oder offene Bugs) |
| ✅ | Abgenommen / Freigegeben |
| ✅⚠️ | Abgenommen mit Known Issues (offene Low-Bugs akzeptiert) |
| ❌ | Fehlt / Blockiert |

## Vorbereitung

| Artefakt | Datei | Status |
|---|---|---|
| PRD | prd.md | [✅ / 🔄 Draft / ❌ Fehlt] |
| Test-Setup | test-setup/ | [✅ / 🔄 Draft / ❌ Fehlt] |
| Design-System | design-system/tokens/ | [✅ / 🔄 Teilweise / ⬜ Leer] |
| Dev Setup | project-config.md | [✅ / ❌ Fehlt] |
| Flows | flows/product-flows.md | [✅ / 🔄 Draft / ❌ Fehlt] |

## Features

| ID | Feature | Spec | UX | Tech | Dev | QA |
|---|---|---|---|---|---|---|
| FEAT-[X] | [Name] | [⬜/🔄/✅] | [⬜/🔄/✅] | [⬜/🔄/✅] | [⬜/🔄/✅] | [⬜ / 🔄 N Bugs offen / ✅ / ✅⚠️ N Known Issues] |

> **QA-Spalte im Detail:**
> `⬜` = noch nicht geprüft · `🔄 2 Critical, 1 High offen` = Dev-Loop läuft · `✅` = abgenommen · `✅⚠️ 3 Low offen` = abgenommen mit Known Issues

## Offene Drafts

[Liste der Dateien mit status: draft – oder: Keine]
```

Status-Werte aus den Dateien lesen:
- YAML-Frontmatter `status: draft` → 🔄 In Bearbeitung
- YAML-Frontmatter `status: approved` → ✅ Freigegeben
- YAML-Frontmatter `qa_status: "🔄 ..."` → 🔄 mit Bug-Detail aus qa_status
- YAML-Frontmatter `qa_status: "✅ ..."` → ✅ oder ✅⚠️ je nach Inhalt
- Datei fehlt → ⬜ (noch nicht begonnen) oder ❌ (erwartet aber fehlend)

## Phase 3: Nächsten Schritt exakt benennen

Wende diese Entscheidungslogik an – in dieser Reihenfolge:

**1. Noch kein PRD?**
→ `Starte mit /red-proto:sparring`

**2. PRD vorhanden, kein Test-Setup (`test-setup/personas.md` fehlt)?**
→ `Empfehlung: /red-proto:test-setup ausführen – Personas und Hypothesen schärfen den späteren Prototyp-Test. Alternativ direkt zu /red-proto:dev-setup.`

**2b. PRD vorhanden, `design-system/tokens/` leer?**
→ `Empfehlung: Bevor /red-proto:dev-setup läuft, Design-System anlegen – Tokens (Farben, Typo, Spacing) beeinflussen Stack-Wahl und werden später automatisch in den Code transportiert. Alternativ ohne DS weiter.`

**3. PRD vorhanden, kein project-config.md?**
→ `Führe /red-proto:dev-setup aus`

**4. Dev-Setup vorhanden, offene Bugs aus früheren Features?**
→ `Offene Bugs gefunden: [Liste]. Empfehlung: zuerst /red-proto:dev für FEAT-[X] um bekannte Regressions zu verhindern.`

**5. Features fehlen oder nicht alle haben Status ≥ "Spec"?**
→ `Definiere Features mit /red-proto:requirements`

**6. Alle Features haben "Spec", aber kein Flows-Dokument?**
→ `Alle Feature-Specs vorhanden – jetzt /red-proto:flows ausführen (einmalig, vor UX)`

**7. Flows vorhanden, aber Features mit Status "Spec" (noch keine UX)?**
→ `Führe /red-proto:ux für FEAT-[X] aus`

**8. Features mit Status "UX", aber noch kein Tech-Design?**
→ `Führe /red-proto:architect für FEAT-[X] aus`

**8b. Features mit Status "Tech", noch keine Abnahme-Screens (optional)?**
→ `Optional: /red-proto:preview FEAT-[X] – erzeugt Screens aus der Spec, damit du das erwartete Ergebnis vor dem Bau begutachten kannst. Alternativ direkt zu /red-proto:dev.`

**9. Features mit Status "Tech", aber noch keine Implementierung?**
→ `Führe /red-proto:dev für FEAT-[X] aus`

**10. Features mit Status "Dev", aber noch kein QA?**
→ `Führe /red-proto:qa für FEAT-[X] aus`

**11. Features mit `qa_status: 🔄` (offene Bugs, Dev-Loop läuft)?**
→ `FEAT-[X] hat offene Bugs (qa_status: [Detail]). Führe /red-proto:dev für FEAT-[X] aus, dann erneut /red-proto:qa`

**12. Features mit `qa_status: ✅` oder `✅⚠️` → alle Done?**
→ `Alle Features abgenommen ✅. Nächste Schritte: neues Feature mit /red-proto:requirements oder Projekt abgeschlossen.`

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
  1. /red-proto:sparring      → Idee → PRD
  2. /red-proto:test-setup    → Personas + Test-Hypothesen (empfohlen)
  3. Design-System anlegen    → design-system/tokens/ (empfohlen vor dev-setup)
  4. /red-proto:dev-setup     → Tech-Stack + Scaffold + Git + DS-Transport
  5. /red-proto:requirements  → Feature Specs (einmal pro Feature)
                                ↓ wenn ALLE Features Specs haben:
  6. /red-proto:flows         → Screen-Inventar + Transitions (einmalig)
  7. /red-proto:ux            → UX-Entscheidungen (einmal pro Feature)

  Dann pro Feature (Build-Loop):
  8. /red-proto:architect → (optional) /red-proto:preview → /red-proto:dev → /red-proto:qa
     └── /red-proto:preview: Abnahme-Screens begutachten bevor gebaut wird
     └── Bei Bugs (🔄): zurück zu /red-proto:dev → /red-proto:qa
     └── QA-Abnahme: ✅ Abgenommen | ✅⚠️ Abgenommen mit Known Issues

Starte mit: /red-proto:sparring
```
