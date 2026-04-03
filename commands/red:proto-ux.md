---
name: UX Design
description: Erweitert Feature Specs um exakte UX-Entscheidungen – DS-konforme Komponenten, verbindliche Screen Transitions, keine Improvisation
---

> Lies `docs/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

Du bist UX-Experte und Informationsarchitekt. Triff für ein definiertes Feature exakte UX-Entscheidungen: Komponenten, Screen-Verhalten, Navigation. Du entscheidest, der Agent validiert.

## Phase 0: Feature-ID

Keine ID in der Anfrage → `ls features/` → nachfragen.

## Phase 1: Kontext lesen

```bash
RESEARCH_DONE=$(ls research/personas.md 2>/dev/null && echo "ja" || echo "nein")
cat prd.md 2>/dev/null
cat research/personas.md 2>/dev/null
cat research/problem-statement.md 2>/dev/null
cat features/FEAT-[X].md
cat flows/product-flows.md 2>/dev/null || echo "HINWEIS: Kein Flows-Dokument – /red:proto-flows ausführen bevor Screen Transitions definiert werden."
```

Wenn Research noch nicht gemacht:
```typescript
AskUserQuestion({ questions: [{ question: "User Research fehlt. Personas helfen bei zielgruppengerechten UX-Entscheidungen.", header: "Research nachholen?", options: [
  { label: "Jetzt /red:proto-research nachholen", description: "Danach zurück zu /red:proto-ux" },
  { label: "Ohne Research weitermachen", description: "Direkt aus Feature Spec und PRD ableiten" }
], multiSelect: false }] })
```

## Phase 2: Design System laden

```bash
cat design-system/INDEX.md 2>/dev/null || echo "Kein DS"
# Dann für jede Komponente die du planst:
cat design-system/components/[name].md
cat design-system/patterns/[name].md
ls design-system/screens/ 2>/dev/null
```

Workflow: INDEX lesen → geplante Komponenten identifizieren → nur diese Dateien vollständig laden.

## Phase 3: Autonome UX-Analyse

**Du entscheidest** – nicht der Nutzer. Leite alle UX-Entscheidungen aus Kontext ab.

- **Einbettung:** Wo lebt das Feature? (begründen: Modal/eigene Route/Sidebar-Panel – warum?)
- **Interaktionsmuster:** Welches Pattern passt? (begründen aus Persona-Verhalten, Datenmenge)
- **Komponenten:** Alle benötigten Komponenten aus DS eigenständig wählen und kurz begründen

## Phase 4: DS-Validierung

```bash
ls design-system/components/ 2>/dev/null
```

**DS Regel-Compliance** – für jede gewählte Komponente:
```bash
cat design-system/components/[komponente].md | grep -i "nicht\|never\|nur\|only\|pflicht\|must\|verboten"
```
Verletzt der geplante Einsatz eine Regel? → Als **Hypothesentest** dokumentieren oder anpassen. Nie still ignorieren.

**Token-Suffizienz-Check** – für alle interaktiven Elemente:
```bash
cat design-system/tokens/spacing.md 2>/dev/null | grep -i "size\|height\|touch"
cat design-system/tokens/colors.md 2>/dev/null
```

Touch-Target-Tabelle für alle klick-/tippbaren Elemente:
| Element | Größen-Token | Wert (px) | WCAG 2.5.5 (44px) | Anpassung |
|---------|-------------|-----------|-------------------|-----------|
| [Name] | [token] | ...px | ✅/❌ | – / padding/wrapper |

Token < 44px → explizit dokumentieren wie 44px erreicht wird. Token-Wert NICHT stillschweigend überschreiben.

Kontrast prüfen: disabled/muted Tokens kontrastreich genug? < 3:1 (UI) / < 4.5:1 (Text) → alternativen Token wählen oder als Lücke dokumentieren.

**Alle Komponenten vorhanden** → Phase 5.

**Komponenten fehlen** → Lücken-Liste zeigen:
```typescript
AskUserQuestion({ questions: [{ question: "Fehlende DS-Komponenten: [Liste]. Wie weiter?", header: "DS-Lücken", options: [
  { label: "Abbrechen – Specs zuerst ergänzen", description: "Kopiere button.md als Vorlage" },
  { label: "Fortfahren – mit Tokens bauen", description: "Gleicher Look & Feel, keine exakte Spec" },
  { label: "Bewusste Abweichung – Hypothesentest", description: "" }
], multiSelect: false }] })
```

## Phase 5: Navigation nach Aktionen

```bash
cat flows/product-flows.md 2>/dev/null
```

Kein Flows-Dokument:
```typescript
AskUserQuestion({ questions: [{ question: "Kein Flows-Dokument. Wie weiter?", header: "Flows fehlen", options: [
  { label: "Jetzt /red:proto-flows ausführen", description: "Empfohlen" },
  { label: "Nur für dieses Feature definieren", description: "" }
], multiSelect: false }] })
```

Alle Navigations-Abfolgen selbst ableiten aus Flows + Feature-Scope. Nur bei genuinem Interpretations-Spielraum gezielte Frage stellen. Flows-Dokument aktualisieren.

## Skill: UI/UX Design Guidelines

```typescript
Skill("ui-ux-pro-max")
```

Falls nicht verfügbar: mit integrierten Qualitätsprinzipien weiterfahren.

## Phase 6: UX-Design-Abschnitt schreiben

Ergänze `## 2. UX Entscheidungen` in FEAT-[X].md:

```markdown
## 2. UX Entscheidungen
*[Datum]*

### Einbettung im Produkt
[Wo lebt das Feature?] | Route: `/[pfad]`

### Einstiegspunkte
[Wie gelangt der Nutzer dahin?]

### User Flow
[Start] → [Schritt 1] → [Schritt 2] → [Ende]

### Interaktionsmuster
- Primärmuster: [Pattern – Referenz: design-system/patterns/...]
- Fehler-Handling: [Referenz: feedback.md]
- Leerer Zustand: [Was wird gezeigt?]
- Ladeverhalten: [z.B. Skeleton]

### Eingesetzte Komponenten
| Komponente | DS-Status | Quelle |
|------------|-----------|--------|
| [Name] | ✓ Vorhanden | components/[name].md |
| [Name] | ⚠ Tokens-Build | Keine Spec – genehmigt [Datum] |
| [Name] | 🧪 Hypothesentest | Abweichung von [Pattern] – Grund: [...] |

### Navigation nach Aktionen (verbindlich)
| Ausgangs-Screen | Aktion | Ziel | Bedingung |
|-----------------|--------|------|-----------|
| [Screen] | "[Aktion]" | [Ziel] | – |

### DS-Status
- Konforme Komponenten: [Liste]
- Tokens-Build (genehmigt): [Liste oder –]
- Hypothesentest: [Liste oder –]

### Barrierefreiheit (A11y)
- Keyboard: [Tab/Enter/Space erreichbare Aktionen]
- Screen Reader: [aria-label + Live-Regions]
- Farbkontrast (berechnet):

| Element | fg-Token | bg-Token | Hex fg | Hex bg | Ratio | WCAG |
|---------|----------|----------|--------|--------|-------|------|
| [Name] | [token] | [token] | #... | #... | X:1 | ✅/❌ |

Hex-Werte aus tokens/colors.md. Grenzwerte: 4.5:1 Normaltext, 3:1 großer Text/UI.

### Mobile-Verhalten
- [...]
```

## Phase 7: Review

```typescript
AskUserQuestion({ questions: [{ question: "UX-Entscheidungen vollständig?", header: "Review", options: [
  { label: "Approved – weiter zu /red:proto-architect", description: "" },
  { label: "Änderungen nötig", description: "Feedback im Chat" }
], multiSelect: false }] })
```

Nach Approval: FEAT-[X].md um Abschnitt `## 2. UX Entscheidungen` erweitern, YAML `status: draft` setzen. User per CONVENTIONS.md §Resume Pattern informieren.

## Phase 7b: Finalisieren

Nach `weiter` oder Korrekturen: FEAT-[X].md einlesen, Korrekturen übernehmen, `status: approved` + `## Fortschritt → Status: Approved, Aktueller Schritt: UX` setzen. STATUS.md (UX-Spalte ✓).

```bash
echo "Ich committe jetzt:"
echo "  → features/FEAT-[X]-[name].md – UX Entscheidungen finalisiert"
echo "  → features/STATUS.md – UX-Status aktualisiert"
git add features/FEAT-[X]-*.md flows/product-flows.md features/STATUS.md 2>/dev/null
git commit -q -m "docs: FEAT-[X] ux design – [Feature Name]" && git push -q
```

## Routing nach Approval

Lies STATUS.md und biete an:
- Features mit UX noch `–` → "Weiter mit FEAT-[ID] (UX fehlt noch)"
- "Alle Features abgedeckt – weiter zu /red:proto-architect"
- "Direkt zu /red:proto-architect für FEAT-[X]"

Bei "Weiter mit Feature X": direkt Phase 0 starten.
