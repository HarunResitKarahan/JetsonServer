import json 
import numpy as np
import time
import os
import snap7
import threading
#from datetime import datetime

import cv2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from . import Plc

# PLC = Plc('10.15.221.254', PlcRack=0, PlcSlot=1)
#PLC2 = Plc.Plc('10.15.221.254', PlcRack=0, PlcSlot=1)
#PLC3 = Plc.Plc('10.15.221.254', PlcRack=0, PlcSlot=1)

# threading.Thread(target=PLC.Read_Bit, args=(90, 4, 0, 0.0275), daemon=True).start()
#threading.Thread(target=PLC2.Read_Bit, args=(90, 4, 1, 0.0275), daemon=True).start()

ROIS_PATH = os.path.join(os.getcwd(),'SafetyZone', 'RealTimeDetection', 'rois.json')



def get_rois(file_path):

    with open(file_path, 'r') as j:
        Lines = j.readlines()

    sayac = 0
    res = []
    ClassId = []
    PolyPointList = []
    IsObjectHave = []
    Reverse = []
    for index, line in enumerate(Lines):
        sayac+=1
        if not (sayac == len(Lines) or sayac == 1):
            json_acceptable_string = str(line).replace("'", "\"")

            if json_acceptable_string[-2] == ",":
                json_acceptable_string = json_acceptable_string[: -2]
            ClassId.append(json.loads(json_acceptable_string)["ClassId"])
            IsObjectHave.append(json.loads(json_acceptable_string)["IsObjectHave"])
            Reverse.append(json.loads(json_acceptable_string)["Reverse"])
            res = []
            res.append(json.loads(json_acceptable_string)["PolyPointList"])
            point = []
            for i in res[0]:
                x = i["X"]
                y = i["Y"]
                point.append([x, y])
            PolyPointList.append(point)

    return ClassId, PolyPointList, IsObjectHave, Reverse

ROIS_CLASS_ID, ROIS_POLY_POINT_LIST, IS_OBJECT_HAVE, REVERSE = get_rois(ROIS_PATH)

def draw_polly_and_check_isin(image, boxes, scores, classes):


    # RoiAlign = ProjectConfig.objects.filter(configKeyID_id = 53).values()
    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)
    classes = np.squeeze(classes).astype(np.int32)
    x = image.shape[0]
    y = image.shape[1]
    # TODO Roi sayisina gore total result dondurulecek sekilde revize edilecek.
    draw_isIn = False
    for polly_point in ROIS_POLY_POINT_LIST:
        draw_poly_(image, polly_point)
    polly_is_in = []
    for i in range(min(12, boxes.shape[0])):
        if scores is None or scores[i] > 0.7:
            box = tuple(boxes[i].tolist())
            
            for index, polly_point in enumerate(ROIS_POLY_POINT_LIST):
                if int(classes[i]) == int(ROIS_CLASS_ID[index]):
                    isIn = check_rois(image, polly_point, box, "BottomCenter")
                    if isIn == True:
                        draw_isIn = isIn
                        polly_is_in.append(str(draw_isIn))
                    else:
                        polly_is_in.append(str(draw_isIn))
                        
                    image = draw_poly(image, polly_point, draw_isIn)
     # print(isIn)
    #if isIn != PLC2.bit_value:
    #    if isIn!= None:
    #        PLC3.Set_bit(DB=90, DBX=4, DB_X=1, value=isIn)
    #    else:
    #        pass
    image = show_ok_nok(image, draw_isIn)
    return image
def draw_poly(image, polygon, isIn):
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    if isIn == True:
        # Blue color in BGR
        color = (0, 0, 255)
        # Line thickness of 2 px
        thickness = 2
        image = cv2.polylines(image, [pts], True, color, thickness)
        # image = cv2.putText(image, 'NOK', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)
    else:
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        image = cv2.polylines(image, [pts], True, color, thickness)
        # image = cv2.putText(image, 'OK', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
    return image
def show_ok_nok (image, isIn):
    if isIn == True:
        # Blue color in BGR
        image = cv2.putText(image, 'NOK', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'OK', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
    return image
def draw_poly_(image, polygon):
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    color = (255, 0, 0)
    thickness = 2
    image = cv2.polylines(image, [pts], True, color, thickness)
    return image
    
def check_rois(image, polygon, box, position):
    width = image.shape[0]
    height = image.shape[1]
    x_min = box[0] * width # [x_min, y_min, x_max, y_max]
    y_min = box[1] * height
    x_max = box[2] * width
    y_max = box[3] * height
    if position == 'BottomCenter':
        point = (x_max-((x_max-x_min)/2), y_min)
    if position == 'MiddleCenter':
        point = (x_max-((x_max-x_min)/2), (y_max-(y_max-y_min)/2))

    pointX = Point(point)
    polygon = Polygon(polygon)

    result = (polygon.contains(pointX))
    # print(result)
    # if result == None:
    #     result = False
    return result
