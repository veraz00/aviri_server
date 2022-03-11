from torchvision import transforms
import numpy as np
import os 
import sys
import time
import shutil
from .image_check import *
import pydicom

def readImageFile(FilewithPath):
    # we could repeat a few times in case the network file transder is not done
    
    img = None
    fileName = os.path.basename(FilewithPath)  # home/data/sample_01.jpg
    ext_str = os.path.splitext(fileName)[1]  # jpg
    repeat_time = 3

    print("Input Image: ", fileName)  
    cycle_cnt = repeat_time
    while cycle_cnt>0 and img is None:
        # try one more time in case libpng error: Read Error
        try:
            if ext_str == '.dcm' or ext_str == '.dicom' or ext_str == '.DCM' or ext_str == '.DICOM':
                ds = pydicom.read_file(FilewithPath)  # read dicom image
                img = ds.pixel_array  # get image array
                img = np.array(img)
                '''
                When using pixel_array with Pixel Data that has an (0028,0002) Samples per Pixel value of 3 
                then the returned pixel data will be in the color space as given by (0028,0004) Photometric Interpretation 
                (e.g. RGB, YBR_FULL, YBR_FULL_422, etc).
                # Bits Allocated (0028,0100) defines how much space is allocated in the buffer for every sample in bits.
                # 0x0028, 0x0101, 'US', "Bits Stored"
                '''
                #pdb.set_trace()
                #if ds[0x0028, 0x0004].value == 'PALETTE_COLOR':
                #    img = pydicom.pixel_data_handlers.util.apply_color_lut(img, ds)

                if ds[0x0028, 0x0100].value == 16:
                    bit_depth = ds[0x0028, 0x0101].value
                    if bit_depth == 16:
                        img16 = img.astype(np.uint16)
                        img = (img16 / 256).astype(np.uint8)
                    elif bit_depth == 12:
                        img = (img / 16).astype(np.uint8)
                    else:
                        img = (img /(2**(bit_depth-8))).astype(np.uint8)
                elif ds[0x0028, 0x0100].value == 8:
                    img = img.astype(np.uint8)
                else:
                    raise Exception("unknown Bits Allocated value in dicom header")

                img = img.reshape(img.shape[0], img.shape[1], -1)
            else:
                img = cv2.imread(FilewithPath, cv2.IMREAD_COLOR) 
                #img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        except:
            print("read image error, ignore the file")  # it should not be happened

        if img is None:
            cycle_cnt = cycle_cnt - 1
            time.sleep(0.02 * (repeat_time-cycle_cnt))

    if img is not None and img.shape[2] == 1:
        # repeat 3 times to make fake RGB images
        img = np.tile(img, [1, 1, 3]) # make 

    return img

def loadImageList(imglist_filepath, force_checking = True):  # testdir = prj_path + 'images/'
    name_list = []
    X = []

    # Loop through the training and test folders, as well as the 'NORMAL' and 'PNEUMONIA' subfolders
    # and append all images into array X.  Append the classification (0 or 1) into array Y.
    #'''
    imgs = []
    name_list = imglist_filepath
    if force_checking == True:
        name_list = is_imglist(name_list)
    
    for FilewithPath in name_list:
        imgs.append(readImageFile(FilewithPath))
    return imgs # images with np


