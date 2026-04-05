## 2. UX Entscheidungen
*[Datum]*

### Einbettung im Produkt
[Wo lebt das Feature?] | Route: `/[pfad]`

### Einstiegspunkte
[Wie gelangt der Nutzer dahin?]

### User Flow
[Start] → [Schritt 1] → [Schritt 2] → [Ende]

### Interaktionsmuster
- Primärmuster: [Pattern – Referenz: design-system/patterns/...]
- Fehler-Handling: [Referenz: feedback.md]
- Leerer Zustand: [Was wird gezeigt?]
- Ladeverhalten: [z.B. Skeleton]

### Eingesetzte Komponenten
| Komponente | DS-Status | Quelle |
|------------|-----------|--------|
| [Name] | ✓ Vorhanden | components/[name].md |
| [Name] | ⚠ Tokens-Build | Keine Spec – genehmigt [Datum] |
| [Name] | 🧪 Hypothesentest | Abweichung von [Pattern] – Grund: [...] |

### Navigation nach Aktionen (verbindlich)
| Ausgangs-Screen | Aktion | Ziel | Bedingung |
|-----------------|--------|------|-----------|
| [Screen] | "[Aktion]" | [Ziel] | – |

### DS-Status
- Konforme Komponenten: [Liste]
- Tokens-Build (genehmigt): [Liste oder –]
- Hypothesentest: [Liste oder –]

### Barrierefreiheit (A11y)
- Keyboard: [Tab/Enter/Space erreichbare Aktionen]
- Screen Reader: [aria-label + Live-Regions]
- Farbkontrast (berechnet):

| Element | fg-Token | bg-Token | Hex fg | Hex bg | Ratio | WCAG |
|---------|----------|----------|--------|--------|-------|------|
| [Name] | [token] | [token] | #... | #... | X:1 | ✅/❌ |

Hex-Werte aus tokens/colors.md. Grenzwerte: 4.5:1 Normaltext, 3:1 großer Text/UI.

### Mobile-Verhalten
- [...]
