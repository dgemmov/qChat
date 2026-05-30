import json, os
from colorama import Fore
from src import user, packet, menu, tag

CONFIG_FILE = "config.json"
INPUT_SYMBOL_COLOR = Fore.RED # GREEN BLUE CYAN MAGENTA RED YELLOW
INPUT_SYMBOL = f"{INPUT_SYMBOL_COLOR}> "

MAIN_COLOR = Fore.GREEN # Main color
MAIN_RESET = Fore.RESET

INPUT_SYMBOL_COLOR_LIST_ARRAY = {
     1: "RED", 
     2: "YELLOW", 
     3: "BLUE", 
     4: "CYAN", 
     5: "MAGENTA",
     6: "GREEN"
}

INPUT_SYMBOL_COLOR_LIST = f"""
[{Fore.RED} 1 {Fore.RESET}] RED
[{Fore.YELLOW} 2 {Fore.RESET}] YELLOW
[{Fore.BLUE} 3 {Fore.RESET}] BLUE
[{Fore.CYAN} 4 {Fore.RESET}] CYAN
[{Fore.MAGENTA} 5 {Fore.RESET}] MAGENTA
[{Fore.GREEN} 6 {Fore.RESET}] GREEN
"""

def CheckInit():
     if not os.path.exists(CONFIG_FILE):
          data = {"port": 5005, "username": "default"}

def UpdateJSON(row: str, data):
     with open(CONFIG_FILE, "r", encoding="utf-8") as file:
          config = json.load(file)

     config[row] = data
     
     with open(CONFIG_FILE, "w", encoding="utf-8") as file:
          json.dump(config, file, indent=5, ensure_ascii=False)

def InitJSON():
     config = {
          "port": 5005,
          "username": user.NAME,
          "symbol": ">",
          "symbolColor": "WHITE"
     }
     
     with open(CONFIG_FILE, "w", encoding="utf-8") as file:
          json.dump(config, file, indent=5, ensure_ascii=False)

def ReadJSON():
     global INPUT_SYMBOL, INPUT_SYMBOL_COLOR, MAIN_COLOR
     config = None
     try:
          with open(CONFIG_FILE, "r", encoding="utf-8") as f:
               config = json.load(f)
          
          user.NAME = config['username']
          packet.port = config['port']
          COLOR_NAME = config['symbolColor']
          INPUT_SYMBOL_COLOR = getattr(Fore, COLOR_NAME, Fore.WHITE)
          MAIN_COLOR = getattr(Fore, COLOR_NAME, Fore.WHITE)
          INPUT_SYMBOL = f"{INPUT_SYMBOL_COLOR}{config['symbol']}{Fore.RESET} "
     except:
          InitJSON()