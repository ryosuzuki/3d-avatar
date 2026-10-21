# Avatar Lab: exported Gaussian appearance in Unity

This starter uses **Unity 6000.4.5f1**, the **Built-in render pipeline**, and the MIT-licensed [UnityGaussianSplatting](https://github.com/aras-p/UnityGaussianSplatting) package, pinned to commit `2c6fed37da67a217367261fcfcd3316d34c73e76`.

## What you get

The exported Gaussian points from your `avatar.ply` download, not the low-quality reconstructed OBJ mesh. The point count depends on the export. Each point keeps its position, rotation, scale, opacity and base color. The starter preserves those exported attributes without additional compression. The server’s colors are baked from rendered views; these are not the full learned neural appearance. This cannot restore details missing from the server’s exported data.

**It is a static Gaussian avatar, not a Mixamo-ready character.** No skeleton or skinned mesh is created. Rotating the entire avatar is not dancing. A neural animation preview on the server is not an exported Unity animation.

## Three-click workflow

1. Unzip the project. This starter contains no person’s avatar or photograph. Copy your downloaded `avatar.ply` into the starter’s `Assets` folder. Open the project root folder in Unity Hub with Unity 6000.4.5f1. Let Unity finish package resolution and script compilation.
2. From the top menu select **Classroom → Avatar Tutorial**.
3. Click **1 Import Assets/avatar.ply (Very High quality)**.
4. Click **2 Build the Gaussian demo scene**. This creates `Assets/AvatarDemo.unity` and selects the avatar in the Hierarchy.
5. Click **3 Open the Game view · Press Play**, then press the Play triangle in the Unity toolbar.
6. To use another result, replace `Assets/avatar.ply` with the original `avatar.ply` from that result's ZIP. Keep the filename. Repeat steps 3–5.

## Manual path, without the classroom helper

1. Open **Tools → Gaussian Splats → Create GaussianSplatAsset**.
2. Set **Input PLY/SPZ File** to your downloaded `avatar.ply`.
3. Set **Output Folder** to `Assets/GaussianAssets`.
4. Set **Quality** to **Very High** and click **Create Asset**.
5. Create an empty GameObject and add the **Gaussian Splat Renderer** component.
6. Assign the generated GaussianSplatAsset to its **Asset** field. The classroom helper also assigns the package's shader and compute-shader references automatically.
7. Frame the avatar using a Camera, then use the Game view.

## Which file should I use?

- `avatar.ply`: original Gaussian representation; use this with the Gaussian renderer.
- `avatar.splat`: another Gaussian interchange format; not a regular Unity mesh or humanoid rig.
- `avatar-static.glb` / `avatar-static.obj`: approximate static mesh. Easier to place in standard mesh workflows but visibly less faithful. The starter deliberately does not use it.
- `preview.mp4`: video, not an interactive 3D object or animation clip.

## AR and Mixamo: what is and is not included

The upstream renderer supports desktop Metal, Direct3D 12 and Vulkan. Its documentation does not guarantee mobile or WebGL. This starter does **not** demonstrate a Quest, iOS or Android build. Do not assume that enabling AR Foundation makes its shaders, sorting, stereo rendering or memory use compatible with a target device.

A real mobile AR lesson must separately choose a device-compatible Gaussian renderer, configure AR Foundation and its platform provider, place the avatar relative to a tracked plane, then build and test on that actual device. Desktop screenshots do not verify AR.

Mixamo accepts a humanoid mesh, not a Gaussian cloud. A character intended for Mixamo needs a clean connected human mesh, appropriate topology, and a usable pose. Simply renaming this PLY or uploading the coarse proxy does not guarantee a valid rig. LHM's internal human-body representation is not, by itself, an exported Unity Humanoid rig.

## Provenance

No Unity UI screenshots or device compatibility claims should be inferred from generated diagrams. Verification status and actual captures are recorded separately in `verification.md`.
