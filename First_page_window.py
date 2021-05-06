from PyQt5 import QtCore, QtGui, QtWidgets
from Fusion_algorithm.Wavelet_Transform import *
import qtawesome


value = 0

class MainUi(QtWidgets.QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    imgs = []


    def __init__(self):
        super().__init__()
        self.init_ui()
        self.add_shadow()

    def init_ui(self):

        # self.setWindowOpacity(0.93)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setFixedSize(700, 750)

        self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.base_widget.setStyleSheet('''QWidget{  border-radius:7px;background-color:rgb(255, 255, 255);}''')
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QtWidgets.QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.main_widget = QtWidgets.QWidget() # 创建窗口主部件
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QtWidgets.QGridLayout() # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout) # 设置窗口主部件布局为网格布局


        self.top_widget = QtWidgets.QWidget()
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QtWidgets.QGridLayout()
        self.top_widget.setLayout(self.top_layout)

        self.middle_widget = QtWidgets.QWidget()
        self.middle_widget.setObjectName('middle_widget')
        self.middle_layout = QtWidgets.QGridLayout()
        self.middle_widget.setLayout(self.middle_layout)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setObjectName('bottom_widget')
        self.bottom_layout = QtWidgets.QGridLayout()
        self.bottom_widget.setLayout(self.bottom_layout)

        self.base_layout.addWidget(self.main_widget)
        self.main_layout.addWidget(self.top_widget, 0, 0, 3, 10)
        self.main_layout.addWidget(self.middle_widget, 3, 0, 6, 10)
        self.main_layout.addWidget(self.bottom_widget, 9, 0, 3, 10)
        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 设置各个窗口中的部件
        self.title_label_1 = QtWidgets.QLabel("Image Fusion")
        self.title_label_1.setObjectName('title_label_1')
        self.title_label_2 = QtWidgets.QLabel("6 files max per time.")
        self.title_label_2.setObjectName('title_label_2')
        self.about_buttton = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "about")
        self.about_buttton.setObjectName('about_buttton')

        self.new_mini = QtWidgets.QPushButton("")
        self.new_close = QtWidgets.QPushButton("")

        self.main_label = QtWidgets.QLabel("")
        self.main_label.setObjectName('main_label')
        self.button_open = QtWidgets.QPushButton(qtawesome.icon('fa.image', color='white'), "open")
        self.button_open.setObjectName('button_1')
        self.button_fuse = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='white'), "fuse")
        self.button_fuse.setObjectName('button_2')
        self.button_redo = QtWidgets.QPushButton(qtawesome.icon('fa.undo', color='white'), "redo")
        self.button_redo.setObjectName('button_3')
        self.fuse_cb = QtWidgets.QComboBox()

        self.fuse_cb.addItems(['基于小波变换的多聚焦图像融合算法', '基于曲波变换的多聚焦图像融合算法',
                               '基于拉普拉斯金字塔变换的图像融合算法', '基于稀疏表示的多聚焦图像融合算法',
                               '基于卷积神经网络的多聚焦图像融合算法'])
        self.fuse_cb.activated.connect(self.choose_method)

        # 设置部件位置
        self.top_layout.addWidget(self.new_mini, 0, 8, 1, 1)
        self.top_layout.addWidget(self.new_close, 0, 9, 1, 1)
        self.top_layout.addWidget(self.title_label_1, 1, 1, 1, 3)
        self.top_layout.addWidget(self.title_label_2, 2, 1, 1, 4)
        self.top_layout.addWidget(self.about_buttton, 1, 7, 1, 2)
        self.middle_layout.addWidget(self.main_label, 0, 1, 6, 8)
        self.bottom_layout.addWidget(self.button_open, 0, 1, 1, 3)
        self.bottom_layout.addWidget(self.button_fuse, 1, 6, 1, 3)
        self.bottom_layout.addWidget(self.button_redo, 0, 6, 1, 3)
        self.bottom_layout.addWidget(self.fuse_cb, 1, 1, 1, 5)

        # 放置图片标签
        self.pic_label_1 = QtWidgets.QLabel()
        self.pic_label_1.setObjectName('pic_label')
        self.pic_label_2 = QtWidgets.QLabel()
        self.pic_label_2.setObjectName('pic_label')


        self.middle_layout.addWidget(self.pic_label_1, 1, 1, 5, 4)
        self.middle_layout.addWidget(self.pic_label_2, 1, 5, 5, 4)

        self.pic_labels = [self.pic_label_1, self.pic_label_2]


        self.main_widget.setStyleSheet('''
            QPushButton{border-radius:5px;color:white}
            QWidget#main_widget{               
                border-radius:5px;
                background:white;
            }          
        ''')

        self.new_close.setFixedSize(15, 15)
        self.new_mini.setFixedSize(15, 15)
        self.new_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.new_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.top_widget.setStyleSheet('''
            QLabel#title_label_1{
                font-size:30px;
                font-weight:700;
                font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
                color:#5CACEE;
            }
            QLabel#title_label_2{
                font-size:13px;
                color:#5CACEE;
            }
        ''')

        self.middle_widget.setStyleSheet('''
            QLabel#main_label{background:#e5f0ff;border-radius:10px;}
            QLabel#pic_label{background:#e5f0ff;}
        ''')

        self.bottom_widget.setStyleSheet('''
            
        ''')
        self.fuse_cb.setStyleSheet('''
            QComboBox{
                border:1px solid #43CD80;
                border-radius:5px;
                height:30px;
                color:#43CD80;
            }           
        ''')
        self.button_open.setStyleSheet('''
            QPushButton{background:#FFD700;height:30px;}
            QPushButton:hover{background:#CD9B1D;}
        ''')
        self.button_fuse.setStyleSheet('''
            QPushButton{background:#6DDF6D;height:30px;}
            QPushButton:hover{background:green;}
        ''')
        self.button_redo.setStyleSheet('''
            QPushButton{background:#5CACEE;height:30px;}
            QPushButton:hover{background:#1874CD;}
        ''')
        self.about_buttton.setStyleSheet('''
        QPushButton{background:#5CACEE;height:25px;}
        QPushButton:hover{background:#1874CD;}
        ''')


        # 设置背景图
        # window_pale = QtGui.QPalette()
        # window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("pic_demo/pictue.jpeg")))
        # self.setPalette(window_pale)

        # 设置控件透明度
        '''
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.main_label.setGraphicsEffect(op)
        self.main_label.setAutoFillBackground(True)
        '''
        # 添加按钮事件
        self.new_close.clicked.connect(self.closeButtonClick)
        self.new_mini.clicked.connect(self.minButtonClick)
        self.button_open.clicked.connect(lambda: self.open_image(self.pic_labels))
        self.button_redo.clicked.connect(lambda: self.clear_image(self.pic_labels))

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
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
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

        files, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, '打开多个图片', "",
                                                       "*.jpg, *.png, *.jpeg, *.JPG, *.JPEG, All Files(*)")
        print(files)
        self.imgs = files
        for i in range(len(files)):
            jpg = QtGui.QPixmap(files[i]).scaled(pic_labels[i].width()-3, pic_labels[i].height()-3)
            self.pic_labels[i].setPixmap(jpg)

    # 清空界面
    def clear_image(self, pic_labels):
        for i in range(2):
            self.pic_labels[i].setPixmap(QtGui.QPixmap(""))

    # 基于小波变换的图像融合算法
    def Wavelet_Transform_method(self):

        img1 = imgOpen(self.imgs[0])
        img2 = imgOpen(self.imgs[1])
        res = testWave(img1, img2)
        testSave(res)



    # 选择融合方法
    def choose_method(self):
        value = self.fuse_cb.currentIndex()
        if value == 0:
            self.Wavelet_Transform_method()
        elif value == 1:
            print("to be continue")




