import socket, requests, keyboard, threading
from src import console, port, control
from src.host import message

Server: bool = False
clients = [] # Connected clients list
server_sock = None

def getUserName(ip):
     for c in clients:
          if ip == c['ip']:
               return c['name']
          else:
               print('Error to get username from client list')

def RunServer():
     global server_sock, Server

     Server = True
     server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     server_sock.bind(("0.0.0.0", 5005))
     
     # port.open_port(5005)
     
     console.clear()
     public_ip = requests.get('https://api.ipify.org').text
     print(f"You launched a server. Your IP to connect: {public_ip}") # \nPress {control.server_exit_button} to shutdown the server.
     
     threading.Thread(target=message.RecieveHandler, daemon=True).start()
     message.MessageHandler()