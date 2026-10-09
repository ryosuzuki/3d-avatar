> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo — walk inside your scanned room

<!-- youtube-demos:start -->
## Watch demos on YouTube

Click the preview or a video title to play. Videos are Unlisted; original MP4 downloads remain in GitHub Releases.

[](https://youtu.be/BF8diLWpprU)

- [▶ 2026-10-08 Ryo Avatar Walking in a Scanned Room](https://youtu.be/BF8diLWpprU)

<!-- youtube-demos:end -->

## Demo preview — October 8, 2026

[](https://youtu.be/BF8diLWpprU)

Photo-textured articulated avatar walking inside the scanned room.

[Watch / download the original demo MP4](https://github.com/ryosuzuki/ryo-body-scan-walk/releases/download/demo-archive-2026-10-08/ryo-walking-in-room.mp4) · [Demo files and provenance](docs/demo/README.md)

Run `node server.mjs`, open http://127.0.0.1:8824 . Node.js required; dependencies and both assets included. No package download needed.

- W/S: articulated forward/backward walking
- A/D: turn the body
- Shift: faster
- Drag: orbit third-person camera; scroll: distance
- Front/follow: inspect your appearance or follow behind
- Reset: return to starting aisle

## Exact source, not a generic avatar

Body: `user-avatar.glb`, created earlier from Ryo's October 8 full-body videos in daily-demo thread (private source discussion omitted) . Uses SAM3D/MHR inferred shape, four authentic photographic views and exact MHR skin weights on 127 joints. The body is a video-derived reconstruction, not measured loose-clothing scan geometry. This demo reuses that exact asset with additional authored walking motion. Face/cloth geometry remains approximate.

Room: actual iPad 3d Scanner App room, previously converted to a textured GLB. Original scans unchanged.

Hyeon's separately shared Ryo Gaussian PLYs were inspected but are static pose states without bones/weights. They were NOT substituted for this articulated avatar, and this delivery does not claim to recover their missing dance motion.

## Motion and scope

New procedural gait animates opposite hips, knees, ankles and arm swings with forward root movement; stopping blends back to source pose. It is authored animation, not Ryo's measured walking performance. Genuine skinned mesh deformation, not a rigid sliding body or billboard. The source's old wave/dance clip is not used for locomotion. Floor is approximately y=0 based on room down-ray intersections. Motion is not physically calibrated, has no foot IK, and may show foot sliding. Desktop third-person prototype: no Quest controller/WebXR, furniture collision, navigation mesh or grab/physics in this body-specific version. Auto walk can enter furniture; use W/S in the aisle for inspection. Room holes are retained.

All assets/dependencies local. No publishing or external inference performed. Browser keyboard/mouse verification and recorded operation are in the dated output.
