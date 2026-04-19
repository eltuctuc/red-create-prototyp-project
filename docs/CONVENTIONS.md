# Framework Conventions
*Verbindliche Regeln für Draft, Approval, Resume und Git Commits – Discovery Phase*

> Wird gelesen von: sparring, test-setup, requirements, ux, flows, architect, preview
> Developer, Dev-Setup und QA sind ausgenommen – sie schreiben direkt.

---

## Draft Convention

### Neue Dateien

Neue Dateien in der Discovery Phase werden als Draft gespeichert:

1. Inhalt im Chat präsentieren (oder direkt schreiben)
2. Datei mit YAML-Frontmatter `status: draft` speichern
3. User informieren (→ siehe Hinweis-Texte unten)
4. Nach `weiter` oder Chat-Korrektur: Frontmatter auf `status: approved` setzen, committen

### Erweiterungen bestehender Dateien

Wenn ein neuer Abschnitt zu einer bestehenden Datei hinzugefügt wird:

1. Abschnitt schreiben
2. YAML-Frontmatter der Datei auf `status: draft` setzen (oder ergänzen falls noch nicht vorhanden)
3. User informieren
4. Nach `weiter`: Frontmatter auf `status: approved` setzen, committen

### YAML-Frontmatter

```yaml
---
status: draft
---
```

Nach Finalisierung:

```yaml
---
status: approved
---
```

---

## Resume Pattern

### Option 1 – Kurze Pause (Minuten bis Stunden)
Geeignet für: sparring, requirements, ux, flows, architect

User tippt `weiter` im Chat. Claude liest die Datei erneut vom Disk und finalisiert.

**Hinweis nach Draft-Speicherung:**
```
📝 Draft gespeichert: [Dateiname]

Öffne die Datei, prüfe sie und bearbeite sie direkt falls nötig.

→ Schreib `weiter` wenn alles passt
→ Oder sag mir direkt was geändert werden soll
```

### Option 2 – Längere Überarbeitung (Stunden bis Tage)
Geeignet für: test-setup (wenn Personas/Hypothesen ausführlicher überarbeitet werden)

User trägt Änderungen in die Draft-Dateien ein, dann `/red-proto:test-setup` erneut aufrufen.
Der Command erkennt Drafts automatisch und wechselt in den Review-Modus.

**Draft-Erkennung beim Command-Neustart:**
```bash
DRAFTS=$(grep -rl "status: draft" test-setup/ 2>/dev/null)
if [ -n "$DRAFTS" ]; then
  echo "DRAFT-MODUS aktiv – folgende Dateien warten auf Finalisierung:"
  echo "$DRAFTS"
fi
```

**Hinweis nach Draft-Speicherung (test-setup):**
```
📝 Draft gespeichert: [Dateiname]

Kurze Pause?
→ Schreib `weiter` wenn du fertig bist

Längere Überarbeitung?
→ Trag deine Änderungen direkt in die Datei ein
→ Dann /red-proto:test-setup erneut aufrufen – ich erkenne den Draft automatisch
```

---

## Feature File Format

Feature-Dateien (`features/FEAT-X.md`) verwenden YAML-Frontmatter UND eine `## Fortschritt`-Sektion:

```yaml
---
status: draft
---
```

```markdown
## Fortschritt
Status: Draft
Aktueller Schritt: [Spec | UX | Tech | Dev | QA | Done]
Fix-Schwelle: [Critical | Critical, High | Critical, High, Medium]
```

**Status-Werte in `## Fortschritt`:**
- `Draft` – gerade geschrieben oder erweitert, wartet auf User-Review
- `Approved` – vom User geprüft und finalisiert

**Aktueller Schritt** spiegelt die zuletzt abgeschlossene Phase wider.

---

## Design-System & Abnahme-Screens

### Design-System vor Dev-Setup

Das Framework empfiehlt, `design-system/tokens/` zu befüllen (Farben, Typo, Spacing, Shadows), **bevor** `/red-proto:dev-setup` läuft. Der Grund: die Tokens beeinflussen die Tech-Stack-Wahl (z.B. sind Figma-Tokens für Tailwind einfacher zu transportieren als für Vuetify), und dev-setup transformiert sie beim Scaffold in das stack-spezifische Format.

Quelle bleibt immer `design-system/`. Die im Code erzeugten Token-Dateien (z.B. `tailwind.config.js`, `tokens.css`) sind **generiert** und werden bei Änderungen neu erzeugt, nicht manuell gepflegt.

### Abnahme-Screens pro Feature

Der optionale Command `/red-proto:preview FEAT-X` erzeugt Screens aus der fertig befüllten Feature-Spec und legt sie unter `features/FEAT-X-name/screens/` ab. Nach Abnahme durch den User sind diese Screens **Ground Truth für `/red-proto:dev`** (visuelle Vorlage) und Referenz für das **Copy-Inventar** in der Feature-Spec.

Format und Metadaten: siehe `ARTIFACT_SCHEMA.md` → "Screen-Index Format".

### Copy-Inventar

Wenn die Feature-Spec einen `### Copy-Inventar (Ground Truth)`-Block enthält, übernimmt `/red-proto:dev` alle sichtbaren Texte **wörtlich** in eine zentrale Copy-Datei (Pfad und Format stack-abhängig, siehe `/red-proto:dev` Phase 1.7). `/red-proto:qa` prüft mechanisch auf Drift.

---

## Git Commit

Kein roher `git diff`. Vor dem Commit immer eine menschenlesbare Zusammenfassung zeigen:

```
Ich committe jetzt:
  → [Datei 1] – [was sich geändert hat, z.B. "Spec neu angelegt"]
  → [Datei 2] – [was sich geändert hat, z.B. "Status auf Approved gesetzt"]
```

Dann erst committen:
```bash
git add [dateien]
git commit -m "[typ]: [kurze beschreibung]"
git push
```
