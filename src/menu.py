from src.host import server, client
from src import user, console, port, tag, packet, serializer, settings
import time, sys, subprocess, os
from colorama import just_fix_windows_console, Fore

if os.name == "nt":
     just_fix_windows_console()

devUserMode: bool = False

text = """
             .oooooo.   oooo                      .
            d8P'  `Y8b  `888                    .o8
 .ooooo oo 888           888 .oo.    .oooo.   .o888oo
d88' `888  888           888P"Y88b  `P  )88b    888
888   888  888           888   888   .oP"888    888
888   888  `88b    ooo   888   888  d8(  888    888 .
`V8bod888   `Y8bood8P'  o888o o888o `Y888""8o   "888"
      888.
      8P'
      "
"""

def menu():
     return f"""
[{serializer.MAIN_COLOR} 1 {serializer.MAIN_RESET}] Run Server
[{serializer.MAIN_COLOR} 2 {serializer.MAIN_RESET}] Run Client
[{serializer.MAIN_COLOR} 3 {serializer.MAIN_RESET}] Settings
[{serializer.MAIN_COLOR} 4 {serializer.MAIN_RESET}] Check Port and Open port
"""

_devMenu = f"""
{tag.info}You have entered developer mode, please select the mode to run
{tag.info}In developer mode, when launching a client or server, the default port + 1 is used. 
{tag.info}This is necessary for a successful connection.

{tag.info}Type 0 to run server and connect to yourself
"""

def Launch():
     print(text)

     time.sleep(0.5)
     console.clear()

     Menu()

def devMenu():
     global devUserMode
     devUserMode = not devUserMode
     packet.port = packet.port + 1 # changing default port

     menu()
     console.clear()
     print(_devMenu + menu())

     try:
          choice = int(input(f"{serializer.INPUT_SYMBOL}"))
     except ValueError:
          print(f"{tag.error} Invalid input! Please select and enter the number.")
          time.sleep(1)
          devMenu()
          return 
     match(choice):
          case 0:
               args = [
               "-m", 
               "dev", 
               "-p", 
               str(packet.port)
               ]
               subprocess.Popen([sys.executable, "main.py"] + args,
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
               packet.port = packet.port - 1
               user.NAME = "devServer"
               server.RunServer()
          case _:
               print(f"{tag.error} Invalid input! Please select and enter the number.")
               time.sleep(1)
               Menu()
          
def Menu():

     console.clear()
     print(menu())

     try:
          choice = int(input(f"{serializer.INPUT_SYMBOL}"))
     except ValueError:
          print(f"{tag.error} Invalid input! Please select and enter the number.")
          time.sleep(1)
          Menu()
          return
     
     match(choice):
          case 1:
               server.RunServer()
          case 2:
               client.SetClientMode()
          case 3: # Settings
               settings.settingsMenu()
          case 4:
               port.open_port(packet.port)
          case 999:
               devMenu()
          case _:
               print(f"{tag.error} Invalid input! Please select and enter the number.")
               time.sleep(1)
               Menu()