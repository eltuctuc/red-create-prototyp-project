# Framework Conventions
*Verbindliche Regeln für Draft, Approval, Resume und Git Commits – Discovery Phase*

> Wird gelesen von: sparring, test-setup, requirements, ux, flows, architect
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
