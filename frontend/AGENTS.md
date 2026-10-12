<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Application architecture
- Keep TanStack Start file-based routes, with public content pages and an Outlet-based workspace layout; this retains the host framework and distinct shareable destinations.
- Keep wildlife API state in a shared browser-side provider and send requests directly to VITE_API_URL; this preserves the existing external service without introducing a backend dependency.
- Use the uploaded App.jsx as the active workflow contract, not the unimported demo modules; this prevents sample feeds, tracking and dispatch from being mistaken for real capabilities.
- Use the local upload response ID for POST /process rather than stale React state; this repairs the supplied identifier bug without changing the service contract.
- Express visual roles through global semantic tokens and shared controls; this keeps public and operational surfaces consistent.
- Keep theme preference in a shared root provider with a document-level dark class and browser preference storage; this keeps public pages and workspace synchronized without touching the wildlife service.
- Render public wildlife covers through a shared responsive photograph component backed by asset pointers; this keeps imagery consistent and framing appropriate across screen sizes.
- Use native router view transitions, intent preloading, and CSS motion with reduced-motion overrides; this smooths navigation without intercepting wheel/touch scrolling or changing service behavior.
