---
name: Preview
description: Optionales Abnahme-Gate – erzeugt Screens in Figma aus der fertigen Feature-Spec, damit der User sie vor der Umsetzung begutachten und abnicken kann
---

> Lies `.claude/red-proto/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

Du bist der Abnahme-Pass vor Dev. Deine Aufgabe: aus der fertig befüllten Feature-Spec (Requirements + UX + Architect) **konkrete Abnahme-Screens in Figma erzeugen**, die der User sich dort anschaut und entweder abnickt oder korrigieren lässt – **bevor** gebaut wird.

**Wichtig:**
- Dieser Command ist **optional**. Features ohne Abnahme-Screens laufen genauso durch die Pipeline.
- Screens werden **in Figma erzeugt**, nicht lokal abgelegt. Der User nimmt sie in Figma ab.
- **Keine PNG/Base64-Ablage im Repo.** Abbilder sind zu groß für die lokale Speicherung und führen zu Timeout- und Ressourcen-Problemen. Das Repo speichert ausschließlich Metadaten + Figma-Frame-URLs.
- Screens sind **ab Abnahme Ground Truth** für `/red-proto:dev`. Dev baut gegen sie (anhand der Figma-Links), nicht mehr nur gegen die Spec.

## Konflikt-Check (Pflicht – vor allen Phasen)

Führe die Prüfung aus `.claude/red-proto/templates/conflict-check.md` aus. Bei Konflikt: stoppe sofort mit der dort dokumentierten Meldung. Der Konflikt wird vom User außerhalb dieses Commands gelöst – kein Dialog hier.

## Phase 0: Voraussetzungen prüfen

```bash
# Welches Feature? – aus Argument oder aus zuletzt bearbeitetem Feature ableiten.
FEAT_FILE=$(ls features/FEAT-[X]-*.md 2>/dev/null | head -1)
if [ -z "$FEAT_FILE" ]; then
  echo "FEHLER: Keine Feature-Spec für FEAT-[X] gefunden."
  exit 1
fi

cat "$FEAT_FILE"

# Spec-Vollständigkeit prüfen
if ! grep -q "## 2. UX" "$FEAT_FILE" || ! grep -q "## 3. Technisches Design" "$FEAT_FILE"; then
  echo "HINWEIS: Feature-Spec ist noch nicht vollständig. /red-proto:preview macht vor allem Sinn, wenn UX und Architect befüllt sind."
fi
```

**Figma-MCP-Check (Pflicht):**

Dieser Command schreibt in Figma. Wenn der Figma-MCP-Server nicht verbunden ist, scheitern die Write-Calls. Prüfe die Verfügbarkeit, bevor du weitermachst:

- Versuche einen harmlosen Read: `mcp__figma__whoami`
- Fehler oder „tool not found" → **stoppen** und dem User sagen: „Figma-MCP-Server nicht erreichbar. Entweder MCP installieren/verbinden oder `/red-proto:preview` überspringen – das Feature läuft auch ohne Abnahme-Gate durch die Pipeline."

Fasse im Chat kurz zusammen, was du über das Feature gelesen hast (1–2 Sätze), damit der User sicher ist, dass du das richtige Feature im Kopf hast.

## Phase 1: Screen-Plan aus Spec ableiten

Bevor du in Figma schreibst, leite aus der Spec ab **welche Screens gebraucht werden**. Quellen:

- **UX-Abschnitt** (`## 2. UX`): welche Komponenten, welche Zustände (Initial, Leer, Gefüllt, Fehler, Loading, Erfolg)
- **Acceptance Criteria**: jeder AC braucht mindestens einen Screen, der ihn visualisiert
- **Flow-Schritte** aus `flows/product-flows.md` (falls vorhanden): jede relevante Transition

Präsentiere den Plan dem User im Chat:

```
Screen-Plan für FEAT-[X] [Name]:

  S-10  Initial (leerer Zustand)
  S-11  Ausgefüllt (typische Eingabe)
  S-12  Fehler (Validierung schlägt fehl)
  S-13  Erfolg (Confirmation)

Erzeuge ich diese 4 Screens in Figma, oder willst du etwas ergänzen/streichen?
```

Warte auf Bestätigung, bevor du Phase 2 startest. Änderungswünsche aufnehmen.

## Phase 2: Ziel-Page in Figma erfragen

Frage den User nach einem **Figma-Page-Link** (nicht Frame-Link). In diese Page schreibt Claude die erzeugten Screens.

```typescript
AskUserQuestion({
  questions: [
    {
      question: "In welche Figma-Page soll ich die Abnahme-Screens schreiben? Gib mir einen Page-Link aus deiner Figma-Datei (Rechtsklick auf die Page → 'Copy link to page').",
      header: "Figma-Ziel",
      options: [
        { label: "Ich gebe dir den Link im Chat", description: "Claude parst fileKey + pageId und erzeugt dort die Screens" },
        { label: "Abbrechen – ich habe noch keine Page angelegt", description: "Lege in Figma eine neue Page an (z.B. 'Preview FEAT-X'), dann /red-proto:preview erneut starten" }
      ],
      multiSelect: false
    }
  ]
})
```

Aus dem Link extrahieren:
- `fileKey` – zwischen `figma.com/design/` und dem nächsten `/`
- `pageId` – aus `node-id=<id>` (die Page-ID steht dort bei einem Page-Link). `-` durch `:` ersetzen.

Validiere mit `mcp__figma__get_metadata(fileKey)` dass die Page existiert und welchen Namen sie trägt. Zeige dem User zur Sicherheit: „Ich schreibe in Page **[Name]** der Datei **[Dateiname]**. Korrekt?"

## Phase 3: Screens in Figma erzeugen

Für jeden Screen aus dem Plan (Phase 1):

1. **Beschreibung formulieren.** Aus Spec-Kontext + Zustand + ggf. DS- oder Library-Referenzen einen klaren Prompt bauen, den der Figma-Generator umsetzen kann. Beispiel: „Login-Screen mit E-Mail-Feld, Passwort-Feld, primärem 'Anmelden'-Button, klein darunter 'Passwort vergessen'-Link. Clean, Sans-Serif, viel Weißraum."

2. **Design-Quelle beachten** (aus `project-config.md`):
   - **DS-Modus** (`UI-Library: keine`) → Tokens aus `design-system/` in den Prompt einweben (Farben, Typo, Spacing, Komponenten-Patterns).
   - **Library-Modus** (`UI-Library: shadcn/ui` o.ä.) → Library-Aesthetic im Prompt referenzieren („shadcn/ui-Stil, Tailwind-Farben").

3. **Aufruf:** `mcp__figma__generate_figma_design(prompt, fileKey, pageId)` — oder falls das Tool eine andere Signatur hat, das entsprechende Äquivalent. Bei Bedarf iterativ via `mcp__figma__use_figma` für präzisere Kontrolle.

4. **Rückgabe des Tools:** eine Frame-URL (oder Node-ID). Diese speichern für Phase 4.

Wenn ein einzelner Generate-Call scheitert: fahre mit den anderen Screens fort und merke den Fehler. Am Ende dem User eine Liste zeigen, welche Screens erzeugt wurden und welche nicht.

## Phase 4: index.md schreiben (nur Metadaten, keine Bilder)

Lege `features/FEAT-[X]-name/screens/index.md` an – **nur diese eine Datei, kein `screens/`-Ordner mit PNGs**:

```markdown
---
status: draft
feature: FEAT-[X]
figma_file: <fileKey>
figma_page: <pageId>
figma_page_url: https://www.figma.com/design/<fileKey>/...?node-id=<pageId>
---

# Abnahme-Screens – FEAT-[X]

**Figma-Page:** [Name der Page]([page-url])

| Screen-ID | Zustand | Flow-Schritt | Figma-Frame | Status |
|-----------|---------|--------------|-------------|--------|
| S-10 | Initial | Einstieg | [Frame-Link](https://www.figma.com/design/.../?node-id=<frameId>) | review |
| S-11 | Ausgefüllt | Nach Eingabe | [Frame-Link](...) | review |
| S-12 | Fehler | Validierung | [Frame-Link](...) | review |
| S-13 | Erfolg | Confirmation | [Frame-Link](...) | review |
```

Alle Screens landen mit Status `review`. Die Abnahme kommt in Phase 6.

**Wichtig:** Keine `*.png`-Dateien ablegen. Auch keine Base64-Strings in der `index.md`. Abbilder bleiben in Figma – das Repo speichert nur die Links.

## Phase 5: Widerspruchs-Check gegen Spec

Bevor du den User zur Abnahme bittest: prüfe die erzeugten Screens auf offensichtliche Widersprüche zur Spec. Du hast die Figma-Frames nicht als Bilder im Chat – du prüfst **über die Metadaten** (Zustände, Flow-Abdeckung).

Lies die Spec und die gerade geschriebene `index.md`. Achte auf:

- **Acceptance Criteria vs. Zustände:** Wird jedes AC durch mindestens einen Screen-Zustand abgedeckt? Fehlen Fehler-, Leer- oder Loading-Zustände?
- **Flow-Schritte:** Sind alle relevanten Transitions aus `flows/product-flows.md` als Screens vorhanden?

Wenn du Lücken siehst, zeige sie dem User:

```
Lücken im Screen-Plan erkannt:
- AC #4 verlangt einen Fehlerzustand, kein entsprechender Screen dabei
- Flow-Schritt "Nach erfolgreichem Login → Dashboard" hat keinen Nachfolger-Screen
```

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Es gibt Lücken zwischen Spec und Screen-Plan. Wie weiter?",
      header: "Lücken-Auflösung",
      options: [
        { label: "Fehlende Screens ergänzen", description: "Ich erzeuge die fehlenden Frames in Figma nach" },
        { label: "Zurück zu /red-proto:requirements", description: "Spec anpassen, dann /red-proto:preview erneut" },
        { label: "Zurück zu /red-proto:ux", description: "UX-Entscheidungen nachziehen, dann /red-proto:preview erneut" },
        { label: "Akzeptieren und weitermachen", description: "Die Lücke ist bewusst – ich vermerke das in index.md" }
      ],
      multiSelect: false
    }
  ]
})
```

Wenn keine Lücken: direkt weiter zu Phase 6.

## Phase 6: User-Abnahme in Figma

Zeige dem User eine kompakte Zusammenfassung im Chat mit **anklickbaren Links** zu den Figma-Frames:

```
Abnahme für FEAT-[X] [Name]:

Figma-Page: [Page-URL]

Screens erzeugt ([N]):
  S-10 – Initial       → [Frame-URL]
  S-11 – Ausgefüllt    → [Frame-URL]
  S-12 – Fehler        → [Frame-URL]
  S-13 – Erfolg        → [Frame-URL]

Öffne die Links in Figma, prüfe die Screens, sag mir ob sie dein erwartetes Ergebnis treffen.
Korrekturen: gib mir direkt Feedback im Chat, ich passe die Frames an.
```

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Passen die Screens zu deiner Vorstellung?",
      header: "Abnahme",
      options: [
        { label: "Ja, alle freigeben", description: "Alle Screens auf 'approved' setzen" },
        { label: "Teilweise – ich nenne im Chat welche", description: "Freigabe pro Screen" },
        { label: "Nein, überarbeiten", description: "Ich gebe dir Korrekturen im Chat, du änderst die Frames" }
      ],
      multiSelect: false
    }
  ]
})
```

**Bei „Überarbeiten":** User gibt Feedback, Claude nutzt `mcp__figma__use_figma` oder `mcp__figma__generate_figma_design` um die betroffenen Frames zu ändern (nicht neu erzeugen, wenn möglich – erhält die Frame-ID). Danach zurück zu Phase 6.

## Phase 7: Finalisieren

Setze in `index.md` für alle freigegebenen Screens Status `approved`. Setze `status: approved` im Frontmatter, wenn **alle** Screens approved sind. Wenn einige noch `review` bleiben: Frontmatter bleibt `draft`.

```bash
git add "features/FEAT-[X]-name/screens/index.md" && git commit -q -m "docs: FEAT-[X] preview-screens in Figma – [Feature Name]" && git push -q
```

Zeige dem User den Abschluss:

```
✅ Preview abgeschlossen für FEAT-[X]

Screens abgenommen:  [N] von [M]
Ground Truth:        Figma-Page [Page-Name]
Referenz im Repo:    features/FEAT-[X]-name/screens/index.md

Nächster Schritt: /red-proto:dev FEAT-[X] – baut gegen die Figma-Frames als visuelle Vorlage.
Nach einer Pause:  /red-proto:workflow zeigt dir exakt wo du stehst.
```

Wenn nicht alle Screens approved sind: klar machen, dass Dev trotzdem starten kann, aber die nicht-abgenommenen Screens als `outdated` markieren soll, wenn sich etwas ändert.

## Wiederholung

`/red-proto:preview FEAT-[X]` kann jederzeit erneut aufgerufen werden – z.B. nach einer Spec-Änderung. Bestehende approved Screens werden dann auf `outdated` gesetzt, bis sie neu bestätigt (oder neu generiert) sind. Der Command erkennt beim Neustart vorhandene `outdated`-Einträge und bietet an, sie gezielt zu erneuern.

## Checklist

- [ ] Feature-Spec vorhanden und mindestens mit Requirements + UX befüllt
- [ ] Figma-MCP erreichbar
- [ ] Screen-Plan vom User bestätigt
- [ ] Figma-Page-Link erhalten und validiert
- [ ] Alle geplanten Frames in Figma erzeugt
- [ ] `features/FEAT-[X]-name/screens/index.md` mit Metadaten + Figma-Links befüllt (keine PNGs, keine Base64)
- [ ] Widerspruchs-/Lücken-Check durchgeführt
- [ ] User-Abnahme eingeholt
- [ ] Approved-Status in `index.md` aktualisiert
- [ ] Commit + Push
