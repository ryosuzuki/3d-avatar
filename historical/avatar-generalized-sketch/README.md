> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Generalized embodied sketch lab

A genuine question → OpenAI-generated constrained geometry schema → validated mesh → visible pen-traced projected edges → same-XY depth morph → semantic illustrative movement pipeline, preserving the original Ryo Gaussian avatar and captured iPad room.

## Run

`python3 server.py --port 8824`, then open http://127.0.0.1:8824/ . Existing authorized OpenAI secret route is read server-side only; no key is in source/client responses. No paid provisioning or automatic topup.

Type a new request, load a saved generated request, or import GLB/OBJ/custom indexed JSON mesh. No arbitrary model code is evaluated. Mesh operations are general swept variable-radius spines, irregular extrusions, revolved profiles, and explicit indexed geometry—not a fixed fish/bird object catalog. `geometry.js` smooth-resamples spines and provides hybrid contour/crease/sparse surface-grid rendering. Morph retains stroke XY while depth unfolds; movement is schematic swimming, flapping, sway or spin, not an anatomical rig.

## Honest limits

Model-generated geometry quality is uneven. Early overly thin fish and stylized chair/plant are retained as failure/variant evidence. Coordinate double transforms and schema mismatches were identified by actual rendered inspection; repaired request/schema iterations are recorded. This route creates procedural illustrations, not photoreal recovered anatomy. Imported meshes preserve their geometry but default motion is illustrative deformation, not generated skeletal animation. Captured room placement is manually aligned, not AR registration.

## Original assets / artifact locations

Original projects are read-only sources `/path/to/local-assets` and `avatar-sketch-worlds`. The two PLY files here are byte-identical copies. `source-manifest.json` records hashes. Large assets/audio/render outputs stay in Storage, not Git. Outputs: `/path/to/local-assets`.

`python3 verify.py` verifies scene records, invalid-operation/index rejection and original asset parity. `node --check app.js` checks module syntax. `proof.mjs` uses the leased agent-1 managed browser and deterministic `window.drawFrame(t)` to inspect real rendered evidence and preserve other tabs. `window.loadRecord(record)` and `window.importMesh(url,name,metadata)` expose the common renderer for additional backends.

Dependencies: Three.js r170, gaussian-splats-3d (vendored with licenses); Playwright only for verification/render scripts. Existing `avatar.js` and `rig.js` implement original Gaussian skinning.

## Three real geometry routes

- Fresh question generation through the existing authorized OpenAI route, validated before mesh construction. A bounded quality-planner experiment uses gpt-4.1; the detailed planner is the UI default and the fast planner is gpt-4.1-mini. Generator schema failures and repairs are retained, not hidden.
- Generic closed-polygon distance-field inflation from the independent lane, imported byte-identically. No category lookup or semantic recognition.
- Actual Hunyuan3D-2 full neural mesh, 50 steps at256 octree resolution on AppleMPS GPU, imported byte-identically from the lane checkpoint. Its source image is an existing fixture; this UI does not pretend to run fresh question-conditioned Hunyuan inference.

`imports.json` exposes those concrete checkpoint assets in the common saved-asset selector. `imported-mesh-receipt.json` contains source hashes/model revision. Hunyuan seahorse92,540vertices/185,068faces and inflated fish15,362vertices/30,720faces are retained without replacement or mesh decimation. Only sketch paths are simplified for legibility; the actual mesh stays intact. Coherent feature paths and true triangle-plane sections avoid dotted downsampling. Ink ribbons have a contrasting halo against the captured bright room.

`comparison.json` is a method demonstration, not a controlled same-input benchmark. `prepare-comparison.py` creates authorized English neural speech; `align-comparison.py` keeps authoritative text and aligns it to complete audio word timestamps. Large binary assets are in Storage with receipts, not Git.

## Verified deliverables

Main comparison: `three-route-comparison.mp4`,78.27seconds,1280×900,H264/AAC,30fps CFR (15unique rendered frames persecond), burned and embedded English captions. Final-file decode and faststart passed; audio/video drift54.7ms. Source-record film: `generated-schema-verified-film.mp4`,115seconds (fish,bird,plant). `artifact-locations.json` records immutable hashes and exact local binary locations. `review.html` plays the exact main comparison file. Complete audio was listened to by an audio-capable model, not a human headphone reviewer. Final-frame probes were actually inspected.
