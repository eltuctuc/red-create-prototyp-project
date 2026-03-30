# Card

## Beschreibung
Container für zusammengehörige Inhalte. Cards gruppieren verwandte Informationen und Aktionen zu einer logischen Einheit. Sie können statisch (reine Anzeige) oder interaktiv (klickbar, z.B. zu Detailansicht) sein.

## Varianten

| Variante      | Verwendung                                                       |
|---------------|------------------------------------------------------------------|
| `default`     | Statische Inhalts-Card (kein Hover-Effekt)                      |
| `interactive` | Klickbare Card (gesamte Card ist Klickziel) mit Hover-Effekt    |
| `compact`     | Reduziertes Padding, für Listen mit vielen Cards                |
| `flat`        | Kein Schatten, nur Border – für Inhalte auf farbigem Hintergrund |
| `highlight`   | Mit farbiger Leiste oder farbigem Hintergrund-Tint (Betonung)   |

## Aufbau (Reihenfolge im DOM)

```
[Card-Wrapper]
  [Card-Header]          ← Optional: Titel + Subtitle + Header-Aktion
    [Card-Media]         ← Optional: Bild/Icon-Bereich oben
  [Card-Body]            ← Pflicht: Hauptinhalt
  [Card-Footer]          ← Optional: Aktionen (Buttons, Links)
```

## Zustände (nur bei Variant: interactive)

| Zustand  | Verhalten                                                        |
|----------|------------------------------------------------------------------|
| `default`| Ruhezustand                                                      |
| `hover`  | Leicht erhöhter Schatten, leichter Hintergrund-Tint              |
| `focus`  | Sichtbarer Focus-Ring (Keyboard-Navigation)                      |
| `active` | Leichter Scale-Down (0.99) oder verstärkter Schatten             |

## Visuelle Specs – Default

| Eigenschaft    | Wert                        |
|----------------|-----------------------------|
| Hintergrund    | `color-bg-surface`          |
| Border         | `1px color-border-default`  |
| Border-Radius  | `radius-lg`                 |
| Schatten       | `shadow-card`               |
| Padding Body   | `spacing-6`                 |
| Padding Compact| `spacing-4`                 |

## Visuelle Specs – Interactive (zusätzlich)

| Eigenschaft       | Hover                        |
|-------------------|------------------------------|
| Schatten          | `shadow-lg`                  |
| Hintergrund       | leichter `color-primary-50`  |
| Transition        | `transition-shadow`          |

## Card-Header

- Titel: `style-h3` oder `style-h4` je nach Kontext
- Subtitle: `style-body-sm`, Farbe `color-text-secondary`
- Header-Aktion: Icon-Button rechts, oder Overflow-Menu

## Card-Footer

- Trennlinie oben: `1px color-border-default`
- Padding: `spacing-4` `spacing-6`
- Layout: Flex, Aktionen rechts-ausgerichtet
- Max. 2 Aktionen – primary + secondary Button

## Regeln

- Interaktive Cards haben genau EINEN Klickbereich (die gesamte Card) – keine verschachtelten Links oder Buttons innerhalb einer klickbaren Card (Ausnahme: Overflow-Menu)
- Wenn mehrere Aktionen nötig sind → Aktionen im Footer, Card selbst nicht klickbar
- Bilder in Cards: immer mit alt-Text, feste Höhe (aspect-ratio), object-fit: cover

## Nicht verwenden wenn

- Für einzelne Kennzahlen → Stat-Komponente
- Für Formular-Felder → Form-Group
- Für Listen-Einträge mit vielen Zeilen → List-Item
