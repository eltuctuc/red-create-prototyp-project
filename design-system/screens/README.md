# Screen-Referenzen

Hier kommen Figma-Exports oder Screenshots deines Design Systems als visuelle Referenz für die Agents.

## Ordner-Struktur

Lege Screens nach User-Flows / Bereichen in Unterordnern ab:

```
screens/
  onboarding/
    01-landing.png
    02-registration.png
    03-email-verification.png
  dashboard/
    01-overview.png
    02-empty-state.png
  [feature-name]/
    01-list.png
    02-detail.png
    03-create-form.png
```

## Benennungs-Konvention

- Numerisches Präfix für die Reihenfolge: `01-`, `02-` ...
- Beschreibender Name: was ist auf dem Screen zu sehen?
- Kein CamelCase, kein Leerzeichen: `kebab-case.png`

## Dateiformat

- **PNG bevorzugt** – verlustfreie Qualität für UI-Details
- **JPG** – akzeptabel für bildlastige Screens
- Mindestauflösung: 1440px Breite für Desktop-Screens
- Mobile-Screens: 375px oder 390px Breite

## Was die Agents damit machen

- `/red:proto-ux` liest die Screens als visuelle Referenz für User Flows und Komponentenstruktur
- `frontend-developer` nutzt Screens als Implementierungs-Referenz
- `ux-reviewer` vergleicht implementierte Screens mit den Referenz-Screens

## Hinweis

Screens sind **Referenz**, kein Pixel-Perfect-Vorgabe. Die Agents sollen die Struktur, Hierarchie und das Layout verstehen – nicht jeden Pixel nachbauen. Abweichungen in der technischen Umsetzung sind okay, solange sie dem Design-Prinzip folgen.
