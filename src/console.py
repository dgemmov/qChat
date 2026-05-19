import os

def clear():
     if os.name == "nt": # 18.05.2026
          os.system("cls") # Only for windows (maybe)
     else:
          os.system("clear")