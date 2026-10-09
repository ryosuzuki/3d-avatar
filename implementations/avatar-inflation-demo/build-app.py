from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=Path('/path/to/local-assets').read_text()
prefix=src[:src.index('function transform(')]
prefix=prefix.replace("import {buildScene,normalize,extractStrokes} from './geometry.js';",'').replace("import {GLTFLoader} from './vendor/GLTFLoader.js';import {OBJLoader} from './vendor/OBJLoader.js';",'')
prefix=prefix.replace("origin=new THREE.Vector3(.55,1.35,.48),scale=.65","origin=new THREE.Vector3(.55,1.32,.48),scale=.85")
(ROOT/'app.js').write_text(prefix+(ROOT/'body.js').read_text())
