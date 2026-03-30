# Design System

Zentrales Verzeichnis für alle Design-Vorgaben. Alle Agents des Frameworks lesen dieses Verzeichnis – es ist die verbindliche Referenz für Entscheidungen in UX-Design, Implementierung und Review.

## Struktur

```
design-system/
  tokens/
    colors.md          ← Farb-Tokens (Primär, Sekundär, Semantic, Neutral)
    typography.md      ← Schriften, Größen, Gewichte, Line-Heights
    spacing.md         ← Spacing-Scale und Named Sizes
    shadows.md         ← Elevation-System
    motion.md          ← Transitions, Durations, Easing (optional)
  components/
    button.md          ← Beispiel-Komponente (kopieren und anpassen)
    input.md           ← Beispiel-Komponente
    card.md            ← Beispiel-Komponente
    [weitere].md       ← Eigene Komponenten hier ablegen
  patterns/
    navigation.md      ← Header, Sidebar, Breadcrumb, Tab-Navigation
    forms.md           ← Formular-Aufbau, Validation, Fehlermeldungen
    feedback.md        ← Toasts, Modals, Loading States, Empty States
    data-display.md    ← Tabellen, Listen, Cards, Badges
  screens/
    README.md          ← Anleitung für Screen-Exports
    [flow-name]/       ← Figma-Exports oder Screenshots nach Flow gruppiert
```

## Anleitung

### Wann befüllst du dieses Verzeichnis?

**Du musst diesen Ordner nicht vor dem ersten Feature vollständig befüllen.** Fang mit dem an was du weißt – ein paar Farb-Tokens, ein Button – und ergänze während der Entwicklung. Was noch nicht definiert ist, füllen die Agents pragmatisch. Was definiert ist, wird verbindlich eingehalten.

Das Design System wächst mit dem Projekt. Das ist normal und gewollt.

### So befüllst du dieses Verzeichnis

1. **Tokens zuerst** – Farben, Typografie und Spacing sind die Basis für alle Komponenten. Trage die Werte aus deinem Figma/Styleguide in die Token-Files ein.

2. **Komponenten** – Jede Komponente bekommt ein eigenes File. Kopiere `components/button.md` als Vorlage. Trage Varianten, Zustände und visuelle Specs ein.

3. **Patterns** – Übergreifende UX-Muster (wie Formulare aufgebaut sind, wie Navigation funktioniert). Diese informieren den UX-Design-Schritt direkt.

4. **Screens** – Exportiere Figma-Screens als PNG und lege sie in den passenden Flow-Unterordner. Benenne sie aussagekräftig: `01-login.png`, `02-dashboard.png`.

### Was passiert mit diesen Inhalten?

| Agent | Liest | Zweck |
|-------|-------|-------|
| `/red:proto-ux` | `components/`, `patterns/` | Nur DS-konforme Komponenten in User Flows |
| `/red:proto-dev` | `tokens/`, `components/` | Tokens und Specs direkt in Code übersetzen |
| `frontend-developer` | alles | Vollständige DS-Referenz bei Implementierung |
| `ux-reviewer` | alles | DS-Compliance-Check nach Implementierung |

### Regeln für Agents

- Existiert eine Komponente im DS → baue keine eigene, nutze die Spec
- Existiert keine passende Komponente → baue eine neue, dokumentiere sie im `## Offene Punkte` im Feature-File
- Tokens haben Vorrang vor Hardcoded-Werten (kein `#3B82F6` direkt – stattdessen den Token-Namen nutzen)
- Abweichungen vom DS sind als UX-Bug zu melden (Severity: Medium oder höher)
