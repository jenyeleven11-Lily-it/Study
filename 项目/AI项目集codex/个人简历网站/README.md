# Kelo Hero Preview

This is a minimal React + Vite + Tailwind preview for `KeloAutomationHero`.

## Run locally

Install a current Node.js LTS release (which includes npm), then run from this folder:

```powershell
npm install
npm run dev
```

Open the local URL printed by Vite. The app contains only the Kelo hero from the supplied prompt; the earlier personal-resume draft has been removed.

The hero uses the supplied Kelo video and logo URLs, so those assets require an internet connection. The video is muted, loops, and is slowed to 0.6×. Tailwind is configured without its global Preflight reset so the component's styles stay scoped.
