# Design Style Guidelines

**Design: Clean Modern Dashboard — Pure Tailwind CSS v3**

No external component library (no MUI, no Ant Design). All layouts use semantic HTML + Tailwind utility classes only.

---

## 1. Layout Structure

```
+------------------+----------------------------------------------+
| Sidebar (fixed)  | Top Header (fixed)                           |
| w-64             | h-16, bg-white, border-b border-gray-200     |
| bg-white         +----------------------------------------------+
| border-r         | Main Content Area (scrollable)               |
| border-gray-200  | p-6, bg-gray-50                              |
|                  |                                              |
| - Year nav       | [ Stat Cards Row ]                           |
| - My APPs        | [ Table / Grid / Charts ]                    |
| - Members        |                                              |
| - app - all      |                                              |
+------------------+----------------------------------------------+
```

**Shell classes:**

```
Root:         flex h-screen overflow-hidden bg-gray-50
Sidebar:      w-64 flex-shrink-0 bg-white border-r border-gray-200 flex flex-col overflow-y-auto
Header:       fixed top-0 left-64 right-0 h-16 bg-white border-b border-gray-200 flex items-center px-6 z-20
Main:         flex-1 overflow-y-auto pt-16 p-6
```

**Responsive — mobile sidebar collapse:**

```
Sidebar:      hidden lg:flex   (hidden on < lg)
Mobile menu:  fixed inset-0 z-50 bg-white (drawer overlay)
Hamburger:    block lg:hidden
```

---

## 2. Color Palette

| Token | Tailwind Class | Hex | Usage |
|-------|---------------|-----|-------|
| Background | `bg-gray-50` | #f9fafb | Page background |
| Surface | `bg-white` | #ffffff | Cards, sidebar, modals |
| Surface Raised | `bg-white shadow-md` | — | Dropdowns, popovers |
| Primary Text | `text-gray-900` | #111827 | Page titles, table data |
| Secondary Text | `text-gray-500` | #6b7280 | Labels, descriptions, timestamps |
| Muted Text | `text-gray-400` | #9ca3af | Placeholder, disabled |
| Primary Blue | `bg-blue-600` / `text-blue-600` | #2563eb | CTA buttons, active nav, links |
| Primary Blue Hover | `hover:bg-blue-700` | #1d4ed8 | — |
| Primary Blue Light | `bg-blue-50` / `text-blue-600` | #eff6ff | Nav active bg, info chips |
| Success | `text-green-700` / `bg-green-100` | — | Completed status |
| Warning | `text-orange-700` / `bg-orange-100` | — | In-progress / pending |
| Danger | `text-red-700` / `bg-red-100` | — | Errors, destructive actions |
| Border | `border-gray-200` | #e5e7eb | Card borders, dividers |
| Border Strong | `border-gray-300` | #d1d5db | Input borders |

**Accent gradient** — use sparingly on hero stats or highlight cards:

```
bg-gradient-to-br from-blue-600 to-indigo-600
```

---

## 3. Typography

**Font family** — add to `tailwind.config.ts` and `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

```typescript
// tailwind.config.ts
theme: {
  extend: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
    },
  },
},
```

**Type scale:**

| Role | Classes | Usage |
|------|---------|-------|
| Page title | `text-2xl font-bold text-gray-900 tracking-tight` | Page h1 |
| Section title | `text-lg font-semibold text-gray-800` | Card headers, section heads |
| Subsection | `text-base font-medium text-gray-700` | Table column headers |
| Body | `text-sm text-gray-600` | Default body text |
| Caption / meta | `text-xs text-gray-500` | Timestamps, hints, labels |
| Stat number | `text-3xl font-bold text-gray-900 tabular-nums` | KPI cards |
| Monospace | `font-mono text-sm text-gray-700` | IDs, codes, slugs |

**Rules:**
- Heading `tracking-tight` on sizes ≥ `text-xl`.
- Always `tabular-nums` for numbers in tables and stat cards (prevents layout shift).
- Max line length in readable text blocks: `max-w-prose`.

---

## 4. Elevation & Shadow System

Use shadows to communicate z-depth, not decoration.

| Level | Class | Usage |
|-------|-------|-------|
| Flat | `shadow-none` | Sidebar items, table rows |
| Resting | `shadow-sm` | Default cards |
| Raised | `shadow-md` | Hovered cards, dropdowns |
| Floating | `shadow-lg` | Modals, command palette |
| Overlay | `shadow-2xl` | Full-screen overlays |

**Card hover lift pattern:**

```
bg-white rounded-xl shadow-sm border border-gray-200 p-6
hover:shadow-md hover:-translate-y-0.5 transition-all duration-200
```

---

## 5. Spacing & Layout Tokens

**Spacing scale** — multiples of 4px only:

| Token | Value | Common use |
|-------|-------|-----------|
| `p-2` | 8px | Icon buttons, tight badges |
| `p-3` | 12px | Small inputs, compact items |
| `p-4` | 16px | Default padding |
| `p-6` | 24px | Card padding, section padding |
| `p-8` | 32px | Page section padding |
| `gap-4` | 16px | Default grid/flex gap |
| `gap-6` | 24px | Card grid gap |
| `space-y-1` | 4px | Sidebar nav items |
| `space-y-6` | 24px | Form sections |

**Page content max-width:**

```
max-w-7xl mx-auto   (for full-width dashboard pages)
max-w-3xl mx-auto   (for detail / form pages)
```

**Stat card grid:**

```
grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6
```

---

## 6. Component Recipes

### Card

```
bg-white rounded-xl shadow-sm border border-gray-200 p-6
hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 cursor-pointer
```

**Stat card with accent top border:**

```tsx
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 relative overflow-hidden">
  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-indigo-500" />
  <p className="text-sm text-gray-500 font-medium">Total Apps</p>
  <p className="text-3xl font-bold text-gray-900 mt-1 tabular-nums">142</p>
  <p className="text-xs text-green-600 mt-2">↑ 12% this month</p>
</div>
```

### Primary Button

```
bg-blue-600 hover:bg-blue-700 active:bg-blue-800
text-white text-sm font-medium
px-4 py-2 rounded-lg
transition-colors duration-150
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
disabled:opacity-50 disabled:cursor-not-allowed
```

### Secondary Button

```
bg-white hover:bg-gray-50 active:bg-gray-100
text-gray-700 text-sm font-medium
border border-gray-300
px-4 py-2 rounded-lg
transition-colors duration-150
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
```

### Danger Button

```
bg-red-600 hover:bg-red-700 text-white text-sm font-medium
px-4 py-2 rounded-lg transition-colors duration-150
focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
```

### Icon Button

```
p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100
transition-colors duration-150
```

### Input Field

```
w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900
placeholder:text-gray-400
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
transition-shadow duration-150
disabled:bg-gray-50 disabled:text-gray-400
```

### Select / Dropdown

```
w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-900 bg-white
focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
```

### Search Input

```tsx
<div className="relative">
  <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
  <input className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm
    focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400" />
</div>
```

### Status Badges

```
Not Started:  bg-gray-100   text-gray-600   px-2.5 py-0.5 rounded-full text-xs font-medium
In Progress:  bg-orange-100 text-orange-700 px-2.5 py-0.5 rounded-full text-xs font-medium
Completed:    bg-green-100  text-green-700  px-2.5 py-0.5 rounded-full text-xs font-medium
Cancelled:    bg-red-100    text-red-700    px-2.5 py-0.5 rounded-full text-xs font-medium
Archived:     bg-gray-100   text-gray-500   px-2.5 py-0.5 rounded-full text-xs font-medium
```

### Progress Bar

```tsx
<div className="space-y-1">
  <div className="flex justify-between text-xs text-gray-500">
    <span>Progress</span>
    <span className="tabular-nums">{progress}%</span>
  </div>
  <div className="w-full bg-gray-100 rounded-full h-1.5">
    <div
      className="bg-blue-600 rounded-full h-1.5 transition-all duration-500 ease-out"
      style={{ width: `${progress}%` }}
    />
  </div>
</div>
```

### Sidebar Nav Item

```tsx
// Active
<a className="flex items-center gap-3 px-3 py-2 rounded-lg
  bg-blue-50 text-blue-600 font-medium text-sm">
  <Icon className="w-4 h-4" />
  <span>Apps</span>
</a>

// Inactive
<a className="flex items-center gap-3 px-3 py-2 rounded-lg
  text-gray-600 hover:bg-gray-50 hover:text-gray-900
  transition-colors duration-150 text-sm">
  <Icon className="w-4 h-4" />
  <span>Members</span>
</a>
```

### Table

```tsx
<div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
  <table className="w-full text-sm">
    <thead>
      <tr className="border-b border-gray-200 bg-gray-50">
        <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Name
        </th>
      </tr>
    </thead>
    <tbody className="divide-y divide-gray-100">
      <tr className="hover:bg-gray-50 transition-colors duration-100">
        <td className="px-6 py-4 text-gray-900">...</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Modal / Dialog

```tsx
{/* Backdrop */}
<div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 transition-opacity" />

{/* Panel */}
<div className="fixed inset-0 z-50 flex items-center justify-center p-4">
  <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 space-y-4">
    <h2 className="text-lg font-semibold text-gray-900">Title</h2>
    ...
  </div>
</div>
```

### Toast / Notification

```tsx
<div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2">
  {/* Success */}
  <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-xl shadow-lg px-4 py-3 min-w-72">
    <div className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />
    <p className="text-sm text-gray-800 font-medium">Saved successfully</p>
  </div>
</div>
```

### Empty State

```tsx
<div className="flex flex-col items-center justify-center py-16 text-center">
  <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-4">
    <FolderIcon className="w-6 h-6 text-gray-400" />
  </div>
  <h3 className="text-sm font-semibold text-gray-900 mb-1">No apps yet</h3>
  <p className="text-sm text-gray-500 max-w-xs mb-4">
    Create your first app to get started tracking progress.
  </p>
  <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
    New App
  </button>
</div>
```

### Skeleton Loading

```tsx
{/* Shimmer effect via CSS in index.css */}
{/* .skeleton { animation: shimmer 1.5s infinite; background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%); background-size: 200% 100%; } */}
{/* @keyframes shimmer { 0% { background-position: 200% 0 } 100% { background-position: -200% 0 } } */}

<div className="bg-white rounded-xl border border-gray-200 p-6 space-y-3">
  <div className="h-4 skeleton rounded w-1/3" />
  <div className="h-3 skeleton rounded w-2/3" />
  <div className="h-3 skeleton rounded w-1/2" />
</div>
```

---

## 7. Motion & Animation

**Principle:** Subtle and purposeful. Never animate just for the sake of it.

**Transition defaults:**

```
Elements entering/exiting:   transition-all duration-200 ease-out
Color/background changes:    transition-colors duration-150
Transform (hover lift):      transition-transform duration-200
Sidebar open/close:          transition-transform duration-300 ease-in-out
Progress bars:               transition-all duration-500 ease-out
```

**Hover lift for clickable cards:**

```
hover:-translate-y-0.5 hover:shadow-md transition-all duration-200
```

**Stagger list animation** — via `index.css`, not inline:

```css
/* index.css */
.stagger-item { opacity: 0; transform: translateY(8px); animation: fadeUp 0.3s ease forwards; }
.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 60ms; }
.stagger-item:nth-child(3) { animation-delay: 120ms; }
.stagger-item:nth-child(4) { animation-delay: 180ms; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}
```

**Page-level fade in:**

```css
.page-enter { animation: pageFade 0.25s ease-out; }
@keyframes pageFade { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
```

**Spinner:**

```tsx
<div className="w-5 h-5 border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin" />
```

**Rules:**
- Never use `transition-all` on elements that change layout (causes jank).
- Prefer `duration-150`–`duration-300`. Never exceed `duration-500` except progress bars.
- Avoid animations for users with `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

---

## 8. Icon System

**Library:** [Heroicons](https://heroicons.com/) — `@heroicons/react`

```bash
npm install @heroicons/react
```

**Size scale:**

| Size | Classes | Usage |
|------|---------|-------|
| XS | `w-3 h-3` | Inline badges, tiny indicators |
| SM | `w-4 h-4` | Nav icons, button icons, table row icons |
| MD | `w-5 h-5` | Header icons, action icons |
| LG | `w-6 h-6` | Empty state, prominent actions |
| XL | `w-8 h-8` | Feature icons in cards |

**Import pattern:**

```tsx
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';
import { CheckCircleIcon } from '@heroicons/react/24/solid'; // solid only for status indicators
```

**Rules:**
- Use `outline` variant by default.
- Use `solid` only for active states and filled status indicators.
- Icons inside buttons must be paired with text or have `aria-label`.
- Always set explicit `w-` and `h-` — never rely on inherited size.

---

## 9. Data Visualization

For charts use **Recharts** (already React-native, no D3 dependency):

```bash
npm install recharts
```

**Chart color palette** (use in this order):

```
Series 1:  #3b82f6  (blue-500)
Series 2:  #10b981  (emerald-500)
Series 3:  #f59e0b  (amber-500)
Series 4:  #8b5cf6  (violet-500)
Series 5:  #ef4444  (red-500)
Series 6:  #06b6d4  (cyan-500)
```

**Chart container pattern:**

```tsx
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
  <div className="flex items-center justify-between mb-6">
    <h3 className="text-base font-semibold text-gray-800">App Progress</h3>
    <span className="text-xs text-gray-400">Last 30 days</span>
  </div>
  <ResponsiveContainer width="100%" height={240}>
    <BarChart data={data} barSize={24}>
      <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" vertical={false} />
      <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#9ca3af' }} axisLine={false} tickLine={false} />
      <YAxis tick={{ fontSize: 12, fill: '#9ca3af' }} axisLine={false} tickLine={false} />
      <Tooltip
        contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
        cursor={{ fill: '#f9fafb' }}
      />
      <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
    </BarChart>
  </ResponsiveContainer>
</div>
```

**Sparkline (inline mini chart):**

```tsx
<ResponsiveContainer width={80} height={32}>
  <LineChart data={sparkData}>
    <Line type="monotone" dataKey="v" stroke="#3b82f6" dot={false} strokeWidth={2} />
  </LineChart>
</ResponsiveContainer>
```

---

## 10. Dark Mode

**Strategy:** `class` strategy — toggled by adding `dark` class to `<html>`.

```typescript
// tailwind.config.ts
darkMode: 'class',
```

**Key dark overrides:**

| Light | Dark |
|-------|------|
| `bg-gray-50` | `dark:bg-gray-950` |
| `bg-white` | `dark:bg-gray-900` |
| `border-gray-200` | `dark:border-gray-800` |
| `text-gray-900` | `dark:text-gray-100` |
| `text-gray-500` | `dark:text-gray-400` |
| `bg-blue-50` | `dark:bg-blue-950` |

**Toggle implementation:**

```tsx
const toggleDark = () => document.documentElement.classList.toggle('dark');
```

**Rule:** Apply dark variants consistently — if a component has `bg-white`, it must also have `dark:bg-gray-900`.

---

## 11. Tailwind v3 Setup

**CSS entry point (`index.css`):**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom base resets */
@layer base {
  * { box-sizing: border-box; }
  html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
}

/* Skeleton shimmer */
.skeleton {
  animation: shimmer 1.5s infinite;
  background: linear-gradient(90deg, #f3f4f6 25%, #e9eaed 50%, #f3f4f6 75%);
  background-size: 200% 100%;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Page entrance */
.page-enter { animation: pageFade 0.25s ease-out; }
@keyframes pageFade {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Stagger list */
.stagger-item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeUp 0.3s ease forwards;
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

❌ Never use `@import "tailwindcss"` — that is Tailwind v4 syntax.

**`tailwind.config.ts`:**

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
```

**`postcss.config.js`:**

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

---

## 12. Consistency Rules

**Do:**
- Always `tabular-nums` on numbers, percentages, dates in tables.
- Always `focus:ring-2 focus:ring-blue-500 focus:ring-offset-2` on every interactive element.
- Always `transition-colors duration-150` on hover color changes.
- Always `disabled:opacity-50 disabled:cursor-not-allowed` on form elements.
- Always `aria-label` on icon-only buttons.
- Spacing multiples of 4px: `p-4`, `gap-4`, `mt-6`.
- Use `gray` (not `grey`).

**Don't:**
- No CSS-in-JS — no `sx` prop, no `styled()`.
- No `@apply` inside `@layer components` — use plain CSS classes instead.
- No `hover:bg-gray-25` — only shades in Tailwind's default scale exist.
- No `shadow-xl` on cards at rest — only `shadow-sm`; reserve larger shadows for modals.
- No layout animations with `transition-all` — only animate specific properties.
- No `!important` — fix specificity instead.
