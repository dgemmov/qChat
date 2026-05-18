import random, time, requests
from src import console, menu
from src.host import client, server

NAME = f"USER {random.randint(0,100)}" # Default username with random numbers

def getUserMode():
     if client.Client:
          return "client"
     elif server.Server:
          return "server"
     else:
          return "unknown"
     
def returnPersonalIP():
     return requests.get('https://api.ipify.org').text

def CheckUser():
     global NAME
     with open('user.txt', 'r') as userFile:
          NAME = userFile.read()
          if len(NAME) > 12 :
               NAME = NAME[:9]+"..."

def UsernameChange():
     global NAME
     console.clear()
     NewUsername = input(f"Your current username is {NAME}\n> ")
     if NewUsername:
          if len(NewUsername) > 12:
               print("NO MORE THAN 12 SYMBOLS!")
               console.clear()
               UsernameChange()
          else:
               NAME = NewUsername
               
               print("You have changed your username")
               with open('user.txt', 'w') as userFile:
                    userFile.write(NAME)

               time.sleep(3)
               menu.Menu()
          