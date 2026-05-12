from src.host import client, server, var
from src import user
from src.file import sendFile
import os

def MessageHandler():
     while 1:  
          msg = input("> ")

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
                    filePath = str(input("Path to your file (<= 25mb): "))
                    if os.path.isfile(filePath):
                         size_in_bytes = os.path.getsize(filePath)
                         for c in server.clients:
                              if currentUser == c['name']:
                                   # sendFile.sendFileRequest(server.getUserName(user.returnPersonalIP()), c['ip'], filePath, size_in_bytes)
                                   sendFile.sendFileRequest('127.0.0.1', c['ip'], filePath, size_in_bytes)
                              else:
                                   print("Undefiend user")
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
                    data, addr = server.server_sock.recvfrom(1024)
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
                    data, addr = client.client_sock.recvfrom(1024)
                    print(f"{data.decode()}")
               except:
                    continue

               if data.decode().strip() == var.code[0]['code']:
                    sendFile.AwaitChoice()

               sentFileByte = data.decode(errors='ignore')
               if sentFileByte.startswith(var.file_flag):
                    sentFileData = sentFileByte[len(var.file_flag):] 
                    print(sentFileData) 