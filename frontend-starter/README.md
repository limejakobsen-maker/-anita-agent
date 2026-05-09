# Anita Agent Dashboard - Frontend Starter

Dette er en startmal for å bygge et moderne dashboard for Anita Agent.

## 🚀 Quick Start

### 1. Initialiser prosjektet

```bash
# Kopier denne mappen
cd "Desktop\PROSJEKTMAPPE AI"
copy-item frontend-starter anita-agent-dashboard -recurse
cd anita-agent-dashboard

# Installer avhengigheter
npm install

# Installer shadcn/ui komponenter
.\install-components.ps1
# eller manuelt:
npx shadcn@latest init
npx shadcn add button card table tabs
```

### 2. Konfigurer miljøvariabler

```bash
copy .env.local.example .env.local
# Rediger .env.local med dine verdier
```

### 3. Start utviklingsserver

```bash
npm run dev
```

Åpne [http://localhost:3000](http://localhost:3000) i nettleseren.

## 📁 Mappestruktur

```
anita-agent-dashboard/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard
│   ├── globals.css        # Global styles
│   └── api/               # API routes
├── components/
│   ├── ui/                # shadcn/ui komponenter
│   ├── layout/            # Layout komponenter
│   └── dashboard/         # Dashboard-spesifikke
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities
├── stores/                # Zustand stores
├── types/                 # TypeScript types
└── public/                # Static assets
```

## 🛠️ Tilgjengelige Kommandoer

| Kommando | Beskrivelse |
|----------|-------------|
| `npm run dev` | Start utviklingsserver |
| `npm run build` | Bygg for produksjon |
| `npm run start` | Start produksjonsserver |
| `npm run lint` | Kjør ESLint |
| `npm run type-check` | TypeScript sjekk |

## 🎨 shadcn/ui Komponenter

Alle komponenter finnes i `components/ui/`. Du kan importere dem:

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
```

## 🔌 WebSocket Integrasjon

```tsx
import { useWebSocket } from "@/hooks/use-websocket"

function Dashboard() {
  const { connected, messages, send } = useWebSocket("ws://localhost:8765")
  
  return (
    <div>
      {connected ? "🟢 Online" : "🔴 Offline"}
    </div>
  )
}
```

## 📚 Dokumentasjon

- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query/latest)

## 💡 Tips

1. **Server Components**: Bruk server components for data fetching
2. **Client Components**: Bruk `'use client'` kun for interaktivitet
3. **shadcn/ui**: Kopier komponenter fra `components/ui/`
4. **Tailwind**: Bruk utility-klasser for styling
5. **Zustand**: Global state management

## 🐛 Feilsøking

### Port 3000 er opptatt
```bash
npm run dev -- --port 3001
```

### WebSocket kobler ikke til
Sjekk at `NEXT_PUBLIC_WS_URL` er riktig i `.env.local`

### shadcn/ui komponenter mangler
```bash
npx shadcn add <komponent-navn>
```

## 📄 Lisens

MIT
