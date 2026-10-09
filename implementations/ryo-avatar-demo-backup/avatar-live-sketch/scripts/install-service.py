from pathlib import Path
import plistlib,sys,subprocess,os
root=Path(__file__).resolve().parents[1]
p=Path.home()/'Library/LaunchAgents/com.ryosuzuki.avatar-live-sketch.plist'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(plistlib.dumps({'Label':'com.ryosuzuki.avatar-live-sketch','ProgramArguments':[sys.executable,str(root/'server.py')],'RunAtLoad':True,'KeepAlive':True,'WorkingDirectory':str(root),'StandardOutPath':'/tmp/openclaw/avatar-live-sketch-server.log','StandardErrorPath':'/tmp/openclaw/avatar-live-sketch-server-error.log'}));p.chmod(0o600)
subprocess.run(['launchctl','bootstrap',f'gui/{os.getuid()}',str(p)],check=True)
