"""CPU regression: run the patched upstream call with strided, multi-person detections.
Run using the LHM++ environment, from the model source directory, with this project
on PYTHONPATH. No weights or GPU inference are needed.
"""
import unittest
import numpy as np
import torch
from pose_compat import install_pose_compat
from engine.pose_estimation.pose_estimator import PoseEstimator

class PoseCompatibilityTest(unittest.TestCase):
    def test_noncontiguous_single_and_multiple_detections(self):
        install_pose_compat()
        for people in (1, 2, 3):
            with self.subTest(people=people):
                estimator = PoseEstimator.__new__(PoseEstimator)
                estimator.device = torch.device('cpu')
                estimator.img_center_padding = lambda im: (im, 0, 0)
                estimator._preprocess = lambda im: (torch.zeros(1, 3, 8, 8), (0, 0, 1, 8, 8))
                estimator.get_camera_parameters = lambda: torch.eye(3).unsqueeze(0)
                def detections(*args, **kwargs):
                    return {'loc': torch.arange(people*4.).reshape(people, 4)[:, ::2],
                            'dist': torch.ones(people, 2)[:, :1],
                            'shape': torch.arange(people*10.).reshape(people, 10)}
                estimator.mhmr_model = detections
                output = estimator(np.zeros((8, 8, 3), dtype=np.uint8))
                self.assertTrue(output.is_full_body)
                np.testing.assert_equal(output.beta, np.arange(10.))

class ImageGridCompatibilityTest(unittest.TestCase):
    def test_irregular_patch_grids(self):
        from pose_compat import install_image_grid_compat
        from core.models.encoders.dinov2.models.vision_transformer import DinoVisionTransformer
        install_image_grid_compat()
        model = DinoVisionTransformer(img_size=518, patch_size=14, embed_dim=12, depth=1, num_heads=3)
        for width, height in ((602, 1022), (518, 518), (504, 840), (336, 1022)):
            with self.subTest(width=width, height=height):
                count = (width // 14) * (height // 14) + 1
                tokens = torch.zeros(1, count, 12)
                output = model.interpolate_pos_encoding(tokens, width, height)
                self.assertEqual(tuple(output.shape), (1, count, 12))

if __name__ == '__main__':
    unittest.main()
