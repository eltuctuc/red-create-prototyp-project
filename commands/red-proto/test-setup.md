---
name: Test-Setup
description: Bereitet den Prototyp-Test vor – Personas (oder Proto-Personas) und Test-Hypothesen, die der Prototyp klären soll
---

> Lies `.claude/red-proto/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

## Phase 0: Draft-Erkennung bei Command-Neustart

```bash
DRAFTS=$(grep -rl "status: draft" test-setup/ 2>/dev/null)
if [ -n "$DRAFTS" ]; then
  echo "DRAFT-MODUS: Folgende Dateien warten auf Finalisierung:"
  echo "$DRAFTS"
fi
```

Wenn Drafts gefunden: Informiere den User welche Dateien noch offen sind und springe direkt zu Phase 4 (Finalisieren).

Du bereitest das Test-Setup für den Prototypen vor. Der Prototyp ist das Research-Instrument – dieser Command produziert also keine neuen Erkenntnisse über Nutzer, sondern klärt:

1. **Gegen wen wird getestet?** → Personas (bestehende nutzen oder Proto-Personas aus Material ableiten)
2. **Was soll der Prototyp beweisen?** → Test-Hypothesen

Keine Discovery, keine Problem-Statement-Map – das Problem ist in der PRD bereits gesetzt.

## Phase 1: Vorhandenes einlesen

```bash
cat prd.md
ls test-setup/ 2>/dev/null
```

Falls `test-setup/` bereits Dateien enthält: lies sie. Keine Duplikate.

Frage den User nach weiterem Material:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Hast du Unterlagen, die ich für Personas und Hypothesen einlesen soll?",
      header: "Input-Materialien",
      options: [
        { label: "Ja, ich gebe dir Dateipfade", description: "Bestehende Personas, Interviews, Analytics, Research-Dokumente" },
        { label: "Ja, ich paste den Inhalt", description: "Direkt im Chat" },
        { label: "Nein, wir arbeiten nur mit dem PRD", description: "Proto-Personas und Hypothesen aus der PRD ableiten" }
      ],
      multiSelect: false
    }
  ]
})
```

Bei Dateipfaden: Dateien vollständig lesen. Extrahiere:
- Bestehende Persona-Beschreibungen
- Nutzerzitate, Frustrationen, Verhaltensweisen
- Hinweise auf offene Fragen oder unklare Annahmen

## Phase 2: Personas

Ordner bei Bedarf anlegen (idempotent):

```bash
mkdir -p test-setup
```

**Wenn bestehende Personas vorhanden sind** (im eingelesenen Material oder bereits in `test-setup/personas.md`): direkt übernehmen, ggf. auf den Prototyp-Kontext zuschneiden. Nicht neu erfinden.

**Wenn keine Personas vorhanden sind:** Proto-Personas aus dem Material ableiten. Proto-Personas sind bewusst leichtgewichtig – sie dienen nur dazu, ein klares Test-Subjekt vor Augen zu haben, nicht als vollwertiges Research-Artefakt.

Stelle dazu gezielte Fragen:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Welche Nutzertypen willst du mit dem Prototypen testen?",
      header: "Test-Personas",
      options: [
        { label: "Technikaffine Early Adopters", description: "Probieren gern Neues aus, hohe Toleranz für Unfertiges" },
        { label: "Pragmatische Nutzer", description: "Wollen Aufgaben effizient erledigen" },
        { label: "Gelegenheitsnutzer", description: "Niedrige Einstiegshürde, brauchen Orientierung" },
        { label: "Power User", description: "Erwarten Tiefe und Effizienz" }
      ],
      multiSelect: true
    }
  ]
})
```

Für jede gewählte Persona kurze Follow-ups: Kontext, Ziel im Produkt, größte Frustration heute. Keine tiefen Research-Interviews – Proto-Level reicht.

Schreibe `test-setup/personas.md` direkt auf die Festplatte:

```markdown
---
status: draft
---

# Test-Personas
*Erstellt von: /red-proto:test-setup — [Datum]*
*Typ: [Bestehende Personas | Proto-Personas aus Material]*

## Persona: [Name]
**Kontext:** [Kurzbeschreibung]
**Ziel im Produkt:** [Was will diese Person konkret erreichen?]
**Größte Frustration heute:** [Was hindert sie aktuell?]
**Tech-Affinität:** [Hoch/Mittel/Niedrig]
**Zitat:** "[Repräsentativer Satz]"

...
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Personas gespeichert – passen die so für den Prototyp-Test?",
      header: "personas.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Weiter mit den Test-Hypothesen" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 3: Test-Hypothesen

Hypothesen formulieren, die der Prototyp klären soll. Eine gute Test-Hypothese hat drei Teile:

- **Annahme:** Was wir glauben
- **Begründung:** Warum wir das glauben (aus PRD/Material)
- **Test-Signal:** Woran wir im Prototyp-Test erkennen, ob die Annahme trägt

Entwickle 4–6 Hypothesen aus PRD + Material. Präsentiere sie im Chat, lass den User priorisieren und anpassen.

Schreibe danach `test-setup/hypotheses.md` direkt auf die Festplatte:

```markdown
---
status: draft
---

# Test-Hypothesen
*Erstellt von: /red-proto:test-setup — [Datum]*

Diese Hypothesen soll der Prototyp im Test klären.

## H1: [Kurztitel]
**Annahme:** [Was wir glauben]
**Begründung:** [Warum – Quelle: PRD / Material / Erfahrung]
**Test-Signal:** [Woran erkennen wir im Test, ob die Annahme trägt]
**Persona-Bezug:** [Welche Persona(s) betrifft das]

## H2: ...
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Hypothesen gespeichert – passt die Liste so?",
      header: "hypotheses.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Test-Setup abschließen" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 4: Finalisieren

Alle Dateien einzeln geprüft. Setze `status: approved` in allen Dateien in `test-setup/` und committe:

```bash
git add test-setup/
git commit -q -m "docs: add test-setup (personas and hypotheses)" && git push -q
```

Prüfe den aktuellen Stand:

```bash
DEV_SETUP_DONE=$([ -f project-config.md ] && echo "ja" || echo "nein")
FEATURES_EXIST=$(ls features/FEAT-*.md 2>/dev/null | wc -l)
echo "Dev-Setup: $DEV_SETUP_DONE | Feature-Specs: $FEATURES_EXIST"
```

Frage dann nach dem nächsten Schritt. Leite die passende Option dynamisch ab:

- **Kein `project-config.md`** → nächster Schritt ist `/red-proto:dev-setup`
- **`project-config.md` vorhanden, keine Features** → nächster Schritt ist `/red-proto:requirements`
- **`project-config.md` vorhanden, Features existieren** → nächster Schritt ist `/red-proto:requirements` im Review-Modus

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Test-Setup abgeschlossen. Wie weiter?",
      header: "Nächster Schritt",
      options: [
        {
          label: "[Dynamisch: /red-proto:dev-setup | /red-proto:requirements | /red-proto:requirements (Review-Modus)]",
          description: "[Dynamisch: passende Beschreibung je nach Modus]"
        },
        {
          label: "Pause – ich mache später weiter",
          description: "Alles ist gespeichert. /red-proto:workflow zeigt dir jederzeit wo du stehst"
        }
      ],
      multiSelect: false
    }
  ]
})
```
