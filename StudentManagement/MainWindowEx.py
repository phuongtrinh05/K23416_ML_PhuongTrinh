import base64
import traceback
import mysql.connector
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def __init__(self, pixmap=None):
        super().__init__()
        self.default_avatar="images/ic_no_avatar.png"
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None
        self.intro = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.tableWidgetStudent.itemSelectionChanged.connect(self.processItemSelection)
        self.pushButtonAvatar.clicked.connect(self.pickAvatar)
        self.pushButtonRemoveAvatar.clicked.connect(self.removeAvatar)
        self.pushButtonInsert.clicked.connect(self.processInsert)
        self.pushButtonUpdate.clicked.connect(self.processUpdate)
        self.pushButtonRemove.clicked.connect(self.processRemove)
        self.pushButtonNew.clicked.connect(self.clearData)
    #Nếu gen từ file ui sang py thì ảnh sẽ trích xuất đường dẫn từ máy và phải sửa lại đường dẫn ở folder, còn neu vẫn giữ nguyên duong dan đó thì bên file Extend tạo thêm 1 hàm setIcon để đẩy ảnh từ trong folder images
    #     self.setIcons()
    # def setIcons(self):
    #     self.pushButtonNew.setIcon(QIcon("images/ic_new.png"))
    #     self.pushButtonInsert.setIcon(QIcon("images/ic_insert.png"))
    #     self.pushButtonUpdate.setIcon(QIcon("images/ic_update.png"))
    #     self.pushButtonRemove.setIcon(QIcon("images/ic_delete.png"))

    def show(self):
        self.MainWindow.show()

    def connectMySQL(self):
        server = "localhost"
        port = 3306
        database = "student_management"
        username = "root"
        password = "@Obama123"

        mysql.connector.HAVE_CEXT = False
        self.conn = mysql.connector.connect(
            host=server,
            port=port,
            database=database,
            user=username,
            password=password,
            use_pure=True
        )

    def selectAllStudent(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "select * from student"
        cursor.execute(sql)
        dataset = cursor.fetchall()
        self.tableWidgetStudent.setRowCount(0)
        row=0
        for item in dataset:
            row = self.tableWidgetStudent.rowCount()
            self.tableWidgetStudent.insertRow(row)

            self.id = item[0]
            self.code = item[1]
            self.name = item[2]
            self.age = item[3]
            self.avatar = item[4]
            self.intro = item[5]

            self.tableWidgetStudent.setItem(row, 0, QTableWidgetItem(str(self.id)))
            self.tableWidgetStudent.setItem(row, 1, QTableWidgetItem(self.code))
            self.tableWidgetStudent.setItem(row, 2, QTableWidgetItem(self.name))
            self.tableWidgetStudent.setItem(row, 3, QTableWidgetItem(str(self.age)))

        cursor.close()

    def processItemSelection(self):
        row = self.tableWidgetStudent.currentRow()
        if row < 0:
            return

        code = self.tableWidgetStudent.item(row, 1).text()
        cursor = self.conn.cursor(buffered=True)  # <-- quan trọng
        try:
            sql = "SELECT id,code,name,age,avatar,intro FROM student WHERE code=%s"
            cursor.execute(sql, (code,))
            item = cursor.fetchone()
            if not item:
                return

            self.id, self.code, self.name, self.age, self.avatar, self.intro = item
            self.lineEditId.setText(str(self.id))
            self.lineEditCode.setText(self.code or "")
            self.lineEditName.setText(self.name or "")
            self.lineEditAge.setText(str(self.age) if self.age is not None else "")
            self.lineEditIntro.setText(self.intro or "")

            # ---- build pixmap từ DB (cover memoryview/bytes/str base64) ----
            pm = QPixmap()
            if self.avatar:
                data = self.avatar
                if isinstance(data, memoryview):
                    data = data.tobytes()
                if isinstance(data, str):
                    try:
                        data = base64.b64decode(data.encode("ascii"))
                    except Exception:
                        data = b""
                if not pm.loadFromData(data):
                    try:
                        pm.loadFromData(base64.b64decode(data))
                    except Exception:
                        pm = QPixmap("images/ic_no_avatar.png")
            else:
                pm = QPixmap("images/ic_no_avatar.png")

            pm = pm.scaled(
                self.labelAvatar.width(),
                self.labelAvatar.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,  # ép ảnh vừa khung, kệ méo
                Qt.TransformationMode.SmoothTransformation

            )
            self.labelAvatar.setPixmap(pm)
        finally:
            cursor.close()

    def selectAllStudent(self):
        cursor = self.conn.cursor(buffered=True)  # <-- thêm buffered
        try:
            cursor.execute("SELECT * FROM student")
            dataset = cursor.fetchall()
            self.tableWidgetStudent.setRowCount(0)
            for item in dataset:
                row = self.tableWidgetStudent.rowCount()
                self.tableWidgetStudent.insertRow(row)
                self.tableWidgetStudent.setItem(row, 0, QTableWidgetItem(str(item[0])))
                self.tableWidgetStudent.setItem(row, 1, QTableWidgetItem(item[1] or ""))
                self.tableWidgetStudent.setItem(row, 2, QTableWidgetItem(item[2] or ""))
                self.tableWidgetStudent.setItem(row, 3, QTableWidgetItem(str(item[3]) if item[3] is not None else ""))
        finally:
            cursor.close()

    def pickAvatar(self):
        filters = "Images (*.png *.jpg *.jpeg);;All files(*)"
        filename, _ = QFileDialog.getOpenFileName(
            self.MainWindow,
            filter=filters,
        )
        if not filename:
            return

        pixmap = QPixmap(filename)
        # ép ảnh vừa khung, méo cũng kệ
        pixmap = pixmap.scaled(
            self.labelAvatar.width(),
            self.labelAvatar.height(),
            Qt.AspectRatioMode.IgnoreAspectRatio,  # ép vừa khung
            Qt.TransformationMode.SmoothTransformation
        )
        self.labelAvatar.setPixmap(pixmap)
        with open(filename, "rb") as image_file:
            self.avatar = base64.b64encode(image_file.read()).decode("ascii")

    def removeAvatar(self):
        self.avatar = None
        pixmap = QPixmap("images/ic_no_avatar.png")
        pixmap = pixmap.scaled(
            self.labelAvatar.width(),
            self.labelAvatar.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.labelAvatar.setPixmap(pixmap)

    def processInsert(self):
        try:
            cursor = self.conn.cursor()
            # query all students
            sql = "insert into student(Code,Name,Age,Avatar,Intro) values(%s,%s,%s,%s,%s)"

            self.code = self.lineEditCode.text()
            self.name = self.lineEditName.text()
            self.age = int(self.lineEditAge.text())
            if not hasattr(self, 'avatar'):
                avatar = None
            intro = self.lineEditIntro.text()
            val = (self.code, self.name, self.age, self.avatar, self.intro)

            cursor.execute(sql, val)

            self.conn.commit()

            print(cursor.rowcount, " record inserted")
            self.lineEditId.setText(str(cursor.lastrowid))

            cursor.close()
            self.selectAllStudent()
        except:
            traceback.print_exc()

    def processUpdate(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "update student set Code=%s,Name=%s,Age=%s,Avatar=%s,Intro=%s" \
              " where Id=%s"
        self.id=int(self.lineEditId.text())
        self.code = self.lineEditCode.text()
        self.name = self.lineEditName.text()
        self.age = int(self.lineEditAge.text())
        if not hasattr(self, 'avatar'):
            self.avatar = None
        self.intro = self.lineEditIntro.text()

        val = (self.code,self.name,self.age,self.avatar ,self.intro,self.id )

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record updated")
        cursor.close()
        self.selectAllStudent()
    def processRemove(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.No:
            return
        cursor = self.conn.cursor()
        # query all students
        sql = "delete from student "\
              " where Id=%s"

        val = (self.lineEditId.text(),)

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record removed")

        cursor.close()
        self.selectAllStudent()
        self.clearData()
    def clearData(self):
        self.lineEditId.setText("")
        self.lineEditCode.setText("")
        self.lineEditName.setText("")
        self.lineEditAge.setText("")
        self.lineEditIntro.setText("")
        self.avatar=None
