> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Ryo Primer Live

Private, runnable Ryo-avatar sketch Q&A prototype. A model **selects, orders, and parameterizes a closed catalog**; locally tested functions calculate and draw geometry. No model-generated code is executed. For numerical families, audited catalog-authored conceptual beats and canonical backend-calculated facts drive the displayed explanation, narration and conversational history. The model selects/orders/parameterizes them; only concept-flow topics use free model prose. English and Japanese numerical explanations use local templates. Raw model prose is retained separately for auditing, not displayed.

## Source and honest scope

- Based on the existing user-owned `avatar-live-sketch`, preserving the actual 160,000-Gaussian Ryo avatar and captured iPad room (provenance in source-provenance.json).
- Composition design inspired by Sean Liu's [jev-interaction](https://github.com/sseanliu/jev-interaction), especially catalog.py and compose_jev.py. **This implementation uses OpenAI gpt-4.1-mini, not the Jev service.** A verified local TypeSafe/Jev credential was not available. It does not claim the Jev README's ~300 ms selection performance.
- Text Q&A and contextual followups are real provider calls. Generated numerical diagrams are not 30 canned scenes. Gallery clips are explicitly recorded test replays.
- Browser-rendered live projected-stylus drawing and parameter previews. The real Gaussian avatar uses a manually fitted skeletal adapter; a thin beam links its reachable hand/pen to the sketch cursor. It is not reconstructed natural hand motion or literal physical board contact; not streaming model selection, not speech-to-speech. Voice is asynchronous OpenAI synthetic shimmer TTS, not a cloned Ryo voice. Tap Play voice if browser autoplay is blocked.
- 20 controlled sketch families; unsupported concepts become honest concept-flow diagrams. Geometry is educational, not a trained attention network or a calibrated physical simulation.
- Changing a slider recomputes geometry locally, not the narration or original explanation. Ask a followup for a new explanation.

## Run

```sh
python3 server.py
# http://127.0.0.1:8821
python3 test-catalog.py
python3 test-server-repair.py  # mocked repair conformance, not live timing
```

Backend reads the existing approved local secret store; never place API keys in HTML, scripts, Git or recordings. Static serving is allowlisted. Requests are same-origin restricted.

Installed user LaunchAgent: org.ryo.primer-live. Service logs: /tmp/openclaw/primer-server*.log. Private tailnet access is configured separately and never publicly exposed.

## Verification and artifacts

Authoritative test questions: cases.json. Recording script: record-cases.mjs (must run under tools-browser's agent-2 FIFO supervisor, actual endpoint verified). Local output location: `/path/to/local-assets`.

Final delivered cases live in `2026-10-09/final-v3/`; earlier passes remain preserved as provisional or superseded evidence. Each case has a real request/response, browser latency, full generated voice, screenshot, video, catalog/finite-geometry checks, and parameter-change evidence. Case recordings include waiting rather than cutting it out. `selectionMs` is backend request-through-compilation latency; `firstUsableSketchMs` is browser submission-to-first rendered labeled answer/sketch frame, not completed ink (drawing completion takes four additional seconds); `audioReadyMs` is submission-to-available audio, and `audioStartedMs` is successful browser playback. A reusable numerical update uses no API call.

Large original assets and generated recordings remain in Storage. Git contains source/reproduction instructions and hashes/location receipts, not asset copies or credentials.

## Delivery composition

`make-montage.py` produces a Japanese-narrated overview of all 30 genuinely generated case clips; waiting is cut only in the montage. `walkthrough.mjs` records actual browser DOM, visible parameter sliders, contextual followup, and actual generated audio. The walkthrough uses repeatedly refreshed browser screenshots in a 30fps recording container; it is not a 30fps application-throughput benchmark. `normalize-cases.py`, `finalize-captions.py` and `validate-program.py` verify the exact delivery media. The final caption is held through a local preview where applicable; sentence alignment is approximate.

Run browser scripts only under the owning profile’s FIFO supervisor. Media remains private under Storage and the local tailnet service. Existing unrelated Tailscale routes are preserved.

## Verified final results

30/30 corrected final live cases pass selection, requested parameters, calculated facts, concept structure, layout and media checks (19 primary families). Labeled response p50 2125ms / p95 3217ms; ink continues about four seconds. Audio ready p50 7230ms / p95 10849ms. Warm MacStudio browser via private tailnet, initial avatar loading excluded; not a remote-headset benchmark. All32 delivery MP4s full-decode verified, H264 High limited yuv420p/CFR30/AAC48k, captions and normalized audio. Source voices and complete programs computationally listened to; no human headphone review.

Live: http://127.0.0.1:8822/ · Gallery: http://127.0.0.1:8822/gallery.html (private Ryo tailnet). Overview128s, genuine UI walkthrough70s, all30 complete clips in CRC-verified ZIP with offline index. Final measured data and delivery receipts remain at the output location above.
