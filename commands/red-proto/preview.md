---
name: Preview
description: Optionales Abnahme-Gate – erzeugt Screens aus der fertigen Feature-Spec, damit der User das erwartete Ergebnis vor der Umsetzung begutachten und korrigieren kann
---

> Lies `.claude/red-proto/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

Du bist der Abnahme-Pass vor Dev. Deine Aufgabe: aus der fertig befüllten Feature-Spec (Requirements + UX + Architect) **konkrete Screens erzeugen**, die der User sich anschaut und entweder abnickt oder korrigieren lässt – **bevor** gebaut wird.

**Wichtig:**
- Dieser Command ist **optional**. Features ohne Abnahme-Screens laufen genauso durch die Pipeline.
- Es gibt **kein visuelles QA**. Die Abnahme ist menschlich – du legst die Screens nur sauber ab, der User begutachtet sie selbst.
- Screens sind **ab Abnahme Ground Truth** für `/red-proto:dev`. Dev baut gegen sie, nicht mehr nur gegen die Spec.

## Phase 0: Voraussetzungen prüfen

```bash
# Welches Feature?
# Aus Argument oder aus zuletzt bearbeitetem Feature ableiten.

FEAT_FILE=$(ls features/FEAT-[X]-*.md 2>/dev/null | head -1)
if [ -z "$FEAT_FILE" ]; then
  echo "FEHLER: Keine Feature-Spec für FEAT-[X] gefunden."
  exit 1
fi

cat "$FEAT_FILE"

# Prüfen: Spec muss Requirements, UX und Architect bereits befüllt haben
if ! grep -q "## 2. UX" "$FEAT_FILE" || ! grep -q "## 3. Technisches Design" "$FEAT_FILE"; then
  echo "HINWEIS: Feature-Spec ist noch nicht vollständig. /red-proto:preview macht vor allem Sinn, wenn UX und Architect befüllt sind."
fi

# Design-System laden
cat design-system/INDEX.md 2>/dev/null

# Figma-Quelle aus project-config.md?
FIGMA_URL=$(grep -A3 "^## Figma-Quellen" project-config.md 2>/dev/null | grep "File-URL:" | cut -d':' -f2- | xargs)
FIGMA_KEY=$(grep -A3 "^## Figma-Quellen" project-config.md 2>/dev/null | grep "File-Key:" | cut -d':' -f2- | xargs)
echo "Figma: URL=$FIGMA_URL | Key=$FIGMA_KEY"
```

Fasse im Chat kurz zusammen was du über das Feature gelesen hast (1–2 Sätze), damit der User sicher ist, dass du das richtige Feature im Kopf hast.

## Phase 1: Quelle wählen

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Woher sollen die Abnahme-Screens kommen?",
      header: "Screen-Quelle",
      options: [
        { label: "Figma – ich gebe dir Node-Links", description: "Du rufst sie per MCP ab und legst sie als PNG in features/FEAT-X/screens/ ab" },
        { label: "Figma – hol sie aus der in project-config.md hinterlegten File", description: "Nur wenn File-Key konfiguriert ist – du findest relevante Frames selbst" },
        { label: "Ich lade PNGs im Chat hoch", description: "Du legst sie unverändert in features/FEAT-X/screens/ ab und befüllst die index.md" },
        { label: "Manuell ablegen", description: "Ich lege die PNGs selbst im Ordner ab – du befüllst nur die index.md nach meinen Angaben" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 2: Screens beschaffen und ablegen

Lege den Zielordner an:

```bash
FEAT_NAME=$(basename "$FEAT_FILE" .md)   # z.B. FEAT-1-login
mkdir -p "features/$FEAT_NAME/screens"
```

### Option A: Figma – Node-Links vom User

Der User liefert einen oder mehrere Figma-URLs. Pro Link:

1. `fileKey` und `nodeId` aus der URL extrahieren (Format: `figma.com/design/{fileKey}/.../node-id={nodeId}`). Beachte: `-` in `nodeId` → `:` umwandeln.
2. `mcp__figma__get_design_context(fileKey, nodeId)` aufrufen – liefert Screenshot-URL, Struktur und Code-Referenz.
3. Screenshot als PNG herunterladen und in `features/$FEAT_NAME/screens/` ablegen. Datei-Name: `S-[NN]-[kurzbezeichnung].png`, fortlaufend nummeriert pro Feature.
4. Zustand und Flow-Schritt aus dem Figma-Frame-Namen oder dem Kontext ableiten.

### Option B: Figma – File-Key aus project-config.md

Wenn ein File-Key konfiguriert ist und der User keine expliziten Links liefert:

1. `mcp__figma__get_metadata(fileKey)` – gibt Seiten-Struktur zurück
2. Zeige dem User im Chat eine Liste der gefundenen Top-Level-Frames, die potentiell zu diesem Feature gehören. Frage:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Welche dieser Frames sind die Abnahme-Screens für FEAT-[X]?",
      header: "Frame-Auswahl",
      options: [
        // dynamisch: für jeden Kandidaten-Frame einen Eintrag
      ],
      multiSelect: true
    }
  ]
})
```

3. Pro ausgewähltem Frame wie in Option A vorgehen.

### Option C: PNG-Upload im Chat

Der User lädt Bilder direkt im Chat hoch. Pro Bild:

1. Bild mit `Read`-Tool verarbeiten – beschreibe im Chat kurz was du siehst (Sicherheit: richtiger Screen?)
2. Datei in `features/$FEAT_NAME/screens/S-[NN]-[kurzbezeichnung].png` ablegen
3. Zustand und Flow-Schritt erfragen, falls nicht aus dem Bild offensichtlich

### Option D: Manuell abgelegt

Der User hat die PNGs selbst abgelegt:

```bash
ls "features/$FEAT_NAME/screens/"*.png 2>/dev/null
```

Zu jeder Datei Zustand und Flow-Schritt erfragen.

## Phase 3: index.md schreiben

Nach ARTIFACT_SCHEMA Format. Datei unter `features/$FEAT_NAME/screens/index.md` anlegen:

```markdown
---
status: draft
feature: FEAT-[X]
source: figma | upload | manual
---

# Screens – FEAT-[X]

Quelle: [Figma-File-URL oder "PNG-Upload" oder "manuell abgelegt"]

| Screen-ID | Datei | Zustand | Flow-Schritt | Figma-Node | Status |
|-----------|-------|---------|--------------|------------|--------|
| S-10 | S-10-empty.png | Initial | Einstieg | 123:456 | review |
| S-11 | S-11-filled.png | Ausgefüllt | Nach Eingabe | 123:457 | review |
```

Alle Screens landen mit Status `review` – die Abnahme kommt in Phase 4.

## Phase 4: Widerspruchs-Check gegen Spec

Vor der User-Abnahme: prüfe die erzeugten Screens auf offensichtliche Widersprüche zur Feature-Spec.

Lies die Spec und die index.md. Achte auf:
- **Acceptance Criteria vs. Screens:** Werden alle AC durch mindestens einen Screen abgedeckt? Fehlende Zustände (Fehler, Leer, Loading) gelistet?
- **Flow-Schritte:** Passen die Screens zu den in `flows/product-flows.md` beschriebenen Transitions?
- **Komponenten aus UX-Entscheidung:** Tauchen die gewählten DS-Komponenten auf den Screens auch auf?

Wenn du Widersprüche siehst, zeige sie dem User im Chat als Liste:

```
Widersprüche erkannt:
- Spec erwartet einen Fehlerzustand (AC #4), kein passender Screen dabei
- Screen S-12 zeigt einen "Erfolgs-Toast" – im UX-Abschnitt steht "Erfolgsmeldung als Inline-Banner"
```

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Es gibt Widersprüche zwischen Spec und Screens. Wie weiter?",
      header: "Widerspruch-Auflösung",
      options: [
        { label: "Zurück zu /red-proto:requirements", description: "Spec anpassen, dann /red-proto:preview erneut" },
        { label: "Zurück zu /red-proto:ux", description: "UX-Entscheidungen nachziehen, dann /red-proto:preview erneut" },
        { label: "Screens überarbeiten", description: "Ich ergänze/korrigiere die Screens, dann neu einreichen" },
        { label: "Akzeptieren und trotzdem weitermachen", description: "Die Abweichung ist bewusst – ich vermerke das in index.md" }
      ],
      multiSelect: false
    }
  ]
})
```

Wenn keine Widersprüche: direkt weiter zu Phase 5.

## Phase 5: User-Abnahme

Zeige dem User eine kompakte Zusammenfassung im Chat:

```
Abnahme für FEAT-[X] [Name]:

Ordner: features/FEAT-[X]-name/screens/
Screens: [N] insgesamt
  - S-10 – Initial (Einstieg)
  - S-11 – Ausgefüllt (Nach Eingabe)
  - S-12 – Fehler (Bei ungültiger Eingabe)

Öffne die PNGs, prüfe sie, sag mir ob sie dein erwartetes Ergebnis treffen.
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
        { label: "Nein, bitte komplett neu", description: "Quelle neu wählen und Phase 2 wiederholen" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 6: Finalisieren

Setze in `index.md` für alle freigegebenen Screens Status `approved`. Setze `status: approved` im Frontmatter, wenn **alle** Screens approved sind. Wenn einige noch `review` bleiben: Frontmatter bleibt `draft`.

```bash
git add "features/$FEAT_NAME/screens/" && git commit -q -m "docs: FEAT-[X] preview screens – [Feature Name]" && git push -q
```

Zeige dem User den Abschluss:

```
✅ Preview abgeschlossen für FEAT-[X]

Screens abgenommen:  [N] von [M]
Ground Truth:        features/FEAT-[X]-name/screens/

Nächster Schritt: /red-proto:dev FEAT-[X] – baut gegen diese Screens als visuelle Vorlage.
Nach einer Pause:  /red-proto:workflow zeigt dir exakt wo du stehst.
```

Wenn nicht alle Screens approved sind: klar machen, dass Dev trotzdem starten kann, aber die nicht-abgenommenen Screens als "outdated" markieren soll, wenn sich etwas ändert.

## Wiederholung

`/red-proto:preview FEAT-[X]` kann jederzeit erneut aufgerufen werden – z.B. nach einer Spec-Änderung. Bestehende approved Screens werden in dem Fall auf `outdated` gesetzt, bis sie neu bestätigt sind. Der Command erkennt beim Neustart vorhandene `outdated`-Einträge und bietet an, sie gezielt zu erneuern.

## Checklist

- [ ] Feature-Spec vorhanden und mindestens mit Requirements + UX befüllt
- [ ] Screen-Quelle gewählt (Figma-Links, File-Key, PNG-Upload oder manuell)
- [ ] Screens in `features/FEAT-[X]-name/screens/` abgelegt mit Naming `S-NN-*.png`
- [ ] `index.md` mit allen Metadaten befüllt
- [ ] Widerspruchs-Check gegen Spec durchgeführt
- [ ] User-Abnahme eingeholt
- [ ] Approved-Status in `index.md` aktualisiert
- [ ] Commit + Push
