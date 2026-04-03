# Design System – Index

Lade dieses File zuerst. Dann nur die Files, die für das aktuelle Feature relevant sind.

---

## Tokens

| File | Inhalt | Wann laden |
|------|--------|------------|
| `tokens/colors.md` | Primär-, Sekundär-, Semantic-, Neutral-Farben + Surface-Aliases | Immer bei visueller Implementierung |
| `tokens/typography.md` | Schriftgrößen, Gewichte, Line-Heights, Font-Stack | Bei Text-Styling |
| `tokens/spacing.md` | Spacing-Scale (4px-Basis), Named Sizes (xs–2xl) | Bei Layout, Abstände, Padding |
| `tokens/shadows.md` | Elevation-System (sm, md, lg, xl) | Bei Cards, Modals, Dropdowns |
| `tokens/motion.md` | Transitions, Durations, Easing-Kurven | Bei Animationen, Hover-Effekten |

## Komponenten

| File | Varianten | Zustände | Wann laden |
|------|-----------|----------|------------|
| `components/button.md` | primary, secondary, ghost, danger, link | default, hover, focus, active, disabled, loading | Bei jeder Aktion/Button |
| `components/input.md` | text, password, textarea, select | default, focus, error, disabled | Bei Formularen |
| `components/card.md` | default, interactive, flat | default, hover | Bei Card-Layouts |

## Patterns

| File | Enthält | Wann laden |
|------|---------|------------|
| `patterns/navigation.md` | Header, Sidebar, Breadcrumb, Tab-Navigation | Bei Navigation-Implementierung |
| `patterns/forms.md` | Formular-Aufbau, Validation, Fehlermeldungen | Bei Formularen |
| `patterns/feedback.md` | Toasts, Modals, Loading States, Empty States | Bei Feedback-Elementen |
| `patterns/data-display.md` | Tabellen, Listen, Cards, Badges | Bei Datendarstellung |

---

## Laderegel für Agents

1. Lies dieses INDEX.md
2. Identifiziere welche Tokens/Komponenten/Patterns das Feature braucht
3. Lade **nur diese Files** – nicht alles auf einmal
4. Nicht definierte Elemente: pragmatisch mit vorhandenen Tokens bauen, im Feature-File unter `## Offene Punkte` dokumentieren

## Status

| Bereich | Status |
|---------|--------|
| Tokens | Beispielwerte – vor Projektstart durch eigene Werte ersetzen |
| Komponenten | 3 Basiskomponenten vorhanden (Button, Input, Card) |
| Patterns | 4 Patterns vorhanden |
| Screens | Leer – Figma-Exports hier ablegen |
