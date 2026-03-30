# Button

## Beschreibung
Löst eine Aktion aus. Buttons sind die primären interaktiven Elemente für Nutzeraktionen – Formulare absenden, Dialoge bestätigen, Prozesse starten.

## Varianten

| Variante    | Verwendung                                                   |
|-------------|--------------------------------------------------------------|
| `primary`   | Primäraktion auf einem Screen – max. 1 pro sichtbarem Bereich |
| `secondary` | Sekundäraktion, Alternative zur primären Aktion             |
| `ghost`     | Tertiäraktion, wenig visuelles Gewicht (z.B. "Abbrechen")   |
| `danger`    | Destruktive Aktionen (Löschen, Unwiderrufliches)            |
| `link`      | Aktion als Link gestylt – nur für Navigation innerhalb von Text |

## Zustände

| Zustand    | Verhalten                                                      |
|------------|----------------------------------------------------------------|
| `default`  | Ruhezustand                                                    |
| `hover`    | Leichte Verdunkelung des Hintergrunds                         |
| `focus`    | Sichtbarer Focus-Ring (`color-border-focus`, 2px, 2px Offset) |
| `active`   | Stärkere Verdunkelung beim Klick                              |
| `disabled` | Reduzierte Opacity (0.5), kein Cursor-Pointer, nicht klickbar |
| `loading`  | Spinner + Text oder nur Spinner (Label bleibt sichtbar)       |

## Größen

| Größe | Padding (h/v)           | Font-Size    | Height  | Icon-Size |
|-------|-------------------------|--------------|---------|-----------|
| `sm`  | `spacing-2` / `spacing-3` | `text-sm`  | 32px    | 14px      |
| `md`  | `spacing-3` / `spacing-4` | `text-sm`  | 40px    | 16px      |
| `lg`  | `spacing-4` / `spacing-6` | `text-base`| 48px    | 18px      |

## Visuelle Specs – Primary

| Eigenschaft      | Default                   | Hover                      | Active                     | Disabled                  |
|------------------|---------------------------|----------------------------|----------------------------|---------------------------|
| Hintergrund      | `color-primary-500`       | `color-primary-600`        | `color-primary-700`        | `color-primary-300`       |
| Text             | `color-text-on-primary`   | `color-text-on-primary`    | `color-text-on-primary`    | `color-text-on-primary`   |
| Border           | keine                     | keine                      | keine                      | keine                     |
| Border-Radius    | `radius-md`               | `radius-md`                | `radius-md`                | `radius-md`               |

## Visuelle Specs – Secondary

| Eigenschaft      | Default                   | Hover                      | Disabled                   |
|------------------|---------------------------|----------------------------|----------------------------|
| Hintergrund      | `color-neutral-0`         | `color-neutral-100`        | `color-neutral-50`         |
| Text             | `color-neutral-800`       | `color-neutral-900`        | `color-neutral-400`        |
| Border           | `1px` `color-border-default` | `1px` `color-neutral-400` | `1px` `color-neutral-200` |

## Icons

- Icons sind optional, immer links vom Text oder zentriert (icon-only)
- Icon-only Buttons: quadratisch, immer mit `aria-label`
- Gap zwischen Icon und Text: `spacing-gap-sm`

## Regeln

- Beschriftungen sind aktiv formuliert: "Speichern", "Bestellung absenden" – nicht "OK" oder "Submit"
- Max. 1 Primary Button pro sichtbarem Kontext
- Danger-Buttons erst nach Bestätigung (Modal oder Inline-Confirm)
- Loading-Zustand bei async Aktionen – kein doppeltes Absenden ermöglichen

## Nicht verwenden wenn

- Die Aktion zu einer anderen Seite navigiert → `<a>`-Tag oder Link-Komponente
- Es mehr als 4 Optionen gibt → Dropdown oder Segment-Control
