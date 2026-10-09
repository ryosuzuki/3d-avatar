# Generalized sketch-to-3D: independent QA snapshot

Inspected active projects read-only at 2026-10-09 18:28 UTC; no browser/API calls or active-file changes. Exact paths/hashes and completed-vs-in-flight states are in `method-comparison-receipt.json`.

| Route | Demonstrated generality | Drawing fidelity | Learned/richer shape | Current gap |
|---|---|---|---|---|
| Closed-boundary inflation | Four silhouettes, including an unseen asymmetric polygon; no category lookup | Exact original boundary and model-space XY | Symmetric depth only | Medial ridges; no hidden anatomy |
| OpenAI constrained geometry | Six validated requests plus novel seahorse; general composition operators | Projected drawing is derived from generated 3D, not a supplied user sketch | Editable organic parts, but uneven morphology | Novel seahorse is fish-like/horizontal despite valid schema |
| Sketch-conditioned SDXL → Hunyuan/TripoSR | Real fish/owl sketch-derived images and learned GLBs; input/mesh hashes match receipts | Conditioning can change details; source stroke identity is not yet the common renderer's first-class input | Rounded fish/eyes/fins and owl/feather volume clearly richer | Fish is one watertight component; owl non-watertight/six components; no rig |

**Completed:** inflation film; 115-second generated-schema film; actual fish/owl neural inference; common imports of inflation fish and a fixture seahorse. **In flight/unverified at snapshot:** lower-conditioning 0.35 images' downstream meshes; a complete embodied film using actual source-stroke → rich-image → rich-mesh chain.

## Improvements to relay

1. Preserve `sourceStrokePaths` independently from mesh-extracted contours. Show the actual sketch → conditioned image → actual learned GLB chain rather than drawing a projection of a mesh generated earlier.
2. Imported seahorse still has noisy interior fragments after path-order repair. Use current-view silhouette contours, only a few long cross-sections, rear-line occlusion/fading and a path-complexity cap. Stroke continuity alone is not contour coherence.
3. Add visual morphology/orientation/contact acceptance criteria. Schema validity cannot establish that an upright seahorse—or arbitrary unseen subject—looks correct.
4. Use faithful inflation as the immediate preview while learned image/mesh inference runs asynchronously. Disclose changes when the richer result differs from the original outline.
5. Keep animation/rig and scientific simulation as separate backends. Generated geometry plus whole-mesh sway does not establish articulated motion or valid physics.

## Tested smoothing improvement

`inflation-smoothing-before-after.png` shows a separate experimental mesh derived from the original unseen polygon, not an overwritten original. Thirty height-only Laplacian steps lock XY and zero-depth boundary; global Z scaling restores volume. Watertightness and topology remain unchanged. Mean adjacent-normal disagreement decreases **39.5%**, p95 decreases **83.6%**. This is a one-shape appearance experiment, not learned hidden geometry or broad acceptance.
