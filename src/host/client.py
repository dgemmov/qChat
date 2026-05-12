import socket, time, threading
from src.host import message
from src import user

Client = False

def SetClientMode():
     global Client

     toConnect = input("Enter IP to connect: ")
     if toConnect:
          Client = True
          RunClient(toConnect)

def RunClient(IP: str = "127.0.0.1"):
     try:
          global client_sock, server_addr

          client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          client_sock.bind(("0.0.0.0", 5006))
          server_addr = (IP, 5005)
          
          client_sock.sendto(f"{user.NAME} has been connected".encode(), server_addr)
          client_sock.sendto(f"$nm:{user.NAME}".encode(), server_addr)

          threading.Thread(target=message.RecieveHandler, daemon=True).start()
          message.MessageHandler()
     except Exception as e:
          print(e)
          time.sleep(5)
          exit(0)