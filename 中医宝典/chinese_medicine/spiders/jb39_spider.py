# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from chinese_medicine.items import ChineseMedicineItem


class Jb39SpiderSpider(CrawlSpider):
    name = 'jb39_spider'
    allowed_domains = ['jb39.com']

    start_urls = ['http://jb39.com/']

    rules = (
        Rule(LinkExtractor(allow=r'jibing/$', deny=r'.*[A-Za-z]+\d+\.htm'), follow=False),
    )

    def parse_detail(self, response):
        '''
        获取疾病信息
        :param response:
        :return:
        '''
        ks_name = response.meta['ks_name']                  # 获取所在科室名
        ks_url = response.meta['ks_url']                    # 获取所在科室url
        sick_url = response.url                             # 获取疾病url
        sick_name = response.xpath('//div[@id="divMain"]/div/h1/text()').extract_first()      # 获取疾病名
        sick_des = response.xpath('//div[@class="spider"]/p').xpath('string(.)').extract_first()         # 描述

        sick_res_href = response.xpath('//div[@id="divMain"]/div/div/div/div[6]/a/@href').extract_first()    # 病因
        sick_res_href = response.urljoin(sick_res_href)
        sick_res = self.parse_(sick_res_href)

        sick_sym_href = response.xpath('//div[@id="divMain"]/div/div/div/div[7]/a/@href').extract_first()    # 症状
        sick_sym_href = response.urljoin(sick_sym_href)
        sick_sym = self.parse_(sick_sym_href)

        sick_dia_href = response.xpath('//div[@id="divMain"]/div/div/div/div[8]/a/@href').extract_first()   # 诊断
        sick_dia_href = response.urljoin(sick_dia_href)
        sick_dia = self.parse_(sick_dia_href)

        sick_com_href = response.xpath('//div[@id="divMain"]/div/div/div/div[9]/a/@href').extract_first()   # 并发症
        sick_com_href = response.urljoin(sick_com_href)
        sick_com = self.parse_(sick_com_href)

        sick_tre_href = response.xpath('//div[@id="divMain"]/div/div/div/div[10]/a/@href').extract_first()   # 治疗
        sick_tre_href = response.urljoin(sick_tre_href)
        sick_tre = self.parse_(sick_tre_href)

        part = response.xpath(".//*[@class='ul-ss-3 jb-xx-bw']").extract_first()
        sick_part = self.process_sick_part(part)                                                            # 部位

        item = ChineseMedicineItem(sick_name=sick_name, sick_url=sick_url, sick_des=sick_des, ks_name=ks_name,
                                   ks_url=ks_url, sick_res=sick_res, sick_sym=sick_sym, sick_dia=sick_dia, sick_com=sick_com,
                                   sick_tre=sick_tre, sick_part=sick_part)

        yield item

    def process_sick_part(self, part):
        '''
        获取该疾病患病部位
        :param part:
        :return:
        '''
        soup = BeautifulSoup(part, 'html.parser')
        lis = soup.find_all("li")
        text = ''
        for li in lis:
            text = text + li.text + ' '
        return text

    def parse_(self, url):
        '''
        提取病因等详情
        :param url:
        :return:
        '''
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        ps = soup.find('div', class_='spider')
        text = ''
        for p in ps.contents:
            text = text + p.text

        return text

    def parse_item(self, response):
        '''
        提取科室疾病
        :param response:
        :return:
        '''
        str_1 = '//*[@id="divMain"]/div/div[2]/ul[1]/li'
        str_2 = '//*[@id="divMain"]/div/div[2]/ul[2]/li'
        length_1 = len(response.xpath(str_1))
        length_2 = len(response.xpath(str_2))
        ks_name = response.meta['ks_name']
        ks_url = response.meta['ks_url']
        #  常见疾病
        for i in range(1, length_1 + 1):

            str_sick_href = str_1 + '[' + str(i) + ']/a/@href'
            href = response.xpath(str_sick_href).extract_first()
            sick_url = response.urljoin(href)

            request = scrapy.Request(url=sick_url, callback=self.parse_detail, dont_filter=True,
                                     meta={"ks_name": ks_name, 'ks_url': ks_url})
            yield request
        # 其他疾病
        if response.xpath(str_2 + '[1]/a/text()').extract_first() != "其他":
            for i in range(1, length_2 + 1):
                str_sick_href = str_2 + '[' + str(i) + ']/a/@href'
                href = response.xpath(str_sick_href).extract_first()
                sick_url = response.urljoin(href)
                request = scrapy.Request(url=sick_url, callback=self.parse_detail,
                                         meta={"ks_name": ks_name, 'ks_url': ks_url})
                yield request
        # 翻页
        next_page = Selector(response).re('<a href="(\S*)">下一页</a>')
        if next_page:
            next_page = response.urljoin(next_page[0])
            request = scrapy.Request(url=next_page, callback=self.parse_item, dont_filter=True,
                                     meta={"ks_name": ks_name, 'ks_url': next_page})
            yield request

    def parse_start_url(self, response):
        '''
        获取全部科室名及对应完整url
        :param response:
        :return:
        '''
        length = len(response.xpath('//*[@id="divMain"]/div/div/ul[1]/li'))     # 统计科室总数
        for i in range(1, length + 1):
            str_ks_href = '//*[@id="divMain"]/div/div/ul[1]/li[' + str(i) + ']/a/@href'     # 科室url
            str_ks_name = '//*[@id="divMain"]/div/div/ul[1]/li[' + str(i) + ']/a/text()'    # 科室名

            href = response.xpath(str_ks_href).extract_first()
            ks_url = response.urljoin(href)          # 链接补全
            ks_name = response.xpath(str_ks_name).extract_first()

            request = scrapy.Request(url=ks_url, callback=self.parse_item, dont_filter=True,
                                     meta={"ks_name": ks_name, 'ks_url': ks_url})
            yield request