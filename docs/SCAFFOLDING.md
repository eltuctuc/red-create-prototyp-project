# Scaffold-Befehle

Genutzt von `/red:proto-dev-setup` Phase 5. Wähle den passenden Block für den bestätigten Stack.

> Bei allen Scaffolds gilt:
> - **"Initialize git repository?"** → **No** – Git richtet das Framework in Phase 6 ein
> - **"Install dependencies?"** → **Yes**
> - **"Project name?"** → Repository-Namen eingeben
> - Alle anderen Fragen: empfohlene Option wählen

---

## JavaScript / TypeScript Web

### Next.js (React)
```bash
mkdir -p [codedir] && cd [codedir]
npx create-next-app@latest . --typescript --tailwind --app --src-dir --no-git
```

### Nuxt
```bash
mkdir -p [codedir] && cd [codedir]
npx nuxi@latest init . --no-git
```

### Vue + Vite
```bash
mkdir -p [codedir] && cd [codedir]
# Interaktiv: TypeScript Ja, Router Ja, Pinia Ja, Vitest Ja, Git Nein
npm create vue@latest .
```

### React + Vite
```bash
mkdir -p [codedir] && cd [codedir]
npm create vite@latest . -- --template react-ts
```

### SvelteKit
```bash
mkdir -p [codedir] && cd [codedir]
npm create svelte@latest .
```

### Angular
```bash
mkdir -p [codedir] && cd [codedir]
npx @angular/cli@latest new . --routing --style=scss --no-git
```

### Remix
```bash
mkdir -p [codedir] && cd [codedir]
npx create-remix@latest . --no-git
```

### Astro
```bash
mkdir -p [codedir] && cd [codedir]
npm create astro@latest .
```

### NestJS (Backend)
```bash
mkdir -p [codedir] && cd [codedir]
npx @nestjs/cli@latest new . --package-manager npm --skip-git
```

### Express (Backend)
```bash
mkdir -p [codedir] && cd [codedir]
npm init -y
npm install express
npm install -D typescript @types/node @types/express ts-node nodemon
```

---

## Python

### FastAPI
```bash
mkdir -p [codedir] && cd [codedir]
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn[standard] python-dotenv
```

### Django
```bash
mkdir -p [codedir] && cd [codedir]
python3 -m venv venv && source venv/bin/activate
pip install django python-dotenv
django-admin startproject config .
```

### Flask
```bash
mkdir -p [codedir] && cd [codedir]
python3 -m venv venv && source venv/bin/activate
pip install flask python-dotenv
```

---

## Java

### Spring Boot
```bash
mkdir -p [codedir]
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.2.0 \
  -d baseDir=. \
  -d groupId=com.example \
  -d artifactId=[repo-name] \
  -d dependencies=web,data-jpa,postgresql \
  -o scaffold.zip
unzip scaffold.zip -d [codedir] && rm scaffold.zip
```

---

## C# / .NET

### ASP.NET Core Web API
```bash
mkdir -p [codedir] && cd [codedir]
dotnet new webapi --output . --no-https false
```

### Blazor
```bash
mkdir -p [codedir] && cd [codedir]
dotnet new blazor --output .
```

---

## Ruby

### Rails
```bash
mkdir -p [codedir] && cd [codedir]
rails new . --database=postgresql --no-git
```

---

## Go

```bash
mkdir -p [codedir] && cd [codedir]
go mod init [repo-name]
go get github.com/gin-gonic/gin
```

---

## Mobile

### React Native (Expo)
```bash
mkdir -p [codedir] && cd [codedir]
npx create-expo-app@latest . --template blank-typescript
```

### Flutter
```bash
mkdir -p [codedir] && cd [codedir]
flutter create .
```

---

## Nicht gelisteter Stack

Nutze die offizielle `create-*` CLI oder den Standard-Scaffolding-Weg des Frameworks. Dokumentiere den verwendeten Befehl in `project-config.md`.
