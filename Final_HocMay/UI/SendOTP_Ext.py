import sys
import random
import smtplib
import bcrypt
from PyQt6 import QtWidgets, QtGui, QtCore
from SendOTP import Ui_OTP
from connectors.connector import Connector


class SendOTPWindow(QtWidgets.QMainWindow, Ui_OTP):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Reset Password with OTP")

        # Khởi tạo database connector
        self.db = Connector(database="data8386")

        # Làm sạch placeholder
        self.lineEditEmail.clear()
        self.lineEditEmail.setPlaceholderText("Enter your registered email")

        # Tạo thêm các trường nhập OTP + mật khẩu (nếu chưa có trong .ui thì bạn có thể thêm)
        self.lineEditOTP = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditOTP.setGeometry(QtCore.QRect(590, 380, 401, 41))
        self.lineEditOTP.setStyleSheet("background-color: rgb(250, 244, 236);border: none;border-bottom: 2px solid rgba(104,83,92);color: rgb(185,110,127);padding-bottom: 7px;")
        self.lineEditOTP.setPlaceholderText("Enter OTP")
        self.lineEditOTP.hide()

        self.lineEditNewPass = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditNewPass.setGeometry(QtCore.QRect(590, 450, 401, 41))
        self.lineEditNewPass.setStyleSheet("background-color: rgb(250, 244, 236);border: none;border-bottom: 2px solid rgba(104,83,92);color: rgb(185,110,127);padding-bottom: 7px;")
        self.lineEditNewPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditNewPass.setPlaceholderText("New Password")
        self.lineEditNewPass.hide()

        self.lineEditConfirm = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEditConfirm.setGeometry(QtCore.QRect(590, 520, 401, 41))
        self.lineEditConfirm.setStyleSheet("background-color: rgb(250, 244, 236);border: none;border-bottom: 2px solid rgba(104,83,92);color: rgb(185,110,127);padding-bottom: 7px;")
        self.lineEditConfirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEditConfirm.setPlaceholderText("Confirm Password")
        self.lineEditConfirm.hide()

        # Nút gửi OTP ban đầu
        self.pushButtonRegister_2.setText("Send OTP")
        self.pushButtonRegister_2.clicked.connect(self.handle_button_click)

        # Icon home
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label_7.mousePressEvent = self.go_home

        # Biến lưu OTP tạm
        self.current_otp = None
        self.email = None
        self.otp_sent = False

    # ===========================================================
    # Quay về màn hình chính (tùy chọn)
    # ===========================================================
    def go_home(self, event):
        QtWidgets.QMessageBox.information(self, "Home", "Back to Home (chưa gán chức năng).")

    # ===========================================================
    # Sự kiện nút "Send OTP" / "Reset Password"
    # ===========================================================
    def handle_button_click(self):
        if not self.otp_sent:
            self.send_otp()
        else:
            self.verify_and_reset()

    # ===========================================================
    # 1️⃣ Gửi OTP qua Gmail
    # ===========================================================
    def send_otp(self):
        email = self.lineEditEmail.text().strip()
        if not email:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter your email!")
            return

        # Kiểm tra email có tồn tại trong DB
        if not self.db.email_exists(email):
            QtWidgets.QMessageBox.warning(self, "Error", "Email not found in system!")
            return

        try:
            otp = str(random.randint(100000, 999999))
            self.current_otp = otp
            self.email = email

            sender = "codera8386@gmail.com"
            password = "codera8386@hihi"  # App password Gmail
            subject = "Smart Retail - OTP Reset Password"
            body = f"Mã OTP để đặt lại mật khẩu của bạn là: {otp}\n\nOTP có hiệu lực trong 30 giây."
            message = f"Subject: {subject}\n\n{body}"

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(sender, password)
                smtp.sendmail(sender, email, message)

            QtWidgets.QMessageBox.information(self, "OTP Sent", f"OTP has been sent to {email}")

            # Sau khi gửi OTP thành công → hiển thị các trường nhập OTP và mật khẩu
            self.lineEditOTP.show()
            self.lineEditNewPass.show()
            self.lineEditConfirm.show()
            self.pushButtonRegister_2.setText("Reset Password")
            self.otp_sent = True

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to send OTP:\n{e}")

    # ===========================================================
    # 2️⃣ Xác minh OTP và đổi mật khẩu
    # ===========================================================
    def verify_and_reset(self):
        otp_input = self.lineEditOTP.text().strip()
        new_pass = self.lineEditNewPass.text().strip()
        confirm_pass = self.lineEditConfirm.text().strip()

        if not all([otp_input, new_pass, confirm_pass]):
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fill in all fields!")
            return

        if otp_input != self.current_otp:
            QtWidgets.QMessageBox.warning(self, "Invalid OTP", "Incorrect OTP!")
            return

        if new_pass != confirm_pass:
            QtWidgets.QMessageBox.warning(self, "Mismatch", "Passwords do not match!")
            return

        try:
            hashed_pwd = bcrypt.hashpw(new_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            conn = self.db.connect()
            cursor = conn.cursor()
            sql = "UPDATE customers SET password_hash = %s WHERE email = %s"
            cursor.execute(sql, (hashed_pwd, self.email))
            conn.commit()
            rows = cursor.rowcount
            conn.close()

            if rows == 1:
                QtWidgets.QMessageBox.information(self, "Success", "Password reset successfully!")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to update password.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))


# ===========================================================
# Chạy thử riêng
# ===========================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = SendOTPWindow()
    w.show()
    sys.exit(app.exec())
