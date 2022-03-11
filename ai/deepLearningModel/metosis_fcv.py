#python scripts
__author__='Du Jiawei'
#Descrption:
from keras.layers.convolutional import (
        Conv2D,
        Conv2DTranspose,
        MaxPooling2D,
        ZeroPadding2D,
        Cropping2D
        )
from keras import backend as K


def FCN(input):
