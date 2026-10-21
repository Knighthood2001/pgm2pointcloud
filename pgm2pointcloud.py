import yaml, numpy as np
from PIL import Image

# 配置文件
yaml_path = 'maps\\test.yaml'
pgm_path = 'maps\\test.pgm'
result_pcd_path = 'map_cloud.pcd'


with open(yaml_path) as f:
    meta = yaml.safe_load(f)
res = meta['resolution']
origin = meta['origin']                     # [x, y, z]
thresh = meta.get('occupied_thresh', 0.65)

img = np.array(Image.open(pgm_path).convert('L'))
ys, xs = np.nonzero(img <= thresh * 255)    # 只取占据像素

pts = np.stack([
    origin[0] + (xs + 0.5) * res,
    origin[1] + (img.shape[0] - ys - 0.5) * res,   # y 翻转
    np.zeros(len(xs)),
], axis=1)

# 存 PCD（ASCII），供定位节点启动时直接加载
with open(result_pcd_path, 'w') as f:
    f.write(f"# .PCD v0.7 - Point Cloud Data file\nVERSION 0.7\nFIELDS x y z\n"
            f"SIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {len(pts)}\nHEIGHT 1\n"
            f"VIEWPOINT 0 0 0 1 0 0 0\nPOINTS {len(pts)}\nDATA ascii\n")
    for p in pts:
        f.write(f"{p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n")
