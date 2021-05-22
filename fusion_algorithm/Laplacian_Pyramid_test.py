import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
from fusion_algorithm import Laplacian_Pyramid as stk


def laplacian_pyramid_method(paths):


    EXTENSIONS = set(["bmp", "jpeg", "jpg", "png", "tif", "tiff"])

    image_files = paths
    image_files = [cv2.imread(name) for name in image_files
                   if os.path.splitext(name)[-1][1:].lower() in EXTENSIONS]

    if any([image is None for image in image_files]):
        raise RuntimeError("One or more input files failed to load.")

    stacked = stk.stack_focus(image_files)
    # img = cv2.cvtColor(stacked, cv2.COLOR_BGR2RGB)
    cv2.imwrite('../Intermediate/Laplacian_Pyramid.jpg', stacked)



if __name__ == '__main__':
    paths = ['../pic_demo/clock/clock_1.png', '../pic_demo/clock/clock_2.png']
    laplacian_pyramid_method(paths)

