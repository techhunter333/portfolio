# Security

Static portfolio site (`optimusbot.dev`) — no backend, no auth, no secrets.

## Surface

| Area | Notes |
|------|--------|
| HTML/JS | Client-only interactions (labs, command palette, theme) |
| External | Lucide (pinned CDN), Google Fonts, CounterAPI visits |
| Contact | `mailto:` only — message never stored server-side |
| Resume | Static `resume.pdf` download |

## Hardening applied

- Content-Security-Policy (meta), nosniff, referrer, permissions-policy
- Lucide pinned (no `@latest`)
- DOM logger uses `textContent` (no free-form `innerHTML` messages)
- Command palette: hash allowlist + safe external URL open (`noopener,noreferrer`)
- API playground endpoint allowlist
- Visitor counter: numeric validation, `credentials: 'omit'`
- Contact form: length limits + `encodeURIComponent` for mailto

## Reporting

If you find a vulnerability in this site or related projects, email **techhunter333@proton.me** with steps to reproduce. Please allow reasonable time before public disclosure.
