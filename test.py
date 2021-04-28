import socket, ssl
from time import sleep
from _thread import *

global ready 
ready=True

def test(contador):

# Instantiate a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = 'localhost'
    PORT = 65439

    ACK_TEXT = 'text_received'
    # Require a certificate from the server. We used a self-signed certificate
    # so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,
                               ssl_version=ssl.PROTOCOL_SSLv23,
                               ca_certs="server.crt",
                               cert_reqs=ssl.CERT_REQUIRED,
                               ciphers="ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")

    ssl_sock.connect((HOST, PORT))

    elementos = list()
    elementos.extend(['user1', 'pass1', str(contador)])

    mensaje = ','.join(x for x in elementos)
    while ready:
        sleep(1)
    # Se invoca el metodo send pasando como parametro el string ingresado por el usuario
    print('sending: ' + mensaje)
    ssl_sock.write(mensaje.encode('utf-8'))
    respuesta = ssl_sock.recv(1024)

    
    ssl_sock.close()   


if __name__ == '__main__':
    sleep(1)
    for i in range (301):
        print(i)
        start_new_thread(test, (i,))
        sleep(0.005)
    ready=False
    sleep(5)
    file = open("mensajes.txt", "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    if(line_count>=300):
        print("Se han recibido todos los mensajes")
    sleep(3)