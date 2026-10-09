> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo private live spatial sketches

A separate derivative of `avatar-sketch-worlds`; preserves the exact 160k original Ryo avatar and the 301106-point Oct 8 iPad Scaniverse room. Ask a question, and backend OpenAI `gpt-4.1-mini` generates an explanation, label positions, bounded stroke vertices and illustrative motion. The avatar pen traces those generated paths; they unfold into depth. Follow-up context is maintained in an HttpOnly session cookie. Neural answer speech uses `gpt-4o-mini-tts`, shimmer (audio remains in backend memory).

## Access

Private tailnet URL: **http://127.0.0.1:8813/**. Requires an already authorized Tailscale device. It is not an internet/public URL. Transport is encrypted by Tailscale WireGuard; the HTTP application does not use TLS because this tailnet currently does not support certificate issuance. Serve uses TCP forwarding to loopback `127.0.0.1:8811`, preserving other Serve handlers. Non-secure-browser Gaussian sorting uses non-shared worker memory.

Task-owned macOS LaunchAgent `com.ryosuzuki.avatar-live-sketch` keeps `server.py` running. It does not restart or modify OpenClaw Gateway. Reinstall: `python3 scripts/install-service.py`. For a manual local run, `python3 server.py`; then open localhost:8811.

## Security and limits

Backend credential is read at runtime from the established local OpenClaw SecretRef file (`openai`); never shipped to the client or committed. Static routes are allowlisted, server source/API code is not downloadable, request origins are restricted, and questions are limited to 1000 characters. Maximum 150 requests per process / 50 per session, no top-up or purchases. Provider failures are bounded and never expose request headers. Private access is tailnet-level, not a second individual-user ACL. Explanation correctness should be independently checked for consequential use.

This is **generated bounded educational geometry**, not freehand sketch recognition, universal 3D generation, calibrated AR registration, lip sync, physical collision, or a full Jev/Chalktalk implementation. The current Q&A generator uses OpenAI directly, not the former fixed Jev topic-selection catalogue. Authored film playback remains available via Film. Hand rig/pen contact are approximate. Generated words are typed canvas lettering, not captured handwriting.

## Evidence

`verification/browser-verification.json` records three novel questions plus a context-dependent follow-up at the actual served IP URL, generated geometry, original assets, and owned-tab cleanup. Separate Mac mini HTTP retrieval verified reachability. `verification/access-verification.json` records network privacy and route state. Parent delivers `live-question-sketch-preview.mp4` (silent real-operation screen recording, no claim of narrated film audio). Screenshots and video are in Storage outputs/avatar-live-sketch/2026-10-08.

## Readable explanations and recorded live audio

The explanation panel is collapsible, scrollable and has Expand/Smaller controls. On iPad portrait and phone widths it becomes a bottom sheet above the question input; answer and limits never overlap. Phone controls have 44px touch targets and 16px text input. Mobile camera framing expands to retain the avatar and sketch.

`verify-ui-and-record.mjs` submits an actual question through the served private URL, records the live scene plus actual generated answer audio through Web Audio/MediaRecorder, then tests desktop, iPad landscape/portrait and phone answer scrolling, expansion and input hitboxes. Recording content is derived from the live scene, DOM explanation and newly generated audio, not from prerecorded film narration. The audible recording is a new derivative; the original silent operation video is preserved.
