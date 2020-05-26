# -*- coding: utf-8 -*-
import scrapy
from Crawl02.items import ShfairItems
from urllib import parse
from scrapy.http import Request

from Crawl02.utils.common import get_md5


class ShfairSpider(scrapy.Spider):
    name = 'shfair'
    allowed_domains = ['shfair-cbd.no4e.com']
    start_urls = ['http://shfair-cbd.no4e.com/portal/list/index/id/208.html?page=1']

    """
    用于解析网页
    """
    def parse(self, response):

        # 爬取当前页的页面数据
        yield from self.parse_detail(response)

        # 爬取下一页的url，并下载
        next_url = response.css('li.page-item:last-child a::attr(href)').extract_first()
        if next_url:
            # 连接当前域名和获取到的url
            total_url = parse.urljoin(response.url, next_url)
            # 使用yield关键字自动交给scrapy进行下载
            # meta属性是一个字典，可以将参数传递给response
            # yield Request(url=total_url, meta={"front_image_url": image_url}, callback=self.parse)
            yield Request(url=total_url, callback=self.parse)

    """
    用于解析当前页面的有用信息，并交给pipelines存储
    """
    def parse_detail(self, response):

        shfair_item = ShfairItems()
        # type = response.css('table.show-info-table tr:not(.table-h) td:nth-child(1)::text').extract()
        # company_cn = response.css('table.show-info-table tr:not(.table-h) td:nth-child(2)::text').extract()
        # company_en = response.css('table.show-info-table tr:not(.table-h) td:nth-child(3)::text').extract()
        # number = response.css('table.show-info-table tr:not(.table-h) td:nth-child(4)::text').extract()
        # image = response.css('#top-pic-slide img::attr(src)').extract_first("")
        # # 获取检索到的第一张图片，默认为空
        # image = response.meta.get("image_url", "")

        # # 类似于字典的调用方式
        # shfair_item["type"] = type
        # shfair_item["company_cn"] = company_cn
        # shfair_item["company_en"] = company_en
        # shfair_item["number"] = number
        # # 这里图片数据默认传入的是一个数组
        # shfair_item["image"] = [image]
        # shfair_item["url_md5"] = get_md5(response.url)
        #
        # # 将item传递到pipelines中
        # yield shfair_item

        types = response.css('table.show-info-table tr:not(.table-h) td:nth-child(1)')
        company_cns = response.css('table.show-info-table tr:not(.table-h) td:nth-child(2)')
        company_ens = response.css('table.show-info-table tr:not(.table-h) td:nth-child(3)')
        numbers = response.css('table.show-info-table tr:not(.table-h) td:nth-child(4)')
        image = response.css('#top-pic-slide img::attr(src)').extract_first("")

        shfair_item["image"] = [image]
        shfair_item["url_md5"] = get_md5(response.url)
        for i in range(len(types)-1):
            shfair_item["type"] = types[i].css('::text').extract_first() if types[i].css('::text').extract() else ""
            shfair_item["company_cn"] = company_cns[i].css('::text').extract_first() if company_cns[i].css('::text').extract() else ""
            shfair_item["company_en"] = company_ens[i].css('::text').extract_first() if company_ens[i].css('::text').extract() else ""
            shfair_item["number"] = numbers[i].css('::text').extract_first() if numbers[i].css('::text').extract() else ""
            yield shfair_item


