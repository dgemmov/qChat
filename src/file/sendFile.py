import os, keyboard
from src import control, packet, tag, serializer
from src.host import client, server, var, message
from src import user
from colorama import ansi, Cursor

fileData = None
reqFile = None

def writeFileToBytes(receiver, sock, path: str = "Unknown.qChat", senderName: str = "Unknown"):
     global fileData
     with open(path, 'rb') as f:
          fileData = f.read()
          packetData = (var.file_flag.encode() + fileData + var.file_flag_name.encode() + path.encode() + var.file_flag_sender.encode() + senderName.encode())
          sock.sendto(packetData, receiver)

def sendFileRequest(senderName: str, receiver: str, filename: str, size: float, username: str): # 21.05.2026 user: str - was added
     if(size > packet.packetSize): # fixed 21.05.2026
          print(f"{tag.warning}You cant send any file that bigger then {packet.packetSize} bytes.")
          return
     
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return
     
     if receiver == '0.0.0.0':
          sender_data = client.client_sock # Force client mode cause in message.py client cant read client list, only server
          receiver = client.server_addr # Send it to server anyway, then server will check it and return to current client
     
     
     request = next((v['code'] for v in var.code if v['code'] == '$filerequest'), "$filerequest")
     sender_data.sendto(request.encode(), receiver)
     packet.SendTimeout()

     writeFileToBytes(receiver=receiver, sock=sender_data, path=filename, senderName=senderName)

def getFileRequest(filename: str, data: bytes, senderName: str):
     print("\033[?1049h" + Cursor.POS(1, 1) + ansi.clear_screen(), end="", flush=True)
     print(f"{tag.info} Incoming file '{serializer.MAIN_COLOR}{filename}{serializer.MAIN_RESET}' from {serializer.MAIN_COLOR}{senderName}{serializer.MAIN_RESET}.")
     print(f"{tag.info} Size: {serializer.MAIN_COLOR}{len(data)}{serializer.MAIN_RESET} bytes.")

     if os.name == "nt":
          import ctypes
          ctypes.windll.user32.PostMessageW(ctypes.windll.kernel32.GetConsoleWindow(), 0x0100, 0x0D, 0) # мегакостыль 
     requestMsg = input(f"{tag.info} Accept this file? (y/n): ").strip().lower()

     if requestMsg == control.accept_file_key.lower():
          print(f"{tag.info} Saving...")
          FileSave(name=filename, data=data)
     else:
          print(f"{tag.warning} Rejected getting a {serializer.MAIN_COLOR}{filename}{serializer.MAIN_RESET}.")

     print(f"\n{tag.info} Press Enter to finish the transfer...")

def FileSave(name: str, data: bytes): # save on receiver computer
     download_path = "downloads"
     if not os.path.exists(download_path):
          os.makedirs(download_path)

     file_name, file_extension = os.path.splitext(name)

     file_path = f"{download_path}/{name}"
     file_count = 1

     while os.path.exists(file_path):
          edited_file_name = f"{file_name} ({file_count}){file_extension}"
          file_path = f"{download_path}/{edited_file_name}"
          file_count += 1

     with open(file_path, "wb") as file:
          try:
               file.write(data)
               savedAs = os.path.basename(file_path)
               print("\r" + ansi.clear_line(), end="", flush=True)
               print(f"{tag.success} File successfully saved as: {serializer.MAIN_COLOR}{savedAs}{serializer.MAIN_RESET}")
               print(f"{tag.info} Location: {serializer.MAIN_COLOR}{file_path}{serializer.MAIN_RESET}")          
          except Exception as e:
               print(f"{tag.error}Error while download has accured: {e}")

def sendFileToUser(receiver: str):
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     confirm = next((v['code'] for v in var.code if v['code'] == '$fileawait'), "$fileawait")
     sender_data.sendto(confirm.encode(), receiver)