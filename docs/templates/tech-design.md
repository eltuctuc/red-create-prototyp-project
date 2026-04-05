## 3. Technisches Design
*[Datum]*

### Component-Struktur
FeatureContainer
├── FeatureHeader
├── FeatureList
│   └── FeatureItem
└── FeatureEmpty

Wiederverwendbar: [Komponente X] aus src/components/...

### Daten-Model
[Was wird gespeichert, wie strukturiert – kein SQL]
Gespeichert in: [localStorage / DB-Tabelle / API-State]

### API / Daten-Fluss
- GET  /api/[resource]   → [Zweck]
- POST /api/[resource]   → [Zweck]

### Tech-Entscheidungen
- **[Entscheidung]:** [Begründung]

### Security-Anforderungen
- Authentifizierung: [Wer darf?]
- Autorisierung: [Rollen/Rechte]
- Input-Validierung: [Wo was]
- OWASP: [XSS/CSRF/SQL-Injection relevante Punkte]

### Dependencies
- `package-name` – Zweck

### A11y-Architektur

| Element | ARIA-Pattern | Entscheidung |
|---------|-------------|--------------|
| Haupt-Container | Landmark? | ... |
| Listen/Grids | aria-label eindeutig? | ... |
| Live-Regions | Trigger (niemals initialer Render!) | ... |
| Fokus-Management | Nach Aktion X → Fokus auf Y | ... |
| Dialoge/Modals | aria-modal, Fokus-Trap, Escape? | ... |

### Test-Setup
- Unit: [Was]
- Integration: [Was]
- E2E: [Was]

### Test-Infrastruktur
- Environment: [happy-dom/jsdom + Limitierungen]
- Mocks: [localStorage → vi.stubGlobal, fetch → vi.fn()]
- Setup/Teardown: [beforeEach/afterEach Patterns]
- Fallstricke: [z.B. "localStorage in happy-dom braucht Stub"]
