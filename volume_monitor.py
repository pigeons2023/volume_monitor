import ctypes
import datetime
import sys
import subprocess
import time
import signal
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom

def show_notification(title, message):
    # Windows 10+ 的通知
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

class VolumeMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Set the application to be DPI aware
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        # Set the window to be frameless and stay on the bottom
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

        # Set the window title
        self.setWindowTitle("Volume Monitor")

        # Set the window icon
        self.setWindowIcon(QIcon("icon.png"))  # Replace with your own icon file

        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # Replace with your own icon file

        # Create right-click menu
        self.menu = QMenu(self)

        # Add "About" option
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.about_action)

        # Add "Exit" option
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.show_password_dialog)
        self.menu.addAction(self.exit_action)

        # Set the tray menu
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        # Start a timer to check volume
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_adjust_volume)
        self.timer.start(60000)  # Check every 60 seconds

        # Style the menu
        self.menu.setStyleSheet("""
            QMenu { background-color: #f0f0f0; color: black; }
            QMenu::item { padding: 5px 20px; }
            QMenu::item:selected { background-color: #0078d7; color: white; }
        """)

        # Set font
        font = QFont("Arial", 10)
        self.setFont(font)

        # Set palette for better visual appearance
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setPalette(palette)

    def show_password_dialog(self):
        # Start password_input.py script
        process = subprocess.Popen(['pythonw', 'password_input.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()  # Get script output

        #密码：日期+年份+月份
        current_date = datetime.datetime.now()
        date_str = current_date.strftime('%d%Y%m')
        nowpassword = date_str

        password = stdout.decode('utf-8').strip()  # Decode and strip whitespace
        if password == nowpassword:  # Replace with your actual password
            self.exit_application()  # Exit application if correct password
        else:
            show_notification("密码错误", "输入的密码不正确，请重试。")

    def show_about(self):
        # Start about.py script
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
        print(f"Current volume: {current_volume}%")  # Print current volume for debugging

        if current_volume < 100:
            self.set_volume(100)
            print("Volume adjusted to 100%")  # Print volume adjustment info

    def exit_application(self):
        self.tray_icon.hide()  # Hide the tray icon
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = VolumeMonitor()
    sys.exit(app.exec_())
