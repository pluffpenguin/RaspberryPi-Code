import socket
from module_led import ModuleLed

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.21.35"
SERVER = str(input("[INPUT] What is the SERVER? "))
ADDR = (SERVER, PORT)

print("[CLIENT] Client Started! {ADDR}")

moduleLed = ModuleLed()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def parseColor(message):
    message = message[2:]
    message = message.split(', ')
    for i in range(0, len(message)):
        message[i] = int(message[i])
    return message

def parseBrightness(message) -> int:
    message = message[2:]
    message = message[:message.find("B:")]
    message = int(message)
    return message

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    
    client.send(send_length)
    client.send(message)
    server_message = client.recv(2048).decode(FORMAT)
    print(f'[SERVER_RESPONSE] {server_message}')
    if server_message[0] == "C":
        color = parseColor(server_message)
        print(f'[RETURN] Color: {color}')
        moduleLed.setAllLeds(color)
    elif server_message[0]== "B":
        brightness = parseBrightness(server_message)
        moduleLed.setBrightness(brightness)
            
        

target_input = input()
while target_input != DISCONNECT_MESSAGE:
    send(target_input)
    target_input = input()

send(DISCONNECT_MESSAGE)