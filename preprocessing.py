import os
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt

root = '../data'
img_folder = os.path.join(root, 'image')
processed_folder = os.path.join(root, 'processed')

def preprocessing():
    for img_file in glob.glob(os.path.join(img_folder, '*.png')):
        img = cv2.imread(img_file)
        denoise_img = cv2.fastNlMeansDenoisingColored(img, None, 28, 28, 7, 21)
        cropped_img = denoise_img[6:21, 8:, :]
        gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)
        processed_img_file = os.path.join(processed_folder, 'processed_' + img_file.split('_')[1].split('.')[0] + '.jpg')
        cv2.imwrite(processed_img_file, thresh)

if __name__ == '__main__':
    preprocessing()