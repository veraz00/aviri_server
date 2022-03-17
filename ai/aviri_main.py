from .aviri_dataset import *
from .get_models import *
from .imagenet_utils import preprocess_input
import time
from torchvision import transforms, datasets
from torch import cuda
from torch.utils.data import DataLoader
import torch.optim as optim
from sklearn import metrics
import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import torch
import glob
import matplotlib.pyplot as plt
import cv2
import torch.nn as nn
import argparse
import pydicom
import imgaug as ia
import torch.nn.functional as F
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
import pickle
from xgboost import XGBClassifier  

import h5py as h5
from keras.models import Model
from keras.optimizers import SGD
from keras.preprocessing import image
from keras import backend as K
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import argparse
import copy
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score, roc_auc_score
from keras import backend as K

models_list = ['VI_CNN']
global_VI_ResNet50 = None
global_heatmap = None
global_feat_model = None

def get_aviri_prediction(img_locations, models_list, force_checking=True, input_tests = None):
    global global_VI_ResNet50
    global global_heatmap
    global global_feat_model
    global global_VI_ResNet50_graph
    global global_heatmap_graph
    global global_feat_model_graph
    global VI
    global VI_Moderate
    
    start = time.time()
    model_fts = []
    predict_results = []


    err_dict = {"err_code": -1,
                "err_message": "unknown error",
                 }
    prefer_GPU = True


    if prefer_GPU:  # not need use GPU here
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    else:
        device = 'cpu'
    
    for i, model_name in enumerate(models_list):

        cp_moderate_filepath = os.path.join(os.path.dirname(__file__), 'model_files', 'moderate_VI_ResNet50_retrain_LowRes_dataset0.dat')
        VI_Moderate = pickle.load(open(cp_moderate_filepath, "rb"))
        cp_filepath = os.path.join(os.path.dirname(__file__), 'model_files', 'VI_ResNet50_retrain_LowRes_dataset7_1st.dat')
        VI =  pickle.load(open(cp_filepath, "rb"))

        cp_heatmap = os.path.join(os.path.dirname(__file__), 'model_files', 'best_model.h5')

        # keras.backend.clear_session()
        print('model_name:', model_name)
        if model_name == 'VI' and global_VI_ResNet50 != VI:
            global_VI_ResNet50 = VI
                
        if model_name == 'VI_Moderate' and global_VI_ResNet50 != VI_Moderate:
            global_VI_ResNet50 = VI_Moderate
        print("Loaded checkpoint '%s'." % cp_filepath)
        global_VI_ResNet50_graph = tf.get_default_graph()
        
            
        
        model_index = 1
        if global_feat_model == None:  
            print('global_feat_model')    
            global_feat_model = get_model(model_index)
            global_feat_model_graph = tf.get_default_graph()
        # else:
        #     global_feat_model_graph = tf.reset_default_graph()
        
        if global_heatmap == None:
            print('global_heatmap')
            global_heatmap = load_model(cp_heatmap)
            global_heatmap_graph = tf.get_default_graph()  
        # else:  
        #     global_feature_model_1_graph = tf.reset_default_graph()   

        model_fts.append(global_VI_ResNet50)  # model_fts is only for resent50 
            
            
    end_time = time.time()
    print('Loading models takes {} seconds' .format(end_time - start))  # Time: 10s 

    if isinstance(img_locations, list):  #  a list of imgs path
        for img_location in img_locations:
            if not os.path.isfile(img_location):
                err_dict["err_code"] = -2
                err_dict["err_message"] = "Image file not found"
                return err_dict
    elif isinstance(img_locations, str):  # str: image path/image folder path
        if os.path.isdir(img_locations):
            img_paths = []
            for img in glob.glob(img_locations + '/*'):
                img_paths.append(os.path.abspath(img))
            img_locations = img_paths
        else:
            img_locations = [os.path.abspath(img_locations)]
    if len(img_locations) > 0:  
        X = loadImageList(img_locations, force_checking=force_checking)  # filename is images (np)
        print("input file number: ", len(X)) 
     
        start_prediction = time.time()
        for num, imgs in enumerate(X):  # imgs is numpy
            img_location = img_locations[num]
            filename = os.path.basename(img_location)  # 111_tyj_Retina_OD_20220124_153145.jpg
            if input_tests:
                im = Image.fromarray(cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB))
                outfile = input_tests + '/{0}_input_test.png'.format(os.path.splitext(filename)[0])
                im.save(outfile)  # save image into outfile
                        
            for i in range(len(models_list)):
                model_name = models_list[i]
                model = model_fts[i]
                if model_name == 'VI' or 'VI_CNN':
                    orig_imgs = imgs.copy()
                    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
                    imgs = cv2.resize(imgs, (224, 224))
                    X_test = [imgs]
                    # get feature
                    with global_feat_model_graph.as_default():
                        feat_test = feat_extract(global_feat_model, X_test, model_index)  # feat_model =  ResNet50(weights='imagenet', include_top=False)
                    with global_VI_ResNet50_graph.as_default():
                        preds = model.predict_proba(feat_test)

                    if preds[0][1] >= 0.0131:  #!!
                        class_val = 1
                    else:
                        class_val = 0
                    print("AI model Softmax output for {0} without any modification: {1}\tclass: {2}".format(img_locations[num], preds, class_val))
            # AI model Softmax output for ./inputs/111_tyj_Retina_OD_20220124_153145.jpg: [[0.98087865 0.01912132]]       class: 1
                    predict_result = get_probability(Y_prob = preds)
                    with global_heatmap_graph.as_default():
                        heatmap_dict = get_heatmap(model = global_heatmap, imgs=orig_imgs, class_val = class_val,\
                        resize = False, filename = filename) 
                    predict_result['heatmap_content'] = heatmap_dict['heatmap_content']  # numpy
                    predict_result['heatmap_name'] = heatmap_dict['heatmap_name']
                else:
                    predict_result['heatmap_content'] = None
                    predict_result['heatmap_name'] = None
                    
                predict_results.append(predict_result)
    # K.clear_session()
    end_prediction = time.time()
    
    print('time for prediction:', end_prediction-start_prediction)  # 1.89 s   
    return predict_results  # a list with a dictionary
    

def get_aviri_AUC(input_obj_list, force_checking=True):
    err_dict = {"err_code": -1,
                "err_message": "unknown error",
                 }

    pred_dict = {"err_code": 0,
                 "auc_macro": 1.0,
                 "auc_micro": 1.0,
                }

    label_test = []
    predict_test = []
    image_num = len(input_obj_list)
    
    try:
        for i in range(0, image_num):
            img_location = input_obj_list[i]["filepath"]

            ret_dict = get_aviri_prediction(img_location, models_list = ['VI_CNN'], force_checking=force_checking, moderate_model=False, input_tests = None)[0]
            if ret_dict["err_code"] == 0:
                cls_probs = [ret_dict["proba_VI0"], ret_dict["proba_VI1"]]
                predict_test.append(cls_probs)
                label_test.append(int(input_obj_list[i]["label"]))
            else:
                err_dict["err_code"] = ret_dict["err_code"]
                err_dict["err_message"] = ret_dict["err_message"]
                return err_dict

        # predict_test = np.concatenate(predict_test)
        predict_test = np.vstack(predict_test)
        # label_test = np.concatenate(label_test)
        label_test = np.vstack(label_test)
        label_test = to_categorical(label_test, predict_test.shape[1])

        try:
            test_auc_macro = roc_auc_score(label_test, predict_test)
            test_auc_micro = roc_auc_score(label_test, predict_test, average='micro')
            pred_dict["err_code"] = 0
            pred_dict["auc_macro"] = test_auc_macro
            pred_dict["auc_micro"] = test_auc_micro
            return pred_dict

        except:
            err_dict["err_code"] = -2
            err_dict["err_message"] = "AUC score cannot be calculated because some class in Ground Truth was missed"
            return err_dict

    except:
        print('get_aviri_AUC exception')
        err_dict["err_code"] = -1
        err_dict["err_message"] = "Exception in get_aviri_AUC API call"
        return err_dict

# --------------------ai function test----------------------------
def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='AVIRI Application')

    parser.add_argument('--input', dest='input_filepath',
                        help='the original images folder to be sorted',
                        default='./inputs', type=str)
    # parser.add_argument('--label', dest='label_file',
    #                     help='the file to label the images',
                        # default=None, type=str)
    parser.add_argument('--output', dest='output_filepath',
                        help='the destination images folder for sorted images',
                        default='./outputs', type=str)
    
    parser.add_argument('--input_test', dest='input_testpath',
                    help='the destination images folder for sorted images',
                    default='./input_test', type=str)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    # if torch.cuda.is_available():
    #     device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
    #     if torch.cuda.device_count()>1:
    #         torch.cuda.set_device(0)
    #         print('torch.torch.cuda.device_count()=', torch.cuda.device_count())
    #         print(torch.cuda.get_device_name(0))

    testdir = args.input_filepath
    if (testdir is not None) and (not os.path.exists(testdir)):
        os.makedirs(testdir)

    input_testdir = args.input_testpath
    if (input_testdir is not None) and (not os.path.exists(input_testdir)):
        os.makedirs(input_testdir)
        
    outputsdir = args.output_filepath
    if (outputsdir is not None) and (not os.path.exists(outputsdir)):
        os.makedirs(outputsdir)
        
    B = open(outputsdir + '/predictions.csv', 'w')
    B.write(
        'err_code, proba_VI0, proba_VI1, proba_others, result, model_name, heatmap_name)\n')
    B.close()
    np.random.seed(1)
    torch.backends.cudnn.deterministic = True
    torch.manual_seed(1)

    # add for API test
    input_paths = glob.glob(testdir + '/*')

    # test API 1-1
    predict_results = get_aviri_prediction(input_paths, models_list = models_list, \
        input_tests = args.input_testpath)
    for ret in predict_results: 
        B = open(outputsdir + '/predictions.csv', 'a')
        B.write('{},{},{},{},{}\n'.format(ret['err_code'], ret['model_name'], ret['proba_VI0'], \
            ret['proba_VI1'], ret['heatmap_name']))
        outfile = outputsdir + '/' + ret['heatmap_name']
        cv2.imwrite(outfile,ret['heatmap_content'])

        
    # test API 1-2
    for file in input_paths[:1]:

        ret = get_aviri_prediction(file, models_list = models_list, input_tests = args.input_testpath)[0]
        outfile = outputsdir + '/' + ret['heatmap_name']
        cv2.imwrite(outfile, ret['heatmap_content'])
        B = open(outputsdir + '/predictions.csv', 'a')
        B.write('{},{},{},{}\n'.format(ret['err_code'], ret['proba_VI0'], ret['proba_VI1'], ret['heatmap_name']))
    
        print('{0} is predicted successfully'.format(file))

    # # test API 2
    test_input_obj_list = []
    label = 0
    tmp_dict = {}
    for file in input_paths:
        tmp_dict["filepath"] = file
        tmp_dict["label"] = label
        test_input_obj_list.append(copy.deepcopy(tmp_dict))
        label = (label + 1) % 2
    ret = get_aviri_AUC(test_input_obj_list)
    print("input: {}; return: {}" .format(test_input_obj_list, ret))

    print("Program is Over!")


