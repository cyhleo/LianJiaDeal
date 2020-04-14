# -*- coding: utf-8 -*-
import scrapy
from LianjiaDeal.items import LianjiadealItem
import re

class DealLianjiaSpider(scrapy.Spider):
    name = 'deal_lianjia'
    allowed_domains = ['lianjia.com']
    base_urls = 'https://xm.lianjia.com/chengjiao/{}/pg{}'
    def start_requests(self):
        region_dict = {'siming':'思明', 'huli':'湖里', 'haicang':'海沧', 'jimei':'集美', 'xiangan':'翔安', 'tongan':'同安'}
        for region,region_name in region_dict.items():
            yield scrapy.Request(self.base_urls.format(region,1),meta={'region':region,'page':1,'region_name':region_name},dont_filter=True)

    def parse(self, response):
        if response and response.url:
            region = response.meta.get('region')
            region_name = response.meta.get('region_name')
            page = response.meta.get('page')
            list_selector = response.xpath(".//ul[@class='listContent']/li")

            for one_selector in list_selector:
                href = one_selector.xpath("./a/@href").extract_first()
                self.logger.debug("{}区成交记录中，第{}页中显示的成交记录的详情页分别是：{}".format(region_name, page, href))
                yield scrapy.Request(href, callback=self.parse_info, dont_filter=True)
            total_page_str = response.xpath('.//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()
            self.logger.debug('total_page_str:{}{}'.format(type(total_page_str),total_page_str))
            total_page = re.search(r'totalPage\":(.*?)\,\"curPage',total_page_str)[1]

            if page < int(total_page):
                page += 1
                yield scrapy.Request(self.base_urls.format(region,page), callback=self.parse, meta={'region':region,'page':page,'region_name':region_name},dont_filter=True)

    def parse_info(self, response):

        if response and response.url:
            item = LianjiadealItem()
            item['name'] = response.xpath('.//div[@class="house-title LOGVIEWDATA LOGVIEW"]/div[@class="wrapper"]/text()').extract_first()
            item['type'] = response.xpath('.//div[@class="base"]//li[1]/text()').extract_first()
            item['total_price'] = response.xpath('.//span[@class="dealTotalPrice"]/i/text()').extract_first()
            item['unit_price'] = response.xpath('.//div[@class="price"]/b/text()').extract_first()
            item['property'] = response.xpath('.//div[@class="transaction"]//li[2]/text()').extract_first()
            item['property_year'] = response.xpath('.//div[@class="base"]//li[13]/text()').extract_first()
            time = response.xpath('.//div[@class="house-title LOGVIEWDATA LOGVIEW"]//span/text()').extract_first()
            item['time'] = re.search(r'(.*?) 成交', time, re.S)[1]
            item['year'] = response.xpath('.//div[@class="content"]//li[8]/text()').extract_first()
            item['area'] = response.xpath('.//div[@class="base"]//li[3]/text()').extract_first()
            item['direction'] = response.xpath('.//div[@class="base"]//li[7]/text()').extract_first()
            item['fitment'] = response.xpath('.//div[@class="base"]//li[9]/text()').extract_first()
            location = response.xpath('.//div[@class="name"]//a/text()').extract()
            item['location'] = ' '.join(location)
            residential = response.xpath('.//div[@class="deal-bread"]/a[5]/text()').extract_first()
            item['residential'] = re.search(r'(.*?)二手', residential)[1]
            item['elevator'] = response.xpath('.//div[@class="content"]//li[14]/text()').extract_first()
            item['purpose'] = response.xpath('.//div[@class="transaction"]//li[4]/text()').extract_first()

            yield item

