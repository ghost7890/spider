# coding:utf-8

"""
汉字转拼音
eg：
输入：中文
输出：zhong wen
"""
import re

class HanzitoPinyin(object):
    """
    将汉字转化成拼音

    """
    def __init__(self):
        super(HanzitoPinyin, self).__init__()
        self.pinyinList = []        # 存储拼音的list
        self.wordsList = []         # 存储汉字的list
        self.pinyin_dict = {}       # 存储拼音的字典
        self.str = ''               # 拼接好的拼音字符串
        self.get_pinyin_dict()

    def _split(self, str):
        """
        将由汉字构成的字符串，切分成单个汉字
        :param text: 汉字字符串
        :return:
        """
        for i in str:
            self.wordsList.append(i)

    def get_pinyin_dict(self):
        """
        获取汉字、拼音对照的字典
        :return:
        """
        with open(r'E:\python3_self_model\pinyin.txt', 'rb') as f:
            pinyin = f.read().decode('utf-8').split('\n')    # pinyin List

        for line in pinyin:
            if not line.strip():
                continue
            tmp = line.split('\t')
            self.pinyin_dict[tmp[0].strip()] = re.sub(r'\d*', '', tmp[1].strip())

    def translation(self, str):
        """
        将汉字字符串转换成拼音
        :param str: 汉字字符串
        :return: 对应的拼音字符串
        """
        self._split(str)

        for word in self.wordsList:
            # print(word)
            self.pinyinList.append(self.pinyin_dict[word])

        if len(self.wordsList) != len(self.pinyinList):
            print('=====================')
            print("ERROR")

        self._join()

        return self.str

    def _join(self):
        """
        将单个字的拼音拼接成字符串
        :return:
        """
        for i in range(len(self.pinyinList)):
            self.str = self.str + self.pinyinList[i] + ' '

if __name__ == '__main__':

    c = HanzitoPinyin()
    str = '漳州'
    print(str)
    str = c.translation(str)
    print(str)