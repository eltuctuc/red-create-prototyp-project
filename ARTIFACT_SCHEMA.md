# Artifact Schema – Product Framework

Alle Agenten des Frameworks lesen aus und schreiben in das Projekt-Wurzelverzeichnis.
Es ist die einzige Source of Truth für den gesamten Workflow.

## Verzeichnisstruktur

```
./
  design-system/                        ← [vom Setup angelegt, inkl. README]
    README.md                           ← Struktur-Empfehlungen (frei wählbar)
    [dein Content]                      ← Tokens/Komponenten/Patterns – Struktur nach Wahl
  [prd.md]                              ← [/red-proto:sparring]
  [test-setup/]                         ← [/red-proto:test-setup]
    personas.md
    hypotheses.md
  [features/]                           ← [/red-proto:requirements]
    STATUS.md                           ← Status-Index aller Features
    [FEAT-X-name.md]                    ← akkumulative Feature-Spec (ux, architect, dev, qa ergänzen)
    [FEAT-X-name/screens/]              ← [/red-proto:preview] optionale Abnahme-Screens
      S-10-*.png
      index.md                          ← Screen-Metadaten (Node-ID, Zustand, Abnahme-Status)
  [flows/]                              ← [/red-proto:flows]
    product-flows.md                    ← Verbindliche Screen-Übersicht + Transition-Tabelle
  [bugs/]                               ← [/red-proto:qa]
    BUG-FEAT1-QA-001.md                 ← Technischer Bug (QA Engineer)
    BUG-FEAT1-UX-001.md                 ← UX-Bug (UX Reviewer)
                                        ← nach Fix umbenannt zu BUG-...-fixed.md (Audit-Trail)
  [context/]                            ← Session-Handoffs und Loop-Logs
    FEAT-1-dev-handoff.md               ← [/red-proto:dev] Handoff für QA-Session (manueller Pfad)
    FEAT-1-loop.log                     ← [/red-proto:dev-qa-loop] Iterations-Log
  [docs/]                               ← [/red-proto:qa, Phase 7]
    produktfähigkeiten.md               ← Was kann das Produkt aktuell?
    releases.md                         ← Release-Historie
  [projektverzeichnis/]                 ← [/red-proto:dev-setup] Projektcode, Name frei wählbar
                                          (Standard: projekt/ – kann aber src/, app/, . usw. sein)
  [project-config.md]                   ← [/red-proto:dev-setup] Tech-Stack, Pfade, Versionierung
```

**Notations-Konvention:**
- `[eckige Klammern]` → wird erst vom genannten Command angelegt. Name oder innere Struktur kann variieren.
- Beim Setup liegen nur `.claude/` und `design-system/` bereit. Alles andere entsteht bei Bedarf.

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

## Screen-Index Format (`./features/FEAT-X-name/screens/index.md`)

Wird von `/red-proto:preview` angelegt, wenn der User vor Dev visuelle Abnahme-Screens durchgehen möchte. Optional – Features ohne `screens/`-Ordner laufen genauso durch die Pipeline.

```markdown
---
status: draft
feature: FEAT-[X]
source: figma | upload | manual
---

# Screens – FEAT-[X]

Quelle: [Figma-File-URL oder "PNG-Upload" oder "manuell abgelegt"]

| Screen-ID | Datei | Zustand | Flow-Schritt | Figma-Node | Status |
|-----------|-------|---------|--------------|------------|--------|
| S-10 | S-10-empty.png | Initial | Einstieg | 123:456 | approved |
| S-11 | S-11-filled.png | Ausgefüllt | Nach Eingabe | 123:457 | approved |
| S-12 | S-12-error.png | Fehler | Bei ungültiger Eingabe | 123:458 | review |
```

**Status-Werte pro Screen:**
- `review` – neu erzeugt, wartet auf User-Abnahme
- `approved` – User hat bestätigt, Dev darf bauen
- `outdated` – Spec oder Design hat sich geändert, Screen muss neu erzeugt werden

**Figma-Node:** nur befüllt wenn Source `figma`. Sonst leer oder `–`.

**Datei-Naming:** `S-NN-kurzbezeichnung.png` – fortlaufende Nummerierung pro Feature.

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
