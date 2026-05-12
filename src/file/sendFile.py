import os, keyboard
from src import control
from src.host import client, server, var
from src import user

fileData = None
reqFile = None

def writeFileToBytes(path: str, receiver: str):
     global fileData
     with open(path, 'rb') as f:
          fileData = f.read()
          server.server_sock.sendto(var.file_flag.encode() + fileData, receiver)

def sendFileRequest(senderName: str, receiver: str, filename: str, size: float):
     if(size > 1000):
          print("You cant send any file that bigger then 1000 bytes.")
          return
     
     msg = f"\n{senderName} has sent you file '{filename}' size: {round(size, 2)}\nType 1 to Accept and 0 to Reject file"
     
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     writeFileToBytes(path=filename, receiver=receiver)
     sender_data.sendto(msg.encode(), receiver)
     sender_data.sendto(var.code[0]['code'].encode(), receiver)

def AwaitChoice():
     choice = str(input("=> "))
     if choice == control.accept_file_key:
          var.code[0]['state'] = True
     else:
          var.code[0]['state'] = False

def sendFileToUser(receiver: str):
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     sender_data.sendto(var.code[1]['code'].encode(), receiver)