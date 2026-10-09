> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Causal sketch lab — Chalktalk-inspired prototype

A working sketch dataflow experiment. Draw any polyline in SOURCE, drag its mint output port to the 3D view's mint input, connect the orange NUMBER port to ROTATE Y, and scrub the number horizontally. Edit vertices changes the source and transformed geometry together. Disconnect rotation freezes its last applied angle; reconnect uses the latest number.

## Run

Requires Node.js 18+; no dependencies needed to run the app.

```sh
node server.mjs
```

Open http://127.0.0.1:8776. `AVATAR_EXPLAINER_PORT` changes the port. The portable ZIP contains source and the complete 77-second narrated MP4. Run the local server before opening the app; there is no external network dependency.

## Honest scope

This is a 2D Canvas renderer with actual 3D vertices and a Y rotation matrix. It is not tracked AR, general sketch recognition, a full Chalktalk implementation, or a live avatar presentation. The app has no playback timeline and contains no predefined shapes. Typed explicit ports deliberately replace automatic glyph recognition. The right view displays the input polyline and an offset wireframe layer, not an inferred solid mesh. No previous Orbit, avatar, or room project was modified.

## Evidence

The capture script performs actual pointer operations, records screenshots after each operation step, and holds frames to match narration. It does not animate application state through a timeline. It verifies two novel input shapes, matrix cosine values, geometry changes, source edits, disconnection and reconnection. Timing is demonstration-paced capture, not a claim of realtime performance measurement.

Outputs: `/path/to/local-assets`.

Narration: OpenAI gpt-4o-mini-tts, shimmer, English synthetic voice. `produce-audio.py` uses the approved local SecretRef backing store, never includes credentials in the project, and is not necessary to run the app. To reproduce capture, install dev dependencies with `npm ci`, use your own managed browser endpoint and approved browser supervisor. Original reference review: `/tmp/openclaw/chalktalk-reference-review/findings-ja.md`; source concept: https://github.com/kenperlin/chalktalk .
