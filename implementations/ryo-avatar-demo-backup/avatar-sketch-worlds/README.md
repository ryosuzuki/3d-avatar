> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Avatar Sketch Worlds

Four implemented, authored pen-to-volume performances, in one 128-second English film. Retains the original **160,000-Gaussian Ryo avatar** and **301,106-Gaussian October 8 iPad Scaniverse room**, byte-identical to the approved baseline assets.

1. Pendulum: the drawn bob opens into volume; the actual swing angle generates its waveform.
2. Fish: the retained silhouette, fins, tail and eye unfold into wireframe cross-sections; time-dependent body and tail deformation makes it swim.
3. Landscape: the original ridge extrudes a terrain grid, the retained river path projects onto that surface and carries current; a cloud contour gains depth and drifts during a camera orbit.
4. Water: original O/H circles open into true world-space spheres, bind with a 104.5° bent arrangement, and turn together. Radii and bonds are schematic, not literal atom scale.

## Run

Unzip the portable project, then:

```sh
cd avatar-sketch-worlds
node server.mjs
```

Open `http://127.0.0.1:8776`. No bundler, API key, network, or npm install is required for playback. Vendor modules and original assets are included in the ZIP. Play/pause, timeline, room toggle and applicable geometry controls remain functional. Mouse drag rotates the view. The authored film exports at 1920×1080, 30 fps.

For automated proofs/rendering, `npm ci` installs the pinned Playwright developer dependency. Run scripts with the executing owner's supervised managed browser lease; `capture.mjs` expects the assigned agent-1 endpoint and a local server at port8808. Production narration generation is optional, uses the configured local OpenAI SecretRef privately, and is not required to view the delivered project.

## Artifacts

Canonical output: `/path/to/local-assets`

- `avatar-sketch-worlds.mp4`: final H.264/AAC film with English captions/subtitles.
- `avatar-sketch-worlds-project.zip`: self-contained source, Gaussian assets, narration and delivery film.
- `delivery-manifest.json`, `artifact-hashes.json`: provenance and checks.
- `proof-49.png`, `proof-86.png`, `proof-117.png`: fish, landscape, and water examples.
- `scene-proof.json`, `geometry-verification.json`, `playback-verification.json`: actual browser evidence.

## Sources and boundaries

Derived from the approved `avatar-chalktalk-expanded`, not a replacement for its originals. Read-only Google Slides reference was actually inspected: slide109/174 'AR other things' is an 11-video AR-book/drawing montage; nearby chemistry, fish/ocean, dinosaur and letter/coloring interaction examples informed example selection. Embedded reference clips were not played. See `references/source-ledger.md`.

This is authored choreography and procedural geometric animation, **not arbitrary sketch recognition or live AI**. Pen/hand IK and Gaussian skinning are approximate; no supplied finger rig or lipsync. Room/avatar rendering is layered to maintain visibility, not physically correct AR occlusion or tracked registration. English cursive labels are typography, not captured handwriting. A private remotely accessible live-Q&A sketch app and later additional demos remain separate, pending scope.
