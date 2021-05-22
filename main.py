from window import *
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
