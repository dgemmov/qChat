from src.host import client, server, var
from src import user, control, packet
from src.file import sendFile
import os

sentFileData = None
sentFileName = None

def CheckMessage(data):
     sentData = data.decode(errors='ignore')
     if data.startswith(var.file_flag.encode()): # Here is Gemini Code
          global sentFileData, sentFileName
          
          flag_name_bytes = var.file_flag_name.encode()
          flag_name_index = data.find(flag_name_bytes)
          
          if flag_name_index > len(var.file_flag.encode()):
               sentFileData = data[len(var.file_flag.encode()):flag_name_index]
               sentFileName = data[flag_name_index + len(flag_name_bytes):].decode(errors='ignore')
               
               print("Accept file? (y/n)")
               var.code[0]['state'] = True
               return True
          else:
               print("Critical error! File name flag not found.")
               return True

     if sentData.startswith(var.code[0]['code']):
          return True # Just skip

def MessageHandler():
     global sentFileName, sentFileData
     while 1:  
          msg = input("> ")

          if var.code[0]['state'] == True:
               if msg == control.accept_file_key:
                    print(sentFileName)
                    sendFile.FileSave(name=sentFileName, data=sentFileData)
               var.code[0]['state'] = False

          if msg.startswith('$'):
               for v in var.code:
                    if msg == var.code[0]['code']:
                         v['state'] = not v['state']
                         sendFile.sendFileToUser()

               if msg == "$userlist":
                    for c in server.clients:
                         print(f"{c['ip']} {c['name']}\n")
               
               if msg == "$sendfile":
                    currentUser = str(input("Who is receiver: "))
                    filePath = str(input(f"Path to your file (limit is {packet.packetSize} bytes): "))
                    if os.path.isfile(filePath):
                         size_in_bytes = os.path.getsize(filePath)
                         if server.Server:
                              for c in server.clients:
                                   if currentUser == c['name']:
                                        sentFileName = filePath
                                        sendFile.sendFileRequest(user.returnPersonalIP(), c['ip'], filePath, size_in_bytes)
                                   else:
                                        print("Undefined user")
                         elif client.Client:
                              pass # here will be code where client send request to server to check is exist this user or not
                    else:
                         print("Undefined file")
               msg = None
          
          if msg != None:
               if client.Client:
                    client.client_sock.sendto(f"{user.NAME}: {msg}".encode(), client.server_addr)
               if server.Server:
                    for c in server.clients:
                         server.server_sock.sendto(f"{user.NAME}: {msg}".encode(), c['ip'])

def RecieveHandler():
     while 1:
          if server.Server:
               try:
                    data, addr = server.server_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data): # Intercepts bytes and check it on flag
                         continue 
               except:
                    continue

               if addr not in [c['ip'] for c in server.clients]:
                    decode = data.decode().strip()
                    if decode.startswith("$nm:"):
                         username = decode[4:]
                         server.clients.append({'ip': addr, 'name': username})
                         continue

               if data.decode() == "$nm:": # skip check if the user was connected before
                    continue

               for c in server.clients:
                    if(c['ip'] != addr):
                         server.server_sock.sendto(data, c['ip'])
               print(f"{data.decode()}")

          if client.Client:
               try:
                    data, addr = client.client_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data): # Intercepts bytes and check it on flag
                         continue 

                    print(f"{data.decode()}") # In the end cause check continue which is upper than sending

               except:
                    continue