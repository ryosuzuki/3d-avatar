> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Exact LHM++ body: free walking in Ryo's room

<!-- youtube-demos:start -->
## Watch demos on YouTube

Click the preview or a video title to play. Videos are Unlisted; original MP4 downloads remain in GitHub Releases.

[](https://youtu.be/VVbNbpoQCKg)

- [▶ 2026-10-08 LHM Avatar Room Walk](https://youtu.be/VVbNbpoQCKg)

<!-- youtube-demos:end -->

## Demo preview — October 8, 2026

[](https://youtu.be/VVbNbpoQCKg)

Articulated Gaussian avatar walking and performing a scripted object interaction.

[Watch / download the original demo MP4](https://github.com/ryosuzuki/lhm-body-room-walk/releases/download/demo-archive-2026-10-08/lhm-body-room-walk.mp4) · [Demo files and provenance](docs/demo/README.md)

This version reuses Hyeon's actual shared `ryo_tpose.ply` (160,000 Gaussians), not the earlier SAM/MHR textured body. Source: (private source discussion omitted) .

Run `node server.mjs`, then open http://127.0.0.1:8831 . W/S walks forward/backward; A/D turns; drag orbits the view. Stop pressing movement keys to stand. Run full task resets and performs walk → grasp → carry → release. Reset returns to the initial position.

The room is Ryo's captured Quest geometry, displayed as a transparent cutaway. This is actual articulated Gaussian rendering, not a video on a plane. Free walking is keyboard-controlled; box manipulation is a scripted sequence. The original supplied PLY has no skeleton; the existing manually fitted 15-bone adapter is preserved. The gait is authored, not recovered from Ryo's real walk. Collision avoidance and Quest controller support are not implemented.

Prior adapter documentation follows; its port 8774 refers to the preserved original project, not this copy.

# Shared Gaussian avatar: continuous object interaction

This demo animates **Hyeon’s actual shared Ryo LHM++ avatar**, not a regenerated body, generic human, textured proxy, or video billboard. All 160,000 source Gaussians are rendered as anisotropic 3D Gaussian splats, with the source colors/opacity and continuously deformed centers/covariances.

## Run

Requires Node.js, a browser with WebGL2, and the supplied assets included here. No build, model upload, paid service, GPU rental, or package installation is needed.

```sh
npm start
```

Open <http://127.0.0.1:8774/> and click **Run full task**. Drag to orbit; use the timeline to inspect any point. The buttons also run the walking and manipulation phases separately and toggle the measured room and added rig.

Sequence: walk to box → reach with both hands → grasp/lift → turn → carry 1.4 m → place on the other table → release → step back. The object is held by a deterministic two-palm attachment while carrying and stays on the destination table after release.

`AVATAR_INTERACTION_PORT` changes the port. The default bind is loopback. `AVATAR_INTERACTION_HOST` can select an explicitly intended local/private interface. No deployment or public publication is performed.

## Source and provenance

- Original source post: <(private source discussion omitted)>, in thread `1791486574.043269` in `daily-demo` (`C08RK4K26AV`).
- Exact source attachment: `lhmpp_tpose_ply.zip`, Slack file `F0C7R66MWUD`, SHA-256 `acd6035f7ff771620463f792e14eced5fa214b8640c3b9b37d627e65c7b94cf8`.
- Original `ryo_tpose.ply` and the byte-identical project asset SHA-256: `add76ef82f23e209b830b756fb942d3f4e4c587188e4776aebcdf3cbcad09f12`.
- Originals remain unchanged at `/path/to/local-assets`.
- Room: Ryo’s real Quest capture `20261002_215403`, original `quest-spatial-studio/editor/sessions/quest-215403/room-geometry.json`. Its byte-identical copy here is `assets/quest-room-geometry.json`, SHA-256 `280da651e832853538fddd7ac856b2d4fb7126f62a99d01e18368dad1ad661bb`.
- Room rendering is a transparent cutaway of measured first-room global/semantic geometry, not a newly generated room. Coordinates are meters, transformed by `[x - 3.5, y + 1.222106, z + 1.7]`. The avatar, route, two tables and orange box are added prototype placements, not captured physical objects or calibrated registration.

`assets/source-provenance.json` preserves the original attachment/message metadata. `provenance.json` records this implementation.

## What was added

The shared PLY is static and contains no skeleton, skin weights or motion track. The source author explicitly suggests binding its canonical Gaussian positions to a body rig. This demo instead supplies an **approximate, manually fitted 15-bone humanoid adapter** with two-influence anatomical segment-based linear blend skinning. This does not claim to recover Hyeon’s original SMPL-X weights, pose parameters, or dance animation.

`rig.js` defines the rest joints and smooth binding. It solves both arms and legs analytically with two-bone IK. `app.js` drives a scripted gait and manipulation trajectory. GPU vertex-shader skinning transforms Gaussian centers and their full 3×3 anisotropic covariance, not only the avatar’s overall transform. Per-frame counting-sort depths use the deformed centers, allowing orbiting during motion.

The palms visibly approach opposite sides of the box. Finger closing, force/friction/contact physics, collision avoidance, autonomous navigation and task planning are **not implemented**. Limb/cloth deformation is approximate, especially at shoulders and extreme poses. This is a runnable interaction proof, not a validated manipulation simulator.

## Verification

Retained evidence: `/path/to/local-assets`.

- Actual managed-browser renders of ready, walk, reach, grasp, carry, release and complete states.
- 18-second, 360-frame H.264 recording captured from this live renderer.
- Button/orbit/toggle readback and per-frame trajectory.
- Checks that the avatar moves, the palms/box remain attached, the released box remains stationary, all transforms are finite, and the source model/hash matches.

The verification runner is environment-specific and uses the established supervised `agent-1` browser and local Playwright installation. Running the app does not require that runner.

Renderer: GaussianSplats3D 0.4.7 and Three.js 0.170.0, MIT; vendored licenses are included.
