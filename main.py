from src.header import *
from src import menu
import argparse, time

parser = argparse.ArgumentParser(description="Dev mode")
parser.add_argument("-m", "--mode", type=str, required=False, help="User connection mode")
parser.add_argument("-p", "--port", type=str, required=False, help="User connection port")
args = parser.parse_args()

if args.mode == "dev":
     from src.host import var
     var.DEBUG = True

     time.sleep(3)
     packet.port = int(args.port)
     user.NAME = "devClient"
     client.Client = True
     client.RunClient("127.0.0.1")

if __name__ == "__main__":
     serializer.ReadJSON()
     console.clear()
     user.CheckUser()
     menu.Launch()