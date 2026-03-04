# Pokimate — Roadmap

## Phase 1 (current)

- [x] Repo bootstrap, docs, root config
- [ ] Backend: auth, models, schemas, routes, engines, services, tests, seed
- [ ] Web: Next.js app, layout, dashboard, finance/debt/investments/life/goals/sync/ai/settings
- [ ] Mobile: Expo app, screens, auth, offline cache
- [ ] Desktop: Tauri wrapper, tray, backend spawn, notifications
- [ ] AI service: scaffold, prompts, cache
- [ ] Polish: error handling, empty states, lint, one-command run

## Phase 2 (backlog)

- Market price integration for investments (optional APIs)
- Health Connect / Apple Health deeper integration
- Multi-currency conversion (optional)
- Category auto-detection rules (regex/keywords) and AI suggestions (user confirms)
- PWA offline write queue (optional; currently read cache + clear offline message)

## Phase 3 (future)

- Optional second device sync strategy (beyond “last backup wins”)
- Custom ruleset override for financial health score (UI)
- More notification triggers (customizable)

## TODO backlog

- Ensure all 5 engine tests pass (XIRR, debt sim, budget math, encryption, health scores)
- Add ruff/flake8 and black to backend CI
- Add eslint/prettier/typecheck to web and mobile
- Document Windows build for Tauri in README_DESKTOP.md
