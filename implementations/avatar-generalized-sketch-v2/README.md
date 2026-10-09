> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Runnable question → source sketch → 3D / v2

Private app: **http://127.0.0.1:8846/** (existing Tailscale required).
Exact Ryo avatar and captured iPad room preserved. Backend-only existing OpenAI credential; no secret in frontend, ZIP or repository. Dedicated LaunchAgent `com.ryosuzuki.avatar-generalized-sketch-v2`, not Gateway or public Funnel.

## What is actually fresh

1. Enter a novel question and choose route.
2. OpenAI gpt-4.1 generates a new recognizable ordered source boundary, explanation, and optional typed organic geometry. No category catalog. Shape accuracy is not guaranteed by schema validity: initial mini-model shapes failed morphology inspection and were superseded. Generated source may use explicit radial samples after validation failures; this is a new constrained sketch, not a repair of supplied drawing.
3. `adapter.py` validates immutable source paths. Inflation uses the actual boundary and symmetric distance-field thickness; organic route compiles safe sweep/lathe/extrude/mesh operations with declared parent/child attachment constraints (identity-transform world-coordinate paths), rather than accepting floating branches as connected. New generated meshes orient normals during construction; imported meshes are never repaired. Geometry remains separate overlapping components, not a boolean-unioned simulation body. It compiles geometry with `geometry.js` (no generated code execution).
4. Both produce `sketch3d.asset.v1`: original paths, raw indexed geometry, separate source/mesh registration, diagnostics, provenance, styles and motion constraints.
5. Original avatar traces supplied centerlines. Registered geometry unfolds in depth and uses sparse depth-tested contours plus sections. Ink/hatch style dispatch works for any accepted mesh. Preview turning is authored, not an inferred rig.
6. Actual new answer audio is generated and played. Invalid input never replaces last valid scene.

## User drawing / external producer

`Draw a boundary` accepts a new pointer-drawn closed polygon. JSON upload also accepts `{closed:true,points:[[x,y],...]}` or explicit sourceStrokePaths. One simple closed boundary; open, self-intersecting or holed shapes reject rather than silently fill/repair.

POST `/api/import`: `{format:'glb'|'obj',assetBase64,sourceStrokePaths,registration:{sourceToDisplay,meshToDisplay},provenance,style,motion}`. Original bytes/hash and source retained; defects reported without automatic repair. Upload the same object as a JSON file. Max16MB input,60k display faces. Larger raw geometry requires an explicitly declared separate derivative; no hidden simplification. No physical engine or rig executor. The fish and owl dropdowns are **PRECOMPUTED** actual learned artifacts with original SVG/SDXL/GLB chain, not fresh GPU requests.

No async GPU producer attached: another GPU worker is active. This app does not invoke or claim live Hunyuan/TripoSR inference. Import contract is ready for a producer to supply verified results independently.

## Run

Python3 with `pip install -r requirements.txt`; existing OpenAI SecretRef/backend store is configured only on the authorized host. `python server.py --host 127.0.0.1 --port 8846` for local reproduction. Default bind is dedicated tailnet IP127.0.0.1, not LAN/public. Browser assets vendored; Node mesh compiler uses local Three.js, no npm install needed for app. `npm install` for Playwright verification only.

## Evidence / boundaries

`current-runtime-acceptance.json`: three fresh current-runtime questions (ginkgo, connected coral, lily pad), zero-error declared branch attachment junctions, actual pointer-drawn polygon, rejected bowtie preserving geometry. Earlier `runtime-verification.json` records superseded pre-attachment testing of ginkgo/manta/coral; it is not the final assembly proof. `runtime-import-verification.json`: actual fish/owl GLB import hash/source retention and backend file denial. `film-recording.json`: fresh requests plus answer audio with real waits retained. `drawing-reach-verification.json`: 24 drawing samples from both live-generated subjects, inverse-kinematics residual below2.5e-16m; this is target reach, not a measured anatomical finger grip or calibrated AR contact. No arbitrary sketch semantic recognition, hidden anatomy from inflation, anatomical rig, full simulation or physical AR calibration. Source/organic contour registration is approximate; boundary exact only for inflation. Rendering writes depth to avoid rear-line tangle, not physical transparency. Browser responsive tests are emulations, not physical Safari/iPad proof.

## Assets / backup

Portable ZIP includes all required avatar/room PLY, vendored renderer, original sourceSVG/conditioned images/originalGLB/displayGLB, generated scenes/audio and provenance. Original meshes and Gaussian files unchanged. Private Git source excludes large binaries; full ZIP/release provide actual binary backup, not merely local file paths. Own outputs preserve prior versions.


## Fresh asynchronous local learned branch

Select **Fresh learned GPU**. A new question first generates validated original source strokes and immediate closed-boundary inflation. `/api/learned` accepts only a fresh stored preview UUID. One bounded background worker observes existing Python producers and queues without interrupting them. It rasterizes the exact supplied strokes, runs pinned cached SDXL+Canny ControlNet, cached U2NetP foreground separation, then pinned TripoSR on **Apple M2 Ultra MPS**. This is real local neural inference, not an RTX4090/CUDA claim or a precomputed fish/owl substitution.

States: queued / running(stage) / success / failure, elapsed time and actual blockers. Max3 jobs per service run, at most2 waiting, one owned stage at a time. Existing-resource wait cap40minutes, stage cap15minutes; only owned subprocess may be terminated on timeout. No shell execution, category lookup, paid provisioning, package installation, or frontend API key. Offline HuggingFace loading means missing cached models fail explicitly.

Original source JSON, raster, conditioned image, learned foreground, raw GLB/OBJ, optional separate display derivative, checkpoint/revision hashes, stage timings and receipts are retained under generated/jobs. The display registration does not alter raw mesh bytes. **Generated source morphology can be wrong; a valid simple polygon is not proof of a recognizable elephant.** SDXL may change the outline, unseen shape is inferred, source–mesh fidelity is not guaranteed, and rigid camera motion is authored—not an inferred anatomical rig.

Runtime dependencies remain the existing local GPU environment and pinned model caches; the portable release includes application source and produced assets, not multi-GB public model caches. The original v2 fish/owl choices are still explicitly precomputed examples; they are never returned as fresh job successes.


## Fresh inference acceptance (2026-10-09)

Three genuinely new requests were attempted. Elephant: actual23228-face neural GLB, recognizable elephant but poor source morphology/downward trunk/incomplete requested fourlegs; warning retained. Morel: actual19168-face GLB produced but image was unrelated leaf/multiple objects; semantic quality rejected, not presented as mushroom success. Nautilus: actual23640-face neural GLB, single recognizable spiral-shell sculpture,51.48seconds for the uncongested job; sectional detail differs from requested opening and anatomy is not verified. TripoSR checkpointSHA256429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee.

The common pipeline now performs image subject review before future meshing; unrelated output fails visibly while the valid immediate preview remains. Review is another model, not a semantic-accuracy guarantee. Proper-axis front registration uses the actual conditioned foreground and inferred vertex colors; no raw geometry changes or category orientation table. Sparse depth-tested curvature lines and faint vertexcolor hints supplement contours. Diagnostic negative signed volume/multiplecomponents are not silently repaired or described as physical-simulation-ready.

The operation film includes real job processing and authored replay of the newly produced mesh. A separately recaptured front-registered display is labeled; no additional neural inference occurred for that display adjustment. All raw input/image/GLB/OBJ/audio and receipts are included in the portable release.
