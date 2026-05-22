import time

packetSize = 4096 # Bytes
port = 5005 # It will be ready for use soon
sock = None # Switch sended packet (To client or to server)

def SendTimeout():
     time.sleep(0.05) # Timeout