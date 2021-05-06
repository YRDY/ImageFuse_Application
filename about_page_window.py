from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome

class about_window_ui(QtWidgets.QMainWindow):
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
        self.setFixedSize(500, 600)

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

        self.closebtn = QtWidgets.QPushButton(qtawesome.icon('fa.times', color='white'), "")
        self.title_label = QtWidgets.QLabel("融合涉及的名词解释")
        self.button_1 = QtWidgets.QPushButton("基于小波变换的融合算法")
        self.button_1.setObjectName('button_method')
        self.button_2 = QtWidgets.QPushButton("基于曲波变换的融合算法")
        self.button_2.setObjectName('button_method')
        self.button_3 = QtWidgets.QPushButton("基于拉普拉斯金字塔变换的融合算法")
        self.button_3.setObjectName('button_method')
        self.button_4 = QtWidgets.QPushButton("基于稀疏表示的融合算法")
        self.button_4.setObjectName('button_method')
        self.button_5 = QtWidgets.QPushButton("基于卷积神经网络的融合算法")
        self.button_5.setObjectName('button_method')
        self.button_6 = QtWidgets.QPushButton("互信息")
        self.button_6.setObjectName('button_evaluatingIndicator')
        self.button_7 = QtWidgets.QPushButton("边缘保持度")
        self.button_7.setObjectName('button_evaluatingIndicator')
        self.button_8 = QtWidgets.QPushButton("功能互信息")
        self.button_8.setObjectName('button_evaluatingIndicator')
        self.button_9 = QtWidgets.QPushButton("平均梯度")
        self.button_9.setObjectName('button_evaluatingIndicator')
        self.button_10 = QtWidgets.QPushButton("空间频率")
        self.button_10.setObjectName('button_evaluatingIndicator')

        self.main_layout.addWidget(self.closebtn, 0, 9, 1, 2)
        self.main_layout.addWidget(self.title_label, 0, 3, 1, 3)
        self.main_layout.addWidget(self.button_1, 1, 1, 1, 4)
        self.main_layout.addWidget(self.button_2, 3, 1, 1, 4)
        self.main_layout.addWidget(self.button_3, 5, 1, 1, 4)
        self.main_layout.addWidget(self.button_4, 7, 1, 1, 4)
        self.main_layout.addWidget(self.button_5, 9, 1, 1, 4)
        self.main_layout.addWidget(self.button_6, 1, 6, 1, 3)
        self.main_layout.addWidget(self.button_7, 3, 6, 1, 3)
        self.main_layout.addWidget(self.button_8, 5, 6, 1, 3)
        self.main_layout.addWidget(self.button_9, 7, 6, 1, 3)
        self.main_layout.addWidget(self.button_10, 9, 6, 1, 3)

        self.main_widget.setStyleSheet('''
            QPushButton{border-radius:5px;}
            QWidget#main_widget{
                border-radius:5px;
                background:white;
            }
            QLabel{
                font-size:20px;
                font-weight:600;
                font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
                color:#5CACEE;
            }
            QPushButton#button_method{
                color:#5CACEE;
                border:1px solid #5CACEE;
                height:50px;
            }
            QPushButton#button_method:hover{
                color:white;
                background:#5CACEE;
            }
            QPushButton#button_evaluatingIndicator{
                color:#FFAEB9;
                border:1px solid #FFAEB9;
                height:50px;
            }
            QPushButton#button_evaluatingIndicator:hover{
                color:white;
                background:#FFAEB9;
            }          
        ''')

        self.closebtn.setFixedSize(30, 30)

        self.closebtn.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        self.closebtn.clicked.connect(self.close)

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




