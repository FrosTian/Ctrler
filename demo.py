from PyQt5.QtWidgets import QApplication, QMainWindow
from resource.receive_transmit import Ui_Form

class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    # 重构
    def retranslateUi(self, From):
        From.setWindowTitle("这是例子")
        self.pushButton.setToolTip("这是<b>粗截屏按钮</b>")
        self.pushButton.setText("截屏")

    @staticmethod
    def terminal_rec(self):
        print('jp')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())