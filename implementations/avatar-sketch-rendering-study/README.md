> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Mesh-independent sketch rendering study

Three experimental sketch-like rendering modes share the **same actual mesh**, camera, source strokes and mesh provenance. No learned-model inference, credential access or paid API call is performed by this study. The film is silent with English captions.

## Inputs and reuse

Frozen fish Hunyuan3D-2mini and owl TripoSR inference assets from the previous source-sketch bridge are copied unchanged. Fish rendering uses the already declared 18,000-face display derivative; its full 140,056-face original is retained. Owl uses all40,592 faces. The third input is an unseen nine-point boundary inflated through the category-free fallback, 1,344 faces. Original SVG fixture strokes are first-class, **not reconstructed from final meshes**. These are experiment-authored fixtures, not human sketch captures.

The exact original avatar and captured room PLYs are unchanged. The private release ZIP contains them; normal Git excludes those large private assets.

## Generic rendering, no category-conditioned style code

Style input is an arbitrary triangle mesh with vertices/faces/adjacency and original sourceStrokePaths. Styling never changes mesh geometry. Hunyuan, TripoSR and immediate boundary-inflation share identical style dispatch:

* **A: sparse contours + cross-sections.** Five horizontal plane intersections produce coherent surface cross-section paths. Max240 section segments; faint12% neutral surface.
* **B: ink + faint surface.** Sparse current-camera silhouettes only, dark ink, 5.5% surface. Lowest line density, but visibly weaker curvature/depth cues.
* **C: silhouette + surface hatching.** Thirteen diagonal plane intersections form curve-following surface lines. Max400 section segments; faint7% surface. This is deterministic plane-based hatching, **not a curvature-based suggestive contour algorithm**.

All modes use coherent edge ordering, short-fragment rejection, path simplification, global segment caps and depth-tested ribbons. The actual mesh writes an occlusion depth mask even when surface opacity is low, so far-side hatch lines do not show through and tangle. This prioritizes readable visible-surface sketches over physically correct transparent-surface optics. Source-sketch reference paths are explicitly separate and faintly overlaid; source/mesh registration remains approximate.

Rendering supports general meshes, not arbitrary sketch recognition, hidden-anatomy guarantees or universal neural-generation quality. Dynamic fish movement is authored, not a model-inferred rig. Avatar grip and layered occlusion remain approximate.

## Recommendation from inspected comparisons

A is the best default for concise educational shapes: enough depth cues without C's extra pattern. B is a useful minimalist state but looked flat for the unseen polygon and owl. C is useful temporarily during rotation to communicate surface depth/curvature; it carries higher line count and should not be universally enabled. The contact sheet and nine measured style states record the comparison; this is one controlled visual test, not a validated human perception experiment.

## Integration schema recommendation

```json
{
  "sourceStrokePaths": [{"points": [[0,0,0]], "closed": false, "sourceId": "svg-path-7"}],
  "mesh": {"originalAsset": "sha256:...", "displayAsset": "sha256:...", "vertices": [], "faces": [], "adjacency": []},
  "registration": {"matrix": [], "method": "uniform-bbox", "exactCorrespondence": false},
  "style": {"mode": "sections", "silhouettePathCap": 12, "sectionSegmentCap": 240, "depthTest": true, "surfaceOpacity": 0.12},
  "motion": {"kind": "authored", "rigInferred": false, "parameters": {}},
  "provenance": {"sourceAuthorship": "experiment-authored fixture", "sourceHash": "...", "conditionedImageHash": "...", "inferenceModel": "...", "device": "mps", "originalMeshHash": "...", "displayDerivativeDeclared": true}
}
```

Keep source stroke coordinates, original mesh coordinates and display registration separate. Never silently replace sourceStrokePaths with mesh projections. Route unknown closed outlines to immediate inflation when a learned backend is unavailable, with limitations disclosed. Style should be independent of shape/category and backend. Contour/hatch parameters must scale with scene units and pixel density.

## Run

Use the private release ZIP for the complete runnable project. Create a Python venv and install requirements.txt, then `python server.py`; open http://127.0.0.1:8842/. Choose shape/style with dropdowns. Imported mesh/provenance datasets are already frozen: playback needs no API key. Browser capture uses the workspace managed-profile queue, creates only task-owned tabs and closes them.

`verify.py` validates original source/mesh hashes and prepared vertex transforms. Browser evidence confirms equal geometry checksums across all three styles for all three inputs. Captioned54-second film uses15fps deterministic screenshot capture encoded30fps with repeated frames; this is not native30fps rendering performance evidence.
