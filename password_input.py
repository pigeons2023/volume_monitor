import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

def get_password():
    # 先设置属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用高 DPI 缩放
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # 使用高 DPI 像素图

    app = QApplication(sys.argv)

    # 设置应用程序的名称和图标
    app.setApplicationName("输入密码")  # 应用程序名称中文化
    app.setApplicationVersion("1.0.0")
    app.setWindowIcon(QIcon("icon.png"))  # 确保你有合适的图标文件

    # 美化输入框和按钮
    # 设置样式表
    app.setStyleSheet("""
        QInputDialog {
            font-size: 14px;  /* 输入对话框字体大小 */
            background-color: #f9f9f9;  /* 输入对话框背景颜色 */
            border: 1px solid #ccc;  /* 输入对话框边框 */
            border-radius: 5px;  /* 输入对话框圆角 */
        }
        QLineEdit {
            padding: 10px;  /* 输入框内边距 */
            border: 1px solid #aaa;  /* 输入框边框 */
            border-radius: 5px;  /* 输入框圆角 */
            font-size: 14px;  /* 输入框字体大小 */
        }
        QPushButton {
            font-size: 14px;  /* 按钮字体大小 */
            background-color: #0078d7;  /* 按钮背景颜色 */
            color: white;  /* 按钮字体颜色 */
            border: none;  /* 去掉按钮边框 */
            padding: 8px 16px;  /* 按钮内边距 */
            border-radius: 5px;  /* 按钮圆角 */
        }
        QPushButton:hover {
            background-color: #005a9e;  /* 悬停时按钮背景颜色 */
        }
        QPushButton:pressed {
            background-color: #004080;  /* 按钮按下时背景颜色 */
        }
    """)

    # 使用 QInputDialog 获取密码
    password, ok = QInputDialog.getText(None, '密码', '请输入密码:', QLineEdit.Password)  # 中文化对话框标题和提示

    if ok:
        print(password)  # 将密码输出到标准输出
    else:
        print("")  # 如果点击“取消”，返回空字符串
    sys.exit()

if __name__ == "__main__":
    get_password()  # 执行获取密码的函数