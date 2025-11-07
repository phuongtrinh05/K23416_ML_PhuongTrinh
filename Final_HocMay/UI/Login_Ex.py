import sys
import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import QtGui, QtCore
from Login import Ui_Login
from Final_HocMay.connector.connector import Connector


class LoginWindow(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Connector(database="data")

        # Lưu thông tin user sau khi login
        self.current_user = None
        self.user_homepage = None

        # Placeholder text
        self.lineEditUserName.clear()
        self.lineEditPassword.clear()
        self.lineEditUserName.setPlaceholderText("UserName")
        self.lineEditPassword.setPlaceholderText("Password")

        # Màu chữ mờ
        style = """
        QLineEdit::placeholder {
            color: rgba(185, 110, 127, 0.6);
        }
        """
        self.lineEditUserName.setStyleSheet(self.lineEditUserName.styleSheet() + style)
        self.lineEditPassword.setStyleSheet(self.lineEditPassword.styleSheet() + style)

        # Nút login
        self.pushButtonLogin.clicked.connect(self.login)

        # Ẩn/hiện mật khẩu bằng icon (label_6)
        self._show_password = False
        self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label_6.installEventFilter(self)
        self.apply_echo_mode()

    # -------- Ẩn / hiện password --------
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if obj is self.label_6:
                self._show_password = not self._show_password
                self.apply_echo_mode()
                return True
        return super().eventFilter(obj, event)

    def apply_echo_mode(self):
        self.lineEditPassword.setEchoMode(
            QLineEdit.EchoMode.Normal if self._show_password else QLineEdit.EchoMode.Password
        )

    # -------- LOGIN --------
    # -------- LOGIN --------
    def login(self):
        username = self.lineEditUserName.text().strip()
        password = self.lineEditPassword.text()

        # ---- KIỂM TRA THIẾU THÔNG TIN ----
        if not username and not password:
            QMessageBox.warning(self, "Error", "Vui lòng nhập username và password!")
            return
        elif not username:
            QMessageBox.warning(self, "Error", "Vui lòng nhập username!")
            return
        elif not password:
            QMessageBox.warning(self, "Error", "Vui lòng nhập password!")
            return

        # ---- NẾU ĐỦ 2 Ô THÌ MỚI KẾT NỐI DB ----
        try:
            conn = self.db.connect()
            cursor = conn.cursor()

            # Lấy thông tin user
            cursor.execute(
                "SELECT UserName, Email, Password FROM customer WHERE UserName = %s",
                (username,)
            )
            row = cursor.fetchone()
            cursor.close()
            self.db.disConnect()

            # row[2] là password đã hash bằng bcrypt
            if row and bcrypt.checkpw(password.encode('utf-8'), row[2].encode('utf-8')):
                self.current_user = {
                    'username': row[0],
                    'email': row[1]
                }
                # LOGIN THÀNH CÔNG → MỞ THẲNG USERHOMEPAGE
                self.open_user_homepage()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Thông tin đăng nhập không hợp lệ! Vui lòng kiểm tra lại."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error:\n{e}")

    def open_user_homepage(self):
        """Mở UserHomePage và đóng Login"""
        try:
            # ĐÚNG với cây thư mục của bạn:
            # Login_Ex.py và UserHomepage_Ex.py cùng nằm trong thư mục
            from UserHomepage_Ex import UserHomepageWindow

            self.user_homepage = UserHomepageWindow(user_data=self.current_user)
            self.user_homepage.show()
            self.close()

        except ImportError:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Error",
                "Không import được UserHomepageWindow.\n"
                "Hãy kiểm tra lại tên file (UserHomepage_Ex.py) và đường dẫn."
            )
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Cannot open UserHomePage:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())