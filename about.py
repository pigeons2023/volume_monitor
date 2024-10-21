import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

def show_about():
    # 先设置属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText("音量监控器\n\n此应用程序用于监控和设置系统音量。\n\n开发者：pigeons2023\n\n版本号：测试版0.5.1")
    msg_box.setWindowTitle("关于")

    # 设置窗口图标
    msg_box.setWindowIcon(QIcon("icon.png"))  # 替换为你图标的路径

    msg_box.setStandardButtons(QMessageBox.Ok)

    # 美化消息框
    msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;  /* 背景颜色 */
                border: 2px solid #ccc;  /* 边框颜色 */
                border-radius: 10px;  /* 圆角 */
            }
            QLabel {
                font-size: 14px;  /* 字体大小 */
                color: #333;  /* 字体颜色 */
            }
            QPushButton {
                font-size: 14px;  /* 按钮字体大小 */
                background-color: #0078d7;  /* 按钮背景颜色 */
                color: white;  /* 按钮字体颜色 */
                border: none;  /* 去掉边框 */
                padding: 8px 16px;  /* 按钮内边距 */
                border-radius: 5px;  /* 圆角 */
            }
            QPushButton:hover {
                background-color: #005a9e;  /* 悬停时按钮背景颜色 */
            }
        """)

    msg_box.exec_()

if __name__ == '__main__':
    show_about()