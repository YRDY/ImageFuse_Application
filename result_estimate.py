import math
from file_refresh import new_report
import cv2
import numpy as np
from skimage.measure import shannon_entropy
from PIL import Image
import scipy.stats as st

def open_resimg(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def open_imgs(paths):
    img1 = cv2.imread(paths[0])
    img2 = cv2.imread(paths[1])
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return gray1, gray2

def calculate_meanvar(array):

    mean, var = cv2.meanStdDev(array)   # 求图片的均值和标准差
    return mean, var

def calculate_entropy(array):
    tmp = []
    for i in range(256):
        tmp.append(0)
    val = 0
    k = 0
    res = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            val = array[i][j]
            tmp[val] = float(tmp[val] + 1)
            k = float(k + 1)
    for i in range(len(tmp)):
        tmp[i] = float(tmp[i]/k)
    for i in range(len(tmp)):
        if(tmp[i] == 0):
            res = res
        else:
            res = float(res-tmp[i]*(math.log(tmp[i])/math.log(2.0)))
    return res

def average_gradient(img):
    tmp = 0
    rows = img.shape[0]-1
    cols = img.shape[1]-1
    for i in range(rows):
        for j in range(cols):
            dx = img.item(i, j) - img.item(i+1, j)
            dy = img.item(i, j) - img.item(i, j+1)
            ds = math.sqrt((dx*dx + dy*dy) / 2)
            tmp += ds
    imgAvG = tmp / ((rows)*(cols))
    return imgAvG

def ComEntropy(img1, img2):
    width = img1.shape[0]
    hegith = img1.shape[1]
    tmp = np.zeros(img1.shape, dtype=int)
    res = 0
    for i in range(width):
        for j in range(hegith):
            val1 = img1[i][j]
            val2 = img2[i][j]
            tmp[val1][val2] = float(tmp[val1][val2] + 1)
    tmp = tmp / (width * hegith)
    for i in range(width):
        for j in range(hegith):
            if (tmp[i][j] == 0):
                res = res
            else:
                res = res - tmp[i][j] * (math.log(tmp[i][j] / math.log(2.0)))
    return res

def calcualte_MI(img, img1, img2):
    # 分别计算A,C和B,C的MI值，在图像融合中，MI值为二者之和，这里取了平均
    img = np.array(img)
    img1 = np.array(img1)
    img2 = np.array(img2)
    mi1 = shannon_entropy(img1) + shannon_entropy(img) - ComEntropy(img1, img)
    mi2 = shannon_entropy(img2) + shannon_entropy(img) - ComEntropy(img2, img)
    mi = (mi1 + mi2) / 2
    return round(mi, 3)




def calculate_all(path, paths):
    img = open_resimg(path)
    img1, img2 = open_imgs(paths)
    mean, var = calculate_meanvar(img)
    entropy = calculate_entropy(img)
    avg = average_gradient(img)
    MI = calcualte_MI(img, img1, img2)
    mean = str(np.round(mean, 4)).replace('[', '').replace(']', '')
    var = str(np.round(var, 4)).replace('[', '').replace(']', '')
    en = str(np.round(entropy, 4))
    avg = str(np.round(avg, 4))
    MI = str(np.round(MI, 4))
    value_list = []
    value_list.append(mean)
    value_list.append(var)
    value_list.append(en)
    value_list.append(avg)
    value_list.append(MI)
    return value_list


if __name__ == '__main__':
    path = './Intermediate/Wavelet_Transform.jpg'
    paths = ['./pic_demo/book/book_1.png', './pic_demo/book/book_2.png']
    value_list = calculate_all(path, paths)
    print(value_list)

