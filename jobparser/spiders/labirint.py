import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem
from pymongo import MongoClient

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    # start_urls = ['https://www.zarplata.ru/vacancy?q=Python']
    # start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        client = MongoClient('172.17.0.2', 27017)
        self.mongo_base = client.spiders
        self.collection = self.mongo_base['labirint']


    def parse(self, response):
        next_page = response.xpath("//a[@class = 'pagination-next__text']/@href").get()
        print('next_page', next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@class = 'product-cover']/div/div/a/@href").getall()
        for link in links:
            l = 'https://'+'labirint.ru' + link
            yield response.follow(l, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        book = {}
        book['url'] = response.url
        book['name'] = response.xpath("//div[@id = 'product-title']//h1/text()").extract()[0]
        book['author'] = response.xpath("//div[@class = 'authors']/a//text()").extract()[0]
        book['common_price'] = response.xpath("//span[@class = 'buying-priceold-val-number']/text()").extract()[0]
        book['discount_price'] = response.xpath("//span[@class = 'buying-pricenew-val-number']/text()").extract()[0]
        book['rate'] = response.xpath("//div[@id = 'rate']/text()").extract()[0]


        self.collection.insert_one(book)
        z = 1
        # yield JobparserItem(url=url, name=name, author=author, common_price=common_price,
        #                     discount_price=discount_price, rate = rate)

