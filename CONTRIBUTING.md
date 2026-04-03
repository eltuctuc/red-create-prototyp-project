# Contributing to red · Create Prototyp Project

Danke, dass du zu diesem Framework beitragen möchtest!

## Wie du beitragen kannst

### Bugs melden

Nutze das [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) und beschreibe:
- Welchen Command du ausgeführt hast
- Was du erwartet hast
- Was stattdessen passiert ist
- Deine Claude Code Version

### Feature-Ideen einreichen

Nutze das [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md). Neue Commands oder Erweiterungen bestehender Commands sind willkommen.

### Commands verbessern

1. Fork das Repository
2. Erstelle einen Branch: `git checkout -b improve/command-name`
3. Ändere die entsprechende `.md`-Datei in `commands/`
4. Teste den Command in einem echten Projekt
5. Öffne einen Pull Request mit dem [PR Template](.github/pull_request_template.md)

## Richtlinien für Commands

- Jeder Command muss eigenständig funktionieren
- Outputs müssen maschinenlesbar sein (andere Commands bauen darauf auf)
- Deutsche Sprache für User-facing Text, Englisch für technische Artefakte
- Kein unnötiger Kontext – Commands lesen vorhandene Artefakte, sie wiederholen sie nicht

## Fragen?

Öffne ein Issue mit dem Label `question`.
