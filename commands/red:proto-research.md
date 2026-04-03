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

Wenn Drafts gefunden: Informiere den User welche Dateien noch offen sind und springe direkt zu Phase 6 (Review und Speichern).

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

Diese Fragen klären ob das PRD eine Web-App, eine native Mobile-App oder beides impliziert. Die Antworten werden direkt an dev-setup weitergegeben.

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Auf welchen Geräten wird das Produkt primär genutzt?",
      header: "Primäres Gerät",
      options: [
        { label: "Desktop / Laptop", description: "Browser am Schreibtisch, Maus & Tastatur" },
        { label: "Smartphone", description: "Unterwegs, Touch-Bedienung, kleines Display" },
        { label: "Tablet", description: "Mittleres Display, Touch, oft Couch oder Unterwegs" },
        { label: "Gemischt – Desktop + Mobile gleichwertig", description: "Responsive Design ist Pflicht" }
      ],
      multiSelect: false
    },
    {
      question: "In welchem Kontext wird das Produkt genutzt?",
      header: "Nutzungskontext",
      options: [
        { label: "Am Schreibtisch / fokussiert", description: "Langer Session, viel Screen-Fläche, kein Ablenkungspotential" },
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

Dokumentiere die Antworten als `research/platform-context.md` mit Draft-Status – dev-setup liest diese Datei und passt die Tech-Stack-Empfehlung entsprechend an.

```markdown
---
status: draft
---

# Platform & Nutzungskontext
*Erstellt von: /red:proto-research — [Datum]*

## Primäres Gerät
[Antwort]

## Nutzungskontext
[Antwort]

## Mobile-Typ
[Antwort]

## Nutzungsfrequenz
[Antwort]

## Implikationen für Tech-Stack
[2–3 Sätze: Was bedeutet das für die Platform-Entscheidung?
z.B.: "Primär Mobile + Native gewünscht → React Native oder Flutter statt Next.js prüfen"
z.B.: "Desktop-fokussiert + täglicher Workflow → Web-App mit Keyboard-Shortcuts, Performance-Budget beachten"]
```

Dann dem User sagen:
```
📝 Draft gespeichert: research/platform-context.md

Kurze Pause?
→ Schreib `weiter` wenn du fertig bist

Echter Research (Interviews, Umfragen, Tage)?
→ Trag deine Findings direkt in die Datei ein
→ Dann /red:proto-research erneut aufrufen – ich erkenne den Draft automatisch
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

Speichere die Forschungsfragen als Draft in `research/research-questions.md`:

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

Dann stoppen und dem User sagen:
```
Forschungsfragen gespeichert in research/research-questions.md.

Führe deinen Research durch (Interviews, Umfragen, Beobachtungen) und trage
die Antworten direkt in die Datei ein – oder beschreibe sie mir beim nächsten Aufruf.

Wenn du fertig bist: /red:proto-research erneut aufrufen.
```

**Bei "Jetzt interaktiv beantworten":**

Gehe jede Frage einzeln durch. Stelle eine Frage im Chat und warte auf die Antwort bevor du zur nächsten gehst:

```
Frage 1 von [N]:
[Vollständiger Fragetext]

(Deine Antwort kann eine Vermutung, eine Beobachtung oder eine Erfahrung sein –
kein perfektes Research nötig, wir arbeiten mit dem was du weißt)
```

Sammle alle Antworten. Speichere danach `research/research-questions.md` als Draft:

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

Danach dem User mitteilen:
```
Antworten gespeichert. Weiter mit Phase 4 – Problem Statement Map.
```

Und direkt mit Phase 4 fortfahren.

## Phase 4: Problem Statement Map erstellen

Eine Problem Statement Map strukturiert das Kernproblem aus Nutzersicht:

```markdown
## Problem Statement Map

### Nutzer
[Wer hat das Problem? Kontext, Situation]

### Problem
[Was ist das konkrete Problem – aus Nutzerperspektive, nicht Lösungsperspektive]

### Impact
[Was sind die Folgen des Problems? Warum ist es wichtig?]

### Aktueller Workaround
[Wie lösen Nutzer das Problem heute? Warum reicht das nicht?]

### Erfolgskriterium
[Woran merkt der Nutzer, dass das Problem gelöst ist?]
```

Präsentiere zur Freigabe, passe auf Basis von Feedback an.

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

Personas-Format:
```markdown
## Persona: [Name]
**Kontext:** [Kurzbeschreibung]
**Ziele:** [Was will diese Person erreichen?]
**Frustrationen:** [Was hindert sie daran?]
**Tech-Affinität:** [Hoch/Mittel/Niedrig]
**Zitat:** "[Repräsentativer Satz dieser Person]"
```

## Phase 6: Review und Speichern

Zeige alle drei Artefakte zusammen. Frage nach Approval:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Sind Research-Grundlagen vollständig?",
      header: "Review",
      options: [
        { label: "Approved", description: "Alle Artefakte sind vollständig" },
        { label: "Anpassungen nötig", description: "Feedback im Chat" }
      ],
      multiSelect: false
    }
  ]
})
```

Nach Approval: Problem Statement Map und Personas als Drafts speichern (YAML `status: draft`, Header mit Dateinamen und Datum). User per CONVENTIONS.md §Resume Pattern (Option 2 – Research) informieren.

## Phase 6b: Finalisieren

Nach `weiter` oder Korrekturen: Alle Research-Dateien einlesen, Korrekturen übernehmen, `status: approved` in allen Dateien setzen.

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

**Modus A (Dev-Setup noch nicht gemacht):**

Sage dem User:
```
Research gespeichert.

Die Platform- und Nutzungskontext-Erkenntnisse stehen jetzt für den Tech-Stack bereit.
Nächster Schritt: /red:proto-dev-setup – ich berücksichtige research/platform-context.md bei der Stack-Empfehlung.
```

**Modus B, keine Features vorhanden:**

Sage dem User:
```
Research nachgeholt. Personas und Problem Statement stehen allen Agents zur Verfügung.
Nächster Schritt: /red:proto-requirements – Feature Specs definieren.
```

**Modus B, Features bereits vorhanden:**

Sage dem User:
```
Research nachgeholt.

Da bereits Feature-Specs existieren: Bitte /red:proto-requirements erneut aufrufen –
im Review-Modus prüfen wir ob die bestehenden Specs mit den neuen Research-Erkenntnissen
noch übereinstimmen oder angepasst werden müssen.

Nächster Schritt: /red:proto-requirements (Review bestehender Specs)
```

Öffne requirements und informiere es explizit, dass es im **Review-Modus** läuft: bestehende Specs gegen Research-Erkenntnisse prüfen, nicht neu schreiben.
