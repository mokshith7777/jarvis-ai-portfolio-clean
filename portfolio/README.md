# Mokshith Reddy — Cinematic Portfolio

A browser-native portfolio built with semantic HTML, modern CSS, vanilla JavaScript and a WebGL 2 fragment shader. No framework, bundler or runtime dependency is required.

## Preview locally
Open `index.html` in a modern browser, or run `python -m http.server 8000` from this directory.

## Performance and resilience
- WebGL 2 background shader with a graceful CSS-only fallback.
- Device-pixel-ratio capped at 1.5.
- Animation pauses when the canvas is off-screen or the tab is hidden.
- Handles WebGL context loss and restoration.
- Responsive layout and reduced-motion support.
- No external runtime libraries. Google Fonts are progressive enhancement.

## Deploy
The repository workflow at `.github/workflows/portfolio-pages.yml` publishes this directory to GitHub Pages.
