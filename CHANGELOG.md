# Changelog

Alle nennenswerten Änderungen an red · Create Prototyp Project sind hier dokumentiert.
Neueste Version zuerst – ältere Versionen weiter unten.

---

## v0.19.3 — 20. April 2026

README aufgeräumt. Voraussetzungen sind jetzt vollständig – inklusive der Windows-Realität.

### Fixes

- **Mermaid-Diagramm repariert:** Der Node-Name `P` war zweimal vergeben – einmal als Preview-Entscheidung, einmal als Workflow-Node. Mermaid hat sie als denselben Node behandelt, das Diagramm war stillschweigend kaputt. Außerdem: Gruppen sauberer strukturiert (Einmalig / Pro Feature / QA-Dev-Loop), Design-System als eigener Schritt sichtbar gemacht, Newlines in Labels auf `<br/>` umgestellt.
- **Installation klarer:** Schritt 2 (`/red-proto:create`) ist jetzt explizit als „nur bei globaler Installation nötig" markiert. Wer lokal installiert, ist nach Schritt 1 fertig – ohne Rätselraten.
- **Projekt-Struktur stimmt:** Feature-Spec-Dateien (`features/FEAT-1-name.md`) und Abnahme-Screens (`features/FEAT-1-name/screens/`) sind jetzt richtig nebeneinander dargestellt, nicht mehr missverständlich verschachtelt.
- **Alte Command-Namen ausgemistet:** `/red:proto-dev-setup` (Schreibweise vor v0.17.0) ist aus den Voraussetzungen raus, `proto-dev`/`proto-qa` in der Philosophie-Sektion auf die aktuellen Namen umgestellt. Die Manual-Installationsanleitung mit dem alten Pfad `commands/red\:proto.md` ist entfernt – `npx red-proto` ist der einzige Weg.

### Neue Informationen

- **Vollständige Voraussetzungen:** Pflicht (Claude Code CLI/IDE, Node.js ≥18, Git, Unix-Shell) und optional (gh, Figma-MCP, Stack-Laufzeit) getrennt aufgeführt. Windows-Hinweis auf WSL/Git Bash explizit – wer in PowerShell arbeitet, weiß jetzt vorher, dass es nicht läuft.
- **Design-System-Abschnitt ehrlicher:** Es gibt zwei Wege – eigenes Markdown-DS oder UI-Library im Stack. Der aktuell mitgelieferte neutrale Starter kollidiert mit Weg 2 und wird in einem späteren Release (v0.20) entfernt. Bis dahin ist der Hinweis drin, damit niemand über stillschweigende Konflikte stolpert.

---

## v0.19.2 — 20. April 2026

### Fixes

- **Einheitliche Phasen-Nummerierung im `frontend-developer`-Agent:** Der Agent hatte bisher eine gemischte Nummerierung mit `1b-Validation`, `1.5`, `1.6`, `1.7` und `4.5` – alles ohne erkennbare Logik zum Rest. Jetzt durchgängig Buchstaben-Suffix: 1b, 1c, 1d, 1e, 1f, 1g und 4b. Kein Fremdkörper mehr.

---

## v0.19.1 — 20. April 2026

### Fixes

- **Einheitliche Phasen-Nummerierung in allen Commands:** Die Commands `/red-proto:dev` und `/red-proto:qa` vermischten historisch Buchstaben-Suffixe (`1b`, `4b`) und Dezimal-Einschübe (`1.5`, `1.6`, `1.7`, `2.5`, `4.5`). Jetzt durchgängig Buchstaben-Suffix – Phase 1 hat Sub-Phasen 1b, 1c, 1d, 1e statt 1.5–1.7. Lesbarkeit und Konsistenz deutlich besser.
- **Fehlende Phase 5 in `/red-proto:requirements`:** Der Command sprang historisch von Phase 4 direkt auf Phase 6 und ließ 5 aus. Phasen sind jetzt lückenlos 0–6, 6b.
- **Verweis in CONVENTIONS.md:** Bezog sich noch auf die alte `Phase 1.7` in dev, jetzt auf `Phase 1e`.

---

## v0.19.0 — 20. April 2026

Von der vagen Idee zum Screen, den der Nutzer abnicken kann, bevor eine Zeile Code entsteht.

### Neue Features

- **Design-System ist Teil des Weges, nicht Deko:** `/red-proto:dev-setup` prüft vor der Stack-Wahl, ob `design-system/tokens/` befüllt ist. Die Tokens beeinflussen die Empfehlung (Tailwind, CSS-Variablen, SwiftUI-Extensions, was auch immer passt) und werden beim Scaffold automatisch ins Projekt transportiert. Leeres DS? Der Workflow erinnert dich daran, bevor gescaffoldet wird – überspringen ist erlaubt, aber nicht stillschweigend.
- **`/red-proto:preview` – optionaler Abnahme-Pass vor Dev:** Nachdem Requirements, UX und Architect-Design stehen, kannst du Screens aus der Spec erzeugen lassen – per Figma-Node-Link, aus einer konfigurierten Figma-File, per PNG-Upload oder manuell abgelegt. Der Command legt sie in `features/FEAT-X-name/screens/` ab und holt deine Abnahme ein, bevor `/red-proto:dev` anfängt zu bauen. Kein visuelles QA, kein Rätselraten für den Entwickler – du siehst vorher, was kommt.
- **UX fragt aktiv nach Design-Vorgaben:** `/red-proto:ux` fragt optional nach Wireframes, Low- oder High-Fi-Screens – als Figma-Links oder als Bilder im Chat. Wenn welche da sind, schärft das die UX-Entscheidungen. Wenn nicht, arbeitet der Agent wie bisher aus Spec + PRD + Design-System.
- **Copy-Inventar stack-agnostisch:** Wenn die Feature-Spec ein `Copy-Inventar (Ground Truth)` enthält, pflegt `/red-proto:dev` die Texte **zeichen-genau** in eine zentrale Copy-Datei ein – je nach Stack `copy.ts`, `copy.py`, `copy.go`, `Copy.swift` oder `copy.json`. `/red-proto:qa` prüft mechanisch per `grep` auf Drift: fehlt ein Text, ist er dupliziert, oder steht er hardcoded in einer Komponente? Alles automatisch ein Bug. Löst ein LLM-Problem, das sonst unsichtbar bis zum Kunden durchrutscht.

### Was sich ändert

- `/red-proto:dev-setup` empfiehlt Tech-Stacks jetzt immer inklusive Design-System-Transport – die Empfehlung nennt explizit, wie deine Tokens im Projekt landen
- `project-config.md` hat zwei neue Abschnitte: `Design-System-Transport` und `Figma-Quellen`
- `/red-proto:workflow` zeigt Design-System als eigenen Vorbereitungs-Schritt und verweist auf `/red-proto:preview`, solange kein Dev gelaufen ist
- Die Pipeline im README und in der Workflow-Übersicht zeigt jetzt beide optionalen Gates: Design-System vor Dev-Setup, Preview vor Dev

### Verbesserungen

- **Tool-Unabhängigkeit zieht sich durch:** Figma bleibt First-Class-Bürger, aber an keiner Stelle verlangt das Framework Figma. PNG-Upload im Chat, manuelle Ablage und konfigurierter File-Key sind gleichwertig. Kein rigides Naming-Schema mehr – Node-Links und Bilder reichen.
- **Kein probabilistisches QA:** Visuelle Abnahme bleibt menschliche Aufgabe. Copy-Drift ist dagegen deterministisch geprüft. Das Framework verspricht nichts, was es nicht halten kann.

---

## v0.18.0 — 19. April 2026

Research war der falsche Name für das, was wirklich vor dem Prototyp passieren muss.

### Neue Features

- **`/red-proto:test-setup` ersetzt `/red-proto:research`:** Der Command heißt jetzt wie das, was er tut – er bereitet den späteren Prototyp-Test vor, statt Discovery-Research zu betreiben. Fokus: Personas (oder Proto-Personas aus vorhandenem Material) und Test-Hypothesen, die der Prototyp klären soll. Keine Problem-Statement-Map mehr – das Problem ist spätestens im PRD gesetzt, sonst würdest du gar nicht prototypen.
- **Test-Hypothesen statt Forschungsfragen:** Jede Hypothese hat jetzt vier Felder: Annahme, Begründung, Test-Signal (woran erkennen wir im Test, ob sie trägt) und Persona-Bezug. Damit wird der Prototyp-Test von Anfang an mit einem klaren "was wollen wir eigentlich wissen?" verknüpft.
- **Platform-Kontext direkt in `/red-proto:dev-setup`:** Die Frage "auf welchem Gerät läuft das Produkt?" hat nichts mit Nutzer-Research zu tun, sondern mit der Tech-Stack-Wahl. Sie lebt jetzt dort, wo sie hingehört. Wenn die PRD klar ist, leitet dev-setup sie direkt ab; nur bei Lücken wird noch gefragt.

### Was sich ändert (Breaking Change)

| Alt | Neu |
|-----|-----|
| `/red-proto:research` | `/red-proto:test-setup` |
| Ordner `research/` | Ordner `test-setup/` |
| `research/personas.md` | `test-setup/personas.md` |
| `research/research-questions.md` | `test-setup/hypotheses.md` |
| `research/problem-statement.md` | entfällt |
| `research/platform-context.md` | entfällt (wandert in dev-setup) |

Bestehende Projekte mit `research/`-Verzeichnis sind davon nicht automatisch betroffen – die Dateien bleiben liegen. Wenn du das Rename mitziehen willst: Ordner umbenennen und ggf. `problem-statement.md` löschen.

### Verbesserungen

- **Klarer Mental-Flow:** Idee → für wen testen wir? → Technik → Features. Test-Setup liegt jetzt bewusst vor Dev-Setup – das Framework führt den Nutzer in der Reihenfolge, die auch inhaltlich passt.
- **Alle Begleit-Dokumente angepasst:** README, ARTIFACT_SCHEMA, CONVENTIONS, Install-Skript und alle Commands referenzieren den neuen Namen und Pfad. Keine widersprüchlichen Verweise mehr.

---

## v0.17.1 — 12. April 2026

Alle Docs sprechen jetzt dieselbe Sprache.

### Fixes

- **Command-Namen in allen Dokumenten korrigiert:** README, ARTIFACT_SCHEMA, Design System, Templates, Agents und Conventions enthielten noch die alten `/red:proto-*`-Namen aus der Zeit vor v0.17.0. Wer die Doku las, sah andere Befehle als die, die tatsächlich funktionieren. Alle 35 Stellen sind jetzt auf `/red-proto:*` aktualisiert.

---

## v0.17.0 — 12. April 2026

Commands wohnen jetzt in einer eigenen Schublade.

### Neue Features

- **Gekapselter Namespace für alle Commands:** Statt `red:proto-workflow.md` direkt im `commands/`-Ordner liegen alle Commands jetzt unter `commands/red-proto/`. Claude Code ruft sie als `/red-proto:workflow`, `/red-proto:sparring` usw. auf – sauber getrennt von anderen Frameworks die möglicherweise denselben Ordner nutzen.
- **`/red-proto:create` statt `/red:proto`:** Der Haupt-Setup-Command heißt jetzt konsequent wie das Framework – `/red-proto:create`. Macht klar was er tut, und passt zur neuen Namenslogik.

### Was sich ändert (Breaking Change)

Die alten Command-Namen (`/red:proto`, `/red:proto-workflow` etc.) funktionieren nach dem Update nicht mehr. Nach `npx red-proto` (Update) sind ausschließlich die neuen Namen aktiv:

| Alt | Neu |
|-----|-----|
| `/red:proto` | `/red-proto:create` |
| `/red:proto-workflow` | `/red-proto:workflow` |
| `/red:proto-sparring` | `/red-proto:sparring` |
| `/red:proto-dev-setup` | `/red-proto:dev-setup` |
| `/red:proto-research` | `/red-proto:research` |
| `/red:proto-requirements` | `/red-proto:requirements` |
| `/red:proto-flows` | `/red-proto:flows` |
| `/red:proto-ux` | `/red-proto:ux` |
| `/red:proto-architect` | `/red-proto:architect` |
| `/red:proto-dev` | `/red-proto:dev` |
| `/red:proto-qa` | `/red-proto:qa` |

---

## v0.16.1 — 5. April 2026

### Fixes

- **`/red:proto` findet jetzt alle Dateien die es kopieren soll:** Bei globalem Install (`npx red-proto`) wurden `docs/` und `design-system/` nicht in `~/.claude/templates/red-create-prototyp-project/` abgelegt – dadurch fehlten nach `/red:proto` Bug-Templates, CONVENTIONS.md und das Design System still und lautlos. Ab jetzt befüllt der globale Install diese Quelle vollständig.
- **Veraltete Command-Namen im Installations-Check behoben:** `/red:proto` erkannte nicht mehr ob das Framework bereits installiert ist, weil es auf alte Namen (`ux-design`, `solution-architect`) statt auf aktuelle `red:proto-*` Namen prüfte.
- **Explizite Verifikation nach dem Kopieren:** Wenn eine kritische Datei nach dem Install fehlt, erscheint jetzt eine klare Warnung mit Lösungshinweis – statt stillem Erfolg der erst beim nächsten QA-Run auffällt.

---

## v0.16.0 — 5. April 2026

Endlich weiß man, ob ein Feature wirklich abgenommen ist – oder ob QA gerade noch kämpft.

### Neue Features

- **QA-Status mit 3 Zuständen:** ⬜ nicht geprüft · 🔄 Dev-Loop läuft (inkl. Anzahl offener Bugs nach Severity) · ✅ abgenommen. Der Haken kommt jetzt nur noch durch explizite Nutzer-Entscheidung – kein automatisches ✅ solange Bugs über der Schwelle offen sind.
- **"Abgenommen mit Known Issues":** Nutzer können ein Feature trotz offener Bugs bewusst als fertig deklarieren. Der Status zeigt dann `✅⚠️ N Low offen` – transparent, kein stilles Wegignorieren.
- **Feature-Tabelle in STATUS.md mit Einzelspalten:** Jede Phase (Spec, UX, Tech, Dev, QA) hat jetzt eine eigene Spalte mit dem jeweiligen Symbol. Auf einen Blick sichtbar, wo jedes Feature im Build-Loop steht.
- **Legende in STATUS.md und Workflow-Ausgabe:** ⬜/🔄/✅/✅⚠️/❌ sind jetzt überall erklärt – kein Rätselraten mehr was ein Symbol bedeutet.

### Verbesserungen

- **`qa_status` im Feature-File Frontmatter:** QA schreibt nach jedem Run den genauen Zustand ins Feature-File. `/red:proto-workflow` liest daraus – der Entscheidungsbaum in Phase 3 nutzt `qa_status` direkt statt Status-Heuristiken.
- **Folge-Run-Frage klarer:** Die dritte Option heißt jetzt explizit "Als abgenommen markieren" mit erklärender Beschreibung – statt dem vagen "Loop beenden".

---

## v0.15.1 — 5. April 2026

### Fixes

- **Widerspruch in `.npmignore` behoben:** `docs/` war fälschlicherweise ausgeschlossen, obwohl `package.json` es explizit einschließt. Das `files`-Feld hatte zwar Vorrang, aber die irreführende Zeile ist jetzt entfernt.

---

## v0.15.0 — 5. April 2026

### Verbesserungen

- **Projektroot bleibt sauber:** Framework-Dateien (Templates, SCAFFOLDING, CONVENTIONS) landen jetzt in `.claude/red-proto/` statt im `docs/`-Ordner des Projekts. Der Projektroot zeigt nur noch eigene Projektdateien – kein Framework-Overhead mehr sichtbar.

---

## v0.14.3 — 5. April 2026

### Fixes

- **Templates werden jetzt tatsächlich mitgeliefert:** Die `docs/`-Ordner (Templates + SCAFFOLDING.md + CONVENTIONS.md) fehlten beim npm-Publish und beim Install-Script – ein stiller Bruch der durch die Token-Optimierung in v0.14.1 entstanden ist. Ab jetzt werden Templates bei der Installation ins Zielprojekt kopiert, sind im npm-Package enthalten, und werden auch beim manuellen `/red:proto`-Setup übertragen. Entschuldigung für den Fehler.

---

## v0.14.2 — 5. April 2026

### Verbesserungen

- **Weniger Klicks beim Dev-Setup:** Die fünf aufeinanderfolgenden Rückfragen in `/red:proto-dev-setup` (Stack, Verzeichnis, GitHub, Repo-Name, Repo-Inhalt) wurden auf drei Blöcke reduziert – Verzeichnis und GitHub landen jetzt in einem Schritt, Repo-Name und Inhalt ebenfalls.
- **Commit-Ankündigungen entfernt:** Die `echo`-Zeilen vor jedem `git add` in `/red:proto-requirements`, `/red:proto-research`, `/red:proto-flows` und `/red:proto-sparring` waren redundant – der Agent kommuniziert im Chat was er tut.

---

## v0.14.1 — 5. April 2026

### Verbesserungen

- **Token-Optimierung – Templates ausgelagert:** Die langen Markdown-Vorlagen für Feature Specs, UX-Entscheidungen, Tech-Design, Bug-Reports und Dev-Handoffs liegen jetzt in `docs/templates/`. Die Commands laden sie nur noch wenn sie wirklich gebraucht werden – statt bei jedem Aufruf im Kontext zu stehen.
- **Scaffold-Befehle ausgelagert:** Die 15+ Framework-Scaffold-Befehle (Next.js, Django, Rails, etc.) wurden aus `/red:proto-dev-setup` in `docs/SCAFFOLDING.md` verschoben. Der Command ist damit deutlich schlanker.
- **Research-Abschluss kompakter:** Die drei fast-identischen AskUserQuestion-Blöcke am Ende von `/red:proto-research` wurden zu einem einzigen dynamischen Block zusammengeführt.

---

## v0.14.0 — 5. April 2026

Feature-Auswahl mit Multi-Select: `/red:proto-ux` und `/red:proto-architect` fragen jetzt zu Beginn gezielt welche Features bearbeitet werden sollen – statt einfach alles in einem Rutsch durchzuarbeiten.

### Neue Features

- **Interaktive Feature-Auswahl in `/red:proto-ux` und `/red:proto-architect`:** Beim Start lesen beide Skills den aktuellen Projektstatus und zeigen welche Features bereit sind (UX-bereit bzw. Tech-bereit). Per Multi-Select entscheidest du selbst was jetzt bearbeitet wird.
- **Zwei Bearbeitungs-Modi:** Wählst du alle Features → werden alle ohne Unterbrechung durchgearbeitet, alle Drafts landen auf der Festplatte, und am Ende kommt eine einzige Freigabe für alles. Wählst du eine Teilmenge → bekommst du nach jedem Feature eine Approval-Frage.
- **Smarte Statuskategorisierung:** Fertige Features, Features in Bearbeitung und noch nicht bereite Features werden sauber getrennt angezeigt – kein Rätselraten mehr was als nächstes dran ist.

---

## v0.13.8 — 5. April 2026

### Verbesserungen

- **Contributor Guidelines erweitert:** `CLAUDE.md` enthält jetzt verbindliche Regeln für Changelog und Release Notes – Pflicht bei jedem Push, Struktur pro Version, Sprache und was nicht erlaubt ist.

---

## v0.13.7 — 5. April 2026

### Fixes

- **Feature Specs landen auf der Festplatte:** `/red:proto-requirements` hat Specs bisher nur im Chat angezeigt und erst nach Freigabe gespeichert. Jetzt wird die Draft-Datei direkt geschrieben – dann Freigabe einholen.
- **Mehrere Features einzeln durcharbeiten:** Wenn mehrere Features erkannt werden, wird zuerst die Aufteilung bestätigt – dann jedes Feature einzeln nacheinander angelegt und freigegeben. Nicht mehr alle auf einmal im Chat.

---

## v0.13.6 — 5. April 2026

### Verbesserungen

- **Contributor Guidelines:** `CLAUDE.md` im Repo-Root eingeführt. Wer am Framework selbst arbeitet, bekommt die Spielregeln direkt in Claude Code – Endnutzer des Frameworks sehen die Datei nicht.

---

## v0.13.5 — 5. April 2026

Intelligenteres Research, weniger Rückfragen, volle Kontrolle Schritt für Schritt.

### Neue Features

- **Dynamischer Platform-Kontext:** `/red:proto-research` liest jetzt die PRD und stellt keine Fragen mehr, wenn Platform und Gerät bereits dort definiert sind. `platform-context.md` wird direkt aus der PRD abgeleitet – nur bei echten Lücken wird nachgefragt.
- **Einzelne Freigabe pro Datei:** Jede Research-Datei (`platform-context.md`, `research-questions.md`, `problem-statement.md`, `personas.md`) wird direkt nach dem Schreiben zur Freigabe vorgelegt – nicht erst am Ende alles auf einmal.
- **Alle Dateien landen auf der Festplatte:** `problem-statement.md` wurde bisher nur im Chat angezeigt. Alle Research-Artefakte werden jetzt sofort als Datei geschrieben.
- **Interaktive Abschlussfrage:** Der nächste Schritt wird jetzt als AskUserQuestion gestellt statt als Textblock.

### Fixes

- **Kein Englisch mehr:** Alle nutzer-sichtbaren "Approved"-Labels durch deutsche Alternativen ersetzt ("Passt so", "Freigegeben") – gilt für das gesamte Framework.

---

## v0.13.4 — 5. April 2026

Die `prd.md` landet jetzt wirklich auf der Festplatte – nicht nur im Chat.

### Fixes

- **PRD wird als Datei geschrieben:** `/red:proto-sparring` hat das PRD bisher nur im Chat angezeigt und die eigentliche Datei nie erstellt. Das Framework arbeitet jetzt wie erwartet: `prd.md` wird direkt nach dem Schreiben als Draft gespeichert, inklusive YAML-Frontmatter und Scope-Typ.
- **Research als klarer nächster Schritt:** Die Abschlussfrage in `/red:proto-sparring` stellt jetzt Research in den Vordergrund – dev-setup ist nur noch die explizite Ausweichoption für alle, die Research überspringen wollen.

---

## v0.13.3 — 3. April 2026

Kein neues Feature, aber ein sauberes Fundament: Diese Version räumt auf, was hinter den Kulissen nicht gestimmt hat.

### Verbesserungen

- **npm-Installation zuverlässiger:** Der `npx red-proto`-Befehl hat beim letzten Publish still und heimlich nicht funktioniert – der Pfad zum Installationsskript war minimal falsch formatiert. Gefixt. Wer `npx red-proto` ausgeführt hat und nichts passiert ist, kann es jetzt erneut versuchen.
- **GitHub Community Standards:** Das Projekt hat jetzt eine vollständige offene Infrastruktur – Lizenz (MIT), Contributing Guide, Code of Conduct, Security Policy und Issue-Templates für Bugs und Feature-Requests.

---

## v0.13.2 — 3. April 2026

### Verbesserungen

- **Klarere Sprache:** Framework-interne Fachbegriffe aus User-facing Texten entfernt. Claude spricht jetzt wie ein Kollege, nicht wie ein Spezifikationsdokument.
- **Weniger Wiederholungen:** Ca. 90 Zeilen duplizierten Text aus 6 Commands entfernt. Schnellere Ausführung, weniger Rauschen.
- **Design System Index:** `design-system/INDEX.md` eingeführt – Agents laden jetzt nur noch die Teile des Design Systems, die sie wirklich brauchen. Weniger Kontext-Overhead, präzisere Ausgaben.

---

## v0.13.0 — 3. April 2026

### Neue Features

- **Uninstall-Befehl:** `npx red-proto uninstall` entfernt das Framework sauber vom System. Wer aussteigt, hinterlässt keine Leichen.
- **Doppelte Installation erkennen:** Wer `npx red-proto` zweimal ausführt, bekommt jetzt eine verständliche Warnung statt stummes Überschreiben.

---

## v0.11.1 — 3. April 2026

### Fixes

- Git gab beim Einrichten eines neuen Projekts ausführliche technische Statusmeldungen aus, die für normale Nutzer keinen Mehrwert hatten. Unterdrückt.

---

## v0.11.0 — 3. April 2026

Der "Wie war nochmal der Stand?"-Release. Wer morgens die KI öffnet und vergessen hat, wo man gestern aufgehört hat, hat jetzt ein System dafür.

### Neue Features

- **Draft-Konvention:** Artefakte werden als Entwurf markiert, bevor sie final sind. Kein versehentliches Weiterarbeiten auf halbgaren Outputs mehr.
- **STATUS.md:** Jedes Feature bekommt eine eigene Statusdatei. Ein Blick reicht, um zu wissen: fertig, in Arbeit, blockiert.
- **Resume-Pattern:** `/red:proto-workflow` zeigt nach einer Unterbrechung exakt, wo man steht und was als nächstes zu tun ist – ohne alles nochmal lesen zu müssen.

---

## v0.10.1 — 3. April 2026

### Verbesserungen

- **Commands um 42% komprimiert:** Alle Commands und Agents wurden gestrafft – weniger Text, gleiche Wirkung. Schnellere Ausführung, weniger Token-Verbrauch.
- **Session Handoff:** Übergabedokument am Ende jeder Dev-Session – damit die nächste Session sofort weiß, wo sie anfangen soll.
- **Design System Index-First:** Agents laden jetzt den Index zuerst und nur bei Bedarf die Details – statt das gesamte Design System auf einmal.

---

## v0.10.0 — 3. April 2026

### Neue Features

- **Dynamisches Feature-Routing:** Nach dem UX-Review entscheidet der Agent jetzt selbst, welcher nächste Schritt sinnvoll ist – statt stur eine vorgegebene Reihenfolge abzuarbeiten.
- **Bessere Bug-Prävention:** Agents machen jetzt Vor-Implementierungs-Checks, bevor sie loslegen. Einige Klassen von Bugs entstehen damit gar nicht mehr.
- **A11y im QA-Prozess verankert:** Accessibility war bisher optional und wurde oft vergessen. Jetzt ist es ein fester Bestandteil des QA-Durchlaufs, mit klarer Zuständigkeit.
- **Feature-Status-Index:** `features/STATUS.md` gibt einen zentralen Überblick über alle Features und ihren Fortschritt.

---

## v0.9.0 — 2. April 2026

### Neue Features

- **Autonomer UX-Agent:** Der `/red:proto-ux`-Command entscheidet jetzt selbst über Komponenten, Einbettung und Navigation – und legt diese Entscheidungen zur Review vor, statt endlose Fragen zu stellen. Weniger Rückfragen, mehr Ergebnis.
- **Requirements-Interview neu gestaltet:** Frage für Frage, mit konkreten Optionen und Freitext-Fallback. Kein Formular mehr, das man ausfüllt – sondern ein echtes Gespräch.
- **Autonome Spec-Ableitung:** Der Requirements-Agent leitet Spezifikationen selbst ab und zeigt sie zur Bestätigung – statt auf manuelle Eingaben zu warten.

### Fixes

- Platzhalter-Templates in den Requirements haben dazu geführt, dass `AskUserQuestion` nicht ausgeführt wurde. Gefixt. Entschuldigung – das war ärgerlich.

---

## v0.8.0 — 2. April 2026

### Neue Features

- **npx-Installer:** Das Framework lässt sich jetzt mit einem einzigen Befehl installieren: `npx red-proto`. Kein manuelles Kopieren von Dateien mehr.
- **Interaktives Research-Interview:** Fragen werden jetzt aufgeteilt und nacheinander gestellt – nicht als Wand aus Stichpunkten auf einmal.
- **Automatische Claude Code Permissions:** Werden beim Setup direkt korrekt gesetzt.

---

## v0.7.0 — 2. April 2026

### Neue Features

- **Research neu positioniert:** `/red:proto-research` läuft jetzt vor dem Dev-Setup – damit der Tech-Stack auf Basis echter Erkenntnisse gewählt wird, nicht umgekehrt.
- **Zwei Research-Modi:** Schneller Modus für kleinere Projekte, tiefer Modus für komplexere Domänen.

### Fixes

- Der Research-Command hat nach seinem Abschluss fälschlicherweise immer auf `/red:proto-requirements` verwiesen – auch wenn das nicht der nächste sinnvolle Schritt war.

---

## v0.6.0 — 1. April 2026

### Neue Features

- **Workflow-Klarheit:** Der übergreifende Ablauf zwischen den Commands ist jetzt expliziter dokumentiert und leichter nachvollziehbar.
- **Session Re-Entry verbessert:** Wer eine Arbeitssitzung unterbricht und später weitermacht, findet sich schneller wieder zurecht.

---

## v0.5.0 — 31. März 2026

### Neue Features

- **npx-Installer:** Das Framework lässt sich jetzt mit `npx red-proto` installieren – kein manuelles Klonen mehr nötig.
- **Developer Self-Review Phase:** Entwickler-Agents überprüfen ihre eigene Arbeit vor der QA – weniger offensichtliche Fehler, schnellere QA-Runden.

---

## v0.4.0 — 30. März 2026

### Neue Features

- **Design System Integration:** `design-system/` mit neutralen Templates eingeführt. Alle visuellen Entscheidungen laufen jetzt durch ein konsistentes System.
- **Screen-Inventar und Transitions:** `/red:proto-flows` verwaltet alle Screens und ihre Übergänge in einer verbindlichen Tabelle.
- **UX Compliance Enforcement:** Der UX-Command prüft jetzt aktiv auf Design-System-Lücken und stellt sicher, dass Flows korrekt integriert sind.

---

## v0.3.1 — 30. März 2026

### Fixes

- Vereinzelte Commands trugen noch alte Namen. Alle verbleibenden Referenzen auf das alte Namensschema wurden auf `red:proto-*` umgestellt.

---

## v0.3.0 — 30. März 2026

### Neue Features

- Einheitliches `red:proto-*`-Namespace für alle Commands. Vorher gab es verschiedene Benennungskonventionen, die für Verwirrung gesorgt haben.

---

## v0.2.1 — 30. März 2026

### Fixes

- Installations-Pfad in der README war falsch angegeben. Templates müssen in `~/.claude/templates/` landen – und jetzt tun sie das auch.

---

## v0.2.0 — 30. März 2026

### Neue Features

- Erste vollständige Pipeline: Sparring → Dev-Setup → Requirements → Flows → UX → Architect → Dev → QA.
- Jeder Command ist eigenständig und kann einzeln eingesetzt werden.

---

## v0.1.0 — 27. März 2026

Der Anfang. Ein Framework als Sammlung von Claude Code Commands – von der Idee bis zum getesteten Prototyp, mit Human-in-the-Loop an jedem Schritt.

Noch roh. Noch ohne Installer. Noch ohne vieles. Aber der Kern war da.
