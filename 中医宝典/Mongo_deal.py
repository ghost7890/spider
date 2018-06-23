import traceback, sys, re
from pymongo import MongoClient

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017
# MONGO_DB = "tex"
# MONGO_COLL = "Chinese_medicine"
MONGO_KS_COLL = 'ks_coll'
MONGO_BW_COLL = 'bw_coll'
MONGO_KS_COLL_ = 'ks_coll_'
MONGO_BW_COLL_ = 'bw_coll_'

class Mongo_deal(object):

    def __init__(self):
        self.get_dbsettings()
        self.connect()      # 连接数据库

        self.ks_sicks = {}  # 存储科室对应的疾病名
        self.bw_sicks = {}  # 存储部位对应的疾病名
        self.all_ks_names = set()  # 存储全部科室名
        self.all_bw_names = set()  # 存储部位名


    def connect(self):
        """
        连接数据库
        :return:
        """
        try:
            self.conn = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
            self.db = self.conn[self.MONGO_DB]
            self.coll = self.db[self.MONGO_COLL]
            self.ks_coll = self.db[MONGO_KS_COLL]
            self.bw_coll = self.db[MONGO_BW_COLL]
            self.bw_coll_ = self.db[MONGO_BW_COLL_]
            self.ks_coll_ = self.db[MONGO_KS_COLL_]
            print('连接成功')

        except Exception:
            print(traceback.format_exc())
            print("Connect Statics Database Fail.")
            sys.exit(1)

    def get_dbsettings(self):
        """
        从db_settings.txt读取设置好的数据库信息
        :return:
        """
        d = {}
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


    def process_bw_part(self):
        """
        处理部位信息
        :return:
        """
        # 清空以前数据
        if self.bw_coll.find().count() != 0:
            self.bw_coll.remove()

        for data in self.coll.find():
            bw_names = data['sick_part'].split()
            for bw_name in bw_names:
                if bw_name not in self.all_bw_names:
                    self.all_bw_names.add(bw_name)
                    self.bw_sicks[bw_name] = []
                self.bw_sicks[bw_name].append(data['sick_name'])
        # 数据清洗
        if '暂无' in self.bw_sicks.keys():
            del (self.bw_sicks['暂无'])
        if '暂无' in self.bw_sicks.keys():
            del (self.bw_sicks['头'])

        # 将数据插入临时集合
        for key, value in self.bw_sicks.items():
            self.bw_coll_.insert({key: value})

        # 排序
        self._sort_bw_db()

    def process_ks_part(self):
        """
        处理科室信息
        :return:
        """
        # 清空以前数据
        if self.ks_coll.find().count() != 0:
            self.ks_coll.remove()

        for data in self.coll.find():
            ks_name = data['ks_name']
            # print(data['sick_part'])
            if ks_name not in self.all_ks_names:
                self.all_ks_names.add(ks_name)
                self.ks_sicks[ks_name] = []

            self.ks_sicks[ks_name].append(data['sick_name'])

        # 将数据插入临时集合
        for key, value in self.ks_sicks.items():
            self.ks_coll_.insert({key: value})

        # 排序
        self._sort_ks_db()

    def sort_pinyin(self, names):
        """
        按拼音首字母排序
        :param names: 需要排序的列表
        :return: 排好序的列表
        """
        f = open('sort_pinyin.txt', 'rb')
        pinyin = f.read().decode('utf-8').split('\n')
        pinyin_dict = {}
        for line in pinyin:
            if not line.strip():
                continue
            tmp = line.split('\t')
            pinyin_dict[tmp[0].strip()] = re.sub(r'\d*', '', tmp[1].strip())

        names_sort_list = sorted(names, key=lambda x: ''.join('%s' % [pinyin_dict.get(i) for i in x]))

        return names_sort_list

    def _sort_bw_db(self):
        """
        将bw_coll集合排序
        :return:
        """
        for data in self.bw_coll_.find():
            del (data['_id'])
            for key, value in data.items():
                sorted_pinyin = self.sort_pinyin(value)
                sorted_pinyin.append(len(sorted_pinyin))
                self.bw_coll.insert({key: sorted_pinyin})
        # 删除临时用的集合
        self.bw_coll_.drop()

    def _sort_ks_db(self):
        """
        将ks_coll集合排序
        :return:
        """
        for data in self.ks_coll_.find():
            del (data['_id'])
            for key, value in data.items():
                sorted_pinyin = self.sort_pinyin(value)
                sorted_pinyin.append(len(sorted_pinyin))
                self.ks_coll.insert({key: sorted_pinyin})
        self.ks_coll_.drop()

if __name__ == '__main__':
    mongo_deal = Mongo_deal()
    mongo_deal.process_ks_part()
    mongo_deal.process_bw_part()