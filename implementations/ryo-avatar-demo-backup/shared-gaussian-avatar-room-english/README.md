> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo · English room explainer

A 56-second, English-narrated version of the Ryo spatial explainer. It uses the **exact original 160,000-Gaussian Ryo avatar** shared by Hyeon, overlaid in Ryo’s **actual Quest room capture 20261002_215403**. Both avatar and room are 3D geometry, not a person-video billboard or a flat room backdrop.

## Run the portable replay

Node 18+ is sufficient. No model credentials, API account, or dependency install is needed for playback.

```sh
node server.mjs
```

Open http://127.0.0.1:8776/ and click Play. English narration, English captions, gestures, progressive pen strokes, timeline diagrams, and spatial nodes share the measured narration clock. Drag to orbit; scrub/pause/restart or hide the room. `?film` hides controls. The server is loopback-only by default; `AVATAR_EXPLAINER_PORT` changes the port.

## Exact assets and derivation

- Avatar: unmodified `assets/ryo_tpose.ply`, 160,000 original Gaussian centers/covariances/color/opacity. SHA-256 `add76ef82f23e209b830b756fb942d3f4e4c587188e4776aebcdf3cbcad09f12`.
- Room: unmodified `assets/quest-room-geometry.json`, SHA-256 `280da651e832853538fddd7ac856b2d4fb7126f62a99d01e18368dad1ad661bb`.
- Room appearance: 16 **authentic calibrated Quest RGB frames**, projected per fragment onto the original room global mesh with recorded camera positions/quaternions and intrinsics. The ceiling is opened in the derived viewer; no room imagery is generated. `room-texture-projection.json` includes original source-frame hashes. Texture preparation source is in `scripts/`.
- Common transform: original Quest meters mapped to `[x-3.5,y+1.222106,z+1.7]`. Avatar feet are placed on the captured floor; diagram objects occupy this same 3D coordinate system.
- Orchestration: actual TypeSafe Jev 1.13.0 choices from the prior verified call, **unchanged selections** and retimed to newly measured English narration. This derivative makes **no new Jev call** and no purchase/top-up.
- Speech: OpenAI `gpt-4o-mini-tts` / `shimmer`, stock English synthetic voice. Segment durations are measured after canonical PCM rewrapping; the full program is loudness-normalized to approximately -16 LUFS.

## Scope and honest limitations

This is deterministic playback of a **saved Jev presentation plan**, not live AI Q&A. The spoken script and visual catalog are authored; Jev selected gesture/focus/color/node-order parameters. The avatar has an added approximate 15-bone rig and analytic arm IK, not the original SMPL-X weights. No Ryo voice clone, facial lip sync, finger articulation, force/contact physics, solved foot planting, or live physical AR registration is claimed. Avatar/board placement is a prototype arrangement inside the measured room.

The room is a coarse measured mesh with authentic projected textures, **not a complete photogrammetric reconstruction**. Captured-scan holes, projection seams, and furniture texture stretching remain visible; unseen faces use a neutral color. Illustrative curves are timing diagrams, not experimental data.

## Export and verification

`capture.mjs` captures deterministic 1920×1080 frames at 30 fps with the executing owner’s supervised managed browser. `verify-final.mjs` verifies the delivered MP4 in actual browser playback. These production scripts need Playwright and the documented OpenClaw browser lease; portable replay does not.

The output directory contains the MP4, English SRT/VTT/transcript, proof screenshots, and a delivery manifest with hashes and complete decode, stream/timing, audio transcript/loudness, full audiovisual model review, browser playback, source-placement, and cleanup evidence. Original Japanese outputs are preserved unchanged.

## Attribution

- Concept inspiration: Sean’s [Jev interaction / Primer](https://github.com/sseanliu/jev-interaction), verified commit `d9bd43ec106144a20395a4e2deb9c7a075e014c0`. No Sean code or recordings are copied.
- [Original shared Ryo avatar]((private source discussion omitted)).
- GaussianSplats3D 0.4.7 and Three.js 0.170.0; MIT licenses in `vendor/`.
