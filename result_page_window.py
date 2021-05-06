from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
from file_refresh import *
import qtawesome


class result_window_ui(QtWidgets.QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.add_shadow()

    def init_ui(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setFixedSize(600, 600)

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

        self.base_layout.addWidget(self.main_widget)
        self.setCentralWidget(self.base_widget)

        self.close_btn = QtWidgets.QPushButton(qtawesome.icon('fa.times', color='white'), "")
        self.close_btn.setObjectName('close_btn')
        self.result_pic_label = QtWidgets.QLabel()
        self.result_pic_label.setObjectName('result_pic')
        self.save_button = QtWidgets.QPushButton(qtawesome.icon('fa.arrow-circle-o-down', color='white'), "save")
        self.save_button.setObjectName('save_button')
        self.show_button = QtWidgets.QPushButton(qtawesome.icon('fa.image', color='white'), "show image")
        self.show_button.setObjectName('show_button')
        self.title_label = QtWidgets.QLabel("Evaluating Indicator")
        self.title_label.setObjectName('title_label')
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setObjectName('table_widget')

        self.table_widget.setColumnCount(5)
        self.table_widget.setRowCount(1)
        self.table_widget.setHorizontalHeaderLabels(('MI', 'QAB/F', 'FMI', 'AVG', 'SF'))

        self.table_widget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.table_widget.horizontalHeader().setDefaultSectionSize(105)

        self.main_layout.addWidget(self.close_btn, 0, 6, 1, 1)
        self.main_layout.addWidget(self.result_pic_label, 1, 1, 4, 3)
        self.main_layout.addWidget(self.show_button, 2, 5, 1, 2)
        self.main_layout.addWidget(self.save_button, 3, 5, 1, 2)
        self.main_layout.addWidget(self.title_label, 6, 1, 1, 3)
        self.main_layout.addWidget(self.table_widget, 7, 1, 2, 5)

        self.main_widget.setStyleSheet('''
            QPushButton{border-radius:5px;}
            QLabel#title_label{
                font-size:20px;
                font-weight:600;
                font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
                color:#5CACEE;
            }
            QPushButton#save_button{
                background:#6DDF6D;
                color:white;
                height:40px;
                width:70px;
            }
            QPushButton#save_button:hover{
                background:green;
            }
            QPushButton#show_button{
                background:#FFAEB9;
                color:white;
                height:40px;
                width:70px;
            }
            QPushButton#show_button:hover{
                background:#EE799F;
            }
            QPushButton#close_btn{background:#F76677;}
            QPushButton#close_btn:hover{background:red;}
        ''')

        self.close_btn.setFixedSize(20, 20)

        # 添加事件
        self.close_btn.clicked.connect(self.close)
        self.show_button.clicked.connect(self.show_img)
        self.save_button.clicked.connect(self.save_img)




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


    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(20)  # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.darkGray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中

    def show_img(self):
        path = './Intermediate'
        new_path = new_report(path)
        jpg = QtGui.QPixmap(new_path).scaled(self.result_pic_label.width()-3, self.result_pic_label.height()-3)
        self.result_pic_label.setPixmap(jpg)

    def save_img(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "./",
                                                     "*.jpg, *.png, *.jpeg, *.JPG, *.JPEG, All Files(*)")
        path = './Intermediate'
        new_path = new_report(path)
        img = Image.open(new_path)
        img.save(fileName2, quality=95, subsampling=0)


