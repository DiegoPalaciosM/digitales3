import threading
def hilo1():
    while True:
        #Accion a ejecutar hilo1

def hilo2():
    while True:
        #Accion a ejecutar hilo1

x = threading.Thread(target=hilo1)
y = threading.Thread(target=hilo2)
x.start()
y.start()
while True:
    #Accion principal
