import sys
import os
import json
import re
from PyQt6 import QtWidgets, QtGui, QtCore

from Login_Ex import LoginWindow
from Register import Ui_Register
from Login import Ui_Login
import bcrypt
from Final_HocMay.connector.connector import Connector


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$") #Kiểm tra email hợp lệ ko


class RegisterWindow(QtWidgets.QMainWindow, Ui_Register):
    def __init__(self, login_window=None):
        super().__init__()
        self.setupUi(self)
        self.db = Connector(database="data")
        self.pushButtonRegister.clicked.connect(self.save_user)
        self._defaults = {self.lineEditUserName: "UserName",self.lineEditEmail: "Email",self.lineEditPass: "Password",
            self.lineEditConfirmPass: "Confirm Password",}
        # xoá text do .ui đặt sẵn, rồi set placeholder
        for le, ph in self._defaults.items():
            le.clear()
            le.setPlaceholderText(ph)
            le.installEventFilter(self)  # để nếu thích thì clear ngay khi focus
        # (tùy chọn) màu placeholder
        for le in self._defaults.keys():
            le.setStyleSheet(le.styleSheet() + "\nQLineEdit::placeholder{color:rgba(185,110,127,0.6);} ")
        self.login_window = login_window
        self.checkBoxTerm.clicked.connect(self.term)
        # Cấu hình toggle mật khẩu
        self._show1 = False
        self._show2 = False
        for lab in (self.labelPassword, self.labelConfirmPassword):
            lab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            lab.installEventFilter(self)
        self.apply_echo_mode()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if obj is self.labelPassword:
                self._show1 = not self._show1
                self.apply_echo_mode()
                return True
            elif obj is self.labelConfirmPassword:
                self._show2 = not self._show2
                self.apply_echo_mode()
                return True
        return super().eventFilter(obj, event)

    def apply_echo_mode(self):
        """Cập nhật hiển thị của mật khẩu"""
        self.lineEditPass.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Normal if self._show1 else QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditConfirmPass.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Normal if self._show2 else QtWidgets.QLineEdit.EchoMode.Password)


    def validate_email(self, email):
        return EMAIL_REGEX.match(email)
    def validate_phone(self, phone):
        return re.fullmatch(r"\d{10}", phone) is not None
    def save_user(self):
        username = self.lineEditUserName.text().strip()
        email = self.lineEditEmail.text().strip()
        pwd = self.lineEditPass.text()
        confirm = self.lineEditConfirmPass.text()
        fields = [username, email, pwd, confirm]
        filled_count = sum(bool(f) for f in fields)

        if filled_count == 0:
            QtWidgets.QMessageBox.warning(self,"Missing Information","Please enter your information!")
            return
        if filled_count == 1:
            QtWidgets.QMessageBox.warning(self,"Incomplete Information","Please fill in all information!")
            return
        if filled_count < 4:
            missing = []
            if not username:
                missing.append("UserName")
            if not email:
                missing.append("Email")
            if not pwd:
                missing.append("Password")
            if not confirm:
                missing.append("Confirm Password")

            # Ghép danh sách còn thiếu thành chuỗi hiển thị
            missing_str = ", ".join(missing)
            QtWidgets.QMessageBox.warning(
                self,
                "Incomplete Information",
                f"Please enter {missing_str}!")
            return

        if not self.validate_email(email):
            QtWidgets.QMessageBox.warning(self,"Invalid Email","Invalid email format!")
            return
        try:
            if self.db.email_exists(email):
                QtWidgets.QMessageBox.warning(self,"Duplicate Email","Email already registered!")
                return
            if pwd != confirm:
                QtWidgets.QMessageBox.warning(self,"Password Mismatch","Password and Confirm Password do not match!")
                return
            # 6. Mã hoá mật khẩu
            hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
            # 7. Lưu xuống MySQL
            rows = self.db.register_customer(username, email, hashed_pwd)


            if rows == 1:
                QtWidgets.QMessageBox.information(
                    self,"Success","Register successfully!")
                self.clear_fields()
                self.back_login()
            else:
                QtWidgets.QMessageBox.warning(self,"Error","Register failed!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Error",f"Database error:\n{e}")
    def clear_fields(self):
        self.lineEditUserName.clear()
        self.lineEditEmail.clear()
        self.lineEditPass.clear()
        self.lineEditConfirmPass.clear()
    def back_login(self):
        if self.login_window:
            self.close()
            self.login_window.show()
        else:
            self.close()
    def term(self):
        msg = (
            "Terms and Conditions:\n\n"
            "1. You agree to comply with all applicable laws.\n"
            "2. Do not use this app for illegal activities.\n"
            "3. We may suspend your account if you break the rules."
        )
        QtWidgets.QMessageBox.information(self, "Terms and Conditions", msg)


# -----------------------------
# Chạy riêng file
# -----------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    register_window = RegisterWindow(login_window=login_window)

    # Thay vì show login, ta show register trước:
    register_window.show()

    sys.exit(app.exec())

