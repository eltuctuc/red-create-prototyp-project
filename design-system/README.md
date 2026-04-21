# Design System

Dieses Verzeichnis enthält dein Design-System – Tokens, Komponenten, Patterns, Screens.

## Struktur ist frei wählbar

Du **musst** keine bestimmte Ordner-Struktur einhalten. Die Agents lesen rekursiv alle `*.md`-Dateien in diesem Verzeichnis und verstehen sie als Design-System-Dokumentation. Nur diese README selbst ist ausgenommen.

Wähle die Anordnung, die dir und deinem Team natürlich vorkommt. Unten stehen drei Beispiele – jedes davon ist gültig.

## Beispiel-Strukturen

### Klassisch (nach Art sortiert)

```
design-system/
  tokens/
    colors.md
    typography.md
    spacing.md
    shadows.md
  components/
    button.md
    input.md
  patterns/
    navigation.md
    forms.md
```

Dies ist die Struktur, mit der das Framework als Starter-Content ausgeliefert wird. Gut, wenn du klare Kategorien willst.

### Flach

```
design-system/
  colors.md
  typography.md
  spacing.md
  effects.md
  icons.md
  layout.md
  components/
    button.md
    combo-box.md
    field.md
    table.md
```

Tokens direkt im Hauptordner, Komponenten sammeln sich in einem Unterordner. Weniger Verschachtelung, schnelles Überfliegen.

### Nach Feature oder Domäne

```
design-system/
  foundations.md
  auth/
    login-button.md
    form-field.md
  dashboard/
    widget-card.md
    metric-display.md
```

Wenn dein Projekt mehrere UI-Bereiche mit eigenen Mustern hat.

## Was die Agents mit dem Inhalt machen

| Agent / Command | Nutzen aus dem DS |
|------------------|-------------------|
| `/red-proto:dev-setup` Phase 1c | Prüft ob DS überhaupt befüllt ist (zählt `*.md`-Dateien) |
| `/red-proto:dev-setup` Phase 5b | Liest Token-Dateien und transformiert sie in Stack-Format (Tailwind-Config, CSS-Variablen, SwiftUI-Extensions, …) |
| `/red-proto:ux` | Nutzt Komponenten/Patterns als Vorlage für UX-Entscheidungen |
| `/red-proto:dev`, `frontend-developer` | Implementiert nach DS-Specs und -Tokens |
| `ux-reviewer` | Prüft Implementierung auf DS-Konformität |

## Wann kein DS nötig ist

Wenn dein Tech-Stack eine **UI-Library** mitbringt (shadcn/ui, Material UI, Vuetify, Chakra, …), bringt die Library Look & Feel bereits mit. In diesem Fall gewinnt die Library: die Agents ignorieren den Markdown-DS stillschweigend und bauen nach Library-Konventionen. Lass diesen Ordner dann leer oder mit Minimal-Notizen.

Eine Kombination aus UI-Library **und** befülltem Markdown-DS ist nicht empfohlen – die Library-Konventionen gewinnen immer, und der DS-Inhalt wirkt dann irreführend.

## Regeln für befüllte DS-Dateien

- **Tokens haben Vorrang vor Hardcoded-Werten.** Kein `#3B82F6` direkt im Code – stattdessen den Token-Namen referenzieren.
- **Existiert eine Komponente → nutze die Spec**, baue keine eigene.
- **Existiert keine passende Komponente → baue eine neue** und ergänze sie im DS, wenn sie wiederverwendbar ist.
- **Abweichungen** vom DS sind als UX-Bug zu melden (Severity: Medium oder höher).
