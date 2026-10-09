> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Transformer avatar explainer

Original 160,000-Gaussian Ryo avatar, in the actual 2026-10-08 iPad Scaniverse room (301,106 room Gaussians). Scene placement is authored, not physical AR registration. Approximate rig; no lip sync. English synthetic OpenAI shimmer voice, not a voice clone.

## Replay
Run `node server.mjs` then open http://127.0.0.1:8776 . Click Play. Serve over HTTP (cross-origin isolation headers are required). The replay is fully local and needs no API key or Node dependencies. `?film` hides controls and question UI. Drag to orbit.

## Live questions — configured original machine only
Run `python3 service/live.py` and open http://127.0.0.1:8791 . Ask a text question. A real TypeSafe Jev request semantically selects one of eight verified Transformer topics, using the previous four turns as context. Validated actions redraw that topic, point at its diagram, and play the corresponding English narration. Unsupported questions are identified. This is bounded question-driven routing, not unrestricted prose/diagram generation, voice input, or live inference visualization.

No API keys are included. The server reads the existing private 1Password credential reference on Ryo's configured machine. It binds loopback, rejects cross-origin POSTs, limits questions to 600 characters and at most 20 requests per process. No top-ups, automatic POST retries, or arbitrary code execution. The portable replay works without this backend. The Ask button requires the configured backend.

## Facts and provenance
The Transformer diagrams are original authored schematics informed by Vaswani et al. (2017), Attention Is All You Need, sections 3.1–3.3 (https://arxiv.org/abs/1706.03762). Decoder-only next-token generation follows the autoregressive language-model formulation. Token boundaries, dimensions, attention scores, and output probabilities are illustrative, not measured model inference. The block shows post-norm; modern decoder-only architectures may use other norm/position schemes. Attention weights are not explanations of reasoning.

`story.json` contains exact segment timings. `app.js` owns deterministic animation, `rig.js`/`avatar.js` preserve the existing Gaussian rig. Third-party renderer licenses remain in `vendor`. Original room SH3 SPZ is preserved; the rendering derivative uses its DC color. Originals were never overwritten.
