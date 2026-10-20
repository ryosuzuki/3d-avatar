# 3d-avatar — implementation catalog

Independent, source-only snapshots of avatar prototypes, organized by implementation. The original repositories remain unchanged. These folders are not a unified application or an API-compatibility layer.

## Watch the demos

These are **recorded demonstrations**, not hosted interactive applications:

- [Avatar walking in a scanned room](https://youtu.be/BF8diLWpprU) — photo-textured skinned body and procedural gait.
- [LHM Gaussian avatar room walk](https://youtu.be/VVbNbpoQCKg) — avatar locomotion in a captured room.
- [Video-driven pose digital twin](https://youtu.be/bolyiEQwc68) — recorded pose and camera coordination.
- [Walk, grasp, carry, and release](https://youtu.be/jT1BSvjkJBI) — Gaussian avatar interaction.
- [Spatial explainer](https://youtu.be/xuH24o_L9Eo) and [room explainer](https://youtu.be/WGyo7UWuWEI).
- [iPad Scaniverse avatar explainer](https://youtu.be/1z5merL9pps) and [mesh avatar explainer](https://youtu.be/S2B1t99FFGM).
- [Transformer avatar explainer](https://youtu.be/UrbC0QWnVQk) and [pen sketch](https://youtu.be/50rebBKIZ0Y).
- [Orbit Sketch Lab](https://youtu.be/CHRsjzaA93Q) and [Chalk Sketch Lab](https://youtu.be/Xs4JrjqZt6I).

**Interactive demos:** there is no public, asset-complete browser deployment in this catalog. Follow each implementation's README and RUN.md to serve it locally with your own assets. A `127.0.0.1` address refers to your own computer, not a shared internet demo. Original private delivery recordings and source notes do not make private avatar/room assets public.

## Choose an implementation

- [ryo-body-scan-walk](implementations/ryo-body-scan-walk/README.md) — photo-textured skinned mesh with procedural walking. [Run instructions](implementations/ryo-body-scan-walk/RUN.md).
- [lhm-body-room-walk](implementations/lhm-body-room-walk/README.md) — Gaussian avatar display and walking inside a captured room. [Run instructions](implementations/lhm-body-room-walk/RUN.md).
- [video-pose-twin](implementations/video-pose-twin/README.md) — avatar display driven by recorded pose and camera data. [Run instructions](implementations/video-pose-twin/RUN.md).
- [ryo-avatar-demo-backup](implementations/ryo-avatar-demo-backup/README.md) — explanation, drawing, and object-manipulation prototypes. [Run instructions](implementations/ryo-avatar-demo-backup/RUN.md).
- [ryo-primer-live](implementations/ryo-primer-live/README.md) — catalog-routed Q&A, calculated sketches, and synthetic speech. [Run instructions](implementations/ryo-primer-live/RUN.md).
- [avatar-generalized-sketch-v2](implementations/avatar-generalized-sketch-v2/README.md) — improved generalized-sketch integration. [Run instructions](implementations/avatar-generalized-sketch-v2/RUN.md).
- [avatar-generalized-sketch](historical/avatar-generalized-sketch/README.md) — historical v1 for comparison with v2. [Run instructions](historical/avatar-generalized-sketch/RUN.md).
- [avatar-inflation-demo](implementations/avatar-inflation-demo/README.md) — avatar demonstration of closed-contour inflation. [Run instructions](implementations/avatar-inflation-demo/RUN.md).
- [avatar-source-sketch-bridge](implementations/avatar-source-sketch-bridge/README.md) — source-sketch and avatar integration. [Run instructions](implementations/avatar-source-sketch-bridge/RUN.md).
- [avatar-sketch-rendering-study](implementations/avatar-sketch-rendering-study/README.md) — comparison of drawing and rendering techniques. [Run instructions](implementations/avatar-sketch-rendering-study/RUN.md).

## Scope and limitations

These are mainly desktop WebGL/web-server prototypes, not verified Unity or Quest ports. Each README describes the original approach, startup commands, and tested scope. Model inference and 3D-generation algorithms are cataloged in [3d-generation](https://github.com/ryosuzuki/3d-generation); tracking platforms are in [image-tracking](https://github.com/ryosuzuki/image-tracking). Integrated avatar-and-room prototypes remain intact even when this duplicates source.

Catalog checks cover source/derivative integrity and JavaScript/Python syntax. They do not constitute new device tests or AI calls. Linked recordings document original demonstrations.

## Reproducibility

`source-index.json` and each `CATEGORY-SNAPSHOT.json` preserve original commits, Git blobs, and sanitized source SHA-256 hashes. Reviewed English changes are recorded separately in `ENGLISH-DERIVATIVES.json`; original source identity is not rewritten. Run `python3 scripts/verify-snapshots.py` to check original copies and declared derivatives. Supply your own assets; see [ASSETS.md](ASSETS.md).

Documentation, UI labels, and authored default narration are English. The Primer implementation intentionally retains Japanese-input detection, nondefault Japanese answer localization, and Japanese-language regression fixtures as language-support data. They are not untranslated English UI. Existing Japanese audio recordings remain labeled as Japanese rather than falsely relabeled or regenerated.

## Authentication

Set `OPENAI_API_KEY` (OpenAI) or `TYPESAFE_API_KEY` (legacy Jev) in the environment for API features. Private credential routes and personal scans are not included in this public catalog.
