# Shadow-Tokens (Elevation-System)

*Ersetze die Beispielwerte durch die Werte aus deinem Design System.*

## Elevation-Skala

| Token-Name      | CSS-Wert                                                                 | Verwendung                                    |
|-----------------|--------------------------------------------------------------------------|-----------------------------------------------|
| `shadow-none`   | `none`                                                                   | Kein Schatten (flache Elemente)               |
| `shadow-xs`     | `0 1px 2px 0 rgb(0 0 0 / 0.05)`                                         | Subtile Abhebung (Inputs im Fokus)            |
| `shadow-sm`     | `0 1px 3px 0 rgb(0 0 0 / 0.10), 0 1px 2px -1px rgb(0 0 0 / 0.10)`     | Buttons, leicht abgehobene Elemente           |
| `shadow-md`     | `0 4px 6px -1px rgb(0 0 0 / 0.10), 0 2px 4px -2px rgb(0 0 0 / 0.10)` | Cards, Karten, Standard-Panels                |
| `shadow-lg`     | `0 10px 15px -3px rgb(0 0 0 / 0.10), 0 4px 6px -4px rgb(0 0 0 / 0.10)`| Dropdowns, Popovers, Floating-Elemente       |
| `shadow-xl`     | `0 20px 25px -5px rgb(0 0 0 / 0.10), 0 8px 10px -6px rgb(0 0 0 / 0.10)`| Modals, Dialoge                              |
| `shadow-2xl`    | `0 25px 50px -12px rgb(0 0 0 / 0.25)`                                   | Sehr prominente Overlay-Elemente              |

## Semantische Shadow-Tokens

| Token-Name           | Referenziert  | Verwendung                           |
|----------------------|---------------|--------------------------------------|
| `shadow-card`        | `shadow-md`   | Standard Card-Elevation              |
| `shadow-dropdown`    | `shadow-lg`   | Dropdown-Menüs, Selects              |
| `shadow-modal`       | `shadow-xl`   | Modals, Dialoge                      |
| `shadow-button`      | `shadow-sm`   | Buttons mit Elevation-Effekt         |
| `shadow-input-focus` | `shadow-xs`   | Input-Fokus-Ring (zusätzlich zu Outline) |
| `shadow-sticky`      | `shadow-md`   | Sticky Header beim Scrollen          |

## Inner Shadows

| Token-Name        | CSS-Wert                                | Verwendung                      |
|-------------------|-----------------------------------------|---------------------------------|
| `shadow-inner`    | `inset 0 2px 4px 0 rgb(0 0 0 / 0.05)` | Inputs, vertiefte Bereiche      |
| `shadow-inner-sm` | `inset 0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtile Vertiefung              |
