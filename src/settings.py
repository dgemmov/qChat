from src.header import *
from src import serializer, console, user, tag, packet, menu
import time
from colorama import Fore

def settingsMenu():
     time.sleep(1.5)
     serializer.ReadJSON()
     console.clear()
     print(f"""
[{serializer.MAIN_COLOR} 1 {serializer.MAIN_RESET}] Change username
[{serializer.MAIN_COLOR} 2 {serializer.MAIN_RESET}] Change port
[{serializer.MAIN_COLOR} 3 {serializer.MAIN_RESET}] Change prefix
[{serializer.MAIN_COLOR} 4 {serializer.MAIN_RESET}] Change accent
[{serializer.MAIN_COLOR} 0 {serializer.MAIN_RESET}] Back to menu
""")
     choice = int(input(f"{serializer.INPUT_SYMBOL}"))
     match(choice):
          case 1:
               user.UsernameChange()
          case 2:
               newPort = int(input(f"{tag.info}New port can't be less than 5000 and be more than 20000\n{serializer.INPUT_SYMBOL}"))
               if newPort > 20000 or newPort < 5000:
                    console.clear()
                    print(f"{tag.error}Your port is not correct.")
                    settingsMenu()
               else:
                    packet.port = newPort
                    print(f"{tag.success}You set new port: {Fore.GREEN}{newPort}{Fore.RESET}")
                    serializer.UpdateJSON("port", newPort)
                    settingsMenu()
          case 3:
               newSymbol = str(input(f"{tag.info}You can type any symbol what you want.\n{serializer.INPUT_SYMBOL}"))
               if len(newSymbol) > 1:
                    print(f"{tag.error}Your choice is more than 1 symbol.")
                    time.sleep(3)
                    settingsMenu()
               else:
                    serializer.UpdateJSON("symbol", newSymbol)
                    print(f"{tag.success}You set new symbol: {newSymbol}")
                    settingsMenu()
          case 4:
               newSymbolColor = int(input(f"{tag.info}You can choose color only from the list.\n{serializer.INPUT_SYMBOL_COLOR_LIST}\n{serializer.INPUT_SYMBOL}"))
               if newSymbolColor > 6 or newSymbolColor < 0:
                    print(f"{tag.error}Your choice is not valid.")
                    settingsMenu()
               else:
                    serializer.UpdateJSON("symbolColor", serializer.INPUT_SYMBOL_COLOR_LIST_ARRAY[newSymbolColor])
                    print(f"{tag.success}You set new color: {serializer.INPUT_SYMBOL_COLOR_LIST_ARRAY[newSymbolColor]}")
                    settingsMenu()
          case 0:
               menu.Launch()