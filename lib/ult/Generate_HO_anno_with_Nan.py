from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.insert(0, '/home/chengao/Dataset/v-coco/')

import numpy as np
import json
import vsrl_utils as vu
import pickle
import copy
import ipdb

def bb_IOU(boxA, boxB):

    ixmin = np.maximum(boxA[0], boxB[0])
    iymin = np.maximum(boxA[1], boxB[1])
    ixmax = np.minimum(boxA[2], boxB[2])
    iymax = np.minimum(boxA[3], boxB[3])
    iw = np.maximum(ixmax - ixmin + 1., 0.)
    ih = np.maximum(iymax - iymin + 1., 0.)
    inters = iw * ih

    # union
    uni = ((boxB[2] - boxB[0] + 1.) * (boxB[3] - boxB[1] + 1.) +
           (boxA[2] - boxA[0] + 1.) *
           (boxA[3] - boxA[1] + 1.) - inters)

    overlaps = inters / uni
    return overlaps

with open('/home/chengao/Project/Network/data/action_index.json') as json_data:
    Action_dic = json.load(json_data) 
    
coco = vu.load_coco()
vcoco_all = vu.load_vcoco('vcoco_trainval')
for x in vcoco_all:
    x = vu.attach_gt_boxes(x, coco)
    
classes = [x['action_name'] for x in vcoco_all]
np.random.seed(1)
trainval_GT = []

trainval_GT = []
for i in range(26):

    vcoco          = vcoco_all[i] # all instances in this action
    positive_index = np.where(vcoco['label'] == 1)[0]
    
    
    print(i, vcoco['action_name'], len(positive_index))

    for id in positive_index:
        UnknownFlag = 1
        image_id = vcoco['image_id'][id][0]
       
            
        if len(vcoco['role_name']) == 2:
            action_name = vcoco['action_name'] + '_' + vcoco['role_name'][1]
            human_box   = vcoco['bbox'][id]
            object_box  = vcoco_all[i]['role_bbox'][id][4:]
            
            if all(np.isnan(object_box)):
                tmp = []
                tmp.append(image_id)
                tmp.append([Action_dic[action_name]])
                tmp.append(human_box)
                tmp.append(object_box)
                trainval_GT.append(tmp)
            continue

        if len(vcoco['role_name']) == 3:
            action_name1 = vcoco['action_name'] + '_' + vcoco['role_name'][1]
            action_name2 = vcoco['action_name'] + '_' + vcoco['role_name'][2]
            human_box    = vcoco['bbox'][id]
            object_box1  = vcoco_all[i]['role_bbox'][id][4:8]
            object_box2  = vcoco_all[i]['role_bbox'][id][8:]
            
            if all(np.isnan(object_box1)) or all(np.isnan(object_box2)):
                tmp = []
                tmp.append(image_id)
                tmp.append([Action_dic[action_name1], Action_dic[action_name2]])
                tmp.append(human_box)
                tmp.append(vcoco_all[i]['role_bbox'][id][4:])
                trainval_GT.append(tmp)

             
                    
pickle.dump( trainval_GT, open( "/home/chengao/Project/Network/data/trainval_GT_HO_Nan.pkl", "wb" ) )


H_dict = dict()

for GT in trainval_GT:
    
    image_id = GT[0]


    if image_id not in H_dict:
        
        H_dict[image_id] = [GT]
    else:
        H_dict[image_id].append(GT)


pickle.dump( H_dict, open( "/home/chengao/Project/Network/data/trainval_GT_HO_Nan_dic.pkl", "wb" ) )


