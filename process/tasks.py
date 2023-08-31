import time
from typing import List

from process import app

import numpy as np
import cv2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.logger import setup_logger

setup_logger()



@app.task
def start_video_processing(video: bytes) -> List[list]:
    cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)

    nparr = np.frombuffer(video, np.uint8)
    video_stream = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    result = []
    for frame in video_stream:
        outputs = predictor(frame)
        instances = outputs['instances']
        scores = instances.scores
        metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
        pred_classes = instances.pred_classes
        class_catalog = metadata.thing_classes
        result.append(class_catalog[pred_classes[0]], scores[0].item())
    
    return result
