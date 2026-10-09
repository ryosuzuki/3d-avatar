#!/bin/zsh
set -e
out=/path/to/local-assets
ffmpeg -y -v error -i "$out/opening-gesture-patch.mp4" -i "$out/visual-master.mp4" -i "$out/third-example-patch.mp4" -filter_complex '[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=start=10:end=60,setpts=PTS-STARTPTS[b];[2:v]setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]' -map '[v]' -an -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p -r 30 -color_range tv -movflags +faststart "$out/visual-master-repaired.mp4"
python3 "${0:A:h}/finalize.py" visual-master-repaired.mp4
