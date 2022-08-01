import os
import cv2
import numpy as np
import tensorflow as tf
import sys
# from numpy import asarray, isin
# from .log_functions import log_for_plc_bit_change


# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

from tensorflow import ConfigProto
from tensorflow import InteractiveSession

# MODEL_NAME_MASKRCNN = 'mask_rcnn_inception_v2_coco_2018_01_28'
# MODEL_NAME_FASTRCNN = 'faster_rcnn_inception_v2_coco_2018_01_28'
# MODEL_NAME_SSD = 'ssd_inception_v2_coco_2018_01_28' 
# LABEL_MAP = 'mscoco_label_map.pbtxt'
# NUM_CLASSES = 5

class ObjectDetection(object):
    def __init__(self):
        self.labels = []
        with open(os.path.join(os.getcwd(),'SafetyZone', 'RealTimeDetection', 'safetyzone_classes.txt'), 'r') as f:
            for item in f.readlines():
                self.labels.append(item)
        self.config = ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.config.gpu_options.per_process_gpu_memory_fraction = 0.4
        self.session = InteractiveSession(config=self.config)
        self.MODEL_NAME = 'SafetyZone/RealTimeDetection/data'
        self.CWD_PATH = os.getcwd()
        self.PATH_TO_CKPT = os.path.join(self.CWD_PATH,self.MODEL_NAME,'Safetyzone-8380_trt.pb') # ssd_inception_v2_coco_trt spellik_trt

        # # Load the Tensorflow model into memory.
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            self.od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                self.serialized_graph = fid.read()
                self.od_graph_def.ParseFromString(self.serialized_graph)
                tf.import_graph_def(self.od_graph_def, name='')

            self.sess = tf.Session(graph=self.detection_graph)

        # # Define input and output tensors (i.e. data) for the object detection classifier

        # # Input tensor is the image
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # # Output tensors are the detection boxes, scores, and classes
        # # Each box represents a part of the image where a particular object was detected
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # # Each score represents level of confidence for each of the objects.
        # # The score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

        # # Number of objects detected
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


    def object_detection(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_expanded})
        for i in range(int(num[0])):
            if int(scores[0][i]*100) >= 30:
        
                box = boxes[0][i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])        

                image = cv2.rectangle(image, (int(box[1]) , int(box[0])), (int(box[3]), int(box[2])), (255, 0, 0), 2)

                image = cv2.putText(image, str(self.labels[int(classes[0][i] - 1)])[:-1], (int(box[3]) - 50, int(box[2]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 2)
                image = cv2.putText(image, "% " + str(int(scores[0][i]*100)), (int(box[1]) + 5, int(box[0]) + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 2) 

        #return image, boxes, scores, classes, num
        return image, boxes, scores, classes

