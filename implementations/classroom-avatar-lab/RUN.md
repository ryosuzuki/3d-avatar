# Restore for next year's lecture

## 1. Restore the website (no GPU needed to inspect the UI)

Use Node 20+ and npm. From this directory:

```sh
npm ci
npm run build
npm test
npm start
# open http://127.0.0.1:8848/
```

The default binds loopback only. The UI/guide work without model weights, but
**Generate requires the worker below**. `data/` is created locally and ignored.
Use HTTP for this local server; it does not implement TLS. Put an HTTPS reverse
proxy in front for a shared deployment. Do not rely on last year's IP address.

## 2. Restore the Linux NVIDIA worker

Original verified hardware: RTX 4090, x86_64 Linux, Python 3.10, PyTorch 2.3.0
CUDA 12.1. Reserve about 8.5 GiB VRAM for one reference, 12.5 GiB for eight,
and 18 GiB RAM. These are admission requests, not guarantees on other hardware.

Copy this folder to `~/gpu-lab/classroom-avatar-lab` on the GPU host. Create a
separate runtime at `~/gpu-lab/video2mr-person-20261015` (or set AVATAR_RUNTIME
in the worker's environment). Inside that runtime:

```sh
git clone https://github.com/aigc3d/LHM-plusplus.git source
cd source
git checkout 906b5d9fb967ab42efb92f6fa55bf22cac86b653
# Resolve Git LFS assets according to upstream instructions if needed.
git apply --check ~/gpu-lab/classroom-avatar-lab/runtime/lhmpp-classroom.patch
git apply ~/gpu-lab/classroom-avatar-lab/runtime/lhmpp-classroom.patch
```

Follow **INSTALL.md at that commit**, not the moving upstream main branch.
Create a Python 3.10 virtual environment at `runtime/env`. Install PyTorch and
CUDA-specific wheels before building pointops/rasterizers. The exact deployed
inventory is `runtime/requirements-freeze.txt`; `requirements-worker.txt` lists
our additional preprocessing/export dependencies. The freeze is a reference,
not a portable pip command: native wheels, pointops, CUDA toolkit/compiler and
platform-specific dependencies must match this machine. Set CUDA_HOME to a real
CUDA 12.1 toolkit/compiler and TORCH_CUDA_ARCH_LIST to the target GPU (4090:8.9).
The default compiler location is `runtime/compiler`.

Download the curated prior/checkpoint files using the helper (review upstream
terms first). It validates recorded sizes and available SHA-256 digests:

```sh
# Run from the classroom folder on the GPU host.
# The helper expects runtime/source here; symlink to your separate source checkout:
ln -s ~/gpu-lab/video2mr-person-20261015/source runtime/source
~/gpu-lab/video2mr-person-20261015/env/bin/python runtime/download-models.py
```

Also download `motion_video.tar` from
https://huggingface.co/3DAIGC/LHMPP-Assets/tree/main and extract the official
`Dance_I` subtree to `assets/motion_video/Dance_I/` beside worker.py.
At least240 sorted JSON files must exist under `smplx_params/`. No weights or
motion assets are redistributed here. The patched downloader uses a ready marker
written by our helper; run the helper before inference or upstream waits for it.

The original server uses the worker host's `gpu-run` admission command. Preserve
that wrapper on shared lab machines. On a dedicated reproduction machine without
it, explicitly replace that command in server.mjs with the site's own admission
mechanism (or a reviewed direct launch); it is not a standard pip dependency.
Never silently bypass a shared GPU scheduler.

## 3. Connect the website to the worker

Configure key-based SSH outside Git. Verify `ssh avatar-gpu hostname` and GPU
availability before running the app. Local deployment configuration:

```sh
export AVATAR_SSH=avatar-gpu
export AVATAR_REMOTE=gpu-lab/classroom-avatar-lab
export AVATAR_PYTHON=../video2mr-person-20261015/env/bin/python
npm start
```

Worker paths are shell-safe without spaces. `AVATAR_REMOTE` is relative to the
remote home or an absolute path. The runtime path is configured on the worker,
not automatically forwarded through SSH. `AVATAR_DATA` overrides local storage;
`PORT` defaults8848; `AVATAR_HOST` defaults127.0.0.1.

For explicit classroom sharing, bind the chosen interface and configure
AVATAR_ALLOWED_IPS as comma-separated exact client addresses, or set
AVATAR_PUBLIC_UNTIL to a future Unix **millisecond** timestamp for temporary
public access. The latter automatically expires. Public access is off by default.
The historical128.138/16 allow rule does **not** establish eduroam/CU Secure
coverage; wireless clients can receive other addresses. Test from an actual
student device. Use a reverse proxy/TLS for shared internet access.

## 4. Recreate the teaching materials

`GUIDE.md` builds into `/guide`. Follow `unity-starter/README.md` for the static
Gaussian route, or `character-starter/README.md` for Mixamo FBX playback. Unity
version6000.4.5f1 and the renderer revision are pinned in the project files.
Download Quaternius/Mixamo assets yourself under their terms; they are not
bundled in this source archive.

The optional `/tutorial` and `/characters` HTML pages reference screenshots,
videos, ZIPs and PDFs under AVATAR_DATA/tutorial and AVATAR_DATA/character-lesson.
Their HTML/helper/project source is preserved, but those bulk lesson artifacts
are not required to run generation. Recreate them from the included starter
projects or restore your separately archived class media. Missing optional media
must not be mistaken for a broken inference installation.

## 5. Acceptance and shutdown

1. npm test and npm run build must pass; run python -m unittest test_mixamo.py
   after installing its dependencies. Pose compatibility tests need upstream.
2. Generate one consented full-body synthetic/sample photo. Check preview,
   dance, PLY, textured GLB and Mixamo ZIP CRC. Then test an8-reference video.
3. Record worker revision, driver/toolkit, timings, VRAM, input provenance and
   results locally. A working UI alone is not GPU acceptance.
4. After class, stop the app process or its deployment service and disable its
   auto-restart. Confirm port8848 is closed. Do not stop other GPU services.

Jobs expire after24hours while the app runs. Keep per-job URLs private; no gallery
or job-list route is provided. Check retention after shutdown/restart as well.
