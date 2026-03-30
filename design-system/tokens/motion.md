# Motion-Tokens (Transitions & Animationen)

*Optional – ersetze oder ergänze nach Bedarf.*

## Durations

| Token-Name          | Wert    | Verwendung                                              |
|---------------------|---------|---------------------------------------------------------|
| `duration-instant`  | `0ms`   | Kein Übergang (z.B. bei prefers-reduced-motion)         |
| `duration-fast`     | `100ms` | Sehr schnelle UI-Reaktionen (Hover-Highlights)          |
| `duration-normal`   | `200ms` | Standard UI-Übergänge (Buttons, Links, Inputs)          |
| `duration-moderate` | `300ms` | Komponenten ein-/ausblenden, Tabs wechseln              |
| `duration-slow`     | `500ms` | Panels, Sidebars, größere Layout-Änderungen             |
| `duration-slower`   | `700ms` | Komplexe Animationen, Onboarding-Flows                  |

## Easing-Funktionen

| Token-Name           | CSS-Wert                        | Verwendung                               |
|----------------------|---------------------------------|------------------------------------------|
| `ease-linear`        | `linear`                        | Fortschrittsbalken, Spinner              |
| `ease-in`            | `cubic-bezier(0.4, 0, 1, 1)`   | Elemente die verschwinden (fade out)     |
| `ease-out`           | `cubic-bezier(0, 0, 0.2, 1)`   | Elemente die erscheinen (fade in, slide) |
| `ease-in-out`        | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard UI-Übergänge                    |
| `ease-bounce`        | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Spielerische, springende Animationen |
| `ease-spring`        | `cubic-bezier(0.175, 0.885, 0.32, 1.275)` | Modals, Tooltips erscheinen     |

## Zusammengesetzte Transitions

| Token-Name                | Wert                                         | Verwendung                    |
|---------------------------|----------------------------------------------|-------------------------------|
| `transition-color`        | `color 200ms ease-in-out`                    | Textfarbe, Ikonfarbe          |
| `transition-bg`           | `background-color 200ms ease-in-out`         | Hintergrundfarbe              |
| `transition-border`       | `border-color 200ms ease-in-out`             | Border-Farbe (Inputs, Fokus)  |
| `transition-shadow`       | `box-shadow 200ms ease-in-out`               | Schatten-Übergänge            |
| `transition-opacity`      | `opacity 200ms ease-in-out`                  | Ein-/Ausblenden               |
| `transition-transform`    | `transform 300ms ease-out`                   | Slides, Scales                |
| `transition-all-fast`     | `all 100ms ease-in-out`                      | Schnelle Multi-Property       |
| `transition-all`          | `all 200ms ease-in-out`                      | Standard Multi-Property       |

## Accessibility-Hinweis

Respektiere `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Alle Übergänge müssen auch ohne Animation funktionieren – sie sind Enhancement, kein Kern der UX.
