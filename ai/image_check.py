import os 
import numpy as np
import cv2
from skimage.exposure import is_low_contrast

def images_extension_valid(imglist):  # absolute path lists
    def is_img(ext):

        # print(ext)
        ext = ext.lower()
        if ext == '.jpg' or ext == '.JPG':
            return True
        elif ext == '.png' or ext == '.PNG':
            return True
        elif ext == '.jpeg' or ext == '.JPEG':
            return True
        elif ext == '.bmp' or ext == '.BMP':
            return True
        elif ext == '.tif' or ext == '.TIF':
            return True
        elif ext == '.tiff' or ext == '.TIFF':
            return True
        # elif ext == '.dcm' or ext == '.dicom' or ext == '.DCM' or ext == '.DICOM':
        #     return True
        else:
            return False

    for img in imglist:
        imgname = os.path.basename(img)
        _, ext = os.path.splitext(imgname)
        if not is_img(ext):
            imglist.remove(img)
    return imglist
            


def images_size_valid(imglist, min_kB=50, max_kB=18432):
    def get_FileSize(filePath):
        fsize = os.path.getsize(filePath)  # bytes
        fsize = fsize / float(1024)
        return round(fsize, 2)

    for img in imglist:
        fsize = get_FileSize(img)
        print('image size bits', fsize)
        if fsize<min_kB or fsize>max_kB:
            imglist.remove(img)

    return imglist


def images_resolution_valid(imglist, min_wh=200, max_wh=6000):
    for img in imglist:
        img_data = cv2.imread(img)
        h, w, c = img_data.shape
        if not (h >= min_wh and h <= max_wh and w >= min_wh and w <= max_wh):
            imglist.remove(img)
    return imglist

# add for image quality checking
def isgray(imgpath):
    img = cv2.imread(imgpath)
    if len(img.shape) < 3:
        return True
    if img.shape[2] < 3:
        return True
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    if (b == g).all() and (b == r).all():
        return True
    return False


def images_quality_valid(imglist):
    valid = False
    # check the brightness, black and white, image channel first
    for img in imglist:
        if isgray(img):
            imglist.remove(img)
            continue
        img_data = cv2.imread(img)
        h, w, c = img_data.shape
        start_h = int(h//3)
        end_h = int(h // 3 * 2)
        start_w = int(w // 3)
        end_w = int(w // 3 * 2)
        crop_img = img_data[start_h:end_h, start_w:end_w, :]
        mean_grey_value = np.average(crop_img)
        if not(mean_grey_value > 20 and mean_grey_value < 230):
            imglist.remove(img)
            continue

        # check the contrast
        # start_h = int(h // 3)
        # end_h = int(h // 3 * 2)
        # start_w = int(w // 3)
        # end_w = int(w // 3 * 2)
        # crop_img = img_data[start_h:end_h, start_w:end_w, :]
        if is_low_contrast(crop_img, fraction_threshold=0.05, lower_percentile=5, upper_percentile=95):
            imglist.remove(img)

    return imglist

def is_imglist(imglist, force_checking = True):
    err_dict = {}
    origin_len = len(imglist)
    
    imglist = images_extension_valid(imglist)
    if len(imglist) < origin_len:
        err_dict["err_code"] = -3
        err_dict["err_message"] = "Invalid image type"
        print(err_dict)
        origin_len = len(imglist)
        return err_dict

    imglist = images_resolution_valid(imglist, min_wh=200, max_wh=6000)
    if len(imglist) < origin_len:
        err_dict["err_code"] = -5
        err_dict["err_message"] = "Image resolution out of range (200x200 - 6000x6000)"
        print(err_dict)
        origin_len = len(imglist)

        return err_dict

    imglist = images_size_valid(imglist)  # 200*200 - 6000*6000
    if len(imglist) < origin_len:
        err_dict["err_code"] = -4
        err_dict["err_message"] = "Image size out of range (50KB - 18MB)"
        print(err_dict)
        origin_len = len(imglist)  
        return err_dict


    # imglist = images_quality_valid(imglist)
    # if len(imglist) < origin_len:
    #     err_dict["err_code"] = -6
    #     err_dict["err_message"] = "Image brightness, color or contrast unqualified"
    #     print(err_dict)
    #     return err_dict
    
    if len(imglist) > 0:
        return imglist
    else:
        err_dict["err_code"] = -2
        err_dict["err_message"] = "No image available"
        return err_dict

