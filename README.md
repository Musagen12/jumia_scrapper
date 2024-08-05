<h1>Web Scraping Project - Jumia</h1>
<h3>Project Overview</h3>

This project involves developing a web scraper to extract product information from Jumia, an e-commerce website. The scraper will gather data such as product names, prices, ratings, and availability. This data can be used for analysis, price comparison, or other purposes.
Features Scraping Product Information: Extract product details including name, price, rating, and availability, Data Storage: Save the scraped data into a CSV file for easy access and analysis and Error Handling: Manage errors and exceptions to ensure the scraper runs smoothly.

<h3>Technologies Used</h3>

Python: Programming language used to write the scraper.
BeautifulSoup: Library for parsing HTML and extracting data from web pages.
Requests: Library to send HTTP requests and receive responses.
Pandas: Library to handle data manipulation and storage.

<h3>Prerequisites</h3>

Before running the project, ensure you have the following installed:

Python 3.x
    
<h3>Installation</h3>

Clone the repository:
    sh

    git clone https://github.com/your-username/jumia-web-scraper.git
    cd jumia-web-scraper

    python3 -m venv venv
    source venv/bin/activate
    
    pip install -r requirements.txt
    
<h3>Usage</h3>

Run the scraper:

    sh
    flask --app hello run
    scrapyrt

On the browser search:
    http://127.0.0.1:9080/crawl.json?spider_name=test&start_requests=true&crawl_args={'cat': item})
    

    View the results:
    The scraped data will be saved in a CSV file named jumia_products.csv. You can open this file using any spreadsheet application or analyze it using Python.


<h3>Contributing</h3>

Contributions are welcome! If you have suggestions for improvements, feel free to fork the repository and create a pull request.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

If you have any questions or issues, please open an issue in the repository.

Happy scraping! 👍👍
