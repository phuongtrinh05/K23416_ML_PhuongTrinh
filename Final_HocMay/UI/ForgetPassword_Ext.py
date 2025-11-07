from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from ForgotPassword import Ui_ForgotPassword
import smtplib, random

# Giả lập database user (có thể thay bằng truy vấn MySQL)
USER_DB = {
    "thuvt@gmail.com": "old_password"
}

# Biến toàn cục để lưu OTP
CURRENT_OTP = None


class ForgotPasswordWindow(QtWidgets.QMainWindow, Ui_ForgotPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Reset Password - Smart Retail")

        # Xóa placeholder mặc định
        self.lineEditEmail.setText("")
        self.lineEditPass.setText("")
        self.lineEditConfirmPass.setText("")
        self.lineEditOTP.setText("")

        # Sự kiện nút Reset
        self.pushButtonRegister.clicked.connect(self.reset_password)

        # Gửi OTP khi người dùng nhập email và nhấn Enter
        self.lineEditEmail.returnPressed.connect(self.send_otp)

    # ===============================
    # 1️⃣ Gửi mã OTP qua Email
    # ===============================
    def send_otp(self):
        global CURRENT_OTP
        email = self.lineEditEmail.text().strip()

        if email not in USER_DB:
            QMessageBox.warning(self, "Warning", "Email không tồn tại trong hệ thống!")
            return

        CURRENT_OTP = str(random.randint(100000, 999999))

        try:
            # Gửi qua SMTP Gmail (bạn có thể thay bằng hệ thống khác)
            sender = "codera8386@gmail.com"
            password = "codera8386!hihi"  # Dùng App Password của Gmail
            message = f"Subject: Smart Retail OTP\n\nMã OTP của bạn là: {CURRENT_OTP}"

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(sender, password)
                smtp.sendmail(sender, email, message)

            QMessageBox.information(self, "OTP Sent", f"Đã gửi OTP đến {email}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gửi OTP thất bại: {e}")

    # ===============================
    # 2️⃣ Reset mật khẩu
    # ===============================
    def reset_password(self):
        global CURRENT_OTP
        email = self.lineEditEmail.text().strip()
        new_pass = self.lineEditPass.text().strip()
        confirm_pass = self.lineEditConfirmPass.text().strip()
        otp = self.lineEditOTP.text().strip()

        # Kiểm tra dữ liệu nhập
        if not all([email, new_pass, confirm_pass, otp]):
            QMessageBox.warning(self, "Warning", "Vui lòng nhập đầy đủ thông tin!")
            return

        if otp != CURRENT_OTP:
            QMessageBox.warning(self, "Warning", "Mã OTP không đúng!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Warning", "Mật khẩu xác nhận không khớp!")
            return

        if email not in USER_DB:
            QMessageBox.warning(self, "Warning", "Email không tồn tại!")
            return

        # Cập nhật mật khẩu
        USER_DB[email] = new_pass
        QMessageBox.information(self, "Success", "Đặt lại mật khẩu thành công!")

        # Reset form
        self.lineEditEmail.clear()
        self.lineEditPass.clear()
        self.lineEditConfirmPass.clear()
        self.lineEditOTP.clear()


# Chạy thử độc lập
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec())
