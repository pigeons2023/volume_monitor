import ctypes
import datetime
import sys
import subprocess
import time
import signal
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom

def show_notification(title, message):
    # Windows 10+ 的通知
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

class VolumeMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # 设置为dpi适配
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

        # 设置标题
        self.setWindowTitle("Volume Monitor")

        # 设置图标
        self.setWindowIcon(QIcon("icon.png"))  # 替换为您自己的图标文件

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # 替换为您自己的图标文件

        # 创建托盘右键菜单
        self.menu = QMenu(self)

        # 添加关于
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.about_action)

        # 添加退出
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.show_password_dialog)
        self.menu.addAction(self.exit_action)

        # 设置托盘菜单
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        # 定时检测音量
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_adjust_volume)
        self.timer.start(60000)  # 60 秒检查一次

        # 设置菜单样式
        self.menu.setStyleSheet("""
            QMenu { background-color: #f0f0f0; color: black; }
            QMenu::item { padding: 5px 20px; }
            QMenu::item:selected { background-color: #0078d7; color: white; }
        """)

        # 设置字体
        font = QFont("Arial", 10)
        self.setFont(font)

        # 设置颜色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setPalette(palette)

    def show_password_dialog(self):
        # 启动 password_input.py 脚本
        process = subprocess.Popen(['pythonw', 'password_input.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()  # 获取脚本输出

        # 密码：小时+日期+年份+月份
        current_date = datetime.datetime.now()
        date_str = current_date.strftime('%H%d%Y%m')
        nowpassword = date_str

        password = stdout.decode('utf-8').strip()  # 解码并去除空白
        if password == nowpassword:
            self.exit_application()  # 如果密码正确则退出应用程序
        else:
            show_notification("密码错误", "输入的密码不正确，请重试。")

    def show_about(self):
        # 启动 about.py 脚本
        subprocess.Popen(['pythonw', 'about.py'])

    def set_volume(self, volume):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, pythoncom.CLSCTX_ALL, None)
        volume_obj = interface.QueryInterface(IAudioEndpointVolume)
        volume_obj.SetMasterVolumeLevelScalar(volume / 100, None)

    def check_and_adjust_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, pythoncom.CLSCTX_ALL, None)
        volume_obj = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = volume_obj.GetMasterVolumeLevelScalar() * 100
        print(f"Current volume: {current_volume}%")  # 打印当前音量

        if current_volume < 100:
            self.set_volume(100)
            print("Volume adjusted to 100%")  # 打印音量调整信息

    def exit_application(self):
        self.tray_icon.hide()  # 隐藏托盘图标
        sys.exit(0)

if __name__ == '__main__':
    # 先设置属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    monitor = VolumeMonitor()
    sys.exit(app.exec_())