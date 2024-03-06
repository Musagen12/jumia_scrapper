The following command were used in the scrapy shell(They can be used in the spiders also) to get the 
corresponding information from individual products:

    item url          response.url   
    item name         response.css("div.col10 h1::text").get()
    brand name        response.css("div.-phs a::text").get()
    item price        response.css("div.df span::text").get()
    item discount     response.css("span.bdg").attrib["data-disc"]
    item rating      response.css("div.stars::text").get()
    image url         response.css("a img.-fw").attrib['data-src']
    availability      response.css("p.-df::text").get()
    return policy     response.css("article.-df p.-ptxs::text").get()    
    warranty          response.css("article.-hr div.-d-co div.markup::text").get()
    weight                  specifications[3].css("li::text").get()
    country of origin       specifications[2].css("li::text").get()
    materials               specifications[4].css("li::text").get()


    list of specifications   specifications = response.css("div.card-b ul.-pvs li.-pvxs")


These commands were used to get the general information from a page. They are a simpler and more lean version of the above commands:

    fetching                                    fetch("https://jumia.co.ke/computing/")
    getting all products                        response.css("article.prd")
    getting the first product                   product = products[0]
    getting the product name/description        product.css("div.name::text").get()
    getting the price of the product            product.css("div.prc::text").get()
    getting the link to the product             product.css("a.core").attrib['href']
    getting the image link                      product.css("a img.img").attrib['data-src']
    