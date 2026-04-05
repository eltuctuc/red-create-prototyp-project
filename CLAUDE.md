# Contributor Guidelines für red · proto

Diese Datei gilt für alle, die aktiv am Framework arbeiten.
Endnutzer des Frameworks sehen diese Datei nicht.

---

## Änderungen schrittweise durchführen

Bei Aufgaben mit mehreren Änderungen (mehrere Dateien, mehrere Schritte, commits, pushes) nicht alles eigenständig in einem Durchgang durchziehen:

1. Plan kurz skizzieren und Bestätigung einholen
2. Ersten Schritt umsetzen, Ergebnis zeigen
3. Auf Freigabe warten bevor der nächste Schritt folgt

Gilt besonders wenn Commits und Pushes involviert sind – einmal gepusht ist schwer rückgängig zu machen.

---

## Vorschläge nicht direkt umsetzen
Wenn "mach Vorschläge" oder ähnliches sagt wird, soll nur eine Liste zur Auswahl erstellt werden – keine direkte Umsetzung.


## Changelog und Release Notes

### Pflicht bei jedem Push

Kein Push ohne Changelog-Eintrag. Reihenfolge immer:
1. CHANGELOG.md aktualisieren
2. Version in package.json erhöhen (patch / minor / major)
3. Commit → Tag → Push + Tags pushen

### Wie ein guter Eintrag aussieht

**Struktur pro Version:**
- Datum immer aus `git log --date=short` – nie schätzen oder erfinden
- Optionaler Einstiegssatz mit Charakter (1 Satz, der den Release trifft)
- `### Neue Features` – nach Nutzerbedeutung sortiert, wichtigstes zuerst
- `### Fixes` – nur wenn vorhanden, immer mit Konsequenz für den Nutzer
- `### Verbesserungen` – für alles andere (Sprache, Performance, Struktur)

**Sprache:**
- Kein technischer Jargon – nicht "bin entry path resolution" sondern "der Pfad zum Installationsskript"
- Jedes Bullet erklärt was der Nutzer davon hat, nicht was technisch geändert wurde
- Bei Bugs die den Nutzer wirklich betroffen haben: kurze Entschuldigung nicht weglassen
- Unterhaltsamer Ton erlaubt – aber Information vor Unterhaltung

**Was nicht erlaubt ist:**
- "Bugfixes und kleine Verbesserungen" als Eintrag – das hilft niemandem
- Commit-Messages 1:1 übernehmen
- Daten erfinden
