from re import T
from torchvision import transforms
import numpy as np

def nparray2tensor(x, cuda=True):
    normalize = transforms.Compose([
        transforms.Resize(size=256),
        transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    if x.shape[-1] == 1:
        x = np.tile(x, [1, 1, 3])

    # ToTensor() expects [h, w, c], so transpose first
    x2 = normalize(transforms.ToPILImage()(x.copy()))
    return x2


def get_probability(Threshold_VI = [0.03111], Y_prob = [[0.03, 0.97]], models_list = ['VI_CNN']): 
    # for single image
    
    model_num = len(models_list)
    num_class = 2
    y_value = np.zeros((num_class, model_num))
    pred_value = np.zeros(model_num)
    pred_result = dict()
    probability_0 = probability_1 = 0
    num_images = Y_prob.shape[0] // model_num
    for ix in range(num_images):
        # VI_CNN

        y_value = np.zeros(num_class)
        for i in range(model_num):
            y_value[0] += Y_prob[ix*model_num + i][0]
            y_value[1] += Y_prob[ix*model_num + i][1]
        y_value[0] = float(y_value[0] / model_num)  # y_value is the average prediction for one image using all models
        y_value[1] = float(y_value[1] / model_num)

        if y_value[1] >= Threshold_VI[i]:
            class_result = 1
            # probability_1 = 0.5 + ((y_value[1] - Threshold_VI[i]) / y_value[1]) * 0.5
            probability_1 = 0.5 + ((y_value[1] - Threshold_VI[i]) / (1-Threshold_VI[i])) * 0.5
            probability_0 = 1- probability_1
        else:
            class_result = 0
            probability_1 = 0.5 - ((Threshold_VI[i] - y_value[1]) / Threshold_VI[i]) * 0.5
            probability_0 = 1- probability_1

        pred_value[ix] = y_value[1]  # 
    
        pred_result['err_code'] = 0
        pred_result['proba_VI0'] = probability_0
        pred_result['proba_VI1'] = probability_1
        # pred_results["proba_others"] = None
        pred_result['result'] = class_result
        pred_result['model_name'] = 'VI_CNN'
        print("Modified probability under threshold {0}: [{1}, {2}]".format(Threshold_VI[0],  probability_0,probability_1))             
    return pred_result



