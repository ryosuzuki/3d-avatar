from pathlib import Path
from server import provider
import json,subprocess,os,hashlib,re
ROOT=Path(os.environ.get('PRIMER_OUT','/path/to/local-assets'))
scripts=[
'質問に応じて、リョウのアバターがスケッチで説明するプロトタイプです。これは実際に生成した三十件のテストをまとめたリプレイです。アテンションや三角形では、モデルが図の種類とパラメータを選び、数値の説明と形は検証済みのコードで計算します。',
'単位円や波の例です。線が描かれてから、数値を動かして関係を確かめられます。追加の質問では、直前の条件を引き継いで、周波数だけを変えることもテストしました。各動画には、質問から図が出るまでの実測時間を残しています。',
'ばね、減衰、放物運動、軌道の例です。これは教育用の簡略モデルで、空気抵抗などを省いています。手が届かない図には、アバターのペンから光の線をつないで描きます。自然な手の動きを収録したものではありません。',
'楕円の形を変えた例に続いて、成長、複利、減衰、正規分布も、別々の計算式で描いています。見た目だけでなく、指定したパラメータや計算結果をチェックしました。試したい図を一覧から選ぶと、同じ質問をライブ画面に入力できます。',
'正規分布の幅を比較し、ベイズの更新とオームの法則も描きました。図のスライダーは、モデルを呼ばずに数値と形を更新します。ただし、その操作だけでは、元の説明文や音声は変わりません。説明も変えたい場合は、続けて質問してください。',
'最後はレンズ、ベクトル、分子、そして日本語の概念図です。現在はテキストの質問と、後から準備される合成音声に対応しています。ジェブの構成方式を参考にしていますが、選択モデルはオープンエーアイです。音声による割り込み対話は、まだ実装していません。']
report=json.loads((ROOT/'assessment.json').read_text());manifest=[];segments=[]
for group,text in enumerate(scripts):
 aid=f'montage-voice-{group+1}';mp3=ROOT/(aid+'.mp3')
 if not mp3.exists():mp3.write_bytes(provider('audio/speech',{'model':'gpt-4o-mini-tts','voice':'shimmer','input':text,'response_format':'mp3','instructions':'Natural Japanese explanatory delivery, calm conversational academic voice. Say リョウ naturally. Clearly pronounce technical terms. Not a cloned voice.'}))
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mp3)]));target=round((dur+.4)*30)/30;length=target/5;parts=[]
 for c in report['cases'][group*5:group*5+5]:
  source=ROOT/(c['prefix']+'.mp4');part=ROOT/f'montage-part-{c["id"]:02}.mp4';start=c['firstUsableSketchMs']/1000+1.2
  subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-i',str(source),'-t',str(length),'-an','-c:v','libx264','-preset','fast','-crf','21','-r','30','-pix_fmt','yuv420p','-vf','scale=out_range=tv,format=yuv420p','-color_range','tv',str(part)],check=True);parts.append(part)
 concat=ROOT/f'montage-group-{group+1}.txt';concat.write_text(''.join("file '"+str(p).replace("'","'\\''")+"'\n" for p in parts));dest=ROOT/f'montage-segment-{group+1}.mp4'
 subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-i',str(mp3),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','21','-vf','scale=out_range=tv,format=yuv420p,tpad=stop_mode=clone:stop_duration=1','-r','30','-pix_fmt','yuv420p','-color_range','tv','-c:a','aac','-ar','48000','-b:a','160k','-af','apad','-t',str(target),'-movflags','+faststart',str(dest)],check=True);segments.append(dest);manifest.append({'segment':group+1,'caseIds':[c['id'] for c in report['cases'][group*5:group*5+5]],'narration':text,'targetSeconds':target,'audioSeconds':dur,'visualAction':'Five actual live-generated case clips, waiting time omitted only in montage','voice':'OpenAI gpt-4o-mini-tts / shimmer, Japanese synthetic voice'})
concat=ROOT/'montage-concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in segments));temp=ROOT/'montage-pre-subtitle.mp4';subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(temp)],check=True)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
cursor=0;srt=[];n=0
for mi,m in enumerate(manifest):
 sentences=[s+'。' for s in m['narration'].split('。') if s];total=sum(len(s) for s in sentences);x=cursor
 for si,text in enumerate(sentences):
  end=sum(z['targetSeconds'] for z in manifest) if mi==len(manifest)-1 and si==len(sentences)-1 else x+m['audioSeconds']*len(text)/total;n+=1;srt.append(f'{n}\n{stamp(x)} --> {stamp(end)}\n{text}\n');x=end
 cursor+=m['targetSeconds']
(ROOT/'montage.srt').write_text('\n'.join(srt));(ROOT/'montage.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d\d:\d\d:\d\d),(\d{3})',r'\1.\2','\n'.join(srt)));(ROOT/'montage-transcript.txt').write_text('\n\n'.join(scripts));final=ROOT/'ryo-primer-montage.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(temp),'-i',str(ROOT/'montage.srt'),'-map','0:v','-map','0:a','-map','1:0','-c:v','libx264','-preset','fast','-crf','21','-vf','scale=out_range=tv,format=yuv420p,tpad=stop_mode=clone:stop_duration=1','-r','30','-pix_fmt','yuv420p','-color_range','tv','-c:a','aac','-ar','48000','-b:a','160k','-af','apad,loudnorm=I=-16:TP=-2.0:LRA=11','-t',str(round(cursor*30)/30),'-c:s','mov_text','-metadata:s:s:0','language=jpn','-movflags','+faststart',str(final)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'],check=True);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)]));(ROOT/'montage-manifest.json').write_text(json.dumps({'segments':manifest,'path':str(final),'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'bytes':final.stat().st_size,'probe':probe,'fullDecodePassed':True,'subtitleTiming':'Authoritative text, sentence proportional approximate alignment','scope':'Recorded test montage, not uninterrupted live execution. Full clips include all waiting.'},ensure_ascii=False,indent=2));print('Montage duration',probe['format']['duration'],'bytes',final.stat().st_size)
