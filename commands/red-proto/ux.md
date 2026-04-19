---
name: UX Design
description: Erweitert Feature Specs um exakte UX-Entscheidungen – DS-konforme Komponenten, verbindliche Screen Transitions, keine Improvisation
---

> Lies `.claude/red-proto/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

Du bist UX-Experte und Informationsarchitekt. Triff für ein definiertes Feature exakte UX-Entscheidungen: Komponenten, Screen-Verhalten, Navigation. Du entscheidest, der Agent validiert.

## Phase 0: Projektstatus lesen und Feature wählen

```bash
cat features/STATUS.md 2>/dev/null
ls features/FEAT-*.md 2>/dev/null
```

Lies STATUS.md vollständig. Kategorisiere alle Features:

- **UX-bereit** (für diesen Skill relevant): Req ✓, UX noch `–`
- **In Bearbeitung**: UX begonnen (status: draft), noch nicht approved
- **UX fertig**: UX ✓ – überspringen
- **Noch nicht ready**: Req fehlt – überspringen

Zeige eine kurze Übersicht im Chat, z.B.:
```
UX-bereit (3):    FEAT-02 Nutzerprofil, FEAT-04 Benachrichtigungen, FEAT-05 Export
In Bearbeitung:   FEAT-03 Dashboard (draft)
Bereits fertig:   FEAT-01 Login
Noch nicht ready: FEAT-06 (Req fehlt)
```

**Wenn genau eine Feature-ID in der Anfrage angegeben** → direkt mit dieser starten, kein Multi-Select nötig. `MODUS = einzeln`.

**Wenn keine ID angegeben:** Multi-Select-Frage mit allen UX-bereiten Features. Erste Option ist immer "Alle":

```typescript
AskUserQuestion({ questions: [{ question: "Welche Features sollen jetzt bearbeitet werden?", header: "Feature-Auswahl", options: [
  { label: "Alle: FEAT-[ID], FEAT-[ID], FEAT-[ID]", description: "Alle in einem Durchlauf – eine Freigabe am Ende" },
  { label: "FEAT-[ID] [Name]", description: "" },
  { label: "FEAT-[ID] [Name]", description: "" }
], multiSelect: true }] })
```

*(Optionen dynamisch aus STATUS.md befüllen. "Alle"-Option konkrete IDs in label nennen.)*

**MODUS bestimmen:**
- "Alle" ausgewählt → `MODUS = alle`
- Teilmenge ausgewählt → `MODUS = einzeln`
- Bearbeitungsreihenfolge: ausgewählte Features in ID-Reihenfolge als `QUEUE` merken.

## Phase 1: Kontext lesen

```bash
TEST_SETUP_DONE=$(ls test-setup/personas.md 2>/dev/null && echo "ja" || echo "nein")
cat prd.md 2>/dev/null
cat test-setup/personas.md 2>/dev/null
cat test-setup/hypotheses.md 2>/dev/null
cat features/FEAT-[X].md
cat flows/product-flows.md 2>/dev/null || echo "HINWEIS: Kein Flows-Dokument – /red-proto:flows ausführen bevor Screen Transitions definiert werden."
```

Wenn Test-Setup noch nicht gemacht:
```typescript
AskUserQuestion({ questions: [{ question: "Das Test-Setup fehlt. Personas helfen bei zielgruppengerechten UX-Entscheidungen.", header: "Test-Setup nachholen?", options: [
  { label: "Jetzt /red-proto:test-setup nachholen", description: "Danach zurück zu /red-proto:ux" },
  { label: "Ohne Test-Setup weitermachen", description: "Direkt aus Feature Spec und PRD ableiten" }
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
  { label: "Jetzt /red-proto:flows ausführen", description: "Empfohlen" },
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

```bash
cat .claude/red-proto/templates/ux-decisions.md
```

Ergänze `## 2. UX Entscheidungen` in FEAT-[X].md nach diesem Template. Fülle alle Platzhalter aus dem Kontext.

## Phase 6b: Draft auf Disk schreiben

Unabhängig vom MODUS: FEAT-[X].md jetzt mit `## 2. UX Entscheidungen` ergänzen und `status: draft` setzen. Datei auf Disk schreiben – noch kein Commit.

---

## Phase 7: Review (nur MODUS = einzeln)

*Wenn MODUS = `alle`: diesen Abschnitt überspringen. Weiter zum nächsten Feature in QUEUE (Phase 1). Wenn QUEUE leer: zu „Finale Freigabe (MODUS = alle)".*

```typescript
AskUserQuestion({ questions: [{ question: "UX-Entscheidungen für FEAT-[X] [Name] vollständig?", header: "Review", options: [
  { label: "Passt – weiter mit nächstem Feature", description: "" },
  { label: "Passt – das war das letzte, weiter zu /red-proto:architect", description: "" },
  { label: "Änderungen nötig", description: "Feedback im Chat" }
], multiSelect: false }] })
```

## Phase 7b: Finalisieren (nur MODUS = einzeln)

Korrekturen übernehmen (falls nötig), `status: approved` + `## Fortschritt → Status: Freigegeben, Aktueller Schritt: UX` setzen. STATUS.md (UX-Spalte ✓).

```bash
git add features/FEAT-[X]-*.md flows/product-flows.md features/STATUS.md 2>/dev/null
git commit -q -m "docs: FEAT-[X] ux design – [Feature Name]" && git push -q
```

Nächstes Feature in QUEUE → Phase 1. Wenn QUEUE leer: abschließen.

---

## Finale Freigabe (nur MODUS = alle)

Alle Features in QUEUE wurden als Draft auf Disk geschrieben. Zeige eine Zusammenfassung:

```
Fertig als Draft:
  ✓ FEAT-02 Nutzerprofil    → features/FEAT-02-nutzerprofil.md
  ✓ FEAT-04 Benachrichtigungen → features/FEAT-04-benachrichtigungen.md
  ✓ FEAT-05 Export          → features/FEAT-05-export.md
```

```typescript
AskUserQuestion({ questions: [{ question: "Alle UX-Designs sehen gut aus?", header: "Finale Freigabe", options: [
  { label: "Alles freigeben und committen", description: "Alle Features auf approved setzen, ein Commit" },
  { label: "Änderungen nötig", description: "Welches Feature – Feedback im Chat" }
], multiSelect: false }] })
```

Nach Freigabe: alle Draft-Dateien auf `status: approved` setzen, `## Fortschritt` aktualisieren, STATUS.md (UX-Spalte ✓) für alle Features. Dann ein einziger Commit:

```bash
git add features/FEAT-*.md flows/product-flows.md features/STATUS.md 2>/dev/null
git commit -q -m "docs: ux design – FEAT-[ID], FEAT-[ID], FEAT-[ID]" && git push -q
```

Abschluss: "Alle UX-Designs freigegeben. Weiter mit `/red-proto:architect`."
