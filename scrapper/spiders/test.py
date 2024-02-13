import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapper.items import ProductItems
from scrapy_selenium import SeleniumRequest
from scrapy.linkextractors import LinkExtractor

class TestSpider(scrapy.Spider):
    name = "test"

    custom_settings = {
        'FEEDS': {
            'search_data.json': {'format': 'json', 'ovewright': True}
        }
    }

    def start_requests(self):
        url = "https://www.jumia.co.ke/"
        yield scrapy.Request(url=url, callback=self.load)

    def load(self, response):
        # Use Selenium to get the page
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.get(response.url)

        # Increase the timeout to 10 seconds or more
        wait = WebDriverWait(driver, 10)

        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        search_query =  self.cat # "lenovo laptops"    
        search_box.send_keys(search_query)

        # Press 'Enter' to perform the search
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "main.has-b2top")))

        yield scrapy.Request(url=driver.current_url, callback=self.parse, meta={'driver': driver})

    def parse(self, response):
        products = response.css("div.-paxs")

        last_page_url = response.css('a[aria-label="Last Page"]::attr(href)').get()

        if last_page_url:
            # If there is a last page URL, extract the page number
            last_page_number = self.extract_page_number(last_page_url)

            if last_page_number:
                # Now you have the total number of pages
                total_pages = int(last_page_number)
                self.log(f'Total number of pages: {total_pages}')

        for product in products:
            relative_url = product.css("a.core").attrib['href']
            product_url = response.urljoin(relative_url)

            yield SeleniumRequest(url=product_url, callback=self.parse_product_page, wait_time=5, dont_filter=True)

        # Follow pagination links using LinkExtractor
        le = LinkExtractor(restrict_css='a.pg')
        for next_page in le.extract_links(response):
            yield response.follow(next_page, self.parse)

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

        """ scrapy crawl test -a cat="lenovo laptops" """

        """ http://127.0.0.1:9080/crawl.json?spider_name=test&start_requests=true&crawl_args={'cat':'lenovo laptops'} """

    def extract_page_number(self, url):
        # Extract the page number from the URL
        try:
            # Assuming the page number is part of the URL, modify this accordingly
            # For example, if the URL is something like '/page/5/', this would extract '5'
            page_number = url.split('/')[-2]  # Adjust this based on your URL structure

            return int(page_number)
        except (ValueError, IndexError):
            # Handle cases where the page number cannot be extracted or converted to an integer
            return None
 