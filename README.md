# Try to run these commands before if stuff doens't work #
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential
pip3 install mysqlclient django scrapy

# To run the scrapy script, please run it in order #

- cd ./Airbnb_scrapper/aibnbscrapper
- scrapy crawl airbnbspider -a location=Puri -a checkIn=2025-05-16 -a checkOut=2025-05-18 -a adults=2 -a children=0

//? Here these parameters: location, checkIn, checkOut and others can be modified

Please make sure your database is not encrypted or you will have to use a "key.properties" file inside of ./backend/backend and ./aibnbscrapper/airbnbscrapper/spiders/

# To run django server #
Please run this:

- cd ./Airbnb_scrapper/backend

- python3 ./manage.py runserver

//? Some apis which are implemeted are:

- localhost:8000/api/all

- localhost:8000/api/{cityName}

//? If you're running it locally use: localhost else: use anything else.

//? {cityName} should be the city you used scrapy to fetch with the parameters 'location={cityName}'


key.properties is defined as:
"
user="username here"
password="password here"
"

please add key.properties in:

./Airbnb_scrapper/aibnbscrapper/spiders 

./Airbnb_scrapper/backend/backend/
