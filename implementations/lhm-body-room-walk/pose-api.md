# Pose input contract

`window.poseDriver.setPose({segments, position:[0,0,0], yaw:0, source:'recorded video'})`

segments: 15 pairs of 3D points [[ax,ay,az],[bx,by,bz]]. Local meters, y-up, floor y=0, front=+Z, anatomical right=-X. position is room-space translation in meters, yaw rotates about +Y radians. The root is manually registered to the room; monocular pose alone does not localize the person in the scanned room.

Order: pelvis, chest, head, right-upper-arm, right-forearm, right-hand, left-upper-arm, left-forearm, left-hand, right-thigh, right-shin, right-foot, left-thigh, left-shin, left-foot.

`getRest()` returns names and rest endpoints; `getState()` reports actual rendered world segments; `clear()` stops external driving. Retarget limb directions to these body proportions before submitting. Each Gaussian's blended rigid transform changes both centers and covariances. This endpoint does not stretch segment lengths and does not infer poses itself. External pose has priority over scripted motion.

The original avatar is Hyeon's exact shared LHM++ PLY; the manually fitted rig is a derived approximation, not supplied SMPL-X bindings. Current walk video demonstrates authored gait and real keyboard movement, NOT video tracking.
