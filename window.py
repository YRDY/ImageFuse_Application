from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtWidgets import QFileDialog

from fusion_algorithm.Wavelet_Transform import *
from fusion_algorithm import Laplacian_Pyramid as lp
from file_refresh import new_report
from result_estimate import calculate_all
from fusion_algorithm.PCA import PCA
import qtawesome
import pandas as pd
import Image

value = 0
imgs = []

qmut_1 = QMutex() # 创建线程锁
qmut_2 = QMutex()
qmut_3 = QMutex()
qmut_4 = QMutex()
qmut_5 = QMutex()


class Thread_1(QThread):

    def __int__(self):
        super(Thread_1, self).__init__()

    def run(self):
        qmut_1.lock()
        img1 = cv2.imread(imgs[0])
        img2 = cv2.imread(imgs[1])
        fusion = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        cv2.imwrite('./Intermediate/weight_mean.jpg', fusion)
        qmut_1.unlock()

class Thread_2(QThread):

    def __int__(self):
        super().__init__()

    def run(self):
        qmut_2.lock()
        img1 = cv2.imread(imgs[0])
        img2 = cv2.imread(imgs[1])
        gray_img_1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_img_2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        rows, cols = gray_img_1.shape
        resimg = np.zeros(np.array(gray_img_1).shape, dtype=int)
        for i in range(rows):
            for j in range(cols):
                item1 = gray_img_1.item(i, j)
                item2 = gray_img_2.item(i, j)
                resimg[i, j] = item1 if item1 < item2 else item2
        # print(resimg)
        cv2.imwrite('./Intermediate/grayValue.jpg', resimg)
        qmut_2.unlock()

class Thread_3(QThread):

    def __int__(self):
        super().__init__()

    def run(self):
        qmut_3.lock()
        pca_result = PCA(imgs)
        pca_result.save('./Intermediate/PCA.jpg')
        qmut_3.unlock()


class Thread_4(QThread):

    def __int__(self):
        super().__init__()

    def run(self):
        qmut_4.lock()
        img1 = imgOpen(imgs[0])
        img2 = imgOpen(imgs[1])
        res = testWave(img1, img2)
        cv2.imwrite('./Intermediate/Wavelet_Transform.jpg', res)
        qmut_4.unlock()


class Thread_5(QThread):

    def __int__(self):
        super().__init__()

    def run(self):
        qmut_5.lock()
        image_files = imgs
        image_files = [cv2.imread(name) for name in image_files]
        stacked = lp.stack_focus(image_files)
        cv2.imwrite('./Intermediate/Laplacian_Pyramid.jpg', stacked)
        # print(imgs)
        qmut_5.unlock()




class MainUi(QtWidgets.QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False


    def __init__(self):
        super().__init__()
        self.init_ui()
        self.add_shadow()

    def init_ui(self):

        # self.setWindowOpacity(0.93)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setFixedSize(900, 800)

        self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.base_widget.setStyleSheet('''QWidget{  border-radius:7px;background-color:rgb(255, 255, 255);}''')
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QtWidgets.QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.base_layout.addWidget(self.main_widget)
        self.main_layout.addWidget(self.left_widget, 0, 0, 10, 6)
        self.main_layout.addWidget(self.right_widget, 0, 6, 10, 3)
        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 设置右半部分部件
        self.right_mini = QtWidgets.QPushButton("")
        # self.right_visit = QtWidgets.QPushButton("")
        self.right_close = QtWidgets.QPushButton("")
        # self.blank = QtWidgets.QPushButton()
        '''
        self.blanck_label_1 = QtWidgets.QLabel()
        self.blanck_label_2 = QtWidgets.QLabel()
        self.blanck_label_3 = QtWidgets.QLabel()
        self.blanck_label_4 = QtWidgets.QLabel()
        self.blanck_label_5 = QtWidgets.QLabel()
        '''
        self.open_button = QtWidgets.QPushButton(qtawesome.icon('fa.image', color='white'), "打开图片")
        self.open_button.setObjectName('open_button')
        self.fuse_cb = QtWidgets.QComboBox()
        self.fuse_cb.addItems(['基于加权平均的图像融合算法', '基于灰度值选大小的图像融合算法',
                               '基于PCA的图像融合算法', '基于小波变换的图像融合算法',
                               '基于金字塔变换的图像融合算法'])
        self.fuse_button = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='white'), "融合")
        self.fuse_button.setObjectName('fuse_button')
        self.save_button = QtWidgets.QPushButton(qtawesome.icon('fa.arrow-circle-o-down', color='white'), "保存图片")
        self.save_button.setObjectName('save_button')
        self.export_button = QtWidgets.QPushButton(qtawesome.icon('fa.arrow-circle-o-down', color='white'), "导出结果")
        self.export_button.setObjectName('export_button')
        self.redo_button = QtWidgets.QPushButton(qtawesome.icon('fa.undo', color='white'), "重选图片")
        self.redo_button.setObjectName('redo_button')

        self.main_label = QtWidgets.QLabel("")
        self.main_label.setObjectName('main_label')
        self.pic_label_1 = QtWidgets.QLabel()
        self.pic_label_1.setObjectName('pic_label')
        self.pic_label_2 = QtWidgets.QLabel()
        self.pic_label_2.setObjectName('pic_label')
        self.title_label = QtWidgets.QLabel("融合结果:")
        self.title_label.setObjectName('title_label')
        self.show_label = QtWidgets.QLabel("")
        self.show_label.setObjectName('main_label')
        self.pic_label_result = QtWidgets.QLabel()
        self.pic_label_result.setObjectName('pic_label')
        # self.value_label = QtWidgets.QLabel("评估指标")
        # self.value_label.setObjectName('title_label')

        self.label1 = QtWidgets.QLabel('均值')
        self.label1.setObjectName('label_name')
        self.label2 = QtWidgets.QLabel('标准差')
        self.label2.setObjectName('label_name')
        self.label3 = QtWidgets.QLabel('信息熵')
        self.label3.setObjectName('label_name')
        self.label4 = QtWidgets.QLabel('平均梯度')
        self.label4.setObjectName('label_name')
        self.label5 = QtWidgets.QLabel('互信息')
        self.label5.setObjectName('label_name')

        self.text1 = QtWidgets.QLineEdit()
        self.text1.setObjectName('text_')
        self.text2 = QtWidgets.QLineEdit()
        self.text2.setObjectName('text_')
        self.text3 = QtWidgets.QLineEdit()
        self.text3.setObjectName('text_')
        self.text4 = QtWidgets.QLineEdit()
        self.text4.setObjectName('text_')
        self.text5 = QtWidgets.QLineEdit()
        self.text5.setObjectName('text_')

        self.text_labels = [self.text1, self.text2, self.text3, self.text4, self.text5]
 
        self.fuse_cb.activated.connect(self.choose_method)

        # 设置部件位置
        self.left_layout.addWidget(self.main_label, 0, 0, 3, 6)
        self.left_layout.addWidget(self.pic_label_1, 0, 0, 3, 3)
        self.left_layout.addWidget(self.pic_label_2, 0, 3, 3, 3)
        self.left_layout.addWidget(self.title_label, 3, 0, 1, 3)
        self.left_layout.addWidget(self.show_label, 4, 0, 3, 6)
        self.left_layout.addWidget(self.pic_label_result, 4, 1, 3, 4)
        self.left_layout.addWidget(self.label1, 7, 0, 1, 1)
        self.left_layout.addWidget(self.label2, 7, 4, 1, 1)
        self.left_layout.addWidget(self.label3, 8, 0, 1, 1)
        self.left_layout.addWidget(self.label4, 8, 4, 1, 1)
        self.left_layout.addWidget(self.label5, 9, 0, 1, 1)

        self.left_layout.addWidget(self.text1, 7, 1, 1, 1)
        self.left_layout.addWidget(self.text2, 7, 5, 1, 1)
        self.left_layout.addWidget(self.text3, 8, 1, 1, 1)
        self.left_layout.addWidget(self.text4, 8, 5, 1, 1)
        self.left_layout.addWidget(self.text5, 9, 1, 1, 1)



        self.right_layout.addWidget(self.right_mini, 9, 7, 1, 1)
        self.right_layout.addWidget(self.right_close, 9, 8, 1, 1)
        self.right_layout.addWidget(self.open_button, 0, 6, 1, 3)
        self.right_layout.addWidget(self.fuse_cb, 1, 6, 1, 3)
        self.right_layout.addWidget(self.fuse_button, 2, 6, 1, 3)
        self.right_layout.addWidget(self.save_button, 5, 6, 1, 3)
        self.right_layout.addWidget(self.export_button, 6, 6, 1, 3)
        self.right_layout.addWidget(self.redo_button, 7, 6, 1, 3)


        # 放置图片标签

        self.pic_labels = [self.pic_label_1, self.pic_label_2]

        self.main_widget.setStyleSheet('''
            QPushButton{border-radius:5px;color:white}
            QWidget#main_widget{               
                border-radius:5px;
                background:white;
            }          
        ''')
        self.right_mini.setFixedSize(25, 25)
        self.right_close.setFixedSize(25, 25)
        self.right_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.right_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        self.left_widget.setStyleSheet('''
            QLabel#title_label{
                font-size:25px;
                font-weight:700;
                font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
                color:#5CACEE;
            }
            QLabel#main_label{background:#e5f0ff;border-radius:10px;}
            QLabel#pic_label{background:#e5f0ff;}
            QLabel#label_name{
                font-size:20px;
                color:#5CACEE;   
            }
            QLineEdit#text_{
                background:#C6E2FF;
                font-size:18px;
                height:20px;
            }
        ''')
        self.fuse_cb.setStyleSheet('''
            QComboBox{
                border:1px solid #43CD80;
                border-radius:5px;
                height:30px;
                color:#43CD80;
            }           
        ''')
        self.open_button.setStyleSheet('''
            QPushButton{background:#FFD700;height:30px;}
            QPushButton:hover{background:#CD9B1D;}
        ''')
        self.fuse_button.setStyleSheet('''
            QPushButton{background:#6DDF6D;height:30px;}
            QPushButton:hover{background:green;}
        ''')
        self.save_button.setStyleSheet('''
            QPushButton{background:#6DDF6D;height:30px;}
            QPushButton:hover{background:green;}
        ''')
        self.export_button.setStyleSheet('''
            QPushButton{background:#5CACEE;height:30px;}
            QPushButton:hover{background:#1874CD;}
        ''')
        self.redo_button.setStyleSheet('''
            QPushButton{background:#5CACEE;height:30px;}
            QPushButton:hover{background:#1874CD;}
        ''')


        # 设置背景图
        # window_pale = QtGui.QPalette()
        # window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("pic_demo/pictue.jpeg")))
        # self.setPalette(window_pale)

        # 设置控件透明度

        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(0.5)
        # self.main_label.setGraphicsEffect(op)
        # self.main_label.setAutoFillBackground(True)


        # 添加按钮事件
        self.right_close.clicked.connect(self.closeButtonClick)
        self.right_mini.clicked.connect(self.minButtonClick)
        self.open_button.clicked.connect(lambda: self.open_image(self.pic_labels))
        self.redo_button.clicked.connect(lambda: self.clear_image(self.pic_labels))
        self.fuse_button.clicked.connect(self.show_result)
        self.save_button.clicked.connect(self.save_pic)
        self.export_button.clicked.connect(self.export_value)



    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(20)  # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.darkGray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中

    # 关闭和最小化
    def closeButtonClick(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()

    def minButtonClick(self):
        self.showMinimized()

    # 移动窗口
    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # 打开图片
    def open_image(self, pic_labels):
        global imgs
        files, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, '打开多个图片', "",
                                                                 "*.jpg, *.png, *.jpeg, *.JPG, *.JPEG, All Files(*)")
        imgs = files
        # print(imgs)
        for i in range(len(files)):
            jpg = QtGui.QPixmap(files[i]).scaled(pic_labels[i].width() - 3, pic_labels[i].height() - 3)
            self.pic_labels[i].setPixmap(jpg)

    def show_result(self):
        path = './Intermediate'
        new_path = new_report(path)
        jpg = QtGui.QPixmap(new_path).scaled(self.pic_label_result.width() - 3, self.pic_label_result.height() - 3)
        self.pic_label_result.setPixmap(jpg)
        value_list = calculate_all(new_path, imgs)
        for i in range(5):
            self.text_labels[i].setText(value_list[i])

    def save_pic(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "./",
                                                     "*.jpg, *.png, *.jpeg, *.JPG, *.JPEG, All Files(*)")
        path = './Intermediate'
        new_path = new_report(path)
        img = Image.open(new_path)
        img.save(fileName2, quality=95, subsampling=0)

    def export_value(self):
        value_list = []
        for i in range(len(self.text_labels)):
            value_list.append(self.text_labels[i].text())
        dct = {'均值': value_list[0],
               '标准差': value_list[1],
               '信息熵': value_list[2],
               '平均梯度': value_list[3],
               '互信息': value_list[4]}
        df = pd.DataFrame(dct, index=[0])
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "./",
                                                     "All Files (*);;Csv Files (*.csv)")
        df.to_csv(fileName2, sep=',')

    # 清空界面
    def clear_image(self, pic_labels):
        for i in range(2):
            self.pic_labels[i].setPixmap(QtGui.QPixmap(""))
        self.pic_label_result.setPixmap(QtGui.QPixmap(""))
        for i in range(5):
            self.text_labels[i].setText("")

    # 基于平均法的图像融合算法
    def Weighted_mean(self):
        self.thread_1 = Thread_1()  # 创建线程
        self.thread_1.start()

    # 基于灰度值判断的图像融合算法
    def choose_gray_value(self):
        # deal_gray_value(self.imgs)
        self.thread_2 = Thread_2()
        self.thread_2.start()

    def pca_method(self):
        self.thread_3 = Thread_3()
        self.thread_3.start()

    # 基于小波变换的图像融合算法
    def Wavelet_Transform_method(self):
        self.thread_4 = Thread_4()
        self.thread_4.start()

    # 基于拉普拉斯金字塔变换的图像融合算法
    def Laplacian_Pyramid_method(self):
        self.thread_5 = Thread_5()
        self.thread_5.start()
        # laplacian_pyramid_method(imgs)



    # 选择融合方法
    def choose_method(self):
        value = self.fuse_cb.currentIndex()
        if value == 0:
            self.Weighted_mean()
        elif value == 1:
            self.choose_gray_value()
        elif value == 2:
            self.pca_method()
        elif value == 3:
            self.Wavelet_Transform_method()
        elif value == 4:
            self.Laplacian_Pyramid_method()










