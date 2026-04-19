# Artifact Schema – Product Framework

Alle Agenten des Frameworks lesen aus und schreiben in das Projekt-Wurzelverzeichnis.
Es ist die einzige Source of Truth für den gesamten Workflow.

## Verzeichnisstruktur

```
./
  prd.md                          ← [/red-proto:sparring] Product Requirements Document
  project-config.md               ← [/red-proto:dev-setup] Tech-Stack, Projektstruktur, Git/GitHub
  design-system/                  ← Verbindliche Design-Vorgaben – wird von /red-proto:ux, /red-proto:dev, ux-reviewer gelesen
    README.md                     ← Ausfüllanleitung
    tokens/
      colors.md                   ← Farb-Tokens (Primär, Sekundär, Semantic, Neutral)
      typography.md               ← Schriften, Größen, Gewichte, Line-Heights
      spacing.md                  ← Spacing-Scale und Border-Radius
      shadows.md                  ← Elevation-System
      motion.md                   ← Transitions, Durations, Easing (optional)
    components/
      [name].md                   ← Ein File pro Komponente (Varianten, Zustände, Specs)
    patterns/
      navigation.md               ← Header, Sidebar, Breadcrumb, Tabs
      forms.md                    ← Formular-Aufbau, Validation, Fehlermeldungen
      feedback.md                 ← Toasts, Modals, Empty States, Skeleton
      data-display.md             ← Tabellen, Listen, Badges, Avatare
    screens/
      README.md                   ← Anleitung für Screen-Exports
      [flow-name]/                ← Figma-Exports nach Flow gruppiert
        [screen].png
  flows/
    product-flows.md              ← [/flows] Verbindliche Screen-Übersicht + Transition-Tabelle
  test-setup/
    personas.md                   ← [/red-proto:test-setup]
    hypotheses.md                 ← [/red-proto:test-setup]
  features/
    FEAT-1-feature-name.md        ← [alle Agenten ergänzen dieses File]
    FEAT-2-feature-name.md
    ...
  bugs/                           ← [/red-proto:qa] Ein File pro Bug – nach Fix umbenannt zu BUG-...-fixed.md (Audit-Trail)
    BUG-FEAT1-QA-001.md           ← Technischer Bug (QA Engineer)
    BUG-FEAT1-UX-001.md           ← UX-Bug (UX Reviewer)
    ...
  docs/
    produktfähigkeiten.md         ← [/red-proto:qa] Was kann das Produkt aktuell? (pro Feature ergänzt)
    releases.md                   ← [/red-proto:qa] Release-Historie: was wann integriert, welche Bugs behoben
  [codeverzeichnis]/              ← [/red-proto:dev] Projektcode – Pfad steht in project-config.md → "Codeverzeichnis"
                                    Standard: projekt/ – kann aber src/, . oder ein anderer Pfad sein
```

## Feature-File Format

Jeder Agent ergänzt seinen Abschnitt. Bestehende Abschnitte werden nie überschrieben.

```markdown
# FEAT-X: Feature Name

## Status
Aktueller Schritt: [Spec | UX | Tech | Dev | QA | Done | REJECTED | ABANDONED]

*(REJECTED = Entscheidung gegen Umsetzung; ABANDONED = Arbeit begonnen aber abgebrochen)*

## Abhängigkeiten
- Benötigt: FEAT-Y (Name) – Grund

---

## 1. Feature Spec
*Ausgefüllt von: /red-proto:requirements**

### User Stories
- Als [Rolle] möchte ich [Aktion], um [Ziel]

### Acceptance Criteria
- [ ] Konkret, testbar, keine Vagheit

### Edge Cases
- Was passiert wenn ...?

### Definitionen (IEEE/IREB)
- **[Begriff]:** [Definition]

---

## 2. UX Entscheidungen
*Ausgefüllt von: /red-proto:ux**

### User Flow
### Interaktionsmuster
### Eingesetzte Komponenten
| Komponente | DS-Status | Quelle |
|------------|-----------|--------|
### Screen Transitions (verbindlich)
| Von | Trigger | Wohin | Bedingung |
|-----|---------|-------|-----------|
### DS-Status dieser Implementierung
- Konforme Komponenten:
- Neue Komponenten (Tokens-Build, genehmigt):
- Bewusste Abweichungen (Hypothesentest):

---

## 3. Technisches Design
*Ausgefüllt von: /red-proto:architect**

### Component-Struktur
### Data Model
### Tech-Entscheidungen
### Security-Anforderungen
### Test-Setup

---

## 4. Implementierung
*Ausgefüllt von: /red-proto:dev**

### Implementierte Dateien
### Offene Punkte

---

## 5. QA Ergebnisse
*Ausgefüllt von: /red-proto:qa**

### Test-Ergebnisse
### Bugs
### Production-Ready: ✅ / ❌
```

## Bug-File Format

Naming-Schema:
- Offen: `BUG-FEAT[X]-QA-[NNN].md` (technisch) oder `BUG-FEAT[X]-UX-[NNN].md` (UX)
- Behoben: `BUG-FEAT[X]-QA-[NNN]-fixed.md` / `BUG-FEAT[X]-UX-[NNN]-fixed.md`

→ Trennung QA/UX verhindert Datei-Konflikte bei parallelem Schreiben.
→ `-fixed` Suffix statt Löschen erhält den Audit-Trail.

```markdown
# BUG-FEAT[X]-[QA|UX]-[NNN]: [Kurztitel]

- **Feature:** FEAT-[X] – [Feature Name]
- **Severity:** Critical | High | Medium | Low
- **Bereich:** Functional | Security | A11y | Performance | UX | Flow | Konsistenz
- **Gefunden von:** QA Engineer | UX Reviewer
- **Status:** Open | Fixed
- **Behoben am:** [Datum – nur bei Status: Fixed]
- **Fix:** [Kurzbeschreibung was geändert wurde – nur bei Status: Fixed]

## Steps to Reproduce
1. ...
2. ...
3. Expected: [Was sollte passieren]
4. Actual: [Was passiert stattdessen]

## Priority
Fix now | Fix before release | Nice-to-have
```

**Nach Fix:** Status auf `Fixed` setzen, `Behoben am` und `Fix` ausfüllen, Datei umbenennen zu `BUG-FEAT[X]-[TYPE]-[NNN]-fixed.md`. Nicht löschen.

---

## Capabilities-Doc Format (`./docs/produktfähigkeiten.md`)

```markdown
# Produkt Capabilities

*Zuletzt aktualisiert: [Datum]*

Übersicht aller produktiven Features – was das Produkt aktuell kann.

## [Feature Name] *(FEAT-[X], seit [Datum])*
[2–4 Sätze: Was kann der User damit tun? Welchen Mehrwert bringt es?]

## [Feature Name] *(FEAT-[X], seit [Datum])*
...
```

Jeder `/red-proto:qa`-Durchlauf ergänzt ein neues Feature-Kapitel, wenn Production-Ready: ✅.

---

## Release-Doc Format (`./docs/releases.md`)

```markdown
# Release History

## [Version / Datum]
### Neue Features
- **FEAT-[X] – [Name]:** [Ein-Satz-Beschreibung]

### Bug Fixes
- **BUG-FEAT[X]-[NNN]:** [Beschreibung des Fixes] *(Severity: [X])*

### Breaking Changes
- (falls vorhanden)
```

Einträge werden chronologisch oben eingefügt (neueste zuerst).

---

## Flows Format (`./flows/product-flows.md`)

```markdown
# Product Flows

## Screens
| Screen-ID | Screen-Name | Route | Feature | Typ |
|-----------|-------------|-------|---------|-----|

## Einstiegspunkte
| Kontext | Einstiegs-Screen | Bedingung |
|---------|-----------------|-----------|

## Screen Transitions
| Von | Trigger | Wohin | Bedingung | Feature |
|-----|---------|-------|-----------|---------|

## Offene Transitions
| Gemeldet von | Von Screen | Situation | Status |
|--------------|------------|-----------|--------|
```

Einträge werden nur ergänzt, nie ohne Bestätigung geändert.
`/red-proto:flows` kann jederzeit erneut aufgerufen werden um neue Features zu integrieren oder Lücken zu schließen.

---

## PRD Format (`./prd.md`)

```markdown
# Product Requirements Document
## Vision
## Zielgruppe
## Kernproblem
## Scope (In)
## Out-of-Scope
## Erfolgskriterien
## Offene Fragen
```

## Project Config (`./project-config.md`)

```markdown
# Projekt-Konfiguration
## Tech-Stack
- Prototyp-Typ: ...
- Frontend: ...
- Backend: ...

## Team-Setup
- Developer aufgeteilt (Frontend/Backend): Ja/Nein/Später

## Verzeichnisse
- Codeverzeichnis: projekt/   ← Anpassen falls Code woanders liegt (src/, . etc.)

## Projektstruktur
*(Von allen Agents als Pfad-Referenz genutzt – befüllt von /red-proto:sparring)*
- Komponenten: src/components/
- Seiten/Views: src/app/
- API-Routen: src/app/api/
- Datenbank/Schema: prisma/
- State/Stores: src/stores/

## Git / GitHub
- Git initialisiert: Ja/Nein
- GitHub-Repository: [URL oder "Nein, nur lokal"]
- Repository-Inhalt: Nur Code | Alles

## Namenskonvention
- Feature-IDs: FEAT-X
- Nächste freie ID: FEAT-1
```
