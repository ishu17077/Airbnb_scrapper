import json
import os
import re

import mysql.connector
import mysql.connector.errorcode
from airbnbscrapper.spiders.constants import dirPath

dbName="Airbnb"
tableName = "scrapper"
database = None
cnx = None


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
   global cnx
   cnx = mysql.connector.connect(
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
   with cnx.cursor() as cursor:
       cursor.execute(createDb)
   

def connectToDatabase():
#    load_dotenv
   global database
   try:
        credentials = getCredentials()
        database = mysql.connector.connect(
            host = "localhost",
            user = credentials['user'],
            password = credentials['password'],
            port = '3306',
            database = dbName
        )
        return database 
   except mysql.connector.Error as e:
       print("Error: "+e)
   
def insertToDatabase(database, title: str, fullUrl: str, avgRating: str, pricePerNight: str, totalPrice: str, imageUrls: list) -> bool:
    try:
        stringImageUrls = json.dumps(imageUrls)
        insertRecordTemplate = f"""INSERT INTO {dbName}.{tableName} (title, full_url, image_urls, avg_rating, price_per_night, total_price
        ) VALUE(%s,%s,%s,%s,%s,%s);
        """
        
        actualRecord = (
            title,
            fullUrl,
            stringImageUrls,
            avgRating,
            pricePerNight,
            totalPrice  
        )
        with database.cursor() as cursor:
            cursor.execute(insertRecordTemplate, actualRecord)
            database.commit()
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    



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

