import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.21.35"
ADDR = (SERVER, PORT)

print("[CLIENT] Client Started! {ADDR}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

target_input = input()
while target_input != DISCONNECT_MESSAGE:
    send(target_input)
    target_input = input()

send(DISCONNECT_MESSAGE)