import socket, ssl


def main():
# Instantiate a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')
    HOST = 'localhost'
    PORT = 65439

    ACK_TEXT = 'text_received'
    # Require a certificate from the server. We used a self-signed certificate
    # so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,
                               ssl_version = ssl.PROTOCOL_TLS,
                               ca_certs="server.crt",
                               cert_reqs=ssl.CERT_REQUIRED,
                               ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")

    ssl_sock.connect((HOST, PORT))


    while  True:
        print("Introduzca el mensaje. Escriba 'salir' para salir")
        mensaje = input()
        
        #invoco  el metodo send pasando como parametro el string ingresado por el  usuario
        if(mensaje=="salir"):
            break
        else:
            print('sending: ' + mensaje)
            ssl_sock.write(mensaje.encode('utf-8'))
            respuesta = ssl_sock.recv(1024)
            print(respuesta)



    


if __name__ == '__main__':
    main()