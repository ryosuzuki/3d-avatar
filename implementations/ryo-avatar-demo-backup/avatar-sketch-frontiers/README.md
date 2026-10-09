> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Avatar Sketch Frontiers

Four additional authored living-sketch examples, in a 144-second English film, derived from `avatar-sketch-worlds`. The original 160,000-Gaussian Ryo avatar and October 8 iPad Scaniverse room (301,106 Gaussians) are retained byte-identically. This complements, rather than replaces, the pendulum/fish/landscape/water film.

- Dinosaur: original outline gains extruded contours and body cross-sections, lowers toward the floor, and walks with alternating legs and tail motion. Stylized, not a paleontological reconstruction.
- Attention: drawn token/head outlines acquire depth; selecting a token changes all three normalized illustrative attention patterns and a displayed weight matrix. Not weights from a real language model.
- Gas: drawn cylinder unfolds into volume containing moving particles; volume and temperature controls update the displayed ideal-gas relative pressure `P ∝ T/V`, fixed N. Particle paths are authored bounded schematic trajectories, not molecular-dynamics collisions or the source of measured pressure. Compression is not asserted always to heat gas.
- Body: a preserved outline opens into depth with lung and heart symbols; breathing/depth/rotation controls change geometry. Schematic, not a medical/anatomical reconstruction.

## Run offline

```sh
node server.mjs
```

Open `http://127.0.0.1:8776`. Vendor modules, model assets, voice and captions are included. No API key or npm install is required for playback. Play/pause, timeline, room toggle, pointer camera orbit and per-example sliders are available. Film mode is `/?film`.

To regenerate browser proofs, install developer dependencies using `npm ci`, start `AVATAR_EXPLAINER_PORT=8812 node server.mjs`, and run `proof.mjs`/`capture.mjs` through the executing owner's browser supervisor. This handoff uses managed profile `agent-1`, verified CDP port18800. Do not adopt another owner's profile. Optional neural narration generation reads the configured local OpenAI SecretRef privately; no credential is distributed.

## Provenance and limitations

Chalktalk and the user's Google Slides examples inspired the broad sketch-to-spatial approach. This derivative relies on the already-inspected first-batch source ledger; it does not claim new reference-video viewing. No Chalktalk code was transplanted.

This is authored sketch choreography/procedural geometry, not arbitrary drawing recognition or live Q&A. Cursive text is typography. Finger grip and Gaussian skinning are approximate; no lip sync. Avatar/room layering prioritizes legibility and is not physical AR occlusion or tracked real-world registration. Floor placement is illustrative. The film keeps the presenter and scanned room.

Canonical outputs: `/path/to/local-assets`. Private backup owner: `sketch_worlds_remaining`; terminal target `origin/main`, exact allowlist `avatar-sketch-frontiers/`. Large film and portable ZIP are GitHub private release assets, not source-history blobs.
