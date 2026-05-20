import os, keyboard
from src import control, packet
from src.host import client, server, var
from src import user

fileData = None
reqFile = None

def writeFileToBytes(receiver: str, sock, path: str = "Unknown.qChat"):
     global fileData
     with open(path, 'rb') as f:
          fileData = f.read()
          sock.sendto(var.file_flag.encode() + fileData + var.file_flag_name.encode() + path.encode(), receiver)

def sendFileRequest(senderName: str, receiver: str, filename: str, size: float):
     if(size > 1000):
          print(f"You cant send any file that bigger then {packet.packetSize} bytes.")
          return
     
     msg = f"\n{senderName} has sent you file '{filename}' size: {round(size, 2)} byte(-s)"
     
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return
     
     sender_data.sendto(msg.encode(), receiver)
     sender_data.sendto(var.code[0]['code'].encode(), receiver)
     packet.SendTimeout()
     writeFileToBytes(receiver=receiver, sock=sender_data, path=filename)

def FileSave(name: str, data: bytes): # save on receiver computer
     download_path = "downloads"
     if not os.path.exists(download_path):
          os.makedirs(download_path)

     with open(f"{download_path}/{name}", "wb") as file:
          try:
               file.write(data)
               print(f"\nFile has been downloaded success! Check out {download_path} folder.")
          except Exception as e:
               print(f"\nError while download has accured: {e}")

def sendFileToUser(receiver: str):
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     sender_data.sendto(var.code[1]['code'].encode(), receiver)