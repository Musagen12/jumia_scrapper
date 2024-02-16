# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class ScrapperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Activated if a product doesn't have a brand name
        brands = ['product_brand']
        for brand in brands:
            value = adapter.get(brand)
            if '('  in value:
                adapter[brand] = "Brand not available"

        # Activated if a product doesn't have a warranty/ availablilty data(warranty=null or availability=null)
        warrantys = ['warranty', 'availability']
        for warranty in warrantys:
            value2 = adapter.get(warranty)
            if value2 == None:
                adapter[warranty] = "Missing data"

        return item
    
class SaveIntoDb:
    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'kali' # your password
        database = 'scrapy'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create able if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jumia(
            id serial PRIMARY KEY, 
            product_name VARCHAR(255),
            product_price VARCHAR(255),
            product_url VARCHAR(255),
            product_rating VARCHAR(255),
            product_image VARCHAR(255),
            product_brand VARCHAR(255),
            availability VARCHAR(255),
            return_policy VARCHAR(255),
            warranty VARCHAR(255)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into jumia (product_name, product_price, product_url, product_rating, product_image, product_brand, availability, return_policy, warranty) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item["product_name"],
            item["product_price"],
            item["product_url"],
            item["product_rating"],
            item["product_image"],
            item["product_brand"],
            item["availability"],
            item["return_policy"],
            item["warranty"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()