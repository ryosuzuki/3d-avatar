import unittest
from repair_mixamo import weld_obj

class MixamoTopology(unittest.TestCase):
    def test_uv_seams_preserve_texture_and_close_geometry(self):
        source='\n'.join(['mtllib avatar-textured.mtl','v 0 0 0','v 1 0 0','v 0 1 0','v 0 0 1','v 0 0 0','vt 0 0','vt 1 0','vt 0 1','vt 1 1','vt .5 .5','usemtl AvatarTexture','f 1/1 3/3 2/2','f 5/5 2/2 4/4','f 2/2 3/3 4/4','f 3/3 5/5 4/4'])
        fixed,report=weld_obj(source)
        self.assertEqual(report,dict(vertices=4,faces=4,boundary_edges=0))
        self.assertIn('f 1/5 2/2 4/4',fixed)
        self.assertIn('vt .5 .5',fixed)
        self.assertIn('usemtl AvatarTexture',fixed)
        self.assertEqual(weld_obj(fixed)[1],report)
    def test_open_mesh_rejected(self):
        with self.assertRaises(ValueError):weld_obj('v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n')
if __name__=='__main__':unittest.main()
