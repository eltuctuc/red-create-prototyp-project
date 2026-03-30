# Spacing-Tokens

*Ersetze die Beispielwerte durch die Werte aus deinem Design System. Basis-Unit: 4px.*

## Spacing-Scale

| Token-Name  | Wert     | px-Äquivalent | Verwendung                                     |
|-------------|----------|---------------|------------------------------------------------|
| `spacing-0` | `0`      | 0px           | Reset, kein Abstand                            |
| `spacing-px` | `1px`   | 1px           | Trennlinien, Borders                           |
| `spacing-0.5`| `0.125rem`| 2px         | Minimale innere Abstände, Icon-Gaps            |
| `spacing-1` | `0.25rem`| 4px           | Sehr enge Abstände (Badge-Padding, Icon-Gap)   |
| `spacing-1.5`| `0.375rem`| 6px         | Kleine innere Abstände                         |
| `spacing-2` | `0.5rem` | 8px           | Kompaktes Padding (Tags, Chips)                |
| `spacing-3` | `0.75rem`| 12px          | Standard Button-Padding (vertikal)             |
| `spacing-4` | `1rem`   | 16px          | Standard-Abstand, Component-Padding            |
| `spacing-5` | `1.25rem`| 20px          | Etwas mehr Luft                                |
| `spacing-6` | `1.5rem` | 24px          | Card-Padding, Section-Abstände                 |
| `spacing-8` | `2rem`   | 32px          | Größere Abstände zwischen Sections             |
| `spacing-10`| `2.5rem` | 40px          | Starke Trennung, Abstand vor Überschriften     |
| `spacing-12`| `3rem`   | 48px          | Seitenbereich-Abstände                         |
| `spacing-16`| `4rem`   | 64px          | Sehr große Abstände, Hero-Sections             |
| `spacing-20`| `5rem`   | 80px          | Layout-Level-Abstände                          |
| `spacing-24`| `6rem`   | 96px          | Maximale Abstände, große Layouts               |

## Semantische Spacing-Tokens

Alias-Namen für häufige Verwendungskontexte:

| Token-Name               | Referenziert  | Verwendung                             |
|--------------------------|---------------|----------------------------------------|
| `spacing-component-xs`   | `spacing-2`   | Kompaktes Komponenten-Padding          |
| `spacing-component-sm`   | `spacing-3`   | Kleines Komponenten-Padding            |
| `spacing-component-md`   | `spacing-4`   | Standard Komponenten-Padding           |
| `spacing-component-lg`   | `spacing-6`   | Großes Komponenten-Padding             |
| `spacing-gap-xs`         | `spacing-2`   | Enger Gap zwischen Elementen           |
| `spacing-gap-sm`         | `spacing-3`   | Kleiner Gap (Icon + Text)              |
| `spacing-gap-md`         | `spacing-4`   | Standard-Gap zwischen Elementen        |
| `spacing-gap-lg`         | `spacing-6`   | Größerer Gap zwischen Gruppen          |
| `spacing-section-sm`     | `spacing-8`   | Kleiner Abstand zwischen Sections      |
| `spacing-section-md`     | `spacing-12`  | Standard Section-Abstand               |
| `spacing-section-lg`     | `spacing-16`  | Großer Section-Abstand                 |
| `spacing-page-x`         | `spacing-6`   | Horizontaler Seiten-Rand (Mobile)      |
| `spacing-page-x-desktop` | `spacing-8`   | Horizontaler Seiten-Rand (Desktop)     |

## Border-Radius

| Token-Name        | Wert        | Verwendung                              |
|-------------------|-------------|-----------------------------------------|
| `radius-none`     | `0`         | Kein Radius, scharfe Ecken             |
| `radius-sm`       | `0.125rem`  | 2px – sehr kleine Elemente (Badges)     |
| `radius-default`  | `0.25rem`   | 4px – Standard (Inputs, Cards)          |
| `radius-md`       | `0.375rem`  | 6px – Buttons, Dropdowns                |
| `radius-lg`       | `0.5rem`    | 8px – Karten, Modals                    |
| `radius-xl`       | `0.75rem`   | 12px – Große Panels                     |
| `radius-2xl`      | `1rem`      | 16px – Sehr abgerundete Elemente        |
| `radius-full`     | `9999px`    | Runde Elemente (Avatare, Pills, Tags)   |
