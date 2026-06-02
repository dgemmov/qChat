from src.host import client, server, var
from src import user, control, packet, tag, serializer, console, menu
from src.file import sendFile
from src.crypto import key_generation, crypto_main
from colorama import ansi, Cursor
import datetime
import os

sentFileSender = "Unknown"
sentFileData = None
sentFileName = None
ReceiverStatus = False

def CheckMessage(data, addr=None):
     if not data: return True
     
     sentData = data.decode(errors='ignore')
     if data.startswith(var.file_flag.encode()): # Here is Gemini Code
          global sentFileData, sentFileName, sentFileSender
          
          flag_name_bytes = var.file_flag_name.encode()
          flag_sender_bytes = var.file_flag_sender.encode()

          flag_name_index = data.find(flag_name_bytes)
          flag_sender_index = data.find(flag_sender_bytes)
          
          if flag_name_index > len(var.file_flag.encode()) and flag_sender_index > flag_name_index:
               sentFileData = data[len(var.file_flag.encode()):flag_name_index]
               
               sentFilePath = data[flag_name_index + len(flag_name_bytes):flag_sender_index].decode(errors='ignore')
               sentFileName = os.path.basename(sentFilePath)
               
               sentFileSender = data[flag_sender_index + len(flag_sender_bytes):].decode(errors='ignore').strip()

               sendFile.getFileRequest(filename=sentFileName, data=sentFileData, senderName=sentFileSender)               
               request = next((v for v in var.code if v['code'] == '$filerequest'), None)
               if request:
                    request['state'] = True

               return True
          else:
               print(f"{tag.error}File name flag not found.")
               return True

     if sentData.startswith(var.server_send_kick):
          kicked = sentData[len(var.server_send_kick):]
          if user.returnUsername() == kicked or kicked == "everybody":
               packet.SendDisconnect()
               print(f"{tag.info}Write $exit to leave the session.")

          return True

     if client.Client:
          if data.startswith(var.crypto_key_flag.encode()):
               server_pub_bytes = data[len(var.crypto_key_flag.encode()):]
               client_pub_bytes, client_private_key = crypto_main.generateDHKeys()
               client_private_dh = client_private_key

               client.temp_cipher = crypto_main.deriveTemporaryKey(server_pub_bytes, client_private_dh) # Create a temporary cipher on the client side
               client.client_sock.sendto(var.client_pub_flag.encode() + client_pub_bytes, client.server_addr)
               return True

          if data.startswith(var.room_key_flag.encode()):
               encrypted_room_key = data[len(var.room_key_flag.encode()):]
               decrypted_room_key = client.temp_cipher.decrypt(encrypted_room_key)
               crypto_main.setRoomKey(decrypted_room_key)
               return True

     if server.Server:
          if data.startswith(var.client_pub_flag.encode()):
               client_pub_bytes = data[len(var.client_pub_flag.encode()):]
               user_ip = addr[0] if isinstance(addr, tuple) else addr
               target = next((c for c in server.clients if (c['ip'][0] if isinstance(c['ip'], tuple) else c['ip']) == user_ip), None)

               fallback_key = server.clients[-1]['private_key'] if server.clients else None
               private_key = target['private_key'] if (target and 'private_key' in target) else fallback_key
               
               if getattr(var, 'DEBUG', True):
                    print(f"\n{tag.info} Received a pub_key from {addr}. Belongs to {target['name'] if target else 'nobody'}")

               if private_key:
                    temp_cipher = crypto_main.deriveTemporaryKey(client_pub_bytes, target['private_key'])
               else:
                    temp_cipher = None
                    if getattr(var, 'DEBUG', True):
                         print(f"{tag.error} Couldn't find any client with IP {addr[0]}!")
               
               if temp_cipher:
                    if getattr(var, 'DEBUG', True):
                         print(f"{tag.success}Successfully created a temp_cipher for {addr}!")

                    from src.crypto import key_generation
                    if not key_generation.key:
                         crypto_main.generateRoomKey()

                    encrypted_room_key = temp_cipher.encrypt(key_generation.key.encode())
                    if addr:
                         server.server_sock.sendto(var.room_key_flag.encode() + encrypted_room_key, addr)
                         if getattr(var, 'DEBUG', True):
                              print(f"{tag.info} Sent encrypted_room_key to {addr}")
               return True

     if any(sentData.startswith(v['code']) for v in var.code):
          return True # Just skip

def MessageHandler():
     global sentFileName, sentFileData, msg
     while 1:  
          timestamp = datetime.datetime.now().strftime("%H:%M:%S")
          msg = input(f"{serializer.INPUT_SYMBOL}")

          if not msg.strip():
               continue

          if msg.startswith('$'):
               print(Cursor.UP(1) + "\r" + ansi.clear_line(), end="")
               print(msg)

               cmd_list = ["$help", "$cmds", "$userlist", "$sendfile", "$clear", "$exit"]

               code = next((v for v in var.code if v['code'] == msg), None)
               if code != None:
                    code['state'] = not code['state']
                    sendFile.sendFileToUser()
                    cmd_list.append(msg)
               
               if msg == "$help" or msg == "$cmds":
                    hint = (
                         f"\n{tag.info} Available commands:\n"
                         f" {serializer.MAIN_COLOR}$help{serializer.MAIN_RESET} or {serializer.MAIN_COLOR}$cmds{serializer.MAIN_RESET} - Show this exact message.\n"
                         f" {serializer.MAIN_COLOR}$userlist{serializer.MAIN_RESET} - Show all connected users.\n"
                         f" {serializer.MAIN_COLOR}$sendfile{serializer.MAIN_RESET} - Send a file to somebody.\n"
                         f" {serializer.MAIN_COLOR}$clear{serializer.MAIN_RESET} - Clear your chat history (client-side).\n"
                         f" {serializer.MAIN_COLOR}$exit{serializer.MAIN_RESET} - Disconnect."
                    )
                    print(hint)

               elif msg == "$userlist":
                    for c in server.clients:
                         print(f"{c['ip']} {c['name']}\n")
               
               elif msg == "$sendfile":
                    currentUser = str(input("Who is receiver: "))
                    requestPath = str(input(f"Path to your file (limit is {packet.packetSize} bytes): "))
                    filePath = requestPath.strip('"\'')
                    if os.path.isfile(filePath):
                         size_in_bytes = os.path.getsize(filePath)
                         if server.Server:
                              target = next((c for c in server.clients if c['name'] == currentUser), None)
                              if target:
                                   sentFileName = filePath
                                   sendFile.sendFileRequest(user.returnUsername(), target['ip'], filePath, size_in_bytes, "None") # Fixed error with file sending
                              else:
                                   print(f"{tag.warning}Undefined user")
                         elif client.Client:
                              sendFile.sendFileRequest(user.returnUsername(), '0.0.0.0', filePath, size_in_bytes, currentUser)
                    else:
                         print(f"{tag.warning}Undefined file")

               elif msg == "$clear": # only visual chat history cleaning
                    console.clear()

               elif msg == "$exit": # Server disconnect
                    global RecieverStatus
                    RecieverStatus = False

                    packet.SendDisconnect()
                    console.clear()
                    menu.Menu()

               elif msg not in cmd_list:
                    print(f"{tag.error} Unknown command: {serializer.MAIN_COLOR}{msg}{serializer.MAIN_RESET}. Check {serializer.MAIN_COLOR}$help{serializer.MAIN_RESET} for commands.")

               continue

          formatted_msg = f"[{timestamp}] You: {msg}"
          print(f"\033[F\033[K{formatted_msg}")
          
          if msg != None:
               message = f"[{timestamp}] {user.NAME}: {msg}"
               encrypted_message = crypto_main.returnEncrypted(message)

               if encrypted_message == None:
                    print(f"{tag.warning} Wait awhile... Getting your connection secured...")
                    continue

               if client.Client:
                    client.client_sock.sendto(encrypted_message, client.server_addr)
               if server.Server:
                    for c in server.clients:
                         server.server_sock.sendto(encrypted_message, c['ip'])

def RecieveHandler(status: bool):
     global RecieverStatus
     RecieverStatus = status
     while RecieverStatus:
          if server.Server:
               try:
                    data, addr = server.server_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data, addr): # Intercepts bytes and check it on flag
                         continue 
               except Exception as e:
                    if getattr(var, 'DEBUG', True):
                         print(f"{tag.error}Caught server exception while receiving data: {e}")
                    continue
               
               try:
                    user_ip = addr[0] if isinstance(addr, tuple) else addr
                    all_ips = [(c['ip'][0] if isinstance(c['ip'], tuple) else c['ip']) for c in server.clients]
                    if user_ip not in all_ips:
                         decode = data.decode(errors='ignore').strip()
                         if decode.startswith("$nm:"):
                              username = decode[4:]
                              server_pub_bytes, server_private_key = crypto_main.generateDHKeys()

                              if getattr(var, 'DEBUG', True):
                                   print(f"\n{tag.info}Created a private key for {username} ({addr}).")
                              # Send Cipher to connected Client
                              server.clients.append({'ip': addr, 'name': username, 'private_key': server_private_key})
                              server.server_sock.sendto(var.crypto_key_flag.encode() + server_pub_bytes, addr)
                              continue

                    if data.decode(errors='ignore') == "$nm:": # skip check if the user was connected before
                         continue

                    for c in server.clients:
                         if(c['ip'] != addr):
                              server.server_sock.sendto(data, c['ip'])

                    print("\r\033[K", end="")
                    print(f"{crypto_main.returnDecrypted(data)}")
                    print(f"{serializer.INPUT_SYMBOL}", end="", flush=True)
               except Exception as e:
                    if getattr(var, 'DEBUG', True):
                         print(f"{tag.error}Caught an exception while parsing packet content: {e}")
                    continue

          if client.Client:
               try:
                    data, addr = client.client_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data, addr): # Intercepts bytes and check it on flag
                         continue 

                    print("\r\033[K", end="")
                    print(f"{crypto_main.returnDecrypted(data)}") # In the end cause check continue which is upper than sending
                    print(f"{serializer.INPUT_SYMBOL}", end="", flush=True)

               except Exception as e:
                    if getattr(var, 'DEBUG', True):
                         print(f"{tag.error}Caught client exception while receiving data: {e}")
                    continue