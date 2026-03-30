# Pattern: Datenanzeige

## Tabellen

### Verwendung

Für strukturierte, vergleichbare Daten mit mehreren Attributen pro Zeile. Nicht für einfache Listen oder Einzel-Werte.

### Aufbau

```
[Table-Toolbar]         ← Optional: Suche, Filter, Bulk-Aktionen, Spalten-Konfiguration
[Table-Header]          ← Sticky bei langen Tabellen; sortierbare Spalten mit Icon
[Table-Body]
  [Table-Row]           ← Hover-Highlight; selektierbar (Checkbox links)
    [Table-Cell]
[Table-Footer]          ← Pagination oder "Alle X Einträge laden"
```

### Regeln

- Spalten-Header: `style-label`, `color-text-secondary`, sortierbar mit Up/Down-Icon
- Zahlen: rechtsbündig, gleiche Dezimalstellen pro Spalte
- Text: linksbündig
- Status/Badges: zentriert (optional)
- Leerer Zustand: Empty-State Pattern (nicht einfach leere Tabelle)
- Mobile: Horizontales Scrollen oder Card-Ansicht als Alternative
- Max. 6–8 Spalten sichtbar – mehr → Spalten ausblendbar

### Zeilenaktionen

- Hover-Aktionen: erscheinen rechts in der Zeile beim Hover (Edit, Delete)
- Overflow-Menu: bei mehr als 2 Aktionen
- Bulk-Aktionen: erscheinen in Toolbar wenn Zeilen selektiert

---

## Listen

### Einfache Liste

Für Elemente mit wenigen Attributen, keine komplexe Sortierung nötig.

```
[List-Item]
  [Leading: Icon/Avatar/Thumbnail]   ← Optional
  [Content]
    [Primary Text]                   ← style-body, color-text-primary
    [Secondary Text]                 ← style-body-sm, color-text-secondary
  [Trailing: Action/Meta/Badge]      ← Optional
```

Trennlinien: `1px color-border-default` zwischen Items (nicht unter letztem Item).

### Geordnete Liste / Rankings

- Nummerierung: konsistent ausgerichtet (rechtsbündig, gleiche Breite)
- Hervorhebung: Top 3 mit Badge oder Icon

---

## Badges / Tags

### Verwendung

Kurze Status-Informationen, Kategorisierungen, Zähler.

### Varianten

| Variante    | Verwendung                              | Farbe                      |
|-------------|------------------------------------------|-----------------------------|
| `success`   | Aktiv, Abgeschlossen, Online            | `color-success-*`           |
| `warning`   | Ausstehend, In Review, Achtung          | `color-warning-*`           |
| `error`     | Fehler, Abgelehnt, Kritisch             | `color-error-*`             |
| `info`      | Neu, Beta, Hinweis                      | `color-primary-*`           |
| `neutral`   | Archiviert, Inaktiv, Standard           | `color-neutral-*`           |

### Regeln

- Maximale Zeichenzahl: 20–25 Zeichen – mehr → Tooltip mit Volltext
- Nicht klickbar (wenn klickbar → Filter-Tag / Chip)
- Dot-Badge: Nur Farbe als Status-Indikator (immer mit sichtbarem Text-Label für Accessibility)
- Zähler-Badge: Auf Icons/Avatare für ungelesene Nachrichten etc.

---

## Statistik / Kennzahlen (Stat Cards)

### Aufbau

```
[Label / Beschreibung]    ← style-body-sm, color-text-secondary
[Hauptwert]               ← text-3xl oder text-4xl, font-weight-bold
[Vergleichswert / Trend]  ← Optional: +12% (grün) oder -3% (rot) + Icon
```

### Regeln

- Trend-Indikatoren: Farbe PLUS Icon (nicht nur Farbe)
- Einheiten klar kennzeichnen: €, %, Stk., ms
- Sehr große Zahlen formatieren: 1.234.567 oder 1,2M
- Loading: Skeleton über dem gesamten Stat-Block

---

## Avatar / Nutzerbilder

### Varianten

| Variante   | Inhalt                                          |
|------------|-------------------------------------------------|
| Bild       | Nutzerfoto (immer mit Fallback)                 |
| Initials   | Fallback: Initialen auf Farbhintergrund         |
| Icon       | Generisches User-Icon (wenn kein Name verfügbar)|

### Größen

| Größe | Durchmesser | Verwendung                         |
|-------|-------------|------------------------------------|
| `xs`  | 24px        | In Tabellenzellen, kompakte Listen |
| `sm`  | 32px        | Kommentar-Avatare, Chips           |
| `md`  | 40px        | Standard Avatar                    |
| `lg`  | 48px        | Profil-Header                      |
| `xl`  | 64px        | Profilseite, Detailansicht         |
| `2xl` | 96px        | Große Profilseite                  |

### Regeln

- Border-Radius: `radius-full` (rund)
- Fallback-Initials: 1–2 Buchstaben, konsistente Farb-Zuweisung (z.B. Hash des Namens)
- Bild: `alt`-Attribut = Nutzername
- Avatar-Group (mehrere): überlappend, max. 4 + "+N" Anzeige
