import sys
from setting import Ui_setting
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIntValidator
class Callsetting(QWidget, Ui_setting):
    def __init__(self):
        super(Callsetting, self).__init__()
        self.setupUi(self)
        self.setupUi_extra()

        self.OkButton.clicked.connect(self.okButtonPress)
        self.CancelButton.clicked.connect(self.close)

    def setupUi_extra(self):
        """
        UI额外的设置
        :return:
        """
        # 限定MONGO_PORT的输入范围[1024,49151]
        pIntValidator = QIntValidator()
        pIntValidator.setRange(1024, 49151)
        self.portLine.setValidator(pIntValidator)

    def okButtonPress(self):
        """
        将指定好的数据库名等信息写入db_settings.txt
        :return:
        """
        db_setttings = []
        db_setttings.append('MONGO_HOST:' + self.ipLine.text() + '\n')
        db_setttings.append('MONGO_PORT:' + self.portLine.text() + '\n')
        db_setttings.append('MONGO_DB:' + self.dbLine.text() + '\n')
        db_setttings.append('MONGO_COLL:' + self.collLine.text() + '\n')
        db_setttings.append('MONGO_KS_COLL:ks_coll\n')
        db_setttings.append('MONGO_BW_COLL:bw_coll\n')
        db_setttings.append('MONGO_KS_COLL_:ks_coll_\n')
        db_setttings.append('MONGO_BW_COLL_:bw_coll_\n')
        with open('db_settings.txt', 'w') as f:
            f.writelines(db_setttings)

        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    import qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = Callsetting()
    win.show()
    sys.exit(app.exec_())