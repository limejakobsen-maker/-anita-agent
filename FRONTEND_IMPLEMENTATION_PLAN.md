# 🎨 Frontend Implementeringsplan for Anita Agent

**Dato:** 17.03.2026  
**Mål:** Modernisere UI med beste gratis verktøy 2025  
**Ansvarlig:** Kimi Code CLI

---

## 📊 INNSIKT: Markedsanalyse 2025

### Trender 2025 (Basert på research)
| Trend | Beskrivelse | Relevans for oss |
|-------|-------------|------------------|
| **shadcn/ui** | Mest populære UI bibliotek 2023-2024 | ✅ Høy - moderne, tilpasningsbar |
| **Next.js 15** | React meta-framework med App Router | ✅ Høy - SSR, API routes |
| **Tailwind CSS** | Utility-first CSS dominans | ✅ Høy - rask utvikling |
| **Svelte 5** | Raskt voksende, kompilator-basert | ⚠️ Medium - mindre økosystem |
| **Vue 4** | Progressiv framework | ✅ Høy - lett å lære |

---

## 🏆 ANBEFALING: Teknologistack

### Alternativ 1: "The Modern Standard" (ANBEFALT)
```
┌─────────────────────────────────────────────────────────┐
│  NEXT.JS 15 (App Router) + React 19                     │
│  ├── shadcn/ui (komponenter)                            │
│  ├── Tailwind CSS (styling)                             │
│  ├── TanStack Query (data fetching)                     │
│  ├── Zustand (state management)                         │
│  └── Recharts (visualisering)                           │
└─────────────────────────────────────────────────────────┘
```

**Fordeler:**
- ✅ Størst økosystem og community
- ✅ Beste dokumentasjon
- ✅ Server Components = bedre ytelse
- ✅ shadcn/ui = kopier-komponenter (ikke npm install)
- ✅ Enkel integrasjon med eksisterende HTTP/WebSocket API

**Ulemper:**
- ⚠️ Steilere læringskurve enn Vue
- ⚠️ Krever Node.js kunnskap

---

### Alternativ 2: "The Vue Way"
```
┌─────────────────────────────────────────────────────────┐
│  NUXT 4 + Vue 4                                         │
│  ├── Nuxt UI (komponenter)                              │
│  ├── Tailwind CSS (styling)                             │
│  ├── Pinia (state management)                           │
│  └── Vue-ECharts (visualisering)                        │
└─────────────────────────────────────────────────────────┘
```

**Fordeler:**
- ✅ Enklere å lære
- ✅ Bedre for mindre team
- ✅ Vue-devtools er fantastisk
- ✅ Automatisk lazy loading

---

## 🎯 ENDELIG ANBEFALING

# ✅ ALTERNATIV 1: Next.js + shadcn/ui

**Begrunnelse:**
1. **Dere har CI/CD pipeline** - Next.js deployer perfekt til Kubernetes
2. **AI System integrasjon** - Enkel WebSocket/HTTP klient
3. **Dashboard-behov** - shadcn/ui har 50+ ferdige komponenter
4. **Fremtidssikker** - Størst community, best støtte
5. **Gratis** - Alt er open source

---

## 🛠️ KOMPONENTBIBLIOTEK: shadcn/ui

### Hva er shadcn/ui?
- **IKKE** et npm-bibliotek du installerer
- Kopier-komponenter rett inn i koden din
- Bygget på Radix UI (tilgjengelighet) + Tailwind
- Full kontroll over styling

### Komponenter inkludert (GRATIS):
```
Layout:
├── Accordion, Collapsible, Resizable
├── Dialog, Drawer, Sheet, Popover
├── Tabs, Card, Separator, ScrollArea

Forms:
├── Button, Checkbox, Combobox, Command
├── Input, Label, Radio Group, Select
├── Slider, Switch, Textarea, Form

Data Display:
├── Table, Data Table (avansert)
├── Calendar, Carousel, Command Palette
├── Avatar, Badge, Skeleton

Feedback:
├── Alert, Alert Dialog, Progress
├── Sonner (toast notifications)
├── Tooltip, Hover Card

Navigation:
├── Breadcrumb, Command, Context Menu
├── Dropdown Menu, Menubar, Navigation Menu
├── Pagination, Sidebar, Toggle Group
```

### Installasjon:
```bash
npx shadcn@latest init
npx shadcn add button table card
```

---

## 📦 ANDRE VERKTØY (GRATIS)

### State Management
| Verktøy | Formål | Størrelse |
|---------|--------|-----------|
| **Zustand** | Global state | ~1KB |
| **TanStack Query** | Server state, caching | ~12KB |
| **Jotai** | Atom-basert state | ~3KB |

### Data Visualisering
| Verktøy | Formål |
|---------|--------|
| **Recharts** | Charts (React-basert) |
| **TanStack Table** | Avanserte tabeller |
| ** Tremor** | Dashboard komponenter |

### Ikoner
| Bibliotek | Antall | Stil |
|-----------|--------|------|
| **Lucide React** | 1000+ | Moderne, konsistent |
| **Heroicons** | 300+ | Tailwind-stil |
| **Radix Icons** | 300+ | Minimalistisk |

### Animasjoner
| Bibliotek | Bruk |
|-----------|------|
| **Framer Motion** | React animasjoner |
| **Tailwind Animate** | CSS animasjoner |

---

## 🎨 ADMIN DASHBOARD MALER (GRATIS)

### 1. shadcn-admin (ANBEFALT)
- **GitHub:** github.com/satnaing/shadcn-admin
- **Tech:** Next.js + shadcn/ui + Tailwind
- **Features:**
  - Dashboard, Tasks, Settings sider
  - Dark/light mode
  - Responsivt design
  - TypeScript
- **Lisens:** MIT (gratis)

### 2. NextAdmin
- **GitHub:** themeselection/nextjs-materio-admin-free
- **Tech:** Next.js + Material UI
- **Features:**
  - 25+ sider
  - Charts
  - Autentisering

### 3. Horizon UI (Chakra)
- **URL:** horizon-ui.com
- **Tech:** Next.js + Chakra UI
- **Features:**
  - Glassmorphism design
  - Dark/light mode
  - Gratis Figma fil

---

## 📋 IMPLEMENTERINGSPLAN

### Fase 1: Oppsett (Uke 1)
```bash
# 1. Opprette Next.js prosjekt
npx create-next-app@latest anita-agent-dashboard \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

# 2. Installere shadcn/ui
cd anita-agent-dashboard
npx shadcn@latest init

# 3. Installere nødvendige komponenter
npx shadcn add button card table tabs dialog
npx shadcn add sidebar navigation-menu
npx shadcn add form input label select

# 4. Installere andre avhengigheter
npm install zustand @tanstack/react-query
npm install recharts lucide-react
npm install framer-motion
```

**Mappestruktur:**
```
anita-agent-dashboard/
├── app/
│   ├── layout.tsx              # Hoved-layout
│   ├── page.tsx                # Dashboard
│   ├── globals.css             # Global styles
│   ├── api/
│   │   └── websocket/          # WebSocket proxy
│   ├── dashboard/
│   │   ├── page.tsx            # Hoveddashboard
│   │   └── layout.tsx          # Dashboard layout
│   ├── projects/
│   │   └── page.tsx            # Prosjektliste
│   └── settings/
│       └── page.tsx            # Innstillinger
├── components/
│   ├── ui/                     # shadcn komponenter
│   ├── layout/                 # Applikasjons-layouts
│   ├── dashboard/              # Dashboard-spesifikke
│   ├── charts/                 # Chart komponenter
│   └── websocket/              # WebSocket hooks
├── hooks/
│   ├── use-websocket.ts        # WebSocket hook
│   ├── use-projects.ts         # Prosjekt data
│   └── use-metrics.ts          # Metrikker
├── lib/
│   ├── utils.ts                # Hjelpefunksjoner
│   └── api.ts                  # API klient
├── stores/
│   └── app-store.ts            # Zustand store
├── types/
│   └── index.ts                # TypeScript types
└── public/
    └── images/
```

### Fase 2: Core Komponenter (Uke 2)

**1. WebSocket Hook:**
```typescript
// hooks/use-websocket.ts
import { useEffect, useRef, useState, useCallback } from 'react';

export function useWebSocket(url: string) {
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const ws = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    ws.current = new WebSocket(url);
    ws.current.onopen = () => setConnected(true);
    ws.current.onclose = () => setConnected(false);
    ws.current.onmessage = (event) => {
      setMessages(prev => [...prev, JSON.parse(event.data)]);
    };
  }, [url]);

  const send = useCallback((data: any) => {
    ws.current?.send(JSON.stringify(data));
  }, []);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);

  return { connected, messages, send };
}
```

**2. Dashboard Layout:**
```typescript
// components/layout/dashboard-layout.tsx
import { Sidebar } from '@/components/layout/sidebar';
import { Header } from '@/components/layout/header';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

**3. Status Dashboard:**
```typescript
// app/dashboard/page.tsx
'use client';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { useWebSocket } from '@/hooks/use-websocket';
import { Activity, Server, Cpu, AlertCircle } from 'lucide-react';

export default function DashboardPage() {
  const { connected, messages } = useWebSocket('ws://localhost:8765');

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Anita Agent Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatusCard 
          title="System Status" 
          value={connected ? "Online" : "Offline"}
          icon={Activity}
          status={connected ? "success" : "error"}
        />
        <StatusCard 
          title="Active Projects" 
          value="3"
          icon={Server}
        />
        <StatusCard 
          title="CPU Usage" 
          value="45%"
          icon={Cpu}
        />
        <StatusCard 
          title="Errors" 
          value="0"
          icon={AlertCircle}
          status="warning"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ProjectList />
        <ActivityLog messages={messages} />
      </div>
    </div>
  );
}
```

### Fase 3: Integrasjon med Backend (Uke 3)

**API Klient:**
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8765';

export async function getStatus() {
  const res = await fetch(`${API_BASE}/status`);
  return res.json();
}

export async function startProject(name: string, requirements: string) {
  const res = await fetch(`${API_BASE}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project: name, description: requirements }),
  });
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
```

### Fase 4: Avanserte Features (Uke 4)

**Real-time Charts:**
```typescript
// components/charts/metrics-chart.tsx
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export function MetricsChart({ data }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="cpu" stroke="#8884d8" />
      <Line type="monotone" dataKey="memory" stroke="#82ca9d" />
    </LineChart>
  );
}
```

---

## 🔧 KONFIGURASJON

### 1. Tailwind Config
```javascript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

### 2. Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8765
NEXT_PUBLIC_WS_URL=ws://localhost:8765
NEXT_PUBLIC_APP_NAME="Anita Agent"
```

---

## 🚀 DEPLOYMENT

### Bygge for produksjon:
```bash
# Bygge statisk export
next build

# Eller for Kubernetes
next build  # Med custom server
```

### Docker:
```dockerfile
# Dockerfile.dashboard
FROM node:20-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

---

## 📊 KOSTNADSOVERSIKT

| Komponent | Kostnad | Lisens |
|-----------|---------|--------|
| Next.js | Gratis | MIT |
| React | Gratis | MIT |
| shadcn/ui | Gratis | MIT |
| Tailwind CSS | Gratis | MIT |
| Zustand | Gratis | MIT |
| TanStack Query | Gratis | MIT |
| Recharts | Gratis | MIT |
| Lucide Icons | Gratis | ISC |
| **TOTALT** | **$0** | - |

---

## ✅ SJEKKLISTE

### Før start:
- [ ] Node.js 18+ installert
- [ ] Git repository klar
- [ ] Eksisterende API dokumentasjon

### Uke 1:
- [ ] Next.js prosjekt opprettet
- [ ] shadcn/ui initialisert
- [ ] Basis layout ferdig

### Uke 2:
- [ ] WebSocket integrasjon
- [ ] Dashboard komponenter
- [ ] Routing

### Uke 3:
- [ ] API integrasjon
- [ ] Data fetching
- [ ] State management

### Uke 4:
- [ ] Charts
- [ ] Testing
- [ ] Deploy til K3d

---

## 🔗 RESSURSER

### Dokumentasjon:
- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [Tailwind Docs](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query/latest)

### Video Tutorials:
- [shadcn/ui Crash Course](https://www.youtube.com/watch?v=7h1sXN4gX7o)
- [Next.js 15 Tutorial](https://www.youtube.com/watch?v=wmnuWjn1j3Q)

### GitHub Repos:
- [shadcn-admin](https://github.com/satnaing/shadcn-admin)
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)

---

## 💡 BEST PRACTICES

1. **Bruk Server Components** for data fetching
2. **Client Components** kun for interaktivitet
3. **TypeScript** for typesikkerhet
4. **shadcn/ui** komponenter kan tilpasses 100%
5. **Zustand** for enkel state management
6. **TanStack Query** for server state og caching

---

**Neste steg:** Kjør setup-kommandoene i Fase 1 for å starte implementering!
