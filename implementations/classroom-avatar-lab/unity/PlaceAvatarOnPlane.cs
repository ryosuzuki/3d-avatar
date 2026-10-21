using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
// AR Foundation 5/6 example. Requires legacy Input or Active Input Handling=Both.
// Static prefab placement only; no humanoid rig or Quest passthrough dependency.
public sealed class PlaceAvatarOnPlane : MonoBehaviour
{
    public ARRaycastManager RaycastManager;
    public GameObject AvatarPrefab;
    readonly List<ARRaycastHit> hits = new List<ARRaycastHit>();
    GameObject placed;
    void Update()
    {
        if (RaycastManager == null || AvatarPrefab == null || Input.touchCount == 0) return;
        Touch touch = Input.GetTouch(0);
        if (touch.phase != TouchPhase.Began) return;
        if (UnityEngine.EventSystems.EventSystem.current != null &&
            UnityEngine.EventSystems.EventSystem.current.IsPointerOverGameObject(touch.fingerId)) return;
        if (!RaycastManager.Raycast(touch.position, hits, TrackableType.PlaneWithinPolygon)) return;
        Pose pose = hits[0].pose;
        if (placed == null) placed = Instantiate(AvatarPrefab, pose.position, pose.rotation);
        else placed.transform.SetPositionAndRotation(pose.position, pose.rotation);
    }
}
