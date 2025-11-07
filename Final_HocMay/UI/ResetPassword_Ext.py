import sys
import bcrypt
from PyQt6 import QtWidgets, QtGui, QtCore
from ResetPassword import Ui_ResetPassword
from connectors.connector import Connector  # Dùng lại class kết nối MySQL từ Register


class ResetPasswordWindow(QtWidgets.QMainWindow, Ui_ResetPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Reset Password - Smart Retail")

        # Thiết lập DB
        self.db = Connector(database="data8386")

        # Xoá text cũ, đặt placeholder
        self.lineEditEmail_2.clear()
        self.lineEditEmail_3.clear()
        self.lineEditEmail_2.setPlaceholderText("New Password")
        self.lineEditEmail_3.setPlaceholderText("Confirm New Password")

        # Gán sự kiện cho nút Reset
        self.pushButtonRegister.clicked.connect(self.reset_password)

        # Gán icon “home” để quay lại trang chính (tuỳ chọn)
        self.label_11.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label_11.mousePressEvent = self.go_home

    # =======================================================
    # 1️⃣ Hàm quay về trang chính (nếu bạn có màn hình Login)
    # =======================================================
    def go_home(self, event):
        QtWidgets.QMessageBox.information(self, "Home", "Back to Home (chưa gán chức năng thật).")

    # =======================================================
    # 2️⃣ Hàm kiểm tra và đặt lại mật khẩu
    # =======================================================
    def reset_password(self):
        # Lấy email và mật khẩu mới từ người dùng
        email, ok = QtWidgets.QInputDialog.getText(
            self, "Email Verification", "Enter your registered email:")
        if not ok or not email.strip():
            return

        new_pass = self.lineEditEmail_2.text().strip()
        confirm_pass = self.lineEditEmail_3.text().strip()

        if not all([email, new_pass, confirm_pass]):
            QtWidgets.QMessageBox.warning(self, "Missing Info", "Please fill in all fields!")
            return

        if new_pass != confirm_pass:
            QtWidgets.QMessageBox.warning(self, "Mismatch", "Passwords do not match!")
            return

        try:
            # Kiểm tra email có tồn tại không
            if not self.db.email_exists(email):
                QtWidgets.QMessageBox.warning(self, "Error", "Email not found in database!")
                return

            # Hash mật khẩu mới
            hashed_pwd = bcrypt.hashpw(new_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # Cập nhật vào MySQL
            conn = self.db.connect()
            cursor = conn.cursor()
            sql = "UPDATE customers SET password_hash = %s WHERE email = %s"
            cursor.execute(sql, (hashed_pwd, email))
            conn.commit()
            rows = cursor.rowcount
            conn.close()

            if rows == 1:
                QtWidgets.QMessageBox.information(self, "Success", "Password has been reset successfully!")
                self.lineEditEmail_2.clear()
                self.lineEditEmail_3.clear()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Reset failed. Please try again.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))


# =======================================================
# 3️⃣ Chạy thử độc lập
# =======================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ResetPasswordWindow()
    window.show()
    sys.exit(app.exec())
