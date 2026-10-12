# VanDrishti — frontend redesign

## Design and architecture
Editorial ivory, charcoal, forest and ochre surfaces; Playfair Display headings and DM Sans body. A cinematic wildlife cover separates the public website from a practical field workspace. All colors are semantic CSS tokens. The cover is generated illustrative imagery, not field evidence or an actual detection output.

This implementation uses the existing Lovable project's React 19, TanStack Start file-based routing and Tailwind v4. The uploaded source is standalone Vite React, but replacing the host framework would break the running project. It is not a drop-in App.jsx replacement for that standalone setup. No new packages, backend, authentication or database were introduced.

## Source organization
- `src/styles.css`: shared tokens, public and workspace layouts, mobile layouts and reduced-motion support (modified).
- `src/components/layout/public-layout.tsx`: public header, mobile navigation, branding and footer (new).
- `src/components/layout/content-page.tsx`: shared public photographic cover (new).
- `src/components/layout/workspace-layout.tsx`: operational sidebar, navigation, errors, configured service and child outlet (new).
- `src/features/wildlife/context.tsx`: shared run state, file validation, original API requests, resolution updates (new).
- `src/features/wildlife/shared.tsx`: headings, status and empty states (new).
- `src/features/wildlife/analysis.tsx`: overview, upload, drag/drop, selected-file state, processing and reset (new).
- `src/features/wildlife/results.tsx`: species counts, confidence, processed playback and intelligence reports (new).
- `src/features/wildlife/registers.tsx`: searchable alerts/reviews and keyboard-accessible explicit resolution dialog (new).
- `src/lib/page-head.ts`: unique leaf page metadata helper (new).
- `src/routes/index.tsx`: public home (replaced).
- `src/routes/platform.tsx`, `how-it-works.tsx`, `about.tsx`: distinct public destinations (new).
- `src/routes/workspace.tsx`: operational layout (new).
- `src/routes/workspace.index.tsx`, `workspace.analysis.tsx`, `workspace.results.tsx`, `workspace.intelligence.tsx`, `workspace.reviews.tsx`, `workspace.alerts.tsx`: operational destinations (new).
- `src/routes/__root.tsx`: app provider, font stylesheet and VanDrishti document metadata/favicon (modified).
- `src/components/ui/button.tsx`: field and cinema variants (modified).
- `src/components/ui/dialog.tsx`: semantic overlay color (modified).
- `src/assets/tiger-forest.jpg`: generated illustrative wildlife cover (new).
- `public/favicon.svg`: brand mark (new).
- `src/test/app-routing.test.tsx`: ten destination matching checks (modified).
- `.env.example`: local and production API configuration (new).
- `AGENTS.md`: architectural invariants (modified).

## Install and run
No dependency additions. The source archive includes package.json and bun.lock for the existing host stack.

```sh
bun install
cp .env.example .env
bun run dev
# Production build, outside the managed Lovable build harness:
bun run build
```

The running preview uses `VITE_API_URL=https://vandrishti-m1.onrender.com`. For local development, set `VITE_API_URL=http://127.0.0.1:8001` in `.env`. If unset, the source retains the original local fallback. Local storage is not used; run state persists across client navigation but resets on a full reload, as in the original app. Public fonts load from Google Fonts with system fallbacks. The wildlife cover is bundled locally and needs no manual asset download.

## Functionality mapping and contracts
| Existing functionality | New destination | Original contract retained |
|---|---|---|
| Video selection, drag/drop, validation, removal | Video analysis | `accept=video/*`, requires video MIME type |
| Upload | Video analysis | POST `/api/v1/analysis-runs/upload`, FormData key `video` |
| Process | Video analysis | POST `/api/v1/analysis-runs/{analysis_run_id}/process`, no request body |
| Retrieve result | Analysis results | GET `/api/v1/analysis-runs/{analysis_run_id}/result` |
| Processed footage | Analysis results | Original API base + `output_video`, HTML video controls |
| Species counts and confidence | Analysis results / overview | `detections.species_counts`, `detections.total`, `detections.average_confidence` |
| M4 intelligence | Intelligence reports | `result.intelligence.title/status/narrative` |
| Retrieve reviews | Review queue | GET `/api/v1/reviews?run_id={analysis_run_id}`, array response |
| Retrieve alerts | Field alerts | GET `/api/v1/alerts?run_id={analysis_run_id}`, array response |
| Resolve review | Review queue dialog | POST `/api/v1/reviews/{review_id}/resolve`, JSON `{resolution_note: trimmedNote}` |
| Search/filter/reset | Alerts / reviews / video analysis | Same local filtering and run reset semantics |

All original active actions have a destination. Failed review resolution retains the dialog and typed note. Duplicate analysis submissions are disabled. Missing data is displayed as unavailable rather than invented zero detections. Partial alert/review fetch warnings remain visible instead of being cleared by navigation.

## Separately documented compatibility correction
The uploaded App.jsx calls `setRunId(analysisRunId)` then interpolates the previous `runId` state in POST `/process`. On a first run, this sends `/null/process`. The redesigned implementation uses the upload response's local `analysisRunId`; method and endpoint suffix are unchanged. The deployed OpenAPI schema confirms `/process` exists. Although the brief mentions `/analyze`, switching to it would change the uploaded contract, so it is not used.

## Unused uploaded modules
AlertPanel, CctvFeeds, Radar3D, ReIDTracker and ReviewModal were not imported by the uploaded App.jsx. Live camera samples, animal identities, radar markers and dispatch alerts were hardcoded demonstrations, not connected functionality. They are not presented as real monitoring. The working review-note behavior is implemented with a dialog instead of window.prompt. Individual animal tracking, live camera feeds and dispatch are explicitly marked as unavailable on the platform page; no fake evidence is seeded.

## Validation actually performed
- Managed build/typecheck: latest recorded result `build OK`.
- Vitest: all ten routing tests passed.
- Browser: desktop public page and analysis page rendered with no page runtime errors.
- Browser: 390px phone page had no horizontal overflow; mobile menu navigated to `/platform`.
- Browser: selected a real generated one-second MP4 and attempted POST upload to the real deployed service. The UI preserved the selected file, showed a clear connection error, and re-enabled retry.
- External backend preflight: HTTP 400, `Disallowed CORS origin` for `http://localhost:8080`.

## Remaining integration blocker
The deployed backend rejects this preview's origin. No CORS, backend service, authentication or schema changes were made. Its owner must permit the preview and eventual production origins before successful browser upload/processing can be verified. Successful live analysis, output playback, populated reports and review resolution remain unverified; no mocked data was used to claim success. A reachable OpenAPI schema does not establish working cross-origin browser analysis. The original output-video URL concatenation is preserved and assumes the backend returns a relative path.