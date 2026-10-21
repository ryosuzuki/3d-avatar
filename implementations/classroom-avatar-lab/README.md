# Classroom Avatar Lab — October 20, 2026 lecture

Source for the classroom photo/video → **LHM++** avatar website, including the
one-/eight-reference upload UI, serial GPU queue, neural dance preview, Gaussian
and textured mesh export, Mixamo ZIP repair, and Unity starter projects.

**The live classroom service was stopped after class. The old IP URL is not a
permanent hosted demo.** Everything here is source, not student uploads or results.

Start with [RUN.md](RUN.md) to restore the website and GPU worker next year.
The original private development repository remains separate; this folder is the
public teaching copy linked from the lecture's existing Avatar GitHub repository.

## Included

- `server.mjs`, `ui.mjs`, HTML/CSS and locked npm dependencies.
- `worker.py`, `export_assets.py`, pose/grid compatibility fixes, textured OBJ repair.
- `runtime/lhmpp-classroom.patch`: the actual eight modified upstream files
  compared with LHM++ commit `906b5d9fb967ab42efb92f6fa55bf22cac86b653`.
- Exact deployed Python package inventory and model-file names/hashes, download helper.
- `unity-starter/`: Gaussian renderer/helper source and original MIT license.
- `character-starter/`: clean humanoid animation setup; download your own Mixamo FBX.
- Upload/privacy regression checks and mesh-repair tests.

## Limits

The neural dance is an official motion prior, **not uploaded-video motion capture**.
PLY/splat files are static Gaussians, not portable rigs. OBJ/GLB files are approximate
textured surface proxies; Mixamo does not restore identity or guarantee rigging.
Quaternius's original rigs were not accepted by the earlier Mixamo test; the tested
teaching route uses Mixamo's built-in Remy. Desktop Unity rendering was checked;
physical Quest/mobile AR deployment was not verified.

No model weights, private recordings, personal avatars, SSH credentials, or
student result IDs are included. Upstream code/model/license conditions still
apply; this folder does not grant a blanket license to research weights or Adobe
characters. See `runtime/LICENSE*` and the renderer's retained license.

## Verification scope

The archived website build and ten HTTP/upload-isolation tests pass. The pinned
upstream patch is checked against the exact baseline. Python syntax and mesh
repair tests are checked separately. Original GPU inference was exercised during
the class; archival checks do not claim a new GPU run or a clean-machine CUDA
installation. Optional screenshot/video downloads referenced by HTML require
separately restoring those teaching artifacts; the primary upload UI and source
guides are included.
