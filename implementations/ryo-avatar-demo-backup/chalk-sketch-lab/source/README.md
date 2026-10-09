> Public source snapshot: personal room/avatar/capture assets are not bundled. Original README below documents the source project; asset-included claims apply only to the original private delivery. Use your own assets and local settings. API scripts use OPENAI_API_KEY or TYPESAFE_API_KEY from your environment.

# Sketch → Space
Chalktalk-inspired causal sketch graph. Open index.html directly or serve with `python3 -m http.server 8766`.
Draw any polyline in Source Sketch, explicitly confirm it, Connect ports shape→view and angle→rotation, then scrub the slider and edit any vertex. Disconnect holds the last downstream geometry. Undo and reset are available. Rotation is genuine R_y matrix multiplication; rendering is orthographic screen-space 3D, not tracked AR. No AI/generic recognition is claimed. Source stroke remains arbitrary, not a glyph template.
Reference inspiration: https://github.com/kenperlin/chalktalk ; https://www.youtube.com/watch?v=ZZi3I_NCiUk&t=322 ; https://x.com/HCI_Research/status/1251898938967207937 . Original implementation; no source code copied.
