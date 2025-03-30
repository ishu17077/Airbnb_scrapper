import json
import scrapy


class AirbnbspiderSpider(scrapy.Spider):
    # name = "airbnbspider"
    # allowed_domains = ["airbnb.co.in"]
    # start_urls = ["https://airbnb.co.in"]
    location = "Darjeeling"
    checkIn = "2025-03-31"
    checkOut = "2025-04-02"
    num_adult = 2
    num_children = 1

    base_url = f"https://www.airbnb.co.in/s/{location}/homes?checkin={checkIn}&checkout={checkOut}&adults={num_adult}&children={num_children}"

    def start_requests(self):
        yield scrapy.Request(url=self.base_url,callback=self.parse)
        return super().start_requests()

    def parse(self, response):
        data = response.xpath("//script[@id='data-deferred-state-0']/text()").get()
        jsonData = json.loads(data)
        targetResult = jsonData['niobeMinimalClientData'][0][1]["data"]["presentation"]["staysSearch"]["results"]["searchResults"]

        for result in targetResult:
            yield{
                'full_url': f'https://www.airbnb.co.in/s/{result["listing"]["id"]}?adult={self.num_adult}&children={self.num_children}&search_mode=regular_search&check_in={self.checkIn}&check_out={self.checkOut}',
                'title': result['listing']['title'],
                'avg_rating': result['avgRatingLocalized'],
                'imageUrls': [res["picture"] for res in result['listing'['contextualPictures']]],
                'options':   
                'location': f"latitude: {result['demandStayListing']['location']['coordinate']['latitude']} longitude: { result['demandStayListing']['location']['coordinate']['latitude']['longitude']}",
                'price_per_night': result['structuredDisplayPrice']['primaryLine']['price'],
                'total_price': result['secondaryLine']['price'],
                


            }