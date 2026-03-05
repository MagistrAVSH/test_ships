# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-page 3D ship viewer web app ("Star Sparrow Fleet") built as a static site with no build step. It displays 20 spaceship models with swappable color skins, engine exhaust effects, and a starfield background. Designed to run as a Telegram Web App or standalone in a browser.

## Running

Serve the project root with any static HTTP server (needed for ES module imports and asset loading):

```bash
npx serve .
# or
python -m http.server 8000
```

No build, lint, or test commands exist — the entire app is a single `index.html` with inline `<script type="module">`.

## Architecture

**Single-file app** — all logic lives in `index.html`:
- Uses Three.js v0.162.0 via CDN import map (no node_modules)
- `package.json` exists only for repo metadata; there are no dependencies to install
- GLB models (`StarSparrow1.glb` – `StarSparrow20.glb`) loaded at runtime via GLTFLoader
- Shared textures in `Textures/` (albedo colors, normal, emission, metallic/smoothness maps)
- `BonusContent/` contains additional FBX/GLB assets not used by the main viewer

**Key systems in index.html:**
- **Renderer setup** — WebGL with ACES tonemapping, Unreal bloom post-processing via EffectComposer
- **Texture remapping** — Unity MetallicSmoothness texture (R=metallic, A=smoothness) is split into separate metalness/roughness textures at runtime via canvas pixel manipulation
- **Ship carousel** — loads/caches GLB models on demand, preloads adjacent ships, slide animation on navigation
- **Skin system** — 10 color skins applied by swapping the albedo texture; engine glow color matches selected skin
- **Engine exhaust** — particle system using custom ShaderMaterial with additive blending + glow sprite
- **Starfield background** — fullscreen shader with procedural stars, nebula bands, and twinkle animation
- **Lock/unlock** — ships start locked (greyscale filter) except ship 1; tap overlay to unlock
- **Telegram integration** — conditional Telegram Web App SDK loading, fullscreen request, vertical swipe disable
