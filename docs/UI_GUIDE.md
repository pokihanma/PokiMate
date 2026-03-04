# Pokimate — UI guide

## Design tokens (Tailwind)

- **Container**: max-w-screen-2xl; padding px-4 sm:px-6 lg:px-8.
- **Card**: rounded-2xl; subtle border; moderate backdrop blur; soft shadow.
- **Typography**:
  - Title: text-2xl font-semibold
  - Section header: text-lg font-medium
  - Body: text-sm text-muted-foreground
  - KPI value: text-3xl font-semibold tracking-tight
- **Spacing**: gap-4, gap-6; vertical rhythm space-y-4.
- **Colors**: Dark-first palette using shadcn theme tokens; avoid neon; focus on readability.

## Layout rules

- **Sidebar**: Fixed on desktop; collapsible on tablet; bottom nav on mobile.
- **Topbar**: Always present on web (month selector, search, sync, user menu).
- **Page start**: Page title → primary action button → secondary actions in overflow.

## UX rules

- **Loading**: Skeletons preferred; spinners for small actions.
- **Empty states**: Clear CTA (e.g. "Add first transaction").
- **Forms**: Client-side validation + display server errors.
- **Tables**: Sortable columns; sticky header on large lists.
- **Charts**: Tooltips, legends, responsive container.

## Components (web)

- **GlassCard**: Card with backdrop blur and subtle border.
- **KpiCard**: Title + large value + optional trend.
- **InsightCard**: Collapsible content block (e.g. AI insight).
- **TransactionsTable**: Sort, filter (date, type, category), search.
- **TransactionForm**: Drawer or modal with validation.
- **SyncPanel**: "Sync now" button, status (last sync, device, count), restore flow with warnings.
- **AiInsightsPanel**: Collapsible sections; "Last generated on ..." cache label.

Use shadcn/ui consistently; maintain dark-first and consistent spacing/typography.
