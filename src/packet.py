import time
from src.host import client, server

packetSize = 4096 # Bytes
port = 5005 # It will be ready for use soon
sock = None # Switch sended packet (To client or to server)

def SendBytes(data: str): # This def is replacing sock.sendto
     if client.Client: 
          client.client_sock.sendto(data, client.server_addr)
     elif server.Server:
          for c in server.clients:
               server.server_sock.sendto(data, c['ip'])

def SendTimeout():
     time.sleep(0.05) # Timeout