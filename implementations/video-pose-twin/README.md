> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo video-driven Gaussian digital twin

<!-- youtube-demos:start -->
## Watch demos on YouTube

Click the preview or a video title to play. Videos are Unlisted; original MP4 downloads remain in GitHub Releases.

[](https://youtu.be/bolyiEQwc68)

- [▶ 2026-10-08 Video-Driven Pose Digital Twin](https://youtu.be/bolyiEQwc68)

<!-- youtube-demos:end -->

## Demo preview — October 8, 2026

[](https://youtu.be/bolyiEQwc68)

Recorded video drives an approximate Gaussian avatar pose adapter.

[Watch / download the original demo MP4](https://github.com/ryosuzuki/video-pose-twin/releases/download/demo-archive-2026-10-08/ryo-video-driven-twin.mp4) · [Demo files and provenance](docs/demo/README.md)

Run `node server.mjs`, then open http://127.0.0.1:8857 in Chrome. No installation is required for the viewer. Bundled dependencies and models work offline.

Play tracked video: original Ryo footage and inferred posture drive the original Hyeon-shared `ryo_tpose.ply` (160,000 Gaussians). Drag the3D view to orbit. Seek source video to compare poses. Re-anchor resets relative movement to the current image location. Use camera asks for local browser camera permission; camera images are processed locally and are never uploaded. Recorded video stops camera tracks.

## Provenance and method

Source clip: `PXL_20261008_192648621.mp4`26–44seconds, filmed2026-10-08, normalized to720px height without audio. The original video is preserved outside this project. MediaPipe Pose Landmarker Lite0.10.22-rc.20250304 infers33 image and world landmarks at10Hz. Saved tracks are inference output, not hand-authored animation. Source timestamp is clip timestamp+26seconds. Avatar uses an added15-bone segment adapter with two-influence Gaussian skinning and covariance deformation. This is not the original SMPL-X rig or an LHM++ inference rerun. Manual fitting can distort clothing and joints.

## Position, tracking and limitations

The room anchor is manually placed. Lateral root movement comes from image hip position relative to initial anchor, scaled with apparent body height. Approximate depth uses apparent body-height ratio. These are monocular estimates, not measured absolute room coordinates; perspective and posture can confound depth. Room geometry is Ryo's Quest take20261002_215403, shifted as documented in app.js. The recording's room and scene are not calibrated to one another.

Back-facing/occluded joints can be wrong. Feet are translated to a floor plane rather than solved with foot IK. No object grabbing, furniture collision, or Quest WebXR integration in this video-driven branch. Webcam UI is provided, but no unattended physical camera was activated for this delivery. Browser webcam performance and physical alignment need an actual attended camera test.

## Recompute

`npm install` then `node infer-video.mjs` with the server running recomputes pose-tracks locally in headless Chrome. `verify-video.mjs` verifies synchronization, actual changing inferred frames, retarget motion and playback, then records the browser. The MP4 is a browser screen capture of real source-video-driven deformation, not a simulated live-camera test.
