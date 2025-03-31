import json
import os
import re

import mysql.connector
from airbnbscrapper.spiders.constants import dirPath

dbName="Airbnb"
tableName = "scrapper"
database = None


def getCredentials(fileLocation=f"{dirPath}/key.properties"):
   try:
      f = open(fileLocation, "r")
      data = f.read()
      user = re.findall(r'user=(.*)', data)
      password = re.findall(r'password=(.*)', data)
      return{
            "user": user[0],
            "password": password[0],
      }
   except:
      return {
         "user": 'root',
         "password": None,
      }


def createNewDatabase():
   credentials = getCredentials()
   global database
   database = mysql.connector.connect(
        host = "localhost",
        user = credentials['user'],
        password = credentials['password'],
        port = '3306',
        auth_plugin='mysql_native_password'
   )
   createDb = f"""
   CREATE DATABASE IF NOT EXISTS {dbName};
   USE {dbName};
   CREATE TABLE IF NOT EXISTS {tableName}(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        full_url VARCHAR(500),
        image_urls TEXT,
        avg_rating VARCHAR(500),
        price_per_night VARCHAR(500),
        total_price VARCHAR(500)
   );
    """
   with database.cursor() as cursor:
       cursor.execute(createDb)
   

def connectToDatabase():
#    load_dotenv
   global database
   try:
        credentials = getCredentials()
        with mysql.connector.connect(
            host = "localhost",
            user = credentials['user'],
            password = credentials['password'],
            port = '3306',
            database = dbName
        ) as database1:
            database = database1
   except mysql.connector.Error as e:
       print("Error: "+e)
   
def insertToDatabase(title: str, full_url: str, avgRating: str, pricePerNight: str, totalPrice: str, imageUrls: list) -> bool:
    global database
    insertRecordTemplate = f"""INSERT INTO {tableName} (title, full_url, image_urls, avg_rating, price_per_night, total_price)
        VALUE(%s, %s, %s, %s, $s, %s)
    """
    imageUrls = json.dumps(imageUrls)
    actualRecord = (
        title,
        full_url,
        imageUrls,
        avgRating,
        pricePerNight,
        totalPrice  
    )
    with database.cursor() as cursor:
        cursor.execute(insertRecordTemplate, actualRecord)
        database.commit()




def accessDatabase():
    pass





def testDatabase():
    describe_scrapper = f"DESCRIBE {tableName}"
    database.reconnect()
    with database.cursor() as cursor:
        cursor.execute(describe_scrapper)
        scapper_schemas = cursor.fetchall()
        for column in scapper_schemas:
            print(column)