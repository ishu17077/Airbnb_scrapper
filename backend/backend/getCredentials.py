import re


def getCredentials(fileLocation="./backend/backend/key.properties"):
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