import socket

HOST = ('127.0.0.1', 7771)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)

# sock.send(b'0123456789')
# sock.send('0123456789'.encode())
# sock.send('0123456789 Hello Вася'.encode("utf-8")) # отправляет столько сколько принимают
sock.sendall('0123456789 Hello Вася'.encode("utf-8")) # отправляет все
data = sock.recv(1024).decode() # ждем отправки ответа
print(data) # печатаем ответ




# ===================================
# если сервер принимает маленькими пакетами например по 2 байта
# отправляем до  тех пор пока все не примут
# req = b"GET / HTTP/1.1"
# sent = 0
# while sent <len(req):
#     sent = sent + sock.send(req[sent:])
    
# sock.close()    



