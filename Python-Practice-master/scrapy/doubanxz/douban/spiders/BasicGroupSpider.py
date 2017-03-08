# coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import DoubanItem
import re

class GroupTestSpider(BaseSpider):
	name = "doubanxz"
	allowed_domains = ["douban.com"]
	start_urls = [
		"http://www.douban.com/group/explore"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		sites = hxs.select("//li[@class='']/div[@class='info']")
		items = []
		for site in sites:
			item = DoubanItem()
			item['groupname'] = site.select("div[@class='title']/a[@class='']/text()").extract()
			item['groupurl'] = site.select("div[@class='title']/a[@class='']/@href").extract()
			item['totalnumber'] = site.select("span[@class='num']/text()").extract()
			items.append(item)
			print repr(item).decode("unicode-escape") + '\n'
		return items

