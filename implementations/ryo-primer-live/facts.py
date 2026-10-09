"""Canonical calculated teaching statements. The model never owns arithmetic."""
import math,re

def computed_facts(e,p):
 k=e['kind']
 if k=='attention':return 'Using the dot product divided by the square root of 3, and stable softmax, the computed weights are '+', '.join(f'{chr(65+i)} {100*w:.2f}%' for i,w in enumerate(e['weights']))+'. These are illustrative 3-dimensional vectors, not trained embeddings.'
 if k=='triangle':return f"For perpendicular legs {e['a']:g} and {e['b']:g}, c = sqrt(a²+b²) = {e['hypotenuse']:.3f}. The relation applies to a right triangle."
 if k=='unitcircle':return f"At {e['angleDegrees']:g} degrees, sin(theta) = {e['sin']:.3f} and cos(theta) = {e['cos']:.3f}. They are the vertical and horizontal coordinates on a unit circle."
 if k in ['wave','spring','pendulum']:return f"The illustrative signal has amplitude {e['amplitude']:g}, frequency {e['frequency']:g} Hz and period {1/e['frequency']:.3f} seconds. It is a sinusoidal teaching signal; mechanical dimensions are not inferred."
 if k=='damped':return f"The curve is exp(-{e['damping']:g} t) cos(2 pi {e['frequency']:g} t). The envelope decays while the oscillation frequency stays fixed."
 if k=='projectile':return f"With gravity 9.81 m/s², no drag and equal launch/landing height, the computed range is {e['range']:.3f} metres, maximum height {e['maxHeight']:.3f} metres and flight time {e['flightTime']:.3f} seconds."
 if k=='orbit':return f"The ellipse has eccentricity {e['eccentricity']:g}; the star is at one focus. At zero eccentricity, the shape is a circle and the focus is its centre. This is a shape schematic, not orbital-time simulation."
 if k=='growth':return f"This logistic teaching curve has rate parameter {e['rate']:g}, carrying capacity normalized to 1, and midpoint at time 5. At time 10 its value is {e['valueAt10']:.4f}."
 if k=='exponential':return f"With annual compound growth {100*e['rate']:g}%, a normalized principal of 1 becomes {e['valueAt10']:.4f} after 10 years: (1 + rate)^10."
 if k=='decay':return f"For exponential decay rate {e['rate']:g} per time unit, the half-life is {math.log(2)/e['rate']:.4f} time units. The remaining fraction at time 10 is {e['valueAt10']:.5f}."
 if k=='normal':return f"The normal density has mean {e['mean']:g} and sigma {e['sigma']:g}. Its peak density is {1/(e['sigma']*math.sqrt(2*math.pi)):.4f}. Density height is not probability; probability is area under the curve."
 if k=='bayes':return f"For prior {100*e['prior']:g}%, sensitivity {100*e['sensitivity']:g}% and false-positive rate {100*e['falsePositive']:g}%, the computed posterior after one positive result is {100*e['posterior']:.2f}%. This is an illustrative probability calculation, not medical advice."
 if k=='circuit':return f"For the ideal resistor, current equals voltage divided by resistance, giving {1000*e['currentA']:.3f} milliamps. Dissipated power is {e['powerW']:.4f} watts."
 if k=='lens':return f"Using the thin-lens equation 1/f = 1/do + 1/di, image distance is {e['imageDistance']:.3f} in the same length units. Magnification is {e['magnification']:.3f}; a negative value denotes an inverted image. The drawing is not to scale."
 if k=='vector':return f"Vector components are ({e['x']:g}, {e['y']:g}); its magnitude is sqrt(x²+y²) = {e['norm']:.3f}. Both drawn component axes use equal geometric units."
 if k=='molecule':
  return ('Water has two bonding domains and two lone-pair domains around oxygen. Its bent bond angle is 104.5 degrees, and its bond dipoles yield a net molecular dipole. Carbon dioxide is linear and nonpolar by symmetry.' if e['formula']=='H2O' else 'Carbon dioxide has two electron domains at carbon; each double bond counts as one domain. Its bond angle is 180 degrees. Opposite bond dipoles cancel by symmetry; unlike bent polar water, carbon dioxide is nonpolar.')+' Atom sizes are schematic, not to scale.'
 if k=='bars':return 'The displayed values are '+', '.join(f'{v:g}' for v in e['values'])+'. They are normalized illustrative values, not empirical measurements.'
 return ''

CONCEPTS={
'attention':'Attention compares a query with keys, then softmax normalizes the relevance scores. Here scale is a multiplicative query/score gain, not a divisor: increasing a positive gain strengthens existing score contrasts; tied scores remain tied.',
 'triangle':'A right triangle satisfies the Pythagorean theorem: the square of its hypotenuse equals the sum of the squared perpendicular legs.',
 'unitcircle':'On the unit circle, cosine is the horizontal coordinate and sine the vertical coordinate. A point to the left of the vertical axis has a negative cosine.',
 'wave':'Amplitude controls peak displacement; frequency controls cycles per second. Changing frequency alone does not change amplitude in this illustrative signal.',
 'pendulum':'For an ideal small-angle pendulum, angular displacement is approximately sinusoidal. Its physical natural frequency depends on gravity and length, not amplitude in that approximation. This displayed signal does not infer an unspecified length.',
 'spring':'An ideal spring oscillator is approximately sinusoidal. Its natural frequency depends on stiffness and mass; amplitude controls displacement. The displayed signal uses chosen illustrative parameters rather than inferred mechanical dimensions.',
 'damped':'Damping shrinks the oscillation envelope over time. The decay parameter controls how quickly the amplitude falls; the cosine term controls oscillation.',
 'projectile':'Without air drag, horizontal velocity stays constant while gravity changes vertical velocity. Launch angle trades horizontal speed against vertical speed; the range and height follow from those components.',
 'orbit':'Changing eccentricity changes an ellipse from a circle to a more elongated shape. The star belongs at one focus, not generally at the geometric centre.',
 'growth':'Logistic growth slows near its carrying capacity and approaches a plateau. The rate parameter changes how quickly the transition occurs.',
 'exponential':'Compound growth applies the same multiplicative factor each year. Growth then acts on the accumulated amount, not only the starting principal.',
 'decay':'Exponential decay removes the same fraction per equal time interval. Its half-life is constant for a constant decay rate, even as the remaining amount decreases.',
 'normal':'A normal distribution is symmetric about its mean. Increasing sigma spreads it out and lowers its peak while total probability stays normalized. Probability is obtained by integrating density over an interval.',
 'bayes':'Bayes combines prior probability with the likelihood of observed evidence. A positive result need not imply a high posterior when the prior is small, because false positives from the larger alternative group can dominate.',
 'circuit':'For an ideal resistor at fixed voltage, increasing resistance reduces current. Ohms law is a linear idealization; actual devices may change with temperature.',
 'lens':'A thin converging lens forms a real inverted image when the object lies beyond the focal length. The thin-lens equation relates focal, object and image distances.',
 'vector':'A vector has signed horizontal and vertical components. Its Euclidean magnitude follows from the Pythagorean relation; reversing a component changes direction, not that component’s squared contribution.',
 'molecule':'Electron-domain geometry describes molecular shape. Bond dipoles add as vectors, so molecular symmetry determines whether their net dipole cancels.',
 'bars':'Bar lengths encode normalized illustrative values. They should not be interpreted as empirical measurements unless a real data source is supplied.'
}
def canonical_answer(raw,evidence,items):
 if all(e['kind']=='flow' for e in evidence):return raw,[]
 # Numerical families use audited conceptual beats + canonical calculations.
 # The model selects/orders/parameterizes these beats; it does not own their truth.
 concepts=[];facts=[]
 for e,p in zip(evidence,items):
  c=CONCEPTS.get(e['kind'],'')
  if c and c not in concepts:concepts.append(c)
  f=computed_facts(e,p)
  if f:facts.append(f)
 return (' '.join(concepts)+'\n\n'+' '.join(facts)).strip()[:3200],facts
JP_CONCEPTS={
'attention':'アテンションはクエリとキーの関連度を比較し、ソフトマックスで重みを正規化します。この図のスケールは割り算ではなく、スコアに掛ける倍率です。倍率を上げると、既存のスコア差が強調されます。同じスコア同士の差は生まれません。',
 'triangle':'直角三角形では、斜辺の長さの二乗が、直交する二辺の長さの二乗の和に等しくなります。',
 'unitcircle':'単位円では、コサインが横座標、サインが縦座標です。縦軸の左側にある点のコサインは負になります。',
 'wave':'振幅は最大変位を、周波数は一秒あたりの繰り返し回数を表します。この例では、周波数だけを変えても振幅は変わりません。',
 'pendulum':'小さな角度で振れる理想的な振り子は、ほぼ正弦波の運動をします。この近似で自然周波数は重力と長さに依存し、振幅には依存しません。ここでは説明用の信号を描いており、未知の長さを推定してはいません。',
 'spring':'理想的なばねの振動はほぼ正弦波です。自然周波数はばね定数と質量に依存し、振幅は変位の大きさを決めます。この図は指定した説明用の信号です。',
 'damped':'減衰によって、振動の包絡線が時間とともに小さくなります。減衰係数は振幅の減り方を、コサインの項は振動を表します。',
 'projectile':'空気抵抗を無視すると、水平方向の速度は一定で、鉛直方向の速度は重力で変化します。投射角を変えると、初速度の水平成分と鉛直成分の配分が変わります。',
 'orbit':'離心率を変えると、円から、より細長い楕円へ形が変わります。恒星は一般には楕円の中心ではなく、一つの焦点にあります。',
 'growth':'ロジスティック成長は、上限となる環境収容力に近づくにつれて遅くなります。速度パラメータは、変化の速さを調整します。',
 'exponential':'複利では、毎年同じ倍率を、その時点で積み上がった額に掛けます。最初の元本だけが増えるわけではありません。',
 'decay':'指数減衰では、同じ時間ごとに、残っている量の一定割合が減ります。減衰率が一定なら、半減期も一定です。',
 'normal':'正規分布は平均を中心に対称です。標準偏差を増やすと幅が広がり、頂点は低くなります。確率は曲線の高さではなく、区間内の面積です。',
 'bayes':'ベイズの定理は、事前確率と、観測された証拠の尤度を組み合わせます。事前確率が小さければ、陽性の結果が出ても、事後確率が必ず高くなるとは限りません。',
 'circuit':'理想的な抵抗では、電圧が一定のとき、抵抗を大きくすると電流が減ります。実際の部品では、温度などによって性質が変わることがあります。',
 'lens':'薄い凸レンズでは、物体が焦点より遠くにあると、倒立した実像ができます。レンズの式は、焦点距離、物体距離、像距離の関係を表します。',
 'vector':'ベクトルは、符号を持つ横成分と縦成分で表せます。ユークリッド長は、各成分の二乗和の平方根です。',
 'molecule':'分子の形には電子領域の配置が関係します。結合の双極子はベクトルとして足し合わされるため、対称性によって分子全体の双極子が打ち消されることがあります。',
 'bars':'棒の長さは、正規化した説明用の数値を表します。実際のデータ源がない場合は、実測値として解釈しないでください。'}
def computed_facts_jp(e,p):
 k=e['kind']
 if k=='attention':return '内積を3の平方根で割り、ソフトマックスで計算すると、重みは'+ '、'.join(f'{chr(65+i)}が{100*w:.2f}パーセント' for i,w in enumerate(e['weights']))+'です。説明用の3次元ベクトルであり、学習済みの埋め込みではありません。'
 if k=='triangle':return f"直交する二辺が{e['a']:g}と{e['b']:g}なら、斜辺は二乗和の平方根で{e['hypotenuse']:.3f}です。"
 if k=='unitcircle':return f"角度{e['angleDegrees']:g}度で、サインは{e['sin']:.3f}、コサインは{e['cos']:.3f}です。"
 if k in ['wave','spring','pendulum']:return f"振幅は{e['amplitude']:g}、周波数は{e['frequency']:g}ヘルツ、周期は{1/e['frequency']:.3f}秒です。物理的な寸法を推定する信号ではありません。"
 if k=='damped':return f"減衰係数は{e['damping']:g}、振動周波数は{e['frequency']:g}ヘルツです。振幅の包絡線は指数関数で減少します。"
 if k=='projectile':return f"重力加速度を毎秒毎秒9.81メートルとし、空気抵抗を無視し、出発点と着地点を同じ高さとすると、到達距離は{e['range']:.3f}メートル、最大高さは{e['maxHeight']:.3f}メートル、飛行時間は{e['flightTime']:.3f}秒です。"
 if k=='orbit':return f"離心率は{e['eccentricity']:g}です。離心率がゼロなら円となり、焦点は中心に一致します。これは形の概念図であり、軌道上の時間変化を再現するものではありません。"
 if k=='growth':return f"速度パラメータは{e['rate']:g}、上限を1に正規化し、中点を時刻5とした曲線です。時刻10の値は{e['valueAt10']:.4f}です。"
 if k=='exponential':return f"年率{100*e['rate']:g}パーセントの複利では、元本を1とすると、10年後は{e['valueAt10']:.4f}になります。"
 if k=='decay':return f"時間単位あたりの減衰率が{e['rate']:g}なら、半減期は{math.log(2)/e['rate']:.4f}時間単位です。時刻10の残存割合は{e['valueAt10']:.5f}です。"
 if k=='normal':return f"平均は{e['mean']:g}、標準偏差は{e['sigma']:g}、頂点の確率密度は{1/(e['sigma']*math.sqrt(2*math.pi)):.4f}です。密度の高さ自体は確率ではありません。"
 if k=='bayes':return f"事前確率{100*e['prior']:g}パーセント、感度{100*e['sensitivity']:g}パーセント、偽陽性率{100*e['falsePositive']:g}パーセントなら、一回の陽性結果後の事後確率は{100*e['posterior']:.2f}パーセントです。教育用の計算で、医学的な助言ではありません。"
 if k=='circuit':return f"理想的な抵抗での電流は{1000*e['currentA']:.3f}ミリアンペア、消費電力は{e['powerW']:.4f}ワットです。"
 if k=='lens':return f"像距離は、同じ長さの単位で{e['imageDistance']:.3f}です。倍率は{e['magnification']:.3f}で、負の値は倒立像を表します。図は縮尺通りではありません。"
 if k=='vector':return f"成分は{e['x']:g}と{e['y']:g}、長さは{e['norm']:.3f}です。描画した二つの成分軸は、同じ幾何学的な単位を使っています。"
 if k=='molecule':return ('水では酸素の周りに二つの結合領域と二つの孤立電子対領域があり、結合角は104.5度です。曲がった形のため、結合の双極子が打ち消し合わず、分子に極性があります。' if e['formula']=='H2O' else '二酸化炭素では、炭素の周りの電子領域は二つです。二重結合も一つの領域として数えます。結合角は180度で、対称な双極子が打ち消し合うため、分子全体は無極性です。')+'原子の大きさは概略で、実際の縮尺ではありません。'
 return computed_facts(e,p)
# Language parity: numerical facts remain local in either supported explanation language.
_canonical_answer_en=canonical_answer
def canonical_answer(raw,evidence,items,language=None):
 if all(e['kind']=='flow' for e in evidence):return raw,[]
 if language=='ja' or re.search('[ぁ-んァ-ン一-龯]',raw):
  concepts=[];facts=[]
  for e,p in zip(evidence,items):
   c=JP_CONCEPTS.get(e['kind'],'')
   if c and c not in concepts:concepts.append(c)
   f=computed_facts_jp(e,p)
   if f:facts.append(f)
  return (' '.join(concepts)+'\n\n'+' '.join(facts)).strip()[:3200],facts
 return _canonical_answer_en(raw,evidence,items)
