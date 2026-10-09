> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Transformer avatar pen sketch

Prerecorded 86.7-second English explanation, using the original 160,000-Gaussian Ryo avatar and 301,106-Gaussian iPad Scaniverse room from October 8, 2026. No new avatar generation; synthetic OpenAI shimmer narration reused unchanged.

## Run

`npm install` then `AVATAR_EXPLAINER_PORT=8791 npm start`; open http://127.0.0.1:8791 . Local playback only, not a live AI conversation. Production capture uses the agent-1 supervised browser lease and `node capture.mjs --capture`.

Original single-line vector lettering, arrows and boxes are progressively drawn with the pen tip driven by the same arclength path. Pen lifts during inter-stroke travel. Analytic two-bone IK follows the contact, with fixed body position. Three drawn attention-head panels lift into separate depth planes as a spatial schematic; they are not model measurements.

## Limitations

Added manual 15-bone adapter, not supplied SMPL-X; no articulated fingers or lip sync. Palm contact approximates pen holding. Room and avatar are layered separately to preserve visibility, not physically registered occlusion. Scene placement is manual, not AR tracking. Diagrams clear between eight chapters; strokes persist within chapters. Claims and probabilities are schematic, not actual model inference. Q KT means query times transposed key; the diagram writes T inline rather than superscript. Final English subtitles are burned in sentence-level timing approximations.

Outputs: /path/to/local-assets . Portable ZIP contains original assets and vendor licenses. Private GitHub source backup intentionally excludes assets from normal Git; source/provenance hashes and release ZIP preserve them. Original explainer project remains untouched.
