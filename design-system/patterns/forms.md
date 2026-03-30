# Pattern: Formulare

## Grundprinzipien

- Ein Formular = eine Aufgabe (kein Mega-Form mit allem auf einmal)
- Labels immer sichtbar – kein Placeholder als Label-Ersatz
- Fehler inline, direkt bei dem Feld das betroffen ist
- Primäraktion am Ende, Abbrechen links davon (oder als Ghost-Button)

## Formular-Aufbau

```
[Form-Header]              ← Optional: Titel + Kurzbeschreibung was der User tun wird
[Pflichtfeld-Hinweis]      ← "* Pflichtfeld" – einmalig, oben
[Field-Groups]             ← Zusammengehörige Felder gruppiert (optional mit Überschrift)
  [Form-Field]
    [Label] *              ← <label> mit for-Attribut
    [Helper-Text]          ← Optional, kurze Erklärung (max. 1 Satz)
    [Input-Komponente]
    [Error-Message]        ← Nur bei Fehler, aria-live="polite"
[Form-Actions]             ← Primär-Button + Abbrechen/Zurück
```

## Feldbreiten

| Typ              | Breite                   | Beispiel                          |
|------------------|--------------------------|-----------------------------------|
| Voller Block     | 100%                     | Nachricht, Notizen, lange Felder  |
| Halbe Breite     | ~50%                     | Vorname + Nachname nebeneinander  |
| Drittel / Viertel| ~33% / ~25%              | PLZ, Hausnummer                   |
| Auto             | Passt sich Inhalt an     | Kurze Codes, Einheiten            |

Auf Mobile: immer 100% Breite.

## Validierung

### Wann validieren?

| Zeitpunkt       | Empfehlung                                                      |
|-----------------|-----------------------------------------------------------------|
| On Submit       | Immer – zeigt alle Fehler auf einmal nach dem Absenden         |
| On Blur         | Für Format-Validierung (E-Mail, Datum) – nicht für Pflichtfelder|
| On Input        | Nur für Passwort-Stärke oder Zeichenzähler – nicht für Fehler  |

### Fehlermeldungen

- Spezifisch: "Bitte gültige E-Mail-Adresse eingeben (z.B. name@firma.de)"
- Nicht: "Ungültige Eingabe" oder "Fehler"
- Auf Submit: Fokus auf erstes Fehler-Feld springen (scroll + focus)
- Globale Fehler (Server-Fehler): Alert-Banner über dem Formular

## Mehrstufige Formulare (Wizard)

- Fortschrittsanzeige: Step-Indicator oben (1 von 3, 2 von 3 ...)
- Jeder Step: eigene Validierung vor dem Weiter-Klick
- Navigation: Zurück-Button behält Eingaben aus vorherigen Steps
- Letzter Step: Zusammenfassung vor dem finalen Absenden (optional)

## Spezielle Felder

### Passwort-Felder

- Immer Toggle für Sichtbarkeit (Eye-Icon rechts im Feld)
- Anforderungen: sichtbar als Checkliste (nicht erst nach Fehler)
- Stärken-Indikator: Progressbar, nicht nur Text

### File Upload

- Drag & Drop + Klick-Alternative
- Erlaubte Dateitypen und Maximalgröße anzeigen (nicht erst als Fehler)
- Hochgeladene Dateien: Dateiname + Lösch-Button sichtbar
- Fortschrittsbalken bei größeren Uploads

### Datum / Uhrzeit

- DatePicker-Komponente, kein manuelles Texteingabe-Datum-Format
- Wenn Range: Start + Ende visuell als zusammengehörig kennzeichnen
- Vergangene/gesperrte Daten: im Picker disabled, nicht nur als Validierungsfehler

## Formular-Aktionen

```
[Abbrechen/Zurück]    [Primäraktion]
    Ghost-Button           Primary-Button
```

- Abbrechen links, Primäraktion rechts (westliche Konvention)
- Abbrechen: fragt nach ungespeicherten Änderungen (Dialog) – wenn Daten verloren gehen
- Primär-Button: Loading-Zustand beim Absenden, kein Doppelklick möglich
- Destruktive Aktionen (Löschen, Unwiderrufliches): Danger-Button + Bestätigungsdialog
