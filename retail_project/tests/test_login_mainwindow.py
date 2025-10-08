from PyQt6.QtWidgets import QApplication, QMainWindow

from retail_project.uis.LoginMainWindowEx import LoginMainWindowEx

app=QApplication([])
login_ui=LoginMainWindowEx()
login_ui.setupUi(QMainWindow())
login_ui.showWindow()
app.exec()