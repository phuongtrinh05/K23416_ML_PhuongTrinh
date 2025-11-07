import sys
from PyQt6 import QtWidgets
from ResetPassword import Ui_ResetPassword  # ✅ alias đúng

class ForgotPasswordWindow(QtWidgets.QMainWindow, Ui_ResetPassword):  # ✅ kế thừa đúng
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # gọi giao diện

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec())
