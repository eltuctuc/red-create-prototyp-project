# Pattern: Feedback & Status-Kommunikation

## Überblick

| Pattern       | Wann einsetzen                                     | Persistent? | Unterbrechend? |
|---------------|----------------------------------------------------|-------------|----------------|
| Toast/Snackbar| Kurze Bestätigung, nicht kritisch                 | Nein (3–5s) | Nein           |
| Alert-Banner  | Wichtige Info auf Page-Ebene, kein sofortiges Handeln | Ja (manuell) | Nein        |
| Modal         | Bestätigung nötig, kritische Entscheidung          | Ja          | Ja             |
| Inline-Error  | Formularfehler, kontextbezogene Fehler             | Ja          | Nein           |
| Empty State   | Kein Inhalt vorhanden (noch nicht oder nach Filter)| Ja          | Nein           |
| Skeleton      | Inhalt lädt, Struktur bekannt                      | Nein        | Nein           |
| Spinner       | Kurze unbekannte Ladedauer                         | Nein        | Optional       |

---

## Toast / Snackbar

### Verwendung

Nach erfolgreichen Aktionen (Speichern, Löschen, Versenden) die keine weitere Bestätigung brauchen.

### Aufbau

```
[Icon]  [Message]  [Action (optional)]  [Close]
```

### Regeln

- Position: Unten rechts (Desktop), unten zentriert (Mobile)
- Autohide: 4–5 Sekunden bei Info/Success, Fehler-Toasts manuell schließen
- Max. 3 gleichzeitig sichtbar – ältere schieben nach oben
- Varianten: `success`, `error`, `warning`, `info`
- Klickbare Aktion: max. 1 (z.B. "Rückgängig"), kurzer Text

### Hintergrundfarben

| Variante  | Hintergrund         | Icon-Farbe          |
|-----------|---------------------|---------------------|
| success   | `color-neutral-900` | `color-success-500` |
| error     | `color-error-700`   | `color-neutral-0`   |
| warning   | `color-warning-500` | `color-neutral-900` |
| info      | `color-neutral-900` | `color-primary-300` |

---

## Alert-Banner

### Verwendung

Für wichtige Informationen auf Seiten-Ebene: Systemwarnungen, Hinweise die für alle Nutzer relevant sind, Bestätigungen nach Redirect.

### Aufbau

```
[Icon]  [Titel (optional)]  [Beschreibung]  [Aktion (optional)]  [Close (optional)]
```

### Regeln

- Oben auf der Seite, direkt unter dem Header
- Nicht zu viele gleichzeitig – max. 1 kritisches + 1 informationales Banner
- Varianten: `success`, `error`, `warning`, `info`
- Schließbar (X-Button) außer bei kritischen Systemmeldungen

---

## Modal / Dialog

### Verwendung

- Bestätigungen für irreversible Aktionen (Löschen, Publishen)
- Komplexere Formulare die aus dem Kontext herausgelöst werden müssen
- Lightboxes / Medien-Ansichten

### Regeln

- Fokus: wird beim Öffnen in das Modal gesetzt (erstes interaktives Element)
- Focus-Trap: Tab navigiert nur innerhalb des Modals
- Schließen: ESC-Taste, X-Button, optional Klick außerhalb (nicht bei kritischen Modals)
- Beim Schließen: Fokus kehrt zum auslösenden Element zurück
- Backdrop: semi-transparentes Overlay (`rgba(0,0,0,0.5)`)
- Max-Breite: 480px (small), 640px (default), 800px (large)
- Mobile: Drawer von unten (full width, 90vh max)

### Bestätigungs-Modals (Danger)

```
[Titel: "X löschen?"]
[Erklärung: "Dies kann nicht rückgängig gemacht werden."]
[Abbrechen]  [Löschen]
  Secondary    Danger
```

---

## Empty State

### Verwendung

Wenn ein Listenbereich / Tabelle / Dashboard-Widget keine Inhalte hat – entweder weil noch nichts erstellt wurde oder der aktuelle Filter keine Treffer liefert.

### Aufbau

```
[Illustration oder Icon]
[Titel: "Noch keine [Objekte]"]
[Beschreibung: Was der Nutzer tun kann]
[Primäraktion: z.B. "Ersten X erstellen"]
```

### Regeln

- Immer eine mögliche Nächste-Aktion anbieten (wenn möglich)
- Bei leerem Filter: "Filter zurücksetzen" als Aktion
- Icon/Illustration: passend zum Kontext, nicht generisch
- Kein "Keine Daten gefunden" – erkläre WAS fehlt und WAS der User tun kann

---

## Skeleton Loader

### Verwendung

Wenn die Struktur des Inhalts bekannt ist und das Laden länger als 300ms dauert.

### Regeln

- Zeigt die Form des zukünftigen Inhalts als graue Platzhalter-Blöcke
- Animierter Shimmer-Effekt (gradient sweep) – aber `prefers-reduced-motion` beachten
- Für Text: Blöcke in variierender Breite (nicht alle gleich lang)
- Für Cards: Card-Umriss mit Platzhaltern für Bild, Titel, Text
- Kein Skeleton länger als 10 Sekunden – danach Error State

---

## Ladezustand (Spinner / Progress)

| Typ             | Wann                                              |
|-----------------|---------------------------------------------------|
| Inline Spinner  | Button-Loading, kurze In-Component Aktionen       |
| Page Spinner    | Seitenübergreifende Ladeoperationen (selten)      |
| Progress Bar    | Upload, Prozesse mit bekannter Dauer              |
| Skeleton        | Inhalt lädt, Struktur bekannt                     |

- Page Spinner: Overlay mit Backdrop, zentrierter Spinner – NUR wenn wirklich nötig
- Spinner-Größen: 16px (inline), 24px (component), 40px (page-level)
