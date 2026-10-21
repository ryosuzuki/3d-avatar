"""Process-local upstream pose-estimator fix; shared LHM++ source stays untouched."""
import inspect
import textwrap


def install_pose_compat():
    from engine.pose_estimation.pose_estimator import PoseEstimator
    original = PoseEstimator.__call__
    source = textwrap.dedent(inspect.getsource(original))
    replacements = {
        'target_human["loc"].view(1, 1, -1)': 'target_human["loc"].reshape(1, -1, 2)',
        'target_human["dist"].view(1, 1, -1)': 'target_human["dist"].reshape(1, -1, 1)',
    }
    for old, new in replacements.items():
        if source.count(old) != 1:
            raise RuntimeError('Pose compatibility patch does not match this model revision.')
        source = source.replace(old, new)
    namespace = dict(inspect.unwrap(original).__globals__)
    exec(compile(source, '<classroom-pose-compat>', 'exec'), namespace)
    PoseEstimator.__call__ = namespace['__call__']


def install_image_grid_compat():
    # PyTorch scale-factor rounding can produce one fewer position token at
    # certain image aspect ratios. Request the exact patch-grid dimensions.
    from core.models.encoders.dinov2.models.vision_transformer import DinoVisionTransformer
    original = DinoVisionTransformer.interpolate_pos_encoding
    source = textwrap.dedent(inspect.getsource(original))
    old = 'scale_factor=(sx, sy),'
    if source.count(old) != 1:
        raise RuntimeError('Image-grid compatibility patch does not match this model revision.')
    source = source.replace(old, 'size=(int(w0), int(h0)),')
    namespace = dict(original.__globals__)
    exec(compile(source, '<classroom-image-grid-compat>', 'exec'), namespace)
    DinoVisionTransformer.interpolate_pos_encoding = namespace['interpolate_pos_encoding']
