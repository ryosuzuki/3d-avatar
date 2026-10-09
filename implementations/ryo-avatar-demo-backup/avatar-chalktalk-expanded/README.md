> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo — three living sketches

Chalktalk-inspired embodied explanation, rendered with the **exact original 160,000-Gaussian Ryo avatar** and **301,106-Gaussian iPad room captured on 2026-10-08**. Neither is replaced by a mesh character, billboard, generated human, or fabricated room. Original `avatar-living-sketch` is preserved unchanged.

## Run

Requires Node 20+ and a modern WebGL2 Chromium browser. No external API calls are needed to run; the English neural narration is included.

```sh
npm install
npm start
```

Open http://127.0.0.1:8776/. Play, scrub the timeline, orbit the camera, and toggle the room. Four sliders change the simulation: amplitude, frequency, vase width, rotation. Seek to 22, 50, or 80 seconds to examine each example. A changed control persists and overrides the corresponding authored choreography.

`window.drawFrame(t)` renders deterministically at a given time. `window.setParameters({...})` accepts `amplitude`, `speed`, `waist`, and `angle` (radians). `window.morphEvidence` exposes current values and coupling evidence. `window.getEvidence()` exposes asset identity, hand IK state, room identity, and camera pose.

## Implemented mechanisms

1. A short embodied pen drawing opens into a wireframe pendulum. Its analytic angle drives the bob's position and the time-history waveform. **The avatar does not draw the waveform.** Amplitude and frequency alter both outputs.
2. A drawn profile sweeps around an axis. All meridians and cross-sections are computed from the retained profile. Changing width edits both the visible profile and the actual wireframe volume.
3. A drawn arrow connects to a 3D coordinate frame. A single Y-rotation value updates the arrow's actual vertices and a synchronized numeric rotation matrix. Rotation is controllable in the runnable project.

World-space ribbon geometry provides consistent visible stroke thickness. Text labels use natural-looking cursive typography rather than segmented block-letter paths. Initial shapes are drawn in approximately 3–4 seconds per multi-stroke example.

## Honest scope

This is an **authored, deterministic explanatory performance** with causal interactive parameters, not a general-purpose recreation of all Chalktalk. Shapes and connections are authored, not recognized from arbitrary live pen input. No general glyph classifier, node-graph editor, connection cutting, fish example, full matrix network, collaboration, gesture tracking, tracked AR, realtime AI, or facial lip sync is implemented. Cursive labels are typography, not captured handwriting. The avatar's rig is a manually fitted anatomical adapter, not supplied SMPL-X weights; its pen-hand pose is approximate.

All source avatar centers/covariances/color/opacity are retained; room has source Gaussian centers/covariances/DC color, with original SH3 `.spz` preserved. Room positioning is manual prototype placement, not AR registration.

## Output and verification

The 88-second narrated 1080p30 MP4, subtitle files, three screenshots, capture/causal-control receipts, asset hashes, codec probe, and loudness report are saved at:

`/path/to/local-assets`

`delivery-manifest.json` records the exact final MP4 and hashes. `capture.mjs` requires the managed-profile supervised browser lease described by this workspace's tools-browser skill; it is a production/export helper, not necessary to run the demo. `scripts/finalize.py` performs muxing and full decode checks.

## References

- Ken Perlin / Chalktalk: https://github.com/kenperlin/chalktalk
- User's starting lecture timecode: https://youtu.be/ZZi3I_NCiUk?t=322
- Chalktalk in AR / Holojam: https://vimeo.com/232230096
- Verified playable excerpt: https://x.com/HCI_Research/status/1251898938967207937

This project reimplements three source-inspired mechanisms; it does not redistribute Chalktalk code. See the accompanying reference coverage ledger for what was actually observed and what remains unimplemented.
