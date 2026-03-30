# Input / Textfeld

## Beschreibung
Einzeiliges Texteingabefeld. Verwendet für kurze Freitext-Eingaben: Name, E-Mail, Suche, Passwort, Zahlen.

## Varianten

| Variante    | Verwendung                                           |
|-------------|------------------------------------------------------|
| `default`   | Standardmäßiges Textfeld                             |
| `search`    | Mit Lupe-Icon links, optional Clear-Button rechts   |
| `password`  | Maskierter Text, Toggle für Sichtbarkeit             |
| `number`    | Nur numerische Eingabe, optional Stepper-Buttons     |

## Zustände

| Zustand    | Verhalten                                                              |
|------------|------------------------------------------------------------------------|
| `default`  | Ruhezustand – Border: `color-border-default`                          |
| `focus`    | Border: `color-border-focus` (2px), kein Box-Shadow                   |
| `filled`   | Hat Inhalt – kein visueller Unterschied außer Content                  |
| `error`    | Border: `color-error-500`, Fehlermeldung darunter, Error-Icon          |
| `success`  | Border: `color-success-500`, Checkmark-Icon (optional)                |
| `disabled` | Opacity 0.5, Background: `color-bg-muted`, kein Cursor                |
| `readonly` | Kein Fokus möglich, Background: `color-bg-muted`, Cursor: `default`   |

## Aufbau (Reihenfolge im DOM)

```
[Label]              ← <label> mit for-Attribut (PFLICHT, kein Placeholder-Ersatz)
[Helper-Text]        ← Optional, kurze Erklärung vor dem Input
[Input-Wrapper]
  [Prefix-Icon]      ← Optional
  [<input>]
  [Suffix-Icon/Action] ← Optional (Clear, Toggle, Unit)
[Error-Message]      ← Nur bei Fehler, mit role="alert" oder aria-live
```

## Größen

| Größe | Padding (h/v)               | Font-Size    | Height |
|-------|------------------------------|--------------|--------|
| `sm`  | `spacing-2` / `spacing-3`   | `text-sm`    | 32px   |
| `md`  | `spacing-3` / `spacing-4`   | `text-base`  | 40px   |
| `lg`  | `spacing-4` / `spacing-4`   | `text-base`  | 48px   |

## Visuelle Specs

| Eigenschaft    | Default                    | Focus                     | Error                    |
|----------------|----------------------------|---------------------------|--------------------------|
| Hintergrund    | `color-neutral-0`          | `color-neutral-0`         | `color-error-100`        |
| Border         | `1px color-border-default` | `2px color-border-focus`  | `1px color-error-500`    |
| Border-Radius  | `radius-default`           | `radius-default`          | `radius-default`         |
| Text           | `color-text-primary`       | `color-text-primary`      | `color-text-primary`     |
| Placeholder    | `color-text-disabled`      | `color-text-disabled`     | `color-text-disabled`    |

## Label-Regeln

- Label ist immer sichtbar – kein Placeholder als Label-Ersatz
- Pflichtfelder: Sternchen (*) im Label + aria-required="true" auf Input
- Pflichtfeld-Hinweis am Anfang des Formulars: "* Pflichtfeld"

## Fehlermeldungen

- Inline direkt unter dem Input, nicht in Alerts oder Toasts
- Text: `color-error-700`, `text-sm`
- Kurz und präzise: "Bitte gültige E-Mail-Adresse eingeben" – nicht "Fehler"
- ID verknüpft mit Input via `aria-describedby`

## Regeln

- Labels sind immer vergeben – niemals nur Placeholder
- Fehlermeldungen sind inline, nicht in Toasts
- Jeder Input hat ein name-Attribut
- Autocomplete-Attribute setzen (email, name, tel etc.)

## Nicht verwenden wenn

- Längerer Freitext → Textarea
- Auswahl aus Optionen → Select oder Radio/Checkbox
- Datumsauswahl → DatePicker
