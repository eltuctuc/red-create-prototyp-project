# Konflikt-Check: Design-System ↔ UI-Library

Dieses Template wird von mehreren Commands und Agents als „Phase 0" ausgeführt – **vor** jeder inhaltlichen Arbeit.

Das Framework erlaubt entweder ein befülltes Design-System **oder** eine gestylte UI-Library, nie beides. Dieser Check stellt sicher, dass der Zustand sauber ist. Er ist strukturagnostisch – funktioniert unabhängig davon, wie der User `design-system/` intern organisiert hat.

## Prüfung

```bash
UI_LIB=$(grep -i "^- UI-Library:" project-config.md 2>/dev/null | sed 's/.*: *//' | head -1)
DS_FILES=$(find design-system -type f -name "*.md" ! -name "README.md" 2>/dev/null | wc -l | xargs)
```

## Logik

Konflikt liegt vor, wenn **beide** Bedingungen zutreffen:
1. `UI_LIB` ist nicht leer und nicht `keine` (also eine echte Library wie `shadcn/ui`, `MUI`, `Chakra`, `Vuetify`, …)
2. `DS_FILES` ist größer als 0

Bei Konflikt: **harter Stop**. Keine Rückfrage-Entscheidung im Chat – das Framework löst den Konflikt nicht automatisch, weil beide Optionen Datei-Operationen ausserhalb der Agent-Arbeit erfordern.

## Stop-Meldung

Gib exakt diese Meldung aus und beende den Command/Agent:

```
⛔  STOP: DS/UI-Library-Konflikt

    project-config.md sagt `UI-Library: [Name]`, aber design-system/
    enthält [N] Inhalts-Dateien (außer README). Das Framework erlaubt
    nur eins von beidem.

    Löse den Konflikt, dann starte diesen Command neu:

    a) DS nutzen       → in project-config.md `UI-Library: keine` setzen,
                          dann /red-proto:dev-setup neu starten
                          (damit Tokens ins Projekt transportiert werden)

    b) Library nutzen  → die DS-Dateien (außer design-system/README.md) entfernen

    Ausführliche Übersicht: /red-proto:workflow
```

## Kein Zustand zu persistieren

Die Entscheidung zwischen a und b **ist** der Projektzustand nach der User-Aktion:

- Option a ausgeführt → `UI-Library: keine` in project-config → Bedingung 1 erfüllt nicht mehr → Check feuert nicht mehr
- Option b ausgeführt → DS hat keine Inhalts-Dateien → Bedingung 2 erfüllt nicht mehr → Check feuert nicht mehr

Deshalb gibt es **keine** Datei, die „die User-Entscheidung" speichert. Der Filesystem-Zustand ist die Wahrheit. Wenn der User später erneut in den Konflikt läuft (z.B. durch Git-Revert, versehentliche DS-Befüllung nach Library-Setup), feuert der Check wieder – richtig so, weil der Zustand erneut inkonsistent ist.

## Ausnahme

Headless-Primitives ohne eigenes Styling (Radix Primitives, React Aria, Headless UI) zählen **nicht** als UI-Library. Sie sind Infrastruktur und dürfen parallel zu einem befüllten DS existieren. Wenn solche Bausteine Teil des Stacks sind, sollten sie in `project-config.md` **nicht** im `UI-Library:`-Feld auftauchen – sondern weiter unten in der Projektstruktur dokumentiert werden (falls überhaupt).
