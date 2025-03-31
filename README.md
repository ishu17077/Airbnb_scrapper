# Try to run these commands before if stuff doens't work #
sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential
pip3 install mysqlclient django scrapy

# To run the scrapy script, please run it in order #

cd ./Airbnb_scrapper/aibnbscrapper\n
scrapy crawl airbnbspider -a location=Puri -a checkIn=2025-05-16 -a checkOut=2025-05-18 -a adults=2 -a children=0\n
//? Here these parameters: location, checkIn, checkOut and others can be modified\n

Please make sure your database is not encrypted or you will have to use a "key.properties" file inside of ./backend/backend and ./aibnbscrapper/airbnbscrapper/spiders/\n

# To run django server #
Please run this:\n
cd ./Airbnb_scrapper/backend\n
python3 ./manage.py runserver\n

//? Some apis which are implemeted are:\n
localhost:8000/api/all\n
localhost:8000/api/{cityName}\n
//? cityName should be the city you used scrapy to fetch with the parameters 'location={cityName}'\n


key.properties is defined as:\n
"\n
user="username here"\n
password="password here"\n
"\n
please add key.properties in: \n
./Airbnb_scrapper/aibnbscrapper/spiders \n
./Airbnb_scrapper/backend/backend/\n