import matplotlib.pyplot as plt
import operator
from pymongo import MongoClient



plt.style.use('ggplot')         # 设置样式

plt.rcParams['font.family'] = ['SimHei']

class Analysis(object):

    def __init__(self, N=5):

        self.MONGO_HOST = '127.0.0.1'
        self.MONGO_PORT = 27017
        self.MONGO_DB = 'Spider'
        self.MONGO_BW_COLL = 'bw_coll'
        self.count = 0
        self.N = N

        self.getdata()
        self.get_Pie_data()
        self.get_Bar_data()
        self.paint()


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


if __name__ == '__main__':
    Analysis(N=6)


