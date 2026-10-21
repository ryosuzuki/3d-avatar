# Animated human classroom starter
Unity 6000.4.5f1, Built-in renderer. No Adobe character assets are bundled.
1. Open project in Unity Hub (Add project from disk).
2. Download Remy + Hip Hop Dancing in your own Mixamo account: FBX for Unity, With Skin, 30 FPS.
3. Copy to Assets/Character.fbx.
4. Classroom > Character Tutorial. Click Select, Configure, Build, Open Game view. Press Play.
The helper uses Unity standard APIs. The material matching is tested with Remy; other models can need manual texture assignment.
Manual path: Inspector > Rig > Humanoid > Create From This Model > Apply. Animation > Loop Time > Apply. Materials > Extract Textures/Materials if gray; assign Base Map/Albedo. Create Animator Controller, drop animation into graph, assign to model Animator, turn Apply Root Motion off for an in-place demo.
This is desktop playback, not a verified mobile/WebXR or Quest deployment.
