> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo · Spatial explainer

An independently authored3D prototype inspired by Sean's Primer / living-blackboard interaction concept. The API-planned variant uses a real TypeSafe AI Jev call to select the presentation cues, then replays that plan against the same narration clock. Uses the **exact Ryo160,000Gaussian avatar** shared by Hyeon, not a regenerated avatar or person-video billboard.

## Run locally

Node18+ is sufficient for the viewer; no model credentials are needed.

```sh
npm start
```

Open http://127.0.0.1:8775/. The saved Jev plan requires no credentials for replay. Add `?baseline=1` to compare the original authored cue behavior. Click Play for synchronized Japanese narration, articulated gestures, progressive transparent-board strokes and diagrams that move into3D. Drag to orbit; scrub, pause/restart, or hide the captured room. `?film` hides playback controls. The endpoint is loopback-only by default. Another port can be set with `AVATAR_EXPLAINER_PORT`.

## What is implemented

- Original anisotropic3DGaussian centers, covariance, color and opacity; unmodified `assets/ryo_tpose.ply`, SHA-256 `add76ef82f23e209b830b756fb942d3f4e4c587188e4776aebcdf3cbcad09f12`.
- Real TypeSafe AI `jev-latest` cue planning via a single bounded `/v1/systemone` request; source request/result and usage evidence retained in the private output receipt. Saved parameters visibly affect stroke color, node target/order/highlights and two-handed gestures.
- Added approximate15-bone skinning and analytic armIK, reused from the earlier walking/box interaction demo.
- Actual transparent3Dboard with progressive diagram marks; pen contact, visible timeline cursor and pointing ray. Persistent diagram nodes visibly leave the board and gain depth.
- Measured narration segment boundaries and a deterministic shared playback clock. Export at1920×1080,30fps.
- Original Ryo Quest room capture geometry, rendered as a dark transparent cutaway. Placement is prototyped, not registered to a physical room.

## Explicit limits

This is **prerecorded / deterministic replay of a saved API-generated orchestration plan**, not a live question-answering AI. Japanese narration and the available visual/gesture catalog are authored; Jev selects gesture/focus/color/node-order parameters. Our independent adapter applies those selections to the original avatar. The video does not regenerate a fresh answer while it plays. Narration uses the stock Japanese OpenAI `gpt-4o-mini-tts` / `shimmer` voice, **not Ryo voice cloning**. Root shifts are authored stage movement, without solved foot planting. No facial lip sync, finger articulation, SMPL-X source weights, tracked writing, force/contact physics or liveAR registration is claimed. The curves are illustrative timing diagrams, not empirical data. Hand and drawing cues are authored synchronization, not model-generated or measured word-level alignment. Live conversational generation and interruption handling are next steps, not implemented features.

## Reference / attribution

- Sean's [jev-interaction / Primer](https://github.com/sseanliu/jev-interaction), verified main `d9bd43ec106144a20395a4e2deb9c7a075e014c0`. Inspiration: progressive explanation steps, shared narration/drawing clocks and referential emphasis. No Sean repository code or recordings are copied into this bundle; repository has no license declaration.
- [Original shared avatar source]((private source discussion omitted)).
- GaussianSplats3D0.4.7 and Three.js0.170.0; MIT licenses included in `vendor/`.

## Reproduce export

`capture.mjs` uses Playwright on the executing owner's managed browser and requires the documented OpenClaw supervised profile lease. Output paths in this task-specific exporter use the canonical Storage project/output location. Viewer playback itself is portable and independent of Playwright or OpenClaw.

The delivered MP4 has burnt-in Japanese captions and an embedded Japanese subtitle track; SRT/VTT and transcript are included in the output directory. See `delivery-manifest.json` for exact hashes, codec/timing/audio QA and cleanup evidence.

API replanning uses the local private1Password credential reference and a fresh account/balance receipt. Those credential-reference/account files are intentionally not shipped in the portable replay bundle. The saved plan contains no API key.
