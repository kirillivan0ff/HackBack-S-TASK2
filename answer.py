import urllib.request
import socket
import time

ACTIVE = False
NUMBER = float(0)
DEFAULT_PAGE = str(urllib.request.urlopen("http://10.10.230.181:3010/").read())
PORT = int(DEFAULT_PAGE[int(DEFAULT_PAGE.find("onPort")) + 8 : int(DEFAULT_PAGE.find("onPort")) + 12])
HOST = '10.10.230.181'
SERVER_REPLY = ''
STEP = 0

print('Waiting for Port 1337 to start calculation...')
while not ACTIVE:
    time.sleep(4)
    if (str(urllib.request.urlopen("http://10.10.230.181:3010/").read())[864:868]) == '1337':
        print("Port active!")
        PORT = int(str(urllib.request.urlopen("http://10.10.230.181:3010/").read())[864:868])
        ACTIVE = True

while ACTIVE:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % HOST
    s.send(request.encode())

    data = s.recv(4096)

    while len(data) > 0:
        SERVER_REPLY += str(data)
        data = s.recv(4096)
    print("-----------------------------")
    STEP += 1
    print(f"Step {STEP}")
    SERVER_REPLY = (str(SERVER_REPLY[171:len(SERVER_REPLY) - 1])).split(' ')

    if PORT == int(SERVER_REPLY[2]):
        time.sleep(1)
    PORT = int(SERVER_REPLY[2])

    print(f'Action: {SERVER_REPLY} Next port: {PORT}')

    if SERVER_REPLY[0] == 'add':
        NUMBER += float(SERVER_REPLY[1])
    elif SERVER_REPLY[0] == 'minus':
        NUMBER -= float(SERVER_REPLY[1])
    elif SERVER_REPLY[0] == 'divide':
        NUMBER = NUMBER/float(SERVER_REPLY[1])
    elif SERVER_REPLY[0] == 'multiply':
        NUMBER = NUMBER * float(SERVER_REPLY[1])

    if SERVER_REPLY == "STOP" or PORT == 9765:
        ACTIVE = False

    print("-----------------------------")
    SERVER_REPLY = ''
    print(f'Current number: {NUMBER}')
    time.sleep(4)

print("The answer is {:.2f}".format(NUMBER))
