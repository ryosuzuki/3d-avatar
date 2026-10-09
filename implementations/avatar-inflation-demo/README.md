> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Embodied closed-stroke inflation

Ryo's original Gaussian avatar pen-traces an input closed boundary; its interior inflates into a genuine triangle mesh while the boundary stays at zero depth. View-dependent contours and sparse surface sections reveal depth without triangle-wireframe clutter. Fish, octopus, leaf, and a previously unseen asymmetric shape use the same category-independent operation.

Derived renderer from `avatar-generalized-sketch`; original sources and exact avatar/room assets are unchanged. Inflation implementation originates in `https://github.com/ryosuzuki/sketch-3d-method-review`.

## Run

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python prepare.py
python3 server.py
```

Open http://127.0.0.1:8832/. `prepare.py` validates watertightness, winding, positive volume and original boundary retention. `inflate.py` accepts arbitrary simple closed polygons. One closed boundary, symmetric thickness; not sketch recognition, hidden anatomy inference, or anatomical articulation. Animation is illustrative. Narration is neural English; backend credential is never included.

Video outputs live in Storage/outputs/avatar-inflation-demo/2026-10-09. `capture.mjs` is a supervised owned-tab renderer; do not run against a managed browser without its ownership lease. Viewer uses exact 160,000-avatar and 301,106-room original Gaussians.

## Private backup and media

Source: https://github.com/ryosuzuki/avatar-inflation-demo . The private release `inflation-2026-10-09` includes the narrated 57.7-second film, screenshots, and complete runnable ZIP containing the exact original Gaussian assets. These private PLY assets are omitted from ordinary Git blobs and identified in `asset-receipt.json`.

Independent method source revision: `35c25a9361f47a439b507de0eebe0fe593610159` at https://github.com/ryosuzuki/sketch-3d-method-review .

QA: all four JSON and GLB meshes are watertight and winding-consistent with positive volume; boundary retention errors below 3e-8. Full MP4 decode, subtitles, stream timing, loudness and real-time browser playback checked. Full perceptual audio listening is not claimed.
