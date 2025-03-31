# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from airbnbscrapper.spiders.mysql_connection import *


def init():
    createNewDatabase()
   #  testDatabase() #? Testing the table to see if it works

