
def funcion(mensaje):
        import socket
        import time
        IP_address = '192.168.0.8'
        Port = 42777
        server_address = (IP_address, Port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        message = mensaje
        sock.send(message.encode("utf-8"))
        time.sleep(0.5)
        sock.close()
