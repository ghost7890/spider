import traceback, sys, time
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QRect, QThread, pyqtSignal
from MainWindow import Ui_MainWindow
import matplotlib
import qdarkstyle
matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fenxi import Analysis
import matplotlib.pyplot as plt
import operator
from pymongo import MongoClient



plt.style.use('ggplot')         # 设置样式

plt.rcParams['font.family'] = ['SimHei']

class UpdateUI(QThread):
    update = pyqtSignal(list)
    def __init__(self, N):
        super(UpdateUI, self).__init__()
        self.N = N
        pass
    def run(self):
        tmp = []
        data = Analysis(self.N)
        tmp.append(data.get_Bar_data())
        tmp.append(data.get_Pie_data())
        self.update.emit(tmp)


class Analysis(object):

    def __init__(self, N=5):

        self.MONGO_HOST = '127.0.0.1'
        self.MONGO_PORT = 27017
        self.MONGO_DB = 'Spider'
        self.MONGO_BW_COLL = 'bw_coll'

        self.connect()
        self.count = 0
        self.N = N

        self.getdata()

    def connect(self):
        """
        连接数据库
        :return:
        """
        try:
            self.conn = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
            self.db = self.conn[self.MONGO_DB]
            self.bw_coll = self.db[self.MONGO_BW_COLL]
        except Exception:
            print(traceback.format_exc())
            print("Connect Statics Database Fail.")
            sys.exit(1)


    def paint(self):
        plt.axes(aspect=1)
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        ax1.barh(self.Bar_names, self.Bar_values, alpha=0.5)
        ax2 = fig.add_subplot(122)
        ax2.pie(x=self.Pie_values, labels=self.Pie_labels, autopct='%.2f%%', explode=self.Pie_explode, shadow=True)
        # plt.show()

    def getdata(self):
        """
        获取患病最多的前N个部位（list）
        :param N:
        :return:
        """
        conn = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        db = conn[self.MONGO_DB]
        bw_coll = db[self.MONGO_BW_COLL]

        d = {}

        for data in bw_coll.find():
            del (data['_id'])
            # print(data)
            for key, value in data.items():
                name = key
                num = value[-1]
                if name != '全身':
                    d[name] = num
                    self.count += num
        self.data = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    def get_Bar_data(self):
        """
        绘制柱状图
        :param data: 需要分析的数据（list）
        :param N: 需要分析的数据的数量
        :return:
        """
        name_sort = []
        num_sort = []
        for key, value in self.data:
            name_sort.append(key)
            num_sort.append(value)

        self.Bar_names = name_sort[:self.N]
        self.Bar_values = num_sort[:self.N]

        return self.Bar_names, self.Bar_values

    def get_Pie_data(self):
        """
        绘制饼状图
        :param data: 需要分析的数据（list）
        :param N: 需要分析的数据的数量
        :return:
        """
        name_sort = []
        num_sort = []
        for key, value in self.data:
            name_sort.append(key)
            num_sort.append(value)

        extra_count = self.count
        self.Pie_labels = name_sort[:self.N]
        self.Pie_values = num_sort[:self.N]
        self.Pie_explode = [0] * (self.N + 1)
        self.Pie_explode[0] = 0.1

        for value in self.Pie_values:
            extra_count -= value

        self.Pie_labels.append('其他')
        self.Pie_values.append(extra_count)

        return self.Pie_labels, self.Pie_values, self.Pie_explode


class CallMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CallMainWindow, self).__init__()

        self.N = 6

        self.setupUi(self)
        self.getdb_settings()
        self.connect()
        self.set_bw_Tree()
        self.set_ks_Tree()
        # self.loadQSS()
        self.show_analysis()


        # 信号,槽的连接
        self.bwtree.clicked.connect(self.on_bw_TreeClicked)
        self.kstree.clicked.connect(self.on_ks_TreeClicked)
        self.searchButton.clicked.connect(self.search_clicked)
        self.searchLine.editingFinished.connect(self.search_clicked)
        self.numLine.editingFinished.connect(self.numLine_finished)
        self.huizhiButton.clicked.connect(self.huizhi_pressed)
        self.sick_name.textChanged.connect(lambda: self.sick_namelineresize(self.sick_name.text()))

    def numLine_finished(self):
        if self.numLine.text() != '':
            self.N = self.numLine.text()
            print(self.N)

    def show_analysis(self):
        plt.axes(aspect=1)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.clear()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.widget.setLayout(layout)
        # self.widget.setLayout(layout)

        # self.plot()

    def huizhi_pressed(self):
        self.updateUI = UpdateUI(int(self.N))
        self.updateUI.update.connect(self.plot)
        self.updateUI.start()

    def plot(self, data):

        self.figure.clf()
        Bar_labels, Bar_values = data[0]
        Pie_labels, Pie_values, Pie_explode = data[1]

        ax1 = self.figure.add_subplot(121)
        ax1.bar(Bar_labels, Bar_values, width=0.5, alpha=0.5)

        ax2 = self.figure.add_subplot(122)
        ax2.pie(x=Pie_values, labels=Pie_labels, autopct='%.2f%%', explode=Pie_explode, shadow=True)

        self.canvas.draw()

    def loadQSS(self):
        """ 加载QSS """
        file = 'style.qss'
        with open(file, 'rt', encoding='utf8') as f:
            styleSheet = f.read()
        self.setStyleSheet(styleSheet)
        f.close()

    def connect(self):
        """
        连接数据库
        :return:
        """
        try:
            self.conn = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
            self.db = self.conn[self.MONGO_DB]
            self.coll = self.db[self.MONGO_COLL]
            self.ks_coll = self.db[self.MONGO_KS_COLL]
            self.bw_coll = self.db[self.MONGO_BW_COLL]
        except Exception:
            print(traceback.format_exc())
            print("Connect Statics Database Fail.")
            sys.exit(1)

        # 将疾病数在疾病信息窗口显示
        ret = self.coll.find()
        self.Number.display(ret.count())

    def getdb_settings(self):
        """
        从db_settings.txt读取设置好的数据库信息
        :return:
        """
        d = {}      # 临时存储数据库信息的字典
        with open('db_settings.txt', 'rb') as f:
            db_settings = f.read().decode('utf-8').split('\n')

        for line in db_settings:
            if not line.strip():
                continue
            tmp = line.split(':')
            d[tmp[0].strip()] = tmp[1].strip()

        self.MONGO_HOST = d['MONGO_HOST']
        self.MONGO_PORT = int(d['MONGO_PORT'])
        self.MONGO_DB = d['MONGO_DB']
        self.MONGO_COLL = d['MONGO_COLL']
        self.MONGO_KS_COLL = d['MONGO_KS_COLL']
        self.MONGO_BW_COLL = d['MONGO_BW_COLL']

    def set_ks_Tree(self):
        """
        建立科室目录树
        :return:
        """
        self.kstree.setHeaderLabels(['目录'])
        for data in self.ks_coll.find():
            root = QTreeWidgetItem(self.kstree)
            del (data['_id'])
            for key, value in data.items():
                root.setText(0, key)
                for name in value[:-1]:
                    QTreeWidgetItem(root).setText(0, name)
            self.kstree.addTopLevelItem(root)

    def set_bw_Tree(self):
        """
        建立部位目录树
        :return:
        """
        self.bwtree.setHeaderLabel('目录')
        for data in self.bw_coll.find():
            del (data['_id'])
            root = QTreeWidgetItem(self.bwtree)

            for key, value in data.items():
                root.setText(0, key)
                for name in value[:-1]:
                    QTreeWidgetItem(root).setText(0, name)
            self.bwtree.addTopLevelItem(root)

    def on_bw_TreeClicked(self):
        """
        单击部位疾病名触发的槽函数
        :return:
        """
        item = self.bwtree.currentItem()
        for data in self.coll.find():
            if data['sick_name'] == item.text(0):
                self.sick_name.setText(data['sick_name'])
                self.sick_des.setText(data['sick_des'])
                self.sick_sym.setText(data['sick_sym'])
                self.sick_res.setText(data['sick_res'])
                self.sick_tre.setText(data['sick_tre'])
                self.ks_name.setText(data['ks_name'])

    def on_ks_TreeClicked(self):
        """
        单击科室疾病名触发的槽函数
        :return:
        """
        item = self.kstree.currentItem()
        for data in self.coll.find():
            if data['sick_name'] == item.text(0):
                self.sick_name.setText(data['sick_name'])
                self.sick_des.setText(data['sick_des'])
                self.sick_sym.setText(data['sick_sym'])
                self.sick_res.setText(data['sick_res'])
                self.sick_tre.setText(data['sick_tre'])
                self.ks_name.setText(data['ks_name'])

    def search_clicked(self):
        """
        单击搜索按钮触发的槽函数
        :return:
        """
        ks_name = self.searchLine.text()
        flag = True
        if ks_name != '':
            for data in self.coll.find():
                if data['sick_name'] == ks_name:
                    flag = False
                    self.sick_name.setText(data['sick_name'])
                    self.sick_des.setText(data['sick_des'])
                    self.sick_sym.setText(data['sick_sym'])
                    self.sick_res.setText(data['sick_res'])
                    self.sick_tre.setText(data['sick_tre'])
                    self.ks_name.setText(data['ks_name'])

                    #####################设置目录选定#######################
                    root = self.kstree.invisibleRootItem()
                    rchild_num = root.childCount()
                    for i in range(rchild_num):
                        child = root.child(i)
                        if child.text(0) == data['ks_name']:
                            cchild_num = child.childCount()
                            for i in range(cchild_num):
                                grandson = child.child(i)
                                if grandson.text(0) == data['sick_name']:
                                    self.kstree.setCurrentItem(grandson)

            if flag:
                reply = QMessageBox.information(self, "警告", "搜索有误，请重新输入", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
                print(reply)
                self.searchLine.clear()

    def sick_namelineresize(self, sick_name):
        """
        疾病名输出栏自动伸缩
        :param sick_name:
        :return:
        """
        sick_len = len(sick_name)
        self.sick_name.setGeometry(QRect(100, 29, int(25*sick_len), 31))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = CallMainWindow()
    win.show()
    sys.exit(app.exec_())