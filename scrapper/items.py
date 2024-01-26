# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()


class ProductItems(scrapy.Item):
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_rating = scrapy.Field()
    product_image = scrapy.Field()
    product_brand = scrapy.Field()
    availability = scrapy.Field()
    return_policy = scrapy.Field()
    warranty = scrapy.Field()