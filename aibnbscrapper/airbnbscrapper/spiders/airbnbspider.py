import json
# import re
import scrapy


class AirbnbspiderSpider(scrapy.Spider):
    name = "airbnbspider"
    # allowed_domains = ["airbnb.co.in"]
    # start_urls = ["https://airbnb.co.in"]
    location = "Darjeeling"
    checkIn = "2025-03-31"
    checkOut = "2025-04-02"
    num_adult = 2
    num_children = 1

    base_url = f"https://www.airbnb.co.in/s/{location}/homes?checkin={checkIn}&checkout={checkOut}&adults={num_adult}&children={num_children}&search_mode=regular_search"

    def start_requests(self):
        yield scrapy.Request(url=self.base_url,callback=self.parse)
        return super().start_requests()
    



    def parse(self, response):
        data = response.xpath("//script[@id='data-deferred-state-0']/text()").get()
        jsonData = json.loads(data)
        targetResult = jsonData['niobeMinimalClientData'][0][1]["data"]["presentation"]["staysSearch"]["results"]["searchResults"]  
        for result in targetResult:
            total_price = None
            price_per_night = None
            
            primaryLine = (result['structuredDisplayPrice']['primaryLine'])
            secondaryLine = (result['structuredDisplayPrice']['secondaryLine'])
            
            
            if is_json_key_present(primaryLine, "accessibilityLabel"):
                price_per_night = primaryLine['accessibilityLabel']
            elif is_json_key_present(primaryLine, "price"):
                price_per_night = primaryLine['price']
            elif is_json_key_present(primaryLine, "discountedPrice"):
                price_per_night = primaryLine['discountedPrice']

            if is_json_key_present(secondaryLine, "accessibilityLabel"):
                total_price = secondaryLine['accessibilityLabel']
            elif is_json_key_present(secondaryLine, "price"):
                total_price = secondaryLine['price']
            
            yield{
                'full_url': f'https://www.airbnb.co.in/s/{result["listing"]["id"]}?adult={self.num_adult}&children={self.num_children}&search_mode=regular_search&check_in={self.checkIn}&check_out={self.checkOut}',
                'title': result['listing']['title'],
                'avg_rating': result['avgRatingLocalized'],
                'imageUrls': [res["picture"] for res in result['contextualPictures']],
                # 'options':  re.findall(r'"messages":\s*\[(.*?)\]', json['listing']['contextualPictures']['caption']),
                # The entire regular expression aims to find the string "messages": followed by optional whitespace, an opening square bracket, then captures everything inside of the square brackets, and then finds the closing square bracket. It is designed to extract the contents of a JSON-like "messages" array.
                # 'coordinates': f"{result['demandStayListing']['location']}", #? Dynamic json keeps changing
                
                'price_per_night':price_per_night if price_per_night != None else 'N/A',
                'total_price': total_price if total_price != None else 'N/A',
            }
            nextPage = jsonData['niobeMinimalClientData'][0][1]["data"]["presentation"]["staysSearch"]["results"]['paginationInfo']['nextPageCursor']
            if nextPage:
                nextUrl = self.base_url + f"&paginationSearch=true&cursor={nextPage}"
                yield scrapy.Request(url=nextUrl, callback=self.parse)

def is_json_key_present(json, key):
    try:
        buf = json[key]
    except:
        return False
    return True
    
    