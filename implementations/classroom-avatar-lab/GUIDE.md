# Avatar Lab: from capture to Unity and AR

## What you generated

The official LHM++ LHMPP-700M reconstructs a person from one selected frame. It synthesizes six views; those are predictions, not six photographs. The upload is used for appearance, NOT video motion capture. Backside, fingers, hair and loose clothing may be inaccurate.

Downloads:

- `avatar.ply`: 160,000 Gaussian splats with baked colors, covariance and opacity. NOT a triangle mesh or a Unity Humanoid rig.
- `avatar.splat`: the same Gaussians in common 32-byte SPLAT format.
- `avatar-static.glb`: approximate colored static triangle mesh for ordinary 3D applications. No bones, skin weights or animation.
- `avatar-static.obj`: approximate mesh for Blender / experimental Mixamo auto-rigging. OBJ vertex colors are not supported by every importer; it has no UV texture map.
- `preview.mp4`: six neural-rendered viewpoints. It can look sharper than the exported geometry.
- `report.json`: actual inference time, GPU and export counts.
- `Unity/PlaceAvatarOnPlane.cs`: AR Foundation example for a static avatar prefab.

## Route A: static avatar in Unity (the quickest classroom exercise)

1. Create a Unity 6 / Unity 2022.3+ 3D project. Use the render pipeline supported by your target XR device.
2. Install the Unity glTFast package (`com.unity.cloud.gltfast`) through Package Manager. See https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@latest/ . If it is not in the registry list, use “Add package by name”.
3. Put `avatar-static.glb` in Assets and let glTFast import it. If your Unity/glTFast version lacks editor import, import the GLB into Blender and export an FBX, then drag that FBX into Assets.
4. Drag the resulting model into the scene. The exporter grounds the feet and preserves Y-up coordinates; verify front direction and size. There is no calibrated real-world scale. Scale the model to your desired height.
5. Make a prefab. Add a capsule or box collider if you need interaction; the mesh is a visual approximation, not a collision scan.

Simple exercise: put a 20 cm-tall avatar on a desk, then use a UI button to rotate its parent GameObject. This needs no skeletal rig.

## Route B: plane placement in mobile AR

1. Install AR Foundation plus ARKit XR Plugin (iOS) or ARCore XR Plugin (Android); enable the provider in XR Plug-in Management. Use matching package versions.
2. Create an XR Origin (Mobile AR) and AR Session. Add AR Plane Manager and AR Raycast Manager to the XR Origin. Enable horizontal plane detection. Grant the device camera permission.
3. Copy `Unity/PlaceAvatarOnPlane.cs` into Assets. This example uses `UnityEngine.Input` (legacy). Set Active Input Handling to “Both” or “Input Manager (Old)” in Player settings, or adapt the script for your Input System actions.
4. Put the script on the XR Origin, assign the AR Raycast Manager and your static avatar prefab. Set a small uniform scale on the prefab root first (e.g. height about 0.2 m).
5. Build to a supported phone. Scan a textured desk and tap an established plane to place the prefab. Later taps move it. This uses the prefab's authored scale.

Quest passthrough is a separate platform: use your Quest/OpenXR/MRUK spatial-placement workflow and put the same prefab under its placement transform. The mobile AR Foundation tap script is not a Quest passthrough implementation. Physical device deployment is not automatically verified by a successful mesh export.

## Is it already rigged? Can I use Mixamo?

LHM++ animates its internal representation using body-model parameters. This does NOT mean exported PLY/SPLAT has a portable skeleton. The provided GLB/OBJ are also **static and unrigged**.

Mixamo auto-rigs triangle humanoid meshes (OBJ/FBX/ZIP), not Gaussian PLY/SPLAT. Use the experimental OBJ route only if you need skeletal animation:

1. Import `avatar-static.obj` into Blender. Inspect front/side/back, remove floating components, fix fused limbs, and keep a single clean humanoid. Hands/arms must be separate enough. Adjust to a neutral A/T pose if necessary. These exports are not guaranteed to auto-rig.
2. For reliable color preservation, create UVs and bake vertex colors to a texture in Blender. The OBJ's extended vertex colors may be dropped by Mixamo. Export FBX with materials/textures or package OBJ/MTL/textures.
3. Upload the cleaned mesh to https://www.mixamo.com/ with your own Adobe account. Place chin, wrists, elbows, knees and groin markers; run auto-rig. If it fails, fix the mesh or use a standard ready-rigged character. Do not upload someone else's capture without permission.
4. Choose an animation. Download the character as **FBX for Unity / With Skin**. Additional clips can be **Without Skin**.
5. In Unity select the character FBX → Rig → Animation Type: Humanoid → Avatar Definition: Create From This Model → Apply. Configure the avatar and resolve any mapping errors. For additional clips use Copy From Other Avatar when compatible.
6. Create an Animator Controller with Idle/Walk states, assign it and the avatar, and test the clip. Add the animated prefab to your AR placement flow. Disable root motion for a character that must remain at the placed anchor, unless intentionally moving it.

This is a separate mesh cleanup + Mixamo workflow. Avatar Lab does not automatically log into Adobe, upload your capture, or produce a verified Mixamo rig.

## Route C: keep the Gaussian representation

Import `avatar.ply` into a compatible 3D Gaussian Splatting renderer, such as UnityGaussianSplatting (https://github.com/aras-p/UnityGaussianSplatting). Follow that package's current pipeline/platform instructions. This is a static Gaussian object. PLY appearance differs from neural preview. Render-pipeline support, mobile/Quest performance and stereo sorting must be tested on your actual device. Animation requires an additional deformable Gaussian/body-model rig; ordinary Mixamo animation clips do not directly animate the PLY.

## Privacy and limits

The classroom app is bound to the CU-facing interface and accepts CU Boulder 128.138.0.0/16 or loopback clients. It does not require Tailscale on student devices. This is not CU SSO. Anyone with a result's random link on the allowed network can access it; keep the link private. Uploaded source, intermediate files and results are deleted after 24 hours while the service is running. Download what you need before then. Keep captures suitable for this classroom prototype; model assets/weights and private lab recordings are never included in downloads. Follow upstream LHM++ and body-model licensing for any use beyond this classroom exercise.


## Quality: choose the right output

- **Neural dance MP4:** highest-fidelity rendered appearance, animated using the official Dance_I motion prior. It is not captured motion and is not an FBX or rig. Use a Unity VideoPlayer when you need this exact rendered appearance; this remains a flat video surface.
- **Gaussian PLY/SPLAT:** freely orbitable static 3D, but baked colors lack the model's neural refinement. Expect lower fidelity than the MP4.
- **Experimental GLB/OBJ:** occupancy approximation only. These are not production character meshes. Do not use them as evidence of LHM++'s neural rendering quality.
- Use a high-resolution full-body photograph of ONE person. Use the crop tool to remove other people. Avoid hands crossing the body and small faces.
- To improve backside coverage, upload a slow full turn-around video and select **8-view turn-around video**. Set start/end around one full rotation; the service samples eight authentic frames, not synthetic views. A stationary video does not help.
- This model cannot restore unseen facial detail or guarantee photoreal identity. A mesh character for close-up facial work needs a different capture/retopology/texturing pipeline.


## Click-by-click Unity video and starter

Open [the visual Unity tutorial](/tutorial) for six real Editor screenshots with highlighted controls, a 48-second captioned walkthrough, a PDF, and a Unity 6000.4.5f1 desktop starter. The starter contains no student avatar: copy your Gaussian `avatar.ply` to `Assets/avatar.ply`, then open Classroom → Avatar Tutorial. This route is static, not rigged, and AR-device compatibility remains unverified.

## Correct Mixamo ZIP

Use `mixamo-avatar.zip`, NOT `classroom-avatar.zip`. The dedicated ZIP contains a UV-mapped OBJ, MTL and 2048px PNG texture. The full download also contains unrelated Gaussian files and source images; it is not a Mixamo upload package. Earlier OBJ vertex colors were not portable to Mixamo, explaining gray results. Texture presence is structurally verified; individual Mixamo auto-rig quality must be reviewed. The underlying mesh remains an approximate proxy.
