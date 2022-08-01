from PIL import Image
import sys
import os
import urllib
from tensorflow.python.compiler.tensorrt import trt_convert as trt

import cv2
import tensorflow as tf
import numpy as np

from tf_trt_models.detection import download_detection_model, build_detection_graph

# 'exec(%matplotlib inline)'

MODEL = 'inference_graph_SafetyZone-8380'
DATA_DIR = './data/'
CONFIG_FILE = 'pipeline.config'   # ./data/ssd_inception_v2_coco.config 
CHECKPOINT_FILE = 'model.ckpt'    # ./data/ssd_inception_v2_coco/model.ckpt

config_path = os.path.join(os.getcwd(), DATA_DIR, MODEL, CONFIG_FILE)
checkpoint_path = os.path.join(os.getcwd(), DATA_DIR, MODEL, CHECKPOINT_FILE)
# config_path, checkpoint_path = download_detection_model(MODEL, 'data')

# print(config_path) "data/ssd_mobilenet_v1_coco_2018_01_28/pipeline.config"
# print(checkpoint_path) "data/ssd_mobilenet_v1_coco_2018_01_28/model.ckpt"


frozen_graph, input_names, output_names = build_detection_graph(
    config=config_path,
    checkpoint=checkpoint_path,
    force_nms_cpu=False,
    score_threshold=0.25,
    batch_size=1
)

print(output_names)
#print(frozen_graph)
#print(input_names)

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

with open('./data/Safetyzone-8380_trt.pb', 'wb') as f:
    f.write(trt_graph.SerializeToString())


