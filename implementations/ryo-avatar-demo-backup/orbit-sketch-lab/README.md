> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Orbit Sketch Lab

A runnable spatial sketch prototype using Ryo's original 160,000 Gaussian avatar and today's 2026-10-08 iPad Scaniverse room (301,106 Gaussians). Persistent hand-traced curves deform into editable orbital paths.

## Run

Use the portable ZIP from the private GitHub release (it includes original assets; source Git alone intentionally excludes them). Requires Node.js, no build or external API:

```
node server.mjs
```

Open http://127.0.0.1:8776. Play the narrated choreography or press **Explore**. Drag the scene to orbit the camera. Drag the white ring up/down to tilt its orbit directly. Change **Orbit inclination**, **Time speed**, and **Sketch ↔ 3D**. The controls modify the actual same curve geometry and planet trajectories. Film mode: `/?film`.

## Scope

This is authored choreography plus a real parameterized demo. It is not arbitrary sketch recognition, live AI, voice cloning, or a calibrated solar-system simulation. Orbital radii/speeds are illustrative, not physically accurate. Manual 15-bone Gaussian deformation; no supplied SMPL-X skeleton, finger animation, or lip sync. Room and avatar use separate visibility layers, not correct physical occlusion. Scan placement is manually fitted, not AR registration.

The original assets remain unchanged from transformer-avatar-sketch except narration. See asset receipts and delivery manifest. The public reference ledger distinguishes text, code, sampled frames, and full-motion review. External reference videos are not included in the delivered film.
