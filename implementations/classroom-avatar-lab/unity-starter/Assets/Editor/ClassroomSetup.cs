using System;
using System.IO;
using System.Reflection;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using GaussianSplatting.Editor;
using GaussianSplatting.Runtime;

public class ClassroomSetup : EditorWindow {
 static Camera cam;
 static string status = "Ready. Import the original Gaussian PLY, not the approximate mesh.";
 [MenuItem("Classroom/Avatar Tutorial")]
 public static void Open() { var w=GetWindow<ClassroomSetup>(); w.titleContent=new GUIContent("Avatar Lab · Unity"); w.position=new Rect(40,60,660,660); w.Show(); }
 void OnGUI() {
 GUILayout.Space(18); GUILayout.Label("AVATAR LAB / UNITY",EditorStyles.boldLabel);
 GUILayout.Label("Keep the original Gaussian appearance",EditorStyles.largeLabel);
 EditorGUILayout.HelpBox("This is a static 3D Gaussian avatar. No humanoid skeleton, Mixamo rig or recovered dance animation is included.",MessageType.Info);
 GUILayout.Space(10);
 if(GUILayout.Button("1   Import Assets/avatar.ply (Very High quality)",GUILayout.Height(48))) Import();
 GUILayout.Space(8);
 if(GUILayout.Button("2   Build the Gaussian demo scene",GUILayout.Height(48))) Scene();
 GUILayout.Space(8);
 if(GUILayout.Button("3   Open the Game view · Press Play",GUILayout.Height(48))) EditorApplication.ExecuteMenuItem("Window/General/Game");
 GUILayout.Space(14); EditorGUILayout.HelpBox(status,MessageType.None);
 GUILayout.Label("Use your own download",EditorStyles.boldLabel);
 GUILayout.Label("Replace Assets/avatar.ply, then repeat steps 1 and 2.");
 GUILayout.Label("Do not drag avatar-static.obj into Unity for the best appearance.");
 GUILayout.Space(14); GUILayout.Label("Desktop first",EditorStyles.boldLabel);
 GUILayout.Label("Verified target: Unity 6, Built-in rendering, Mac Metal.");
 GUILayout.Label("Mobile AR / Quest is a separate renderer + device test.");
 GUILayout.Label("This project does NOT claim working mobile AR.");
 }
 static void Set(object o,string n,object v) { o.GetType().GetField(n,BindingFlags.NonPublic|BindingFlags.Instance).SetValue(o,v); }
 public static void Verify() { Debug.Log("CLASSROOM_STARTER_SCRIPT_VERIFIED"); }
 public static void Import() {
 if(!File.Exists("Assets/avatar.ply")){ EditorUtility.DisplayDialog("Add your avatar", "Copy your downloaded avatar.ply into this project’s Assets folder first.", "OK"); return; }
 var c=ScriptableObject.CreateInstance<GaussianSplatAssetCreator>();
 Set(c,"m_InputFile",Path.GetFullPath("Assets/avatar.ply")); Set(c,"m_OutputFolder","Assets/GaussianAssets");
 var f=c.GetType().GetField("m_Quality",BindingFlags.NonPublic|BindingFlags.Instance); f.SetValue(c,Enum.ToObject(f.FieldType,0));
 c.GetType().GetMethod("ApplyQualityLevel",BindingFlags.NonPublic|BindingFlags.Instance).Invoke(c,null);
 c.GetType().GetMethod("CreateAsset",BindingFlags.NonPublic|BindingFlags.Instance).Invoke(c,null);
 AssetDatabase.Refresh(); status="Imported the original PLY with uncompressed Gaussian attributes.";
 }
 static T Find<T>(string query) where T:UnityEngine.Object { foreach(var id in AssetDatabase.FindAssets(query)) { var a=AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(id)); if(a)return a; } return null; }
 public static void Scene() {
 if(Find<GaussianSplatAsset>("t:GaussianSplatAsset")==null){ EditorUtility.DisplayDialog("Import first", "Import Assets/avatar.ply before building the scene.", "OK"); return; }
 if(!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
 EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
 var go=new GameObject("Avatar — original Gaussian splats"); go.SetActive(false); var r=go.AddComponent<GaussianSplatRenderer>();
 r.m_Asset=Find<GaussianSplatAsset>("t:GaussianSplatAsset");
 r.m_ShaderSplats=Find<Shader>("RenderGaussianSplats t:Shader");
 r.m_ShaderComposite=Find<Shader>("GaussianComposite t:Shader");
 r.m_ShaderDebugPoints=Find<Shader>("GaussianDebugRenderPoints t:Shader");
 r.m_ShaderDebugBoxes=Find<Shader>("GaussianDebugRenderBoxes t:Shader");
 r.m_CSSplatUtilities=Find<ComputeShader>("SplatUtilities t:ComputeShader");
 go.SetActive(true);
 var cg=new GameObject("Main Camera"); cg.tag="MainCamera"; cam=cg.AddComponent<Camera>(); cam.clearFlags=CameraClearFlags.SolidColor; cam.backgroundColor=new Color(.86f,.88f,.86f); cam.fieldOfView=35; cam.nearClipPlane=.01f;
 var b=new Bounds((r.m_Asset.boundsMin+r.m_Asset.boundsMax)*.5f,r.m_Asset.boundsMax-r.m_Asset.boundsMin); cam.transform.position=b.center+new Vector3(0,0,Mathf.Max(3.5f,b.size.y*1.9f)); cam.transform.LookAt(b.center);
 EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene(),"Assets/AvatarDemo.unity");
 Selection.activeGameObject=go;
 status="Scene built. Original Gaussian appearance; still static, not rigged.";
 Debug.Log("CLASSROOM_SETUP asset="+r.m_Asset+" setup="+r.HasValidRenderSetup+" shader="+r.m_ShaderSplats+" compute="+r.m_CSSplatUtilities);
 }
}
