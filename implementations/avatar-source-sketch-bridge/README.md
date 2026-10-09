> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Actual source sketch to learned volume

An embodied comparison of two existing inference routes, preserving original source strokes separately from learned-mesh contours. This project performs **no new GPU inference**. All inference was completed in the separately evidenced experiment and frozen here.

## Run

The release ZIP includes private avatar/room PLY assets. With Python 3, create a venv, install requirements.txt and run `python server.py`, then open http://127.0.0.1:8836/. The checked-in Git source excludes PLY assets and generated audio; use the private release ZIP for a complete runnable copy. Playback of prepared cases requires no credential or model service. Uploading a simple closed-polygon JSON runs immediate CPU inflation, not category recognition.

## Frozen routes

* Fish: actual experiment-authored SVG centerlines → SDXL ControlNet conditioning → alpha-preprocessed actual image → Hunyuan3D-2mini on Apple MPS → 140,056-face original GLB. Display uses a declared 18,000-face quadric derivative; the original GLB remains byte-identical.
* Owl: actual experiment-authored SVG centerlines → SDXL conditioning → actual input image → TripoSR on Apple MPS → 40,592-face original GLB. Display applies only an explicit coordinate rotation, uniform scaling and centering.

These are not human sketch captures, a prerecorded live inference run, exact stroke-to-mesh registration, or a claim of category-independent learned-model success. Original SVG paths existed before image/mesh generation and are sampled directly. A white paper rectangle is excluded. Original paths remain gold planar references, while current-camera silhouettes come separately from the actual learned surface.

Independent uniform registration means the learned contour **can differ** from the drawing; inferred hidden surfaces and anatomy are not guaranteed. Shape depth unfolds as an authored presentation of a precomputed mesh. Fish motion is authored, not an anatomical rig. Pen grip and avatar occlusion are approximate.

## Rendering

Sparse view-dependent silhouette edge paths, coherent ordering, length filtering, Douglas–Peucker simplification, segment caps and depth-tested contour ribbons avoid dense all-triangle wireframes. Neutral shading is chosen for readability, not inferred original color. The exact captured room and original Ryo Gaussian data are unchanged.

`source-chain-verification.json` records the immutable input chain; `source/receipts` retains original inference receipts. `prepare.py` documents original source materialization and registration. Prepared `data/*.json` is sufficient for the runnable release without external experiment directories. `verify.py` checks source identity, geometry provenance and unchanged Gaussian hashes.

## Unknown-input fallback

The local /api/inflate endpoint takes a simple closed boundary, preserving its boundary while constructing a symmetric thickness volume. It has no category lookup, hidden-part reasoning or articulation, and cannot replace a learned anatomically complex mesh. The nine-point held-out polygon in unseen-input.json and data/fallback.json is separate from the fish/owl cases.

## Film

English neural narration uses the already authorized backend OpenAI credential, never bundled or sent to the frontend. `voice.py` requires the local private credential only when regenerating speech. Prepared browser playback is credential-free. Capture creates only owned managed browser targets; the browser supervisor is required in this workspace.
