from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from Final_HocMay.connector.connector import Connector
from Final_HocMay.Models.PurchaseStatistic import PurchaseStatistic
from ChartHandle import ChartHandle
from MainWindow import Ui_Admin


class MainWindowEx(Ui_Admin):
    def __init__(self):
        self.connector = None
        self.purchaseStatistic = None
        self.chartHandle = ChartHandle()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.setWindowTitle("Holiday Statistic Dashboard")

        # Thiết lập vùng hiển thị biểu đồ
        self.setupPlot()

        # Gán sự kiện nút bấm
        self.pushButton.clicked.connect(self.showTop12HolidayDescriptions)

        # Kết nối database khi mở chương trình
        self.connectDatabase()

    # ==========================================================
    # 🟩 1️⃣ Kết nối Database
    # ==========================================================
    def connectDatabase(self):
        try:
            self.connector = Connector(
                server="localhost",
                port=3306,
                database="data",
                username="root",
                password="thuvt23406@"
            )
            self.connector.connect()
            self.purchaseStatistic = PurchaseStatistic(self.connector)
            print("✅ Database connected successfully!")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Database Error", str(e))

    # ==========================================================
    # 🟩 2️⃣ Cấu hình khu vực biểu đồ
    # ==========================================================
    def setupPlot(self):
        self.figure = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

    # ==========================================================
    # 3️⃣ Nút "12 mô tả ngày lễ phổ biến nhất"
    # ==========================================================
    def showTop12HolidayDescriptions(self):
        if self.purchaseStatistic is None:
            QMessageBox.warning(self.MainWindow, "Warning", "Database is not connected.")
            return

        # Lấy dữ liệu thống kê
        df = self.purchaseStatistic.processHolidayDescription()
        if df is None or df.empty:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Không có dữ liệu để hiển thị.")
            return

        # Hiển thị dữ liệu trong bảng giao diện
        self.showDataIntoTableWidget(df)

        # Hiển thị biểu đồ trực tiếp
        self.chartHandle.visualizeBarChart(
            self.figure,
            self.canvas,
            df,
            columnX="description",
            columnY="count",
            title="Top 12 Most Frequent Holiday Descriptions"
        )

    # ==========================================================
    # 4️⃣ Hiển thị DataFrame lên bảng trong giao diện
    # ==========================================================
    def showDataIntoTableWidget(self, df):
        """Đổ dữ liệu từ DataFrame vào bảng QTableWidget trong UI"""
        # Chuyển sang tab "List of data" (nếu tab 0 đúng là tab đó)
        self.tabWidget.setCurrentIndex(0)

        table = self.tableWidgetListofData

        # Xóa dữ liệu cũ (giữ lại cấu trúc widget)
        table.clear()

        # Chuẩn bị header
        headers = [str(c) for c in df.columns]  # ✅ ép sang chuỗi
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Set số dòng
        table.setRowCount(len(df))

        # Đổ dữ liệu từng ô
        for row_idx in range(len(df)):
            for col_idx, col_name in enumerate(df.columns):
                value = df.iloc[row_idx, col_idx]
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        # Căn chỉnh
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)

        QtWidgets.QApplication.processEvents()


# ==========================================================
# 🔵 5️⃣ Chạy ứng dụng
# ==========================================================
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindowEx()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
