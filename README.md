# red · Create Prototyp Project

Ein KI-gestütztes Product Development Framework für [Claude Code](https://claude.ai/code) – von der vagen Idee bis zum getesteten Prototyp, mit Human-in-the-Loop an jedem Schritt.

---

## Was ist das?

Eine Sammlung von Claude Code Commands, die eine vollständige Produktentwicklungs-Pipeline abbilden. Du beschreibst deine Idee in natürlicher Sprache – Claude führt die Pipeline aus, du triffst die Entscheidungen.

### Commands

```
/red-proto:workflow     → Nach jeder Pause: zeigt wo du stehst und was als nächstes zu tun ist

/red-proto:sparring     → Idee schärfen → PRD
/red-proto:test-setup   → Personas + Test-Hypothesen für den Prototyp
/red-proto:dev-setup    → Tech-Stack wählen, Projekt scaffolden, Git/GitHub einrichten
/red-proto:requirements → Feature Specs – einmal pro Feature, für ALLE Features
/red-proto:flows        → Screen-Inventar + verbindliche Transition-Tabelle (einmalig)
/red-proto:ux           → UX-Entscheidungen pro Feature
/red-proto:architect    → Technisches Design + Security + Test-Setup pro Feature
/red-proto:preview      → Abnahme-Screens aus Spec, vor Dev begutachten
/red-proto:dev          → Implementierung (Frontend + Backend parallel, falls nötig)
/red-proto:qa           → Tests + Accessibility + Security + Copy-Drift + Bug-Reports
/red-proto:dev-qa-loop  → Automatischer dev→qa-Loop bis Bugs unter Fix-Schwelle (alternativ zu manuellem Wechsel)
```

Jeder Command ist eigenständig – du kannst über `/red-proto:workflow` jederzeit wiedereinsteigen, er sagt dir wo du stehst. Commands bauen aufeinander auf: jeder liest den Output des vorherigen und ergänzt die gemeinsamen Artefakte.

### Workflow

**Einmalig pro Projekt:**

1. `/red-proto:sparring` – Idee in ein PRD überführen
2. `/red-proto:test-setup` *(empfohlen)* – Personas + Hypothesen für den späteren Prototyp-Test
3. **Design-System anlegen** *(empfohlen)* – `design-system/tokens/` befüllen (Farben, Typo, Spacing), damit `/red-proto:dev-setup` die Tokens in den Stack transportieren kann. Optional: auch Components/Patterns als Markdown ablegen
4. `/red-proto:dev-setup` – Tech-Stack wählen, Projekt scaffolden, DS-Tokens ins Projekt transportieren, Git/GitHub einrichten
5. `/red-proto:requirements` – Feature-Spec pro Feature, bis **alle** Features eine Spec haben
6. `/red-proto:flows` – einmaliges Screen-Inventar + Transitions über alle Features hinweg; wird pro Feature weiter ergänzt

**Pro Feature:**

7. `/red-proto:ux` – UX-Entscheidungen in die Spec; fragt optional nach Wireframes/Lo-Fi/Hi-Fi als Input
8. `/red-proto:architect` – Tech-Design, Security, Test-Setup in die Spec
9. `/red-proto:preview` *(optional)* – Abnahme-Screens erzeugen (Figma-MCP, PNG-Upload oder manuell) und vom User abnehmen lassen, bevor gebaut wird

**QA-Dev-Loop pro Feature** *(mindestens einmal):*

Zwei Wege – manuell oder automatisch:

- **Manuell:**
  10. `/red-proto:dev` – Implementierung, schreibt `context/FEAT-x-dev-handoff.md`
  11. `/red-proto:qa` – **in neuer Session** – Tests + Bug-Reports
  12. Bugs über Schwelle? → zurück zu 10. Keine Bugs → Feature fertig.

- **Automatisch** (empfohlen für längere Loops):
  10. `/red-proto:dev-qa-loop FEAT-X` – orchestriert die Iterationen selbst. In jeder Runde spawnt der Command zwei Subagenten (einen für dev, einen für qa), sammelt die Bugs, berechnet ein Risk-Level und iteriert, bis keine Bugs mehr über der Fix-Schwelle offen sind. Bei zwei aufeinanderfolgenden HIGH-Risk-Runden bietet er einen Exit an. Log liegt unter `context/FEAT-X-loop.log`.

**Wiedereinstieg:** `/red-proto:workflow` funktioniert an jedem Punkt und zeigt dir, wo du im Ablauf stehst.

### Workflow

```mermaid
flowchart TD
    A([Idee]) --> B

    subgraph setup["📐 Einmalig pro Projekt"]
        B["/red-proto:sparring<br/>Idee → PRD"]
        B --> T{Test-Setup?}
        T -->|empfohlen| TS["/red-proto:test-setup<br/>Personas + Hypothesen"]
        T -->|überspringen| DS
        TS --> DS{Design-System?}
        DS -->|empfohlen| DSA["Design-System anlegen<br/>design-system/tokens/"]
        DS -->|überspringen| C
        DSA --> C["/red-proto:dev-setup<br/>Tech-Stack + GitHub + DS-Transport"]
        C --> F["/red-proto:requirements<br/>Specs für alle Features"]
        F --> G["/red-proto:flows<br/>Screen-Inventar + Transitions (einmalig)"]
    end

    subgraph feature["🔁 Pro Feature wiederholen"]
        G --> H["/red-proto:ux<br/>UX-Entscheidungen"]
        H --> I["/red-proto:architect<br/>Tech-Design + Security + Tests"]
        I --> PRQ{Preview?}
        PRQ -->|optional| PR["/red-proto:preview<br/>Abnahme-Screens"]
        PRQ -->|überspringen| QL
        PR --> QL
    end

    subgraph loop["🔄 QA-Dev-Loop (mindestens 1x pro Feature)"]
        QL["/red-proto:dev<br/>Implementierung"]
        QL --> QL2["Handoff schreiben<br/>context/FEAT-x-dev-handoff.md"]
        QL2 --> K["/red-proto:qa<br/>Tests + Bugs (neue Session)"]
        K --> L{Bugs über Schwelle?}
        L -->|ja| QL
        L -->|grün ✅| M([Production-Ready])
    end

    M --> N{Weitere Features?}
    N -->|ja| H
    N -->|nein| O([Release 🎉])

    WF(["/red-proto:workflow<br/>Wiedereinstieg jederzeit"])
    WF -.-> setup
    WF -.-> feature
    WF -.-> loop
```

> **Session-Trennung im QA-Dev-Loop:** `/red-proto:dev` und `/red-proto:qa` laufen bewusst in getrennten Sessions. `/red-proto:dev` schreibt am Ende ein Handoff-File in `context/`, das `/red-proto:qa` in der neuen Session einliest. Das verhindert Kontext-Akkumulation und hält den Token-Verbrauch niedrig.

---

## Voraussetzungen

Pflicht:

- **[Claude Code](https://docs.anthropic.com/claude-code)** – eingerichtet und authentifiziert. Verfügbar als CLI, als Desktop-App (Mac/Windows), als Web-App (claude.ai/code) und als IDE-Extension (VS Code, JetBrains). Wichtig: die Chat-App „Claude" (claude.ai im Browser oder Claude Desktop) ist nicht dasselbe – sie führt keine Slash-Commands aus.
- **[Node.js ≥18](https://nodejs.org/)** mit `npm`/`npx` – für die Framework-Installation (`npx red-proto`).
- **Git** – das Framework commitet nach jedem Schritt, ohne Git funktioniert praktisch nichts.
- **Unix-kompatible Shell** – die Commands nutzen Bash-Syntax (`cat`, `grep`, `mkdir -p`, Heredocs).
  - macOS, Linux: nativ vorhanden
  - **Windows: WSL oder Git Bash** – PowerShell/cmd funktionieren nicht zuverlässig

Optional:

- **[`gh` CLI](https://cli.github.com/)** – nur wenn `/red-proto:dev-setup` ein GitHub-Repo anlegen soll.
- **Figma-MCP-Server** – nur wenn `/red-proto:preview` Screens direkt aus Figma ziehen soll. Ohne MCP lädst du PNGs im Chat hoch oder legst sie manuell ab.
- **Stack-Laufzeit** – Python, Go, Swift etc. werden erst nach der Stack-Wahl in `/red-proto:dev-setup` relevant, nicht vorher.

---

## Installation

### Schritt 1 – Framework mit `npx red-proto` installieren

```bash
npx red-proto@latest
```

Der Installer fragt interaktiv:

- **Lokal** (`./.claude/` im aktuellen Ordner) → Commands **und** Projektstruktur werden sofort angelegt. **Das reicht. Kein Schritt 2 nötig.**
- **Global** (`~/.claude/`) → Commands sind in allen Projekten verfügbar, aber die Projektstruktur muss separat pro Projekt angelegt werden → **Schritt 2 nötig**.

> **Hinweis:** Nicht global und lokal gleichzeitig installieren – Claude Code zeigt die Commands sonst doppelt an. Der Installer warnt dich, wenn eine andere Installation erkannt wird.

> **Update:** Denselben Befehl erneut ausführen – der Installer erkennt bestehende Installationen.

**Deinstallieren:**

```bash
npx red-proto --uninstall
```

Entfernt alle Commands und Agents – deine Projektdateien (`features/`, `test-setup/`, `prd.md` usw.) bleiben unangetastet.

---

### Schritt 2 – **Nur bei globaler Installation:** `/red-proto:create` pro Projekt ausführen

Überspringen, wenn du in Schritt 1 „Lokal" gewählt hast – dann ist alles bereits angelegt.

Bei globaler Installation legst du die Projektstruktur pro Projekt einmal an:

```bash
mkdir mein-projekt && cd mein-projekt
claude
```

Dann in Claude Code:

```
/red-proto:create
```

`/red-proto:create` legt dieselben Ordner (`test-setup/`, `features/`, `flows/`, `bugs/`, `docs/`, `context/`, `design-system/`) an, die bei lokaler Installation sofort entstehen.

---

### Loslegen

```
/red-proto:sparring
```

---

## Was wird installiert?

Nach dem Setup hat dein Projekt folgende Struktur:

```
./
  .claude/
    commands/          ← Alle Pipeline-Commands (red-proto:sparring, red-proto:dev, ...)
    agents/            ← Sub-Agents (frontend-developer, ux-reviewer, ...)
  design-system/       ← Optional: Tokens/Komponenten/Patterns als Markdown
    tokens/            ← Farben, Typografie, Spacing, Shadows, Motion
    components/        ← Button, Input, Card, ...
    patterns/          ← Navigation, Formulare, Feedback, Datendarstellung
    screens/           ← Referenz-Screens (Mockups globaler Patterns)
  features/
    STATUS.md          ← Zentraler Status-Index aller Features
    FEAT-1-name.md     ← Feature-Spec (erstellt von /red-proto:requirements,
                         akkumulativ ergänzt von ux, architect, dev, qa)
    FEAT-1-name/
      screens/         ← Optional: Abnahme-Screens (von /red-proto:preview)
        S-10-*.png
        index.md       ← Metadaten der Abnahme-Screens
  flows/               ← Screen-Inventar + verbindliche Transition-Tabellen
  test-setup/          ← Personas + Test-Hypothesen für Prototyp-Tests
  bugs/                ← Bug-Reports (werden nicht gelöscht, sondern zu -fixed.md)
  context/             ← Session-Handoffs (dev → qa Übergaben)
  docs/                ← Produktfähigkeiten + Release-Historie
  prd.md               ← Product Requirements Document (erstellt von /red-proto:sparring)
  project-config.md    ← Tech-Stack, Pfade, Versionierung
```

Details zu allen File-Formaten: [ARTIFACT_SCHEMA.md](./ARTIFACT_SCHEMA.md)

---

## Das Design System

Für einen Prototypen ist ein eigenes Design-System **nicht zwingend**. Du hast zwei Wege:

1. **Eigenes Design-System als Markdown** – du legst in `design-system/tokens/`, `components/` und `patterns/` deine Vorgaben ab, bevor `/red-proto:dev-setup` läuft. Der Dev-Setup transportiert die Tokens dann automatisch in das stack-spezifische Format (Tailwind-Config, CSS-Variablen, SwiftUI-Extensions, …). `/red-proto:preview` nutzt dieselben Markdowns, wenn Screens in Figma angelegt werden.
2. **UI-Library im Tech-Stack** – z.B. shadcn/ui, Material UI, Vuetify. Look & Feel kommt aus der Library selbst, und dieser Weg gewinnt: sobald eine UI-Library im Code-Verzeichnis installiert ist, ignorieren die Agents das Markdown-DS und bauen nach Library-Konventionen.

**Nicht kombinieren.** UI-Library und Markdown-DS beißen sich – wenn beides da ist, gewinnt die Library und das Markdown-DS wird stillschweigend ignoriert. Entscheide dich vor `/red-proto:dev-setup` für einen Weg.

> **Geplant für v0.20:** Aktuell bringt der Installer noch einen vorbefüllten, neutralen Design-System-Ordner mit. Für Weg 2 ist das Ballast. In v0.20 soll der Installer nur noch den leeren Ordner anlegen, und die Bevorzugung (Library-First, DS-Fallback) explizit in den Agents codiert werden.

Für Weg 1 gilt: Agents laden das Design-System **selektiv** – zuerst den Index, dann nur die konkret benötigten Komponenten- und Token-Files.

**Drei Zustände pro Komponente** (bei Weg 1 relevant):

| Status | Bedeutung |
|--------|-----------|
| `DS-konform` | Implementiert nach Spec – keine Anpassung nötig |
| `Tokens-Build` | Nutzt DS-Tokens, aber keine fertige Komponente vorhanden – Agent baut selbst |
| `Hypothesen-Test` | Bewusstes Abweichen – UX-Entscheidung mit Begründung |

---

## Empfohlene Skills

Das Framework läuft ohne zusätzliche Skills, nutzt sie aber wenn vorhanden:

| Skill | Genutzt von | Effekt |
|-------|-------------|--------|
| `ui-ux-pro-max` | `/red-proto:ux`, `ux-reviewer` Agent | Deutlich bessere UX-Qualität |
| `frontend-design` | `frontend-developer` Agent | Bessere Component-Implementierung |

Skills werden in Claude Code unter **Einstellungen → Skills** installiert.

---

## Framework-Philosophie

**Human-in-the-Loop:** Kein Agent geht alleine weiter – jeder Schritt braucht eine explizite Bestätigung.

**Akkumulativ statt überschreibend:** Jeder Agent ergänzt seinen Abschnitt im Feature-File, bestehende Abschnitte bleiben erhalten.

**Session-Trennung:** `/red-proto:dev` und `/red-proto:qa` laufen bewusst in getrennten Sessions. Das verhindert Kontext-Akkumulation und hält den Token-Verbrauch pro Session niedrig. Das Handoff-File in `context/` ist die Brücke.

**Flows als Navigationsvertrag:** `/red-proto:flows` erstellt eine verbindliche Transition-Tabelle, die UX und Developer als gemeinsame Quelle der Wahrheit nutzen. Undokumentierte Transitions werden gemeldet, nicht stillschweigend implementiert.

**Audit-Trail:** Bugs werden nicht gelöscht, sondern zu `-fixed.md` umbenannt.

**SemVer:** Automatisches Versioning – PATCH bei Bug-Fixes, MINOR bei neuen Features, MAJOR bei intentionalem Release.

---

## Lizenz

MIT
