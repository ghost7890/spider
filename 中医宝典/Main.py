# coding : utf-8
import sys
import os
import subprocess

from Mongo_deal import Mongo_deal
from start import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QFont
from CallMainWindow import CallMainWindow
from Callsettings import Callsetting
from subprocess import Popen

class Spider_Thread(QThread):

    SignalAppendText = pyqtSignal(str)
    SignalExit = pyqtSignal()

    def __init__(self, command):
        super(Spider_Thread, self).__init__()
        self.command = command
        self.running = 1

    def stop(self):
        self.running = 0

        if hasattr(self, "process"):
            self.process.kill()
            os.system("taskkill /F /IM scrapy.exe")#调用外部命令结束ping.exe
        print("thread stoped")

    def run(self):
        self.process = Popen(self.command, stdout=subprocess.PIPE, shell=True)
        while self.running:
            data = self.process.stdout.readline()
            if not data:
                self.SignalExit.emit()
                break
            else:
                self.SignalAppendText.emit(data.decode())


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    主界面
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 信号与槽连接
        self.startButton.clicked.connect(self.spider_start)
        self.pauseButton.clicked.connect(self.spider_cancel)
        self.menuButton.clicked.connect(self.showmenuUI)
        self.settingButton.clicked.connect(self.showsettingsUI)
        # 初始化爬虫线程
        self.thread = None

        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(10)

    def spider_start(self):
        """
        启动spider
        :return:
        """
        if self.thread:
            return
        self.thread = Spider_Thread('scrapy crawl jb39_spider')
        self.thread.SignalAppendText.connect(
            self.onTextAppend, type=Qt.QueuedConnection)

        self.thread.SignalExit.connect(self.onExit, type=Qt.QueuedConnection)
        self.thread.start()

    def spider_cancel(self):
        """
        取消spider
        :return:
        """
        if self.thread:
            self.thread.stop()

        mongo_deal = Mongo_deal()
        mongo_deal.process_ks_part()
        mongo_deal.process_bw_part()
        self.onTextAppend('--------------------------------------\n数据处理完毕')

    def onTextAppend(self, text):
        """
        将spider的log输出到plaintTextEdit控件
        :param text: 待输出的信息
        :return:
        """
        self.plainTextEdit.appendPlainText(text)


    def onExit(self):
        """
        退出线程
        :return:
        """
        self.thread = None

    def showmenuUI(self):
        """
        显示疾病信息界面
        :return:
        """
        self.menu = CallMainWindow()
        self.menu.show()

    def showsettingsUI(self):
        """
        显示设置界面
        :return:
        """
        self.settings = Callsetting()
        self.settings.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())








