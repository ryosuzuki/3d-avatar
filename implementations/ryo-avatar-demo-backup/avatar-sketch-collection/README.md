> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Living Sketch Collection

One 272-second ordered English compilation of the already verified 128-second Sketch Worlds and 144-second Sketch Frontiers films. No scene footage was regenerated and no API requests were made.

Eight chapters: pendulum/waveform; fish; landscape/river/cloud; water molecule; walking dinosaur; spatial attention; ideal gas; schematic body.

## Outputs

- `avatar-sketch-collection-master.mp4`: 1080p30, original video streams copied without reencoding.
- `avatar-sketch-collection-slack.mp4`: 720p30, 14.9MB compact derivative; existing preview video streams copied without another video generation.
- `narration.srt`/`.vtt`: original subtitle text, second film shifted exactly 128 seconds.
- Chapters embedded in both films and saved as `chapters.json`.

Output directory: `/path/to/local-assets`.

## Reproduce

`python3 build.py` uses FFmpeg/ffprobe and the existing two project/source film paths recorded in `delivery-manifest.json`. Both inputs and original neural PCM narration remain at their existing Storage locations, with private GitHub backups. The combined PCM samples are copied in order; master AAC is encoded at 192 kbps, compact AAC at 128 kbps. `python3 verify-frames.py` compares every decoded frame with the original ordered source frames and verifies exact source PCM sample ordering. No model, credential, browser, or network is required to compile or verify.

## Boundaries

This is an authored film compilation, not a single interactive recognition engine or complete Chalktalk replication. Eight procedural examples preserve the original avatar/room and each source's disclaimers. Attention weights, gas trajectories and body organs are schematic; no measured LLM attention, molecular dynamics or medical reconstruction. Rig/hand grip and layered occlusion limitations remain. Live generated Q&A is a separately delivered application.

Publication owner: `sketch_worlds_remaining`; exact owned backup path `avatar-sketch-collection/`, terminal target `origin/main`. Large MP4s are private release assets, not Git-history blobs.
