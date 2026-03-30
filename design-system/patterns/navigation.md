# Pattern: Navigation

## Globale Navigation (Header / Top-Nav)

### Aufbau

```
[Header-Wrapper]                ← sticky, z-index über Content
  [Logo / Brand]                ← Links, immer sichtbar, klickbar = Home
  [Primary Nav]                 ← Horizontale Links (Desktop) oder Hamburger (Mobile)
  [Secondary Actions]           ← Suche, Notifications, User-Avatar/Menu
```

### Regeln

- Aktiver Navigationspunkt: `color-primary-500` Unterstrich oder Hintergrund-Tint
- Max. 5–7 Hauptnavigationspunkte – mehr → Mega-Menu oder Sidebar
- Mobile: Hamburger-Icon (3 Linien), öffnet Drawer von links oder oben
- Skip-Navigation-Link: erster Element im DOM (für Keyboard/Screen Reader)
- Sticky Header: `shadow-sticky` beim Scrollen aktivieren

### Aktiver Zustand

| Element         | Visual                                          |
|-----------------|-------------------------------------------------|
| Link            | `color-primary-600` + Unterstrichen oder Tint   |
| Icon-Tab        | Gefülltes Icon + `color-primary-500` Label      |
| Sidebar-Item    | `color-bg-muted` Hintergrund + `color-primary-600` Text |

---

## Sidebar-Navigation

### Verwendung

Für Anwendungen mit vielen Bereichen oder komplexer Hierarchie.

### Aufbau

```
[Sidebar-Wrapper]               ← Feste Breite: 240–280px; collapsible auf 64px
  [App Logo / Name]
  [Navigation Groups]
    [Group Label]               ← Optional, Uppercase, text-xs, color-text-secondary
    [Nav-Item]                  ← Icon + Label, aktiver Zustand
    [Nav-Item (mit Sub-Items)]  ← Aufklappbar (Accordion)
  [Bottom-Section]              ← Settings, Logout, User-Info
```

### Regeln

- Collapsible: Im Collapsed-Zustand nur Icons mit Tooltip
- Sub-Navigation: Max. 1 Ebene Tiefe in der Sidebar
- Scrollbar: Nur wenn mehr Items als sichtbare Höhe (overflow-y: auto)

---

## Breadcrumb

### Verwendung

Bei tiefen Hierarchien (ab 3 Ebenen). Nicht für flache Navigation.

### Aufbau

```
[Home] / [Kategorie] / [Aktuelle Seite]
```

### Regeln

- Trennzeichen: `/` oder `›` – konsistent
- Aktuelle Seite: Nicht klickbar, `color-text-secondary`
- Eltern-Seiten: Klickbar, `color-primary-600`
- Mobil: Nur 1–2 Levels anzeigen + "..." für ausgeblendete

---

## Tab-Navigation

### Verwendung

Für die Navigation zwischen gleichwertigen Content-Bereichen innerhalb einer Seite oder eines Panels.

### Regeln

- Max. 5–6 Tabs sichtbar – bei mehr: scrollbar oder Overflow-Dropdown
- Aktiver Tab: Unterstrich (`color-primary-500`, 2px) + `color-primary-600` Text
- Tab-Panel: `role="tabpanel"`, Tab: `role="tab"`, Wrapper: `role="tablist"`
- Keyboard: Pfeiltasten wechseln zwischen Tabs, Enter/Space aktiviert

---

## Back-Navigation

### Regeln

- "<- Zurück" nur wenn nicht aus der Hauptnavigation erreichbar
- Immer expliziter Linktext, nicht nur ein Zurück-Pfeil (Screen Reader!)
- Navigiert zur vorherigen Seite (nicht Browser-Back, da ggf. abweichender State)
