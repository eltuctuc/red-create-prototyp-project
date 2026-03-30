# Typografie-Tokens

*Ersetze die Beispielwerte durch die Werte aus deinem Design System.*

## Schriftfamilien

| Token-Name           | Wert                                    | Verwendung                        |
|----------------------|-----------------------------------------|-----------------------------------|
| `font-family-base`   | `'Inter', system-ui, sans-serif`        | Fließtext, Labels, UI-Elemente    |
| `font-family-heading`| `'Inter', system-ui, sans-serif`        | Überschriften (falls abweichend)  |
| `font-family-mono`   | `'JetBrains Mono', 'Courier New', mono` | Code, technische Werte            |

## Schriftgrößen

| Token-Name     | Wert    | px-Äquivalent | Verwendung                           |
|----------------|---------|---------------|--------------------------------------|
| `text-xs`      | `0.75rem` | 12px        | Badges, Captions, Meta-Infos         |
| `text-sm`      | `0.875rem`| 14px        | Labels, Helper-Text, Tabelleninhalt  |
| `text-base`    | `1rem`    | 16px        | Standard Body-Text                   |
| `text-lg`      | `1.125rem`| 18px        | Größerer Body-Text, Intro-Text       |
| `text-xl`      | `1.25rem` | 20px        | Kleine Überschriften (h4, h5)        |
| `text-2xl`     | `1.5rem`  | 24px        | Abschnittsüberschriften (h3)         |
| `text-3xl`     | `1.875rem`| 30px        | Seitenüberschriften (h2)             |
| `text-4xl`     | `2.25rem` | 36px        | Hero-Überschriften (h1)              |
| `text-5xl`     | `3rem`    | 48px        | Display-Text, große Kennzahlen       |

## Schriftgewichte

| Token-Name         | Wert  | Verwendung                             |
|--------------------|-------|----------------------------------------|
| `font-weight-normal` | 400 | Standard Body-Text                     |
| `font-weight-medium` | 500 | Labels, leichte Betonung               |
| `font-weight-semibold`| 600| Buttons, Navigationsitems, Subheadings |
| `font-weight-bold`   | 700 | Überschriften, starke Betonung         |

## Line-Heights

| Token-Name           | Wert  | Verwendung                         |
|----------------------|-------|------------------------------------|
| `leading-tight`      | 1.25  | Überschriften, kurze Labels        |
| `leading-snug`       | 1.375 | Subheadings, Buttons               |
| `leading-normal`     | 1.5   | Standard Body-Text                 |
| `leading-relaxed`    | 1.625 | Langer Fließtext, bessere Lesbarkeit|

## Letter-Spacing

| Token-Name            | Wert       | Verwendung                        |
|-----------------------|------------|-----------------------------------|
| `tracking-tight`      | `-0.025em` | Große Überschriften               |
| `tracking-normal`     | `0`        | Standard                          |
| `tracking-wide`       | `0.025em`  | Buttons, Badges, Uppercase-Labels |
| `tracking-wider`      | `0.05em`   | Sehr kurze Uppercase-Labels       |

## Text-Styles (zusammengesetzte Tokens)

Fertige Kombinationen für häufige Elemente:

| Style-Name       | Größe      | Gewicht | Line-Height   | Verwendung              |
|------------------|------------|---------|---------------|-------------------------|
| `style-h1`       | `text-4xl` | bold    | `leading-tight` | Seitentitel            |
| `style-h2`       | `text-3xl` | bold    | `leading-tight` | Abschnittstittel       |
| `style-h3`       | `text-2xl` | semibold| `leading-snug`  | Card-Titel, Panels     |
| `style-h4`       | `text-xl`  | semibold| `leading-snug`  | Unterabschnitte        |
| `style-body-lg`  | `text-lg`  | normal  | `leading-relaxed`| Intro-Texte           |
| `style-body`     | `text-base`| normal  | `leading-normal` | Standard-Fließtext    |
| `style-body-sm`  | `text-sm`  | normal  | `leading-normal` | Hilfstext, Captions   |
| `style-label`    | `text-sm`  | medium  | `leading-tight`  | Formular-Labels       |
| `style-button`   | `text-sm`  | semibold| `leading-tight`  | Button-Text           |
| `style-caption`  | `text-xs`  | normal  | `leading-normal` | Bildunterschriften    |
| `style-code`     | `text-sm`  | normal  | `leading-normal` | Code-Blöcke           |
