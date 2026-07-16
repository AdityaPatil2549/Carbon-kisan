# CarbonCredit.in — Frontend Design & UX Guidelines
**Version 1.0 · July 2026**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Design Philosophy](#2-design-philosophy)
3. [Color System](#3-color-system)
4. [Typography](#4-typography)
5. [Spacing & Layout](#5-spacing--layout)
6. [Component Library](#6-component-library)
7. [Page-by-Page Specifications](#7-page-by-page-specifications)
   - 7.1 [Landing Page](#71-landing-page)
   - 7.2 [Farmer Login](#72-farmer-login)
   - 7.3 [Farmer Dashboard](#73-farmer-dashboard)
   - 7.4 [Log Practice (Farmer Portal)](#74-log-practice-farmer-portal)
   - 7.5 [Buyer Login](#75-buyer-login)
   - 7.6 [Buyer Dashboard](#76-buyer-dashboard)
   - 7.7 [Buyer Marketplace](#77-buyer-marketplace)
8. [Multilingual & Accessibility](#8-multilingual--accessibility)
9. [Motion & Animation](#9-motion--animation)
10. [Responsive Design](#10-responsive-design)
11. [Innovative Feature Suggestions](#11-innovative-feature-suggestions)
12. [Do's and Don'ts](#12-dos-and-donts)

---

## 1. Project Overview

**CarbonCredit.in** is a two-sided marketplace connecting Indian farmers practising sustainable agriculture with CSR-driven corporate buyers seeking verified carbon offsets.

| Role | Primary Goal |
|---|---|
| Farmer | Log sustainable practices → get ML-estimated CO₂ credits → earn income |
| CSR Buyer | Browse verified credits → purchase → receive certificates for compliance |

The frontend must feel **trustworthy, simple, and empowering** for two very different user types — rural farmers (often low digital literacy) and urban corporate sustainability managers.

---

## 2. Design Philosophy

### Core Principles

**1. Earth-first Aesthetics**
Every visual choice reinforces the environmental mission. The palette, iconography, and language should feel like the product grew out of the soil — not a fintech dashboard.

**2. Dual Simplicity**
The farmer side must be operable by someone with a basic smartphone and limited English. The buyer side can carry more data density, but never at the cost of clarity.

**3. Trust Through Transparency**
Carbon credit integrity is the product's core promise. Every number shown must be accompanied by its source (ML model, ICRISAT data, etc.). Nothing is hidden behind vague labels.

**4. Progressive Disclosure**
Show the essentials first. Let users drill down only when they want to. Avoid overwhelming either user type with all data at once.

---

## 3. Color System

### Primary Palette

| Token | Hex | Usage |
|---|---|---|
| `--color-forest` | `#1A3A2A` | Primary background (dark mode base) |
| `--color-canopy` | `#0F2318` | Sidebar, card backgrounds, deeper surfaces |
| `--color-moss` | `#2D5A3D` | Secondary surfaces, elevated cards |
| `--color-sprout` | `#3D9B5A` | Primary interactive green — CTA buttons, active states |
| `--color-leaf` | `#5DC978` | Highlights, icons, data callouts |
| `--color-mint` | `#A8E6BC` | Subtle accents, hover states, borders |
| `--color-sky` | `#2563EB` | Buyer-side accent — CTA buttons (CSR buyer flows) |
| `--color-sky-light` | `#60A5FA` | Buyer accent highlights |

### Neutral Palette

| Token | Hex | Usage |
|---|---|---|
| `--color-ash` | `#F4F6F4` | Light mode background (if used) |
| `--color-stone` | `#9CA89C` | Secondary text, placeholder text |
| `--color-chalk` | `#D1D9D1` | Borders, dividers |
| `--color-white` | `#FFFFFF` | Primary text on dark, icons |

### Semantic Colors

| Token | Hex | Usage |
|---|---|---|
| `--color-success` | `#22C55E` | Sold status, successful actions |
| `--color-warning` | `#F59E0B` | Pending verification, expiring OTP |
| `--color-error` | `#EF4444` | Errors, rejected verifications |
| `--color-info` | `#3B82F6` | Info banners, live activity dots |

### Color Usage Rules

- **Dark mode is the default** — lighter surfaces feel clinical; dark earth tones feel organic and trustworthy.
- Farmer portal uses the **green family** as the primary interaction color.
- Buyer portal uses the **sky blue** for primary CTAs to differentiate the two experiences.
- Never use pure black (`#000000`) as a background; always use `--color-canopy` or `--color-forest`.
- Maintain **WCAG AA contrast ratio** minimum (4.5:1) for all body text.

---

## 4. Typography

### Font Stack

```
Primary (UI): "Inter", "Noto Sans", system-ui, sans-serif
Accent (Headings): "Plus Jakarta Sans", "Inter", sans-serif
Indic Scripts: "Noto Sans Devanagari", "Noto Sans Telugu", "Noto Sans Kannada", sans-serif
Monospace (IDs, numbers): "JetBrains Mono", "Fira Code", monospace
```

> **Note:** Indic script fonts are loaded lazily only when the user selects that language. Do not load all language packs on initial render.

### Type Scale

| Name | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| `display` | 36–48px | 700 | 1.15 | Landing page hero headline |
| `heading-1` | 28px | 700 | 1.2 | Page titles |
| `heading-2` | 22px | 600 | 1.3 | Section headers |
| `heading-3` | 18px | 600 | 1.35 | Card titles |
| `body-lg` | 16px | 400 | 1.6 | Primary body text |
| `body` | 14px | 400 | 1.6 | Dashboard content, form labels |
| `body-sm` | 12px | 400 | 1.5 | Metadata, timestamps |
| `label` | 12px | 500 | 1.4 | Tags, badges, status chips |
| `mono` | 13px | 500 | 1.4 | Credit IDs, numeric codes |

### Typography Rules

- Numbers in stat cards always use **monospace** to prevent layout shift.
- For farmer-facing text, prefer **16px minimum** body size to aid readability on small screens.
- Bilingual labels (e.g. "Wheat / गेहूँ") are formatted as: `English · Native` with the native script in `--color-mint` colour.
- Never use text smaller than 11px anywhere in the UI.

---

## 5. Spacing & Layout

### Grid System

- **Desktop:** 12-column grid, 24px gutters, max content width `1280px`
- **Tablet (768–1024px):** 8-column grid, 20px gutters
- **Mobile (<768px):** 4-column grid, 16px gutters

### Spacing Scale (multiples of 4px)

| Token | Value | Usage |
|---|---|---|
| `--space-1` | 4px | Icon padding, micro gaps |
| `--space-2` | 8px | Tight internal padding |
| `--space-3` | 12px | Form element inner padding |
| `--space-4` | 16px | Standard component padding |
| `--space-5` | 20px | Card padding |
| `--space-6` | 24px | Section gaps |
| `--space-8` | 32px | Large section separators |
| `--space-10` | 40px | Page-level vertical rhythm |
| `--space-12` | 48px | Hero section padding |

### Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | 6px | Badges, chips, tags |
| `--radius-md` | 10px | Input fields, small cards |
| `--radius-lg` | 16px | Primary cards, modal panels |
| `--radius-xl` | 24px | Hero sections, feature panels |
| `--radius-full` | 9999px | Pills, toggle buttons, avatars |

---

## 6. Component Library

### 6.1 Buttons

**Primary Button (Farmer — Green)**
```
Background: --color-sprout
Text: white, 14px, weight 600
Padding: 12px 24px
Border-radius: --radius-md
Hover: brightness(1.1) + subtle upward translate (2px)
Active: brightness(0.95) + scale(0.98)
```

**Primary Button (Buyer — Blue)**
```
Background: --color-sky
Text: white, 14px, weight 600
Same sizing as above
```

**Secondary Button**
```
Background: transparent
Border: 1.5px solid --color-chalk
Text: white
Hover: Background --color-moss
```

**Icon Button**
```
Size: 36×36px minimum (touch target 44×44px)
Background: --color-canopy
Border-radius: --radius-md
```

### 6.2 Cards

**Stat Card**
```
Background: --color-moss
Border: 1px solid rgba(93, 201, 120, 0.15)
Border-radius: --radius-lg
Padding: --space-5
Shadow: 0 2px 8px rgba(0,0,0,0.3)
Hover: border-color rgba(93,201,120,0.4) + shadow elevation increase
```

**Content Card**
```
Background: --color-canopy
Border: 1px solid rgba(255,255,255,0.06)
Border-radius: --radius-lg
```

**Live Activity Item**
```
Left border: 3px solid --color-success (green pulse dot) or --color-info (blue)
Background: --color-forest
Padding: 12px 16px
Border-radius: --radius-md
```

### 6.3 Form Elements

**Input Field**
```
Background: rgba(255,255,255,0.05)
Border: 1.5px solid --color-chalk (opacity 0.3)
Focus border: --color-leaf
Border-radius: --radius-md
Padding: 12px 16px
Text: white, 14px
Placeholder: --color-stone
```

**Dropdown / Select**
```
Same as input field
Chevron icon: --color-stone
```

**Slider**
```
Track: --color-chalk (opacity 0.3)
Fill: --color-sprout
Thumb: white circle, 18px diameter, shadow
```

**OTP Input Boxes**
```
Size: 52×56px
Border: 2px solid --color-chalk (opacity 0.3)
Filled: Border --color-sprout, Background rgba(61,155,90,0.15)
Active: Border --color-leaf
```

### 6.4 Status Badges

| Badge | Background | Text |
|---|---|---|
| Sold | `rgba(34,197,94,0.15)` | `--color-success` |
| Available | `rgba(59,130,246,0.15)` | `--color-sky-light` |
| Pending | `rgba(245,158,11,0.15)` | `#F59E0B` |
| Verified | `rgba(93,201,120,0.2)` | `--color-leaf` |

### 6.5 Navigation Bar

```
Background: --color-canopy with 12px blur backdrop-filter
Height: 64px
Border-bottom: 1px solid rgba(255,255,255,0.06)
Logo: --color-sprout brand mark + wordmark
Nav links: 14px, weight 500, --color-stone → --color-white on hover/active
Active indicator: underline, 2px, --color-sprout
Sticky on scroll
```

### 6.6 Language Selector

```
Compact dropdown in the top navigation bar
Flag emoji + language name (e.g. 🇮🇳 मराठी)
Options: English, हिंदी, मराठी, తెలుగు, ಕನ್ನಡ, தமிழ், বাংলা, ਪੰਜਾਬੀ
Applies to all farmer-facing text, labels, and system messages
```

---

## 7. Page-by-Page Specifications

---

### 7.1 Landing Page

**URL:** `carboncredit.in`

**Purpose:** Introduce the platform and route users to their respective portal.

#### Layout

```
[Navbar]
  Logo (left) | Nav links: How it works · About · Contact (center) | Log in (right)

[Hero Section — full viewport height, centered]
  Animated leaf/earth icon (subtle float animation)
  H1: "Carbon credits for every farmer."
  H2: "Verified. Tradeable. Impactful."
  Body: One-paragraph pitch (2–3 sentences max)
  
  [Two CTA Cards — side by side, not plain buttons]
  ┌──────────────────────┐  ┌──────────────────────┐
  │  🌾 I'm a Farmer     │  │  🏢 I'm a CSR Buyer  │
  │  [green background]  │  │  [blue background]   │
  │  Short line below    │  │  Short line below    │
  └──────────────────────┘  └──────────────────────┘

[Footer — minimal]
  © 2026 CarbonCredit.in · Privacy · Terms · Contact
```

#### Design Notes

- CTA elements are **cards**, not just buttons — they have subtle icons, a title, and a one-line description ("Log your sustainable practices" / "Purchase verified credits for your CSR goals"). This reduces friction and sets expectations.
- **Animated background:** Very subtle upward-drifting particle effect using SVG/canvas — tiny leaf or CO₂ molecule shapes, low opacity. Adds life without distraction.
- The hero section has a **soft radial gradient** behind the CTA cards: dark forest green → transparent.
- No stats block, no "how it works" steps on the landing page — keep it clean and conversion-focused.
- On mobile, CTA cards stack vertically.

---

### 7.2 Farmer Login

**URL:** `carboncredit.in/farmer/login`

#### Layout

```
[Centered card — max-width 480px]
  Logo + "Farmer Login" heading
  Subline: "Verify your identity to access your portal"

  [Mobile number field with +91 prefix]
  [OTP box row — 6 boxes]
  OTP status: "Sent to +91 XXXXX · expires in 4:32" + Resend OTP link

  [7/12 Document Verification section]
    Option A: Upload 7/12 Utara / Pahani / land ID (PDF or image, max 5MB)
    Option B: Enter 7/12 ID number manually (e.g. MH-NAS-2024-XXXXXX)
    
  [Language preference dropdown — prominent]
  
  [Verify and continue — full-width primary green button]
  
  "New farmer? Register here" — link below
```

#### Design Notes

- Keep this exactly as designed — it is already well-structured.
- The document verification section uses a toggle/tab pattern between "Upload" and "Enter manually" — ensure only one is active at a time.
- **Language preference** must be the very first thing a farmer changes if needed — consider making it accessible even before OTP, via a floating language pill in the top-right corner.
- On success, animate a green checkmark before navigating to dashboard.

---

### 7.3 Farmer Dashboard

**URL:** `carboncredit.in/farmer/dashboard`

#### Navigation (Farmer Portal)

```
[Top Nav — dark, sticky]
  Logo | Dashboard · Log Practice · Credits · Refer  |  [Language selector] [Farmer name + badge]
```

#### Layout

```
[Greeting Banner]
  "Good morning, Rajan. Your farm in Nashik, MH."
  Personalised time-based greeting in selected language.

[Summary Row — 3 stat cards]
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Total Earned │  │Credits Issued│  │CO₂ Sequestered│
│   ₹4,820     │  │     12       │  │  0.84 t      │
└──────────────┘  └──────────────┘  └──────────────┘
  (CO₂ shown in tonnes for easy comprehension)

[Two-column section below]

LEFT — Credit Wallet History
  Title: "Credit Wallet"
  List of past credits (scrollable):
    Each row: Crop · Practice · Weight | Status badge | Price
    [+ Log new practice] button at bottom

RIGHT — Live Activity Feed
  Title: "Live Activity" + green pulsing dot
  Scrolling feed of platform-wide events:
    - CC-XXXX purchased by [Company] for ₹XXX
    - [Farmer name] (State) issued credit — XXX kg
    - Your credit CC-XXXX was sold for ₹XXX ✓ (highlighted in green)
  Limit to last 10 items; auto-refresh every 30s.

[Monthly Credits Chart — full width]
  Bar chart: CO₂ kg per month (last 6 months)
  X-axis: Month names (in selected language)
  Bars: --color-sprout with slight gradient

[Refer a Farmer — bottom section]
  Title: "Refer a farmer, earn ₹50 per referral"
  Your referral link: [carboncredit.in/r/XXXXXX] [Copy] [Share via WhatsApp]
  Referrals made: N | Bonus earned: ₹XXX
  A simple progress nudge: "Refer 2 more to unlock ₹200 bonus"
```

#### Design Notes

- Every number label must be in the user's selected language.
- The **Live Activity feed** should distinguish the farmer's own transactions with a highlighted card (left border in `--color-success`, slightly different background).
- The **Refer section** uses WhatsApp sharing natively — this is the most used channel in rural India.
- Keep the "Log new practice" button visible and persistent — it is the farmer's core action.
- **Mobile-first:** On mobile, columns stack. Stat cards become a horizontal scroll row. The live activity feed is collapsed into an accordion by default.

---

### 7.4 Log Practice (Farmer Portal)

**URL:** `carboncredit.in/farmer/log-practice`

#### Layout

```
[Two-column layout]

LEFT — Input Form
  [+ Log a practice]
  
  Crop type (dropdown, bilingual labels)
  Practice type (dropdown, bilingual labels)
  Soil pH (range slider, value shown live)
  Land area in acres (range slider)
  Upload land image (optional, drag/tap)
  Fertilizer use (dropdown)
  
  [Estimate Carbon →] — full-width button

RIGHT — Estimated Result (updates after estimation)
  [Green highlight card]
    CO₂ Sequestered: XXX kg
    Credit value: ₹XXX
    Practice multiplier: X.Xx (type)
  Model info: "XGBoost · ICRISAT soil data · R² 0.81"
  
  [Issue credit to wallet] — primary CTA
  [Save as draft] — secondary

  [Monthly credits chart — smaller version]
```

#### Design Notes

- This page is exactly as designed — no structural changes needed.
- The bilingual crop/practice labels (e.g. "No-till / बिना जुताई") must respect the selected language.
- "Estimate Carbon" triggers a brief loading animation (spinning leaf icon) before showing results.
- Estimated result card animates in with a fade + slight scale up.
- "Issue credit to wallet" triggers a confirmation modal: "You are about to issue 124 kg CO₂ credit for ₹620. Confirm?"

---

### 7.5 Buyer Login

**URL:** `carboncredit.in/buyer/login`

#### Layout

```
[Centered card — max-width 480px]
  Logo + "CSR Buyer Login"
  Subline: "Access requires a verified corporate email"

  [Work email field]
  [Password field with show/hide toggle]
  [Log in — full-width blue button]

  — or —

  [New CSR Buyer? Request access — collapsible form]
    Full name | Company name | Work email
    ⚠ "Gmail, Yahoo, or personal emails are not accepted"
    [Request buyer access button]

  [Forgot password · Contact support] — footer links
```

#### Design Notes

- This page is correct as designed — no structural changes.
- The "Request access" section should animate open smoothly (accordion).
- Error state for personal emails should trigger immediately on input blur (not just on submit).

---

### 7.6 Buyer Dashboard

**URL:** `carboncredit.in/buyer/dashboard`

#### Navigation (Buyer Portal)

```
[Top Nav]
  Logo | Dashboard · Marketplace · Purchases · Certificates  |  [Company name + CSR badge]
```

#### Layout

```
[Summary Row — 4 stat cards]
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Credits Bought│  │Total CO₂ Off.│  │ Total Spent  │  │Farmers Supp. │
│    1,240     │  │   148 t      │  │   ₹6.2L      │  │     84       │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘

[Two-column section]

LEFT — Purchase History
  Title: "Purchase History"
  Table/list:
    CC-ID | Farmer Name | Crop · Practice | Weight | Price | Date | Download Receipt
  Paginated, 10 per page.

RIGHT — Live Activity Feed
  Title: "Live Activity" + green pulse dot
  Recent platform-wide purchases:
    CC-XXXX · [Farmer] · XXX kg — purchased by [Company] for ₹XXX
    [Farmer name] (State) issued credit — XXX kg
  Auto-refresh every 30s.

[CSR Certificate Section — full width]
  Title: "Your CSR Certificates"
  Grid of certificate cards:
    [Year/Quarter] | CO₂ Offset: XX t | Status: Verified | [Download PDF] [Share]
  "Generate new certificate" button → triggers modal to select date range
```

#### Design Notes

- The **Certificates** section is a key trust and compliance feature. Each certificate card should look premium — slight border glow, verified checkmark badge in green.
- Purchase history table should have a **CSV export** option.
- The buyer dashboard uses blue as the accent color (stat card highlights in `--color-sky-light` instead of green).
- Live activity on the buyer side emphasises credits being issued across India — reinforces supply confidence.
- Keep "Go to Marketplace" as a prominent persistent CTA (sticky sidebar button or floating button on mobile).

---

### 7.7 Buyer Marketplace

**URL:** `carboncredit.in/buyer/marketplace`

#### Layout

```
[Full-width two-column layout]

LEFT — Credit Heatmap (fixed sidebar on desktop)
  Title: "Credit Heatmap — India"
  Interactive SVG map of India
  States coloured by credit density (4-tier scale: Low/Medium/High/Very High)
  Legend included
  Clicking a state filters the listings on the right
  Tooltip on hover: "[State] — XXX credits available"

RIGHT — Filters + Listings

  [Filter Bar — collapsible on mobile]
    State / region (dropdown)
    Crop type (dropdown)
    Farming type / practice (dropdown)
    Price range ₹ (Min–Max dual input)
    Sort by (dropdown: Price low→high, Price high→low, Newest, Highest CO₂)
    [Apply filters] button | [Clear all] link

  [Listings Grid — 3 columns on desktop, 2 on tablet, 1 on mobile]
  
  Each listing card:
  ┌─────────────────────────────┐
  │ [Farmer Name]    ₹XXX      │
  │ [City, State]              │
  │ XXX kg CO₂                 │
  │ [Crop] · [Practice]        │
  │ [Date] · [CC-ID]           │
  │ [Buy Credit — blue button] │
  └─────────────────────────────┘

  Pagination: "Showing 1–12 of 28 listings"
  Load more / paginate below

[Buy Credit Flow — Modal on click]
  Farmer details | Credit summary | Price | "Confirm Purchase" CTA
  On confirm: Show success animation + "Certificate will be generated within 24 hours"
```

#### Design Notes

- The heatmap is the **visual centerpiece** — invest in making it interactive and clean. Use an SVG India map with state paths. Animate state fill on filter change.
- Clicking a state on the map = same as selecting that state in the filter dropdown (they are synced).
- Listing cards: Show the farmer's first name only (privacy), their state, the credit weight, crop, practice, and price. Keep it scannable.
- "Buy Credit" triggers a review modal — never a single-click purchase.
- Add a **"Bulk purchase" flow**: Allow buyers to select multiple listings (checkbox on card) and checkout all at once. This is critical for large CSR buyers purchasing in volume.

---

## 8. Multilingual & Accessibility

### Language Support

| Language | Script | Priority |
|---|---|---|
| English | Latin | Default |
| हिंदी | Devanagari | P1 |
| मराठी | Devanagari | P1 (Maharashtra focus) |
| తెలుగు | Telugu | P2 |
| ಕನ್ನಡ | Kannada | P2 |
| தமிழ் | Tamil | P2 |
| বাংলা | Bengali | P3 |
| ਪੰਜਾਬੀ | Gurmukhi | P3 |

### Implementation Rules

- Language preference is stored in `localStorage` and synced with the user profile.
- The **Buyer portal is English-only** — CSR managers are assumed to be English-proficient.
- The **Farmer portal is fully multilingual**: all labels, dropdowns, error messages, dashboard text, and chart axis labels must be translated.
- Bilingual labels for crop/practice dropdowns: "English name / Native name" (e.g. "Wheat / गेहूँ").
- Audio pronunciation helper for crop names (small speaker icon next to dropdown options) — optional but recommended for low-literacy users.
- All images must have descriptive `alt` text.
- Touch targets are minimum **44×44px** on all interactive elements.
- Focus rings must be visible (2px solid `--color-leaf`) on all keyboard-navigable elements.
- Form errors are announced via `aria-live` regions.

---

## 9. Motion & Animation

### Principles

- **Purposeful only**: Animations must guide attention or provide feedback — never decorative noise.
- **Fast and subtle**: All transitions under 300ms. Loading states under 500ms.
- **Respect `prefers-reduced-motion`**: All animations disabled when this OS setting is active.

### Animation Spec

| Element | Animation | Duration | Easing |
|---|---|---|---|
| Page transition | Fade in + 8px upward slide | 200ms | `ease-out` |
| Card hover | Scale 1.01 + shadow elevation | 150ms | `ease` |
| CTA button hover | Translate Y(-2px) | 150ms | `ease` |
| OTP box fill | Scale pulse (1.0→1.05→1.0) + border color | 200ms | `spring` |
| Stat card number | Count-up animation on mount | 800ms | `ease-out` |
| Live activity item | Slide in from right | 250ms | `ease-out` |
| Modal open | Fade + scale (0.96→1.0) | 200ms | `ease-out` |
| Heatmap state hover | Fill color transition | 150ms | `ease` |
| Credit issued success | Green checkmark + confetti burst (subtle) | 600ms | — |
| Hero background particles | Continuous slow float upward | Loop | `linear` |

---

## 10. Responsive Design

### Breakpoints

| Breakpoint | Width | Label |
|---|---|---|
| `xs` | < 480px | Small mobile |
| `sm` | 480–767px | Mobile |
| `md` | 768–1023px | Tablet |
| `lg` | 1024–1279px | Laptop |
| `xl` | ≥ 1280px | Desktop |

### Mobile-Specific Rules (Farmer Portal Priority)

- **Bottom navigation bar** on mobile for farmer portal: Dashboard · Log Practice · Credits · Refer (4 tabs, icon + label).
- Stat cards in a **horizontal scroll row** (peek of next card to indicate scroll).
- Live activity collapsed into a **"Recent Activity" expandable section** by default.
- Upload land image uses the **native camera** on mobile (input `accept="image/*" capture="environment"`).
- Sliders (soil pH, land area) use large touch-friendly thumb sizes (24px diameter).
- OTP boxes are large enough to type comfortably (min 52px wide each).
- Language selector is a **bottom sheet** on mobile, not a dropdown.

---

## 11. Innovative Feature Suggestions

The following additions are recommended to raise the product's quality and usability without adding complexity.

---

### For the Farmer Portal

**🌱 A. Soil Health Snapshot Widget**
A simple card on the farmer dashboard that shows the estimated soil carbon trend based on logged practices over time. A small sparkline graph: "Your soil health is improving ↑". This makes the abstract concept of carbon tangible and motivating for farmers.

**📷 B. Crop Photo Verification (Lightweight)**
When a farmer uploads a land image in Log Practice, run a simple ML check client-side or server-side to confirm the image contains a field/crop (basic vegetation detection). Show a small "Image verified ✓" badge. This increases buyer confidence without adding bureaucratic steps for the farmer.

**📱 C. WhatsApp Credit Alerts**
Opt-in toggle: "Notify me on WhatsApp when my credit is sold." Sends a simple WhatsApp template message ("Your 96 kg credit for No-till Soy was purchased by Infosys Foundation. ₹480 credited to your account."). Eliminates need for the farmer to open the app to check updates.

**🏆 D. Farmer Achievement Badges**
Subtle gamification: badges for milestones (First credit issued, 500 kg sequestered, 5 referrals made). Displayed on the dashboard. Not a game — framed as recognition. Increases retention and platform loyalty.

**🗺 E. Nearest Krishi Vigyan Kendra Locator**
A small info card: "Need help with sustainable practices? Find your nearest KVK →". Opens a map. Connects the digital platform to on-ground agricultural support without CarbonCredit.in needing to build it.

---

### For the Buyer Portal

**📊 F. CSR Impact Report Generator**
On the Certificates page, a "Generate Impact Report" button that auto-generates a PDF report: company logo, total CO₂ offset, number of farmers supported, state-wise breakdown, and credit IDs — formatted for MCA CSR filings or ESG reports. This saves the CSR manager hours of manual work.

**🔔 G. Credit Alert / Watchlist**
Let buyers set an alert: "Notify me when credits from Maharashtra wheat farmers below ₹600 become available." Keeps buyers engaged without requiring daily logins. Can be email or dashboard notifications.

**📦 H. Bulk Purchase Cart**
On the Marketplace, a floating cart icon that accumulates selected listings. Buyers can review, adjust quantities, and checkout all at once — similar to an e-commerce cart. Eliminates the one-by-one purchase flow for large buyers who need 50+ credits.

**🤝 I. Farmer Profile Preview**
When a buyer clicks a listing card, a side panel (not a full modal) slides in with a brief farmer profile: name, village, years farming, total credits issued historically, and a photo (if the farmer opted in). Adds a human connection and increases conversion.

**📅 J. Forward Purchasing / Subscription**
Allow buyers to pre-commit to purchasing X kg of carbon credits per quarter from a specific region or crop type. Gives farmers income predictability and gives CSR buyers automated CSR fulfilment. Flag as "Beta" and roll out to enterprise buyers first.

---

## 12. Do's and Don'ts

### ✅ Do's

- Use the established color tokens — never introduce ad-hoc hex values.
- Always show the ML model source and accuracy (R²) alongside estimated values.
- Test all farmer-facing flows on a low-end Android device (4-inch screen, slow connection).
- Use real Indian crop names and bilingual labels throughout.
- Keep the purchase flow always two steps minimum: "Review → Confirm."
- Validate corporate email domains on the buyer registration form client-side.
- Use WhatsApp-share URLs for farmer referrals (most accessible sharing channel).
- Show empty states with a helpful prompt (e.g. "No credits yet. Log your first practice →").

### ❌ Don'ts

- Don't use red anywhere except for error states — it conflicts with the green palette.
- Don't auto-submit forms or purchases without explicit user confirmation.
- Don't show the full farmer surname or village name in public-facing listing cards (privacy).
- Don't load all language font files on initial page load — lazy-load per language.
- Don't use stock photography of farmers — use illustration or actual user-consented photos.
- Don't over-animate the farmer portal — keep it fast and predictable.
- Don't show raw kg CO₂ numbers on buyer-facing pages without also showing the tonne equivalent.
- Don't use jargon ("sequestration," "XGBoost") without a simple tooltip explanation.

---

*Document maintained by the CarbonCredit.in product & design team.*
*For questions, contact: design@carboncredit.in*
