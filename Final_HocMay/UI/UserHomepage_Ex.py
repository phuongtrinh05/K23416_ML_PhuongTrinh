import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from UserHomepage import Ui_UserHomepage


class UserHomepageWindow(QMainWindow, Ui_UserHomepage):
    def __init__(self, user_data=None):
        super().__init__()
        self.setupUi(self)
        self.user_data = user_data or {}

        # Hiển thị thông tin user ở tiêu đề cửa sổ
        username = self.user_data.get("username", "User")
        email = self.user_data.get("email", "")
        self.setWindowTitle(f"User Homepage - {username}")

        # Label Logout → gán click event
        self.labelLogout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.labelLogout.mousePressEvent = self.logout_clicked

        # Các nút hiện chưa làm gì
        self.pushButtonApply.clicked.connect(self.show_under_development)

    def show_under_development(self):
        QMessageBox.information(self, "Thông báo", "Tính năng này đang được phát triển!")

    # -------- Xử lý sự kiện logout --------
    def logout_clicked(self, event):
        reply = QMessageBox.question(
            self,
            "Đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất và quay lại trang đăng nhập không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            from Login_Ex import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()


