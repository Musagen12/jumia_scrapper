import scrapy
from scrapper.items import ProductItems


class SpecificSpider(scrapy.Spider):
    name = "specific"
    allowed_domains = ["jumia.co.ke"]
    #place the url of a specific item
    start_urls = ["https://www.jumia.co.ke/black-white-black-white-whisky-750ml-49559205.html"]

    custom_settings = {
        'FEEDS': {
            'tracked_item_data.json': {'format': 'json', 'ovewright': True}
        }
    }

    def parse(self, response):
        products = response.css("article.prd")

        product_item = ProductItems()

        product_item['product_name'] = response.css("div.col10 h1::text").get()
        product_item['product_price'] = response.css("div.df span::text").get()
        product_item['product_url'] = response.url
        product_item['product_rating'] = response.css("div.stars::text").get()
        product_item['product_image'] = response.css("a img.-fw").attrib['data-src']
        product_item['product_brand'] = response.css("div.-phs a::text").get()
        product_item['availability'] = response.css("p.-df::text").get() or response.css("div.-pts span::text").get()
        product_item['return_policy'] = response.css("article.-df p.-ptxs::text").get()
        product_item['warranty'] = response.css("article.-hr div.-d-co div.markup::text").get()

        yield product_item
