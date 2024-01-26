import scrapy
from scrapper.items import ProductItems
from scrapy_selenium import SeleniumRequest


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.co.ke"]
    start_urls = ["https://jumia.co.ke/computing/"]

    def parse(self, response):
        products = response.css("article.prd")

        for product in products:
            relative_url = product.css("a.core").attrib['href']

            product_url = "https://jumia.co.ke" + relative_url

            yield SeleniumRequest(url = product_url, callback=self.parse_product_page, wait_time=5)



        next_page = response.css('a.pg::attr(href)').get()
        next_page_url = "https://jumia.co.ke" + next_page

        yield SeleniumRequest(url = next_page_url, callback=self.parse, wait_time=5)

    
    def parse_product_page(self, response):
        
        product_item = ProductItems()

        product_item['product_name'] = response.css("div.col10 h1::text").get()
        product_item['product_price'] = response.css("div.df span::text").get()
        product_item['product_url'] = response.url
        product_item['product_rating'] = response.css("div.stars::text").get()
        product_item['product_image'] = response.css("a img.-fw").attrib['data-src']
        product_item['product_brand'] = response.css("div.-phs a::text").get()
        product_item['availability'] = response.css("p.-df::text").get()
        product_item['return_policy'] = response.css("article.-df p.-ptxs::text").get()
        product_item['warranty'] = response.css("article.-hr div.-d-co div.markup::text").get()

        yield product_item         