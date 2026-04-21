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
| `/red-proto:dev-setup` Phase 1c | Prüft ob DS befüllt ist – entscheidet DS-Modus vs. Library-Modus |
| `/red-proto:dev-setup` Phase 5b | Im DS-Modus: liest Token-Dateien rekursiv und transformiert sie in Stack-Format (Tailwind-Config, CSS-Variablen, SwiftUI-Extensions, …). Im Library-Modus übersprungen. |
| `/red-proto:ux` | Im DS-Modus: nutzt Komponenten/Patterns als Vorlage. Im Library-Modus: nutzt Library-Konventionen statt DS. |
| `/red-proto:dev`, `frontend-developer` | Im DS-Modus: baut eigene Komponenten nach DS-Specs. Im Library-Modus: nutzt nur Library, liest das DS nicht. |
| `ux-reviewer` | Im DS-Modus: prüft Implementierung auf DS-Konformität. Im Library-Modus: prüft gegen Library-Konventionen. |
| `/red-proto:workflow` | Meldet Konflikt wenn DS-Inhalt und `UI-Library: [Name]` gleichzeitig gesetzt sind. |

## Wann kein DS nötig ist

Das Framework fährt einen **Entweder-Oder-Modus** zwischen DS und UI-Library. Entschieden wird in `/red-proto:dev-setup`, das Ergebnis steht dann in `project-config.md` als `UI-Library: [Name]` oder `UI-Library: keine`.

**Wenn du mit einer gestylten UI-Library arbeiten willst** (shadcn/ui, Material UI, Vuetify, Chakra, …): lass dieses Verzeichnis leer (nur diese README). Die Library bringt Look & Feel mit, der Frontend-Agent nutzt ausschließlich Library-Komponenten, das DS wird nicht gelesen.

**Wenn du ein eigenes DS willst:** befülle dieses Verzeichnis. Der Stack wird dann **ohne** gestylte UI-Library empfohlen (shadcn/ui & Co. entfallen). Der Frontend-Agent baut eigene Komponenten passend zum DS.

Beides zusammen ist **nicht** erlaubt. Wenn das Framework einen Konflikt erkennt (`UI-Library: shadcn/ui` gesetzt UND DS-Dateien vorhanden), brechen alle Feature-Commands und Agents ab, bis du den Widerspruch aufgelöst hast (DS-Dateien entfernen oder `UI-Library: keine` in `project-config.md` setzen und `/red-proto:dev-setup` neu starten). Kein Dialog im Chat – die Entscheidung trifst du außerhalb über die Dateien selbst.

Ausnahme: **Headless-Primitives** ohne eigenes Styling (Radix Primitives, React Aria, Headless UI) zählen nicht als UI-Library – sie sind Infrastruktur für Keyboard und Accessibility und dürfen parallel zum DS genutzt werden.

## Regeln für befüllte DS-Dateien

- **Tokens haben Vorrang vor Hardcoded-Werten.** Kein `#3B82F6` direkt im Code – stattdessen den Token-Namen referenzieren.
- **Existiert eine Komponente → nutze die Spec**, baue keine eigene.
- **Existiert keine passende Komponente → baue eine neue** und ergänze sie im DS, wenn sie wiederverwendbar ist.
- **Abweichungen** vom DS sind als UX-Bug zu melden (Severity: Medium oder höher).
