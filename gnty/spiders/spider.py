import scrapy

from scrapy.loader import ItemLoader

from ..items import GntyItem
from itemloaders.processors import TakeFirst


class GntySpider(scrapy.Spider):
	name = 'gnty'
	start_urls = [
		'https://about.gnty.com/news/',
		'https://about.gnty.com/cashs-blog/'
	              ]

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//nav[@class="pagination"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//section[@class="news_article"]//div[@class="rich-text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date"]/text()').get()

		item = ItemLoader(item=GntyItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
