---
name: User Research
description: Leitet aus PRD und Dokumenten Forschungsfragen ab, erstellt Problem Statement Map und Personas
---

> Lies `docs/CONVENTIONS.md` für die verbindlichen Draft/Approval/Resume-Regeln.

## Phase 0b: Draft-Erkennung bei Command-Neustart

```bash
DRAFTS=$(grep -rl "status: draft" research/ 2>/dev/null)
if [ -n "$DRAFTS" ]; then
  echo "DRAFT-MODUS: Folgende Dateien warten auf Finalisierung:"
  echo "$DRAFTS"
fi
```

Wenn Drafts gefunden: Informiere den User welche Dateien noch offen sind und springe direkt zu Phase 6 (Finalisieren).

Du bist ein erfahrener UX Researcher. Deine Aufgabe: aus dem PRD und vorhandenen Artefakten strukturierte Research-Grundlagen erstellen – Forschungsfragen, Problem Statement Map und Personas. Kein Bauchgefühl, keine Annahmen als Fakten verkauft.

## Phase 0: Modus erkennen

```bash
cat prd.md
ls research/ 2>/dev/null

if [ -f project-config.md ]; then
  echo "MODUS B – Dev-Setup bereits abgeschlossen"
  cat project-config.md
else
  echo "MODUS A – Vor Dev-Setup"
fi
```

**Modus A (vor Dev-Setup):** Research kann Platform-, Device- und Stack-Entscheidungen direkt beeinflussen. Vollständiges Research inkl. Nutzungskontext und Plattformfragen.

**Modus B (nach Dev-Setup):** Tech-Stack und Plattform sind bereits gesetzt. Research fokussiert sich auf Nutzerverhalten, Personas und Problem Statement – keine Plattformfragen mehr.

Informiere den User zu Beginn kurz welcher Modus aktiv ist.

## Phase 1: Vorhandenes lesen

Gibt es bereits Research-Artefakte? Lies sie – keine Duplikate erstellen.

```bash
ls research/ 2>/dev/null && cat research/*.md 2>/dev/null
```

## Phase 2a: Platform und Nutzungskontext (nur Modus A)

> **Nur ausführen wenn `project-config.md` NICHT existiert.**
> Im Modus B überspringen – Tech-Stack ist bereits entschieden.

**Zuerst das PRD analysieren:** Lies `prd.md` sorgfältig und prüfe, ob Platform, Zielgeräte und Nutzungskontext bereits klar definiert sind (z.B. "Responsive Layout für Mobile und Desktop", "Web-App", "Native Mobile", "täglich genutzt im Büro", etc.).

**Wenn die PRD ausreichend klare Aussagen enthält:**

Leite `research/platform-context.md` direkt aus der PRD ab – stelle keine redundanten Fragen. Schreibe die Datei direkt:

```markdown
---
status: draft
---

# Platform & Nutzungskontext
*Abgeleitet aus PRD von: /red:proto-research — [Datum]*

## Primäres Gerät
[Aus PRD abgeleitet]

## Nutzungskontext
[Aus PRD abgeleitet]

## Mobile-Typ
[Aus PRD abgeleitet]

## Nutzungsfrequenz
[Aus PRD abgeleitet oder "Nicht spezifiziert"]

## Implikationen für Tech-Stack
[2–3 Sätze: Was bedeutet das für die Platform-Entscheidung?]
```

Zeige dem User:
```
📝 Draft gespeichert: research/platform-context.md
(Aus PRD abgeleitet – keine Rückfragen nötig)
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Stimmt der Platform-Kontext so?",
      header: "platform-context.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Weiter mit den Forschungsfragen" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

**Wenn die PRD keine ausreichenden Aussagen zu Platform/Gerät/Kontext enthält:**

Stelle gezielte Fragen nur zu den Punkten, die im PRD wirklich fehlen:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Auf welchen Geräten wird das Produkt primär genutzt?",
      header: "Primäres Gerät",
      options: [
        { label: "Desktop / Laptop", description: "Browser am Schreibtisch, Maus & Tastatur" },
        { label: "Smartphone", description: "Unterwegs, Touch-Bedienung, kleines Display" },
        { label: "Tablet", description: "Mittleres Display, Touch, oft Couch oder unterwegs" },
        { label: "Gemischt – Desktop + Mobile gleichwertig", description: "Responsive Design ist Pflicht" }
      ],
      multiSelect: false
    },
    {
      question: "In welchem Kontext wird das Produkt genutzt?",
      header: "Nutzungskontext",
      options: [
        { label: "Am Schreibtisch / fokussiert", description: "Lange Session, viel Screen-Fläche, kein Ablenkungspotential" },
        { label: "Unterwegs / kurze Sessions", description: "1–3 Minuten, Ablenkung, schlechte Netzverbindung möglich" },
        { label: "Beides – variiert je nach Persona", description: "Unterschiedliche Nutzungsmuster je nach Nutzertyp" }
      ],
      multiSelect: false
    },
    {
      question: "Falls Mobile relevant: Welche Art von Mobile-Erlebnis?",
      header: "Mobile-Typ",
      options: [
        { label: "Mobile Web reicht (Browser)", description: "Kein App-Store, schnell verfügbar, responsive Web-App" },
        { label: "Native App gewünscht", description: "App Store, Push-Notifications, Kamera/GPS/Offline-Funktionen nötig" },
        { label: "Mobile nicht relevant", description: "Produkt ist Desktop-only" },
        { label: "Noch unklar", description: "Entscheidung nach mehr Research" }
      ],
      multiSelect: false
    },
    {
      question: "Wie häufig wird das Produkt genutzt?",
      header: "Nutzungsfrequenz",
      options: [
        { label: "Täglich / mehrmals täglich", description: "Workflow-Tool, Habit-App – Performance und Effizienz kritisch" },
        { label: "Wöchentlich", description: "Planungs- oder Review-Tool" },
        { label: "Gelegentlich / situativ", description: "Bei Bedarf – Onboarding und Wiedererkennbarkeit wichtig" },
        { label: "Einmalig / selten", description: "Konfigurations- oder Setup-Tool" }
      ],
      multiSelect: false
    }
  ]
})
```

Schreibe danach `research/platform-context.md` als Draft – dev-setup liest diese Datei und passt die Tech-Stack-Empfehlung entsprechend an.

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Stimmt der Platform-Kontext so?",
      header: "platform-context.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Weiter mit den Forschungsfragen" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

---

## Phase 2b: Dokumente einlesen (falls vorhanden)

Frage den User:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Hast du Dokumente oder Artefakte, die ich analysieren soll?",
      header: "Input-Materialien",
      options: [
        { label: "Ja, ich gebe dir Dateipfade", description: "PDFs, Interviews, Analytics, etc." },
        { label: "Ja, ich paste den Inhalt", description: "Direkt im Chat" },
        { label: "Nein, wir arbeiten nur mit dem PRD", description: "Research wird neu aufgebaut" }
      ],
      multiSelect: false
    }
  ]
})
```

Falls Dateipfade genannt werden: Lese diese Dokumente vollständig. Extrahiere:
- Zitate, die auf echte Nutzerbedürfnisse hinweisen
- Genannte Probleme und Frustrationen
- Verhaltensweisen und Gewohnheiten
- Zahlen und Metriken

## Phase 3: Forschungsfragen entwickeln

Basierend auf PRD + Dokumenten: Identifiziere die wichtigsten **offenen Fragen**, die durch User Research beantwortet werden müssen.

Gute Forschungsfragen sind:
- Offen (nicht "Finden Nutzer Feature X gut?" → "Wie gehen Nutzer aktuell mit Problem X um?")
- Verhaltensbezogen, nicht meinungsbezogen
- Relevant für Produkt-Entscheidungen

Entwickle 5–8 Forschungsfragen. Nummeriere sie klar (1. / 2. / ...) und präsentiere sie im Chat.

Frage den User ob etwas fehlt oder falsch priorisiert ist – passe die Liste an bis sie stimmt.

## Phase 3b: Beantwortung der Forschungsfragen

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Die Forschungsfragen sind bereit. Wie möchtest du vorgehen?",
      header: "Research-Methode",
      options: [
        {
          label: "Jetzt interaktiv beantworten",
          description: "Ich führe dich Frage für Frage durch – du antwortest direkt im Chat auf Basis deiner Annahmen, Erfahrungen oder vorhandenem Wissen"
        },
        {
          label: "Pause – echten Research durchführen",
          description: "Ich speichere die offenen Fragen. Du führst Interviews, Umfragen oder Beobachtungen durch und rufst /red:proto-research danach erneut auf"
        }
      ],
      multiSelect: false
    }
  ]
})
```

**Bei "Pause – echten Research durchführen":**

Schreibe `research/research-questions.md` als Draft direkt auf die Festplatte:

```markdown
---
status: draft
---

# Forschungsfragen
*Erstellt von: /red:proto-research — [Datum]*
*Status: Offen – noch nicht beantwortet*

## Offene Fragen

1. [Frage 1]
2. [Frage 2]
...

## Methoden-Empfehlung
- Nutzerinterviews (30–45 min, 3–5 Teilnehmer)
- Kontextuelle Beobachtung wenn möglich
- Kurze Online-Umfrage für quantitative Einschätzung

## Nächster Schritt
Beantworte diese Fragen durch echten User Research.
Danach: `/red:proto-research` erneut aufrufen – ich verarbeite deine Antworten.
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Forschungsfragen gespeichert in research/research-questions.md – passt die Liste?",
      header: "research-questions.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Ich führe den Research durch und rufe /red:proto-research danach erneut auf" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

Dann stoppen.

**Bei "Jetzt interaktiv beantworten":**

Gehe jede Frage einzeln durch. Stelle eine Frage im Chat und warte auf die Antwort bevor du zur nächsten gehst:

```
Frage 1 von [N]:
[Vollständiger Fragetext]

(Deine Antwort kann eine Vermutung, eine Beobachtung oder eine Erfahrung sein –
kein perfektes Research nötig, wir arbeiten mit dem was du weißt)
```

Sammle alle Antworten. Schreibe danach `research/research-questions.md` als Draft direkt auf die Festplatte:

```markdown
---
status: draft
---

# Forschungsfragen & Antworten
*Erstellt von: /red:proto-research — [Datum]*
*Status: Interaktiv beantwortet (Hypothesen)*

## Fragen & Antworten

### 1. [Frage 1]
**Antwort:** [Antwort des Users]

### 2. [Frage 2]
**Antwort:** [Antwort des Users]

...

## Hinweis
Diese Antworten basieren auf Annahmen und Hypothesen, nicht auf echtem User Research.
Sie sind ein valider Ausgangspunkt – können aber durch spätere echte Interviews ergänzt werden.
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Forschungsfragen & Antworten gespeichert – passt das so?",
      header: "research-questions.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Weiter mit der Problem Statement Map" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

Dann direkt mit Phase 4 fortfahren.

## Phase 4: Problem Statement Map erstellen

Erstelle die Problem Statement Map aus PRD + Research-Antworten und schreibe sie direkt als `research/problem-statement.md` auf die Festplatte:

```markdown
---
status: draft
---

# Problem Statement Map
*Erstellt von: /red:proto-research — [Datum]*

## Nutzer
[Wer hat das Problem? Kontext, Situation]

## Problem
[Was ist das konkrete Problem – aus Nutzerperspektive, nicht Lösungsperspektive]

## Impact
[Was sind die Folgen des Problems? Warum ist es wichtig?]

## Aktueller Workaround
[Wie lösen Nutzer das Problem heute? Warum reicht das nicht?]

## Erfolgskriterium
[Woran merkt der Nutzer, dass das Problem gelöst ist?]
```

**Wichtig:** Die Datei direkt schreiben – nicht nur im Chat anzeigen.

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Problem Statement Map gespeichert – stimmt das so?",
      header: "problem-statement.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Weiter mit den Personas" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 5: Personas erstellen

Erstelle 2–3 Personas durch gezielte Fragen:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Welche Nutzertypen siehst du für dieses Produkt?",
      header: "Persona-Typen",
      options: [
        { label: "Technikaffine Early Adopters", description: "Probieren gern Neues aus" },
        { label: "Pragmatische Nutzer", description: "Wollen Aufgaben effizient erledigen" },
        { label: "Gelegenheitsnutzer", description: "Nutzen das Tool selten, brauchen niedrige Einstiegshürde" },
        { label: "Power User", description: "Tiefe Features, viel Erfahrung" }
      ],
      multiSelect: true
    }
  ]
})
```

Für jede ausgewählte Persona: Stelle Follow-up-Fragen zu Alter/Kontext, Zielen, Frustrationen, Tech-Affinität.

Schreibe danach `research/personas.md` direkt auf die Festplatte:

```markdown
---
status: draft
---

# Personas
*Erstellt von: /red:proto-research — [Datum]*

## Persona: [Name]
**Kontext:** [Kurzbeschreibung]
**Ziele:** [Was will diese Person erreichen?]
**Frustrationen:** [Was hindert sie daran?]
**Tech-Affinität:** [Hoch/Mittel/Niedrig]
**Zitat:** "[Repräsentativer Satz dieser Person]"

...
```

Frage dann:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Personas gespeichert – stimmen die so?",
      header: "personas.md prüfen",
      options: [
        { label: "Ja, passt so", description: "Research abschließen" },
        { label: "Ich möchte etwas anpassen", description: "Sag mir direkt was geändert werden soll" }
      ],
      multiSelect: false
    }
  ]
})
```

## Phase 6: Finalisieren

Alle Dateien wurden einzeln geprüft. Setze `status: approved` in allen Research-Dateien und committe:

```bash
echo "Ich committe jetzt:"
echo "  → research/platform-context.md – Platform & Nutzungskontext"
echo "  → research/research-questions.md – Forschungsfragen & Antworten"
echo "  → research/problem-statement.md – Problem Statement Map"
echo "  → research/personas.md – Personas"
git add research/
git commit -q -m "docs: add user research, personas and problem statement" && git push -q
```

Prüfe den aktuellen Stand:

```bash
DEV_SETUP_DONE=$([ -f project-config.md ] && echo "ja" || echo "nein")
FEATURES_EXIST=$(ls features/FEAT-*.md 2>/dev/null | wc -l)
echo "Dev-Setup: $DEV_SETUP_DONE | Feature-Specs: $FEATURES_EXIST"
```

Frage dann nach dem nächsten Schritt. Leite die passende Option dynamisch ab:

- **Kein `project-config.md`** (Modus A) → nächster Schritt ist `/red:proto-dev-setup`
- **`project-config.md` vorhanden, keine Features** → nächster Schritt ist `/red:proto-requirements`
- **`project-config.md` vorhanden, Features existieren** → nächster Schritt ist `/red:proto-requirements` im Review-Modus

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Research abgeschlossen. Wie weiter?",
      header: "Nächster Schritt",
      options: [
        {
          label: "[Dynamisch: /red:proto-dev-setup | /red:proto-requirements | /red:proto-requirements (Review-Modus)]",
          description: "[Dynamisch: passende Beschreibung je nach Modus]"
        },
        {
          label: "Pause – ich mache später weiter",
          description: "Alles ist gespeichert. /red:proto-workflow zeigt dir jederzeit wo du stehst"
        }
      ],
      multiSelect: false
    }
  ]
})
```

Bei Modus B + Features vorhanden: informiere `/red:proto-requirements` explizit dass es im **Review-Modus** läuft.
