import torch
import numpy as np
import torchvision 
from .imagenet_utils import preprocess_input
import cv2
import os
from keras import backend as K
from keras.preprocessing import image
from .helper import *


def get_model(index):
    models = ['VGG16', 'ResNet50', 'DenseNet112', 'ResNet101', 'ResNet18', 'ResNet34', 'ResNet50_FCN',
              'ResNet50_Pretrain', 'EfficientNetB0']
    print("get model: {}" .format(models[index]))
    # 0 :vgg, 1:resnet 50 2:densenet
    if index == 0:
        from .deepLearningModel.vgg16 import VGG16
        model = VGG16(weights="imagenet",include_top=False)
        return model
    if index == 1:
        from .deepLearningModel.resnet50 import ResNet50
        model = ResNet50(weights='imagenet', include_top=False)
        return model
    if index == 2:
        from densenet.densenet import DenseNetImageNet121
        #image_dim = (224, 224, 3)
        model = DenseNetImageNet121(weights='imagenet',include_top=False)
        return model

def feat_extract(model, img, index=1):
    if torch.cuda.is_available():
        device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
    if index <= 2:
        img = np.array(img, dtype=np.float32)
        img = preprocess_input(img)
        feat = model.predict(img)
        feat = np.reshape(feat, (feat.shape[0],-1))
    else:
        img_num = img.shape[0]
        img_x = img.transpose(0,3,2,1)
        for i in range(img_num):
            img_tmp = img[i,:,:,:]
            img_tmp = img_tmp.astype(np.uint8)

            # x = img[:, ::-1, :, :]

            img_x[i,:,:,:] = nparray2tensor(img_tmp, True)

        img_x = torch.from_numpy(img_x)
        if torch.cuda.is_available():
            # img_x = img_x.to(device)
            model = model.to(device)

        model.eval()
        batch_size = 16
        feature_test = []
        for i in range(0, img_num, batch_size):
            start_idx = i
            end_idx = i + batch_size
            if end_idx >= img_num:
                end_idx = img_num

            input_img = img_x[start_idx:end_idx, :, :, :]
            input_img = input_img.to(device)
            if index != 7:
                feat, out = model(input_img)
            else:
                # import pdb
                # pdb.set_trace()
                # print(model)
                feat, out = model(input_img)

            feature_test.append(feat.detach().cpu().numpy())

        feat = np.vstack(feature_test)
        # feat = np.reshape(feature_test, (feature_test.shape[0], -1))

    return feat


def get_heatmap(model, imgs, class_val, resize, filename):  
    # imgs is from loadImageList(img_locations, force_checking=force_checking) 
    orig_imgs = imgs.copy()
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    imgs = cv2.resize(imgs, (224, 224))
    x = image.img_to_array(imgs)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # class_val = np.argmax(preds)
    african_elephant_output = model.output[:, class_val]
    last_conv_layer = model.get_layer('block5_conv3')
    grads = K.gradients(african_elephant_output, last_conv_layer.output)[0]
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate([x])
    for i in range(512):
        conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    # plt.matshow(heatmap)
    # plt.show()
    # We use cv2 to load the original image
    if resize == True:
        img = cv2.resize(orig_imgs, (512, 512))
    else:
        img = orig_imgs

    # We resize the heatmap to have the same size as the original image
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    # We convert the heatmap to RGB
    heatmap = np.uint8(255 * heatmap)
    # We apply the heatmap to the original image
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # 0.4 here is a heatmap intensity factor
    superimposed_img = heatmap * 0.4 + img
    # print('heatmap', superimposed_img.shape)

    # final_img = np.concatenate((img, superimposed_img), axis=1)
    # Save the image to disk
    return {'heatmap_content':superimposed_img, 'heatmap_name':os.path.splitext(filename)[0] + '_heatmap.jpg'}



