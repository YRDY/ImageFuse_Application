import Image
import numpy as np

def PCA(paths):
    imgs = []
    for name in paths:
        imgs.append(np.array(Image.open(name), 'f'))
    imgsize = imgs[0].size
    # print(imgsize)
    allImg = np.concatenate((imgs[0].reshape(1, imgsize), imgs[1].reshape(1, imgsize)), axis=0)
    covImage = np.cov(allImg)
    D, V = np.linalg.eig(covImage)
    if D[0] > D[1]:
        a = V[:, 0] / V[:, 0].sum()
    else:
        a = V[:, 1] / V[:, 1].sum()
    res = imgs[0]*a[0]+imgs[1]*a[1]
    result = Image.fromarray(np.uint8(res))
    return result



if __name__ == '__main__':
    paths = ['../pic_demo/book/book_1.png', '../pic_demo/book/book_2.png']
    PCA(paths)