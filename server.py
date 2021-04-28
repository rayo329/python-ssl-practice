import pickle
import ssl
import socket
import select
from _thread import *
import collections

''' Socket variables '''
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65439

ACK_TEXT = 'text_received'

ServerSocket = socket.socket()


ServerSocket.bind((HOST, PORT))


print('Waiting for a Connection..')
ServerSocket.listen(5)

#Receives messages from the client
def receiveTextViaSocket(sock):
    # Gets the text via the socket
    try:

        while True:

            encodedMessage = sock.recv(1024)

            # Decodes the received text message
            message = encodedMessage.decode('utf-8')
            c = collections.Counter(message)
            if(c[","]>=2):
                
                recibido = message.split(",")

                username = recibido[0]

                password = recibido[1]

        
                dictAcc = {}
                with open("dict.txt") as f:
                    for line in f:
                        (key, val) = line.rstrip().split(",")
                        dictAcc[key] = val

                for key in dictAcc:
                    if (username == key and password == dictAcc[key]):
                        answer = "Usuario verificado, mensaje recibido"
                        mensaje=""
                        i=0
                        for element in recibido:
                            if(i>=2):
                                mensaje = mensaje + "," + element
                                i=i+1
                        print(mensaje)
                        f= open("mensajes.txt","a")
                        f.write(message.split(",")[2] + "\n")
                        f.close()
                        break;
                    else:
                        answer = "Usuario incorrecto, mensaje ignorado"
                
                verified = bytes(answer, 'utf-8')
                sock.sendall(verified)
            else:
                answer = "Usuario incorrecto, mensaje ignorado"
                verified = bytes(answer, 'utf-8')
                sock.sendall(verified)
    except Exception:
        pass
    
    

while True:
    Client, address = ServerSocket.accept()
    
    connstream = ssl.wrap_socket(Client,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")
    start_new_thread(receiveTextViaSocket, (connstream,))

ServerSocket.close()
