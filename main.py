from First_page_window import *
from about_page_window import *
from result_page_window import *
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    first_page_window = MainUi()
    about_window = about_window_ui()
    result_window = result_window_ui()
    first_page_window.about_buttton.clicked.connect(about_window.show)
    first_page_window.button_fuse.clicked.connect(result_window.show)
    first_page_window.show()
    sys.exit(app.exec_())
