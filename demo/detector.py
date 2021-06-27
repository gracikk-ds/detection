# install mmcv-full thus we could use CUDA operators
# !pip install mmcv-full

# Install mmdetection
# !rm -rf mmdetection
# !git clone https://github.com/open-mmlab/mmdetection.git
# %cd mmdetection
# !pip install -e .

# !apt-get -q install tree

import mmcv
from mmcv import Config
from mmdet.apis import inference_detector, init_detector, show_result_pyplot
from mmdet.datasets import build_dataset
from mmdet.models import build_detector


class detector:
    def inference_result(self):
        cfg = Config.fromfile('./configs/cfg.py')
        checkpoint = './configs/epoch_20.pth'
        model = init_detector(cfg, checkpoint, device='cpu')

        img = mmcv.imread('./static/uploads/test_pic.png')
        result = inference_detector(model, img)
        model.show_result(img, result, show=False, out_file='./static/uploads/result_img.png', thickness=4)
