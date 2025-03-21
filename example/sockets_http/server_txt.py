import socket

# HOST = socket.gethostname()


HOST = ('127.0.0.1', 7771)

# print(HOST)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen()


print("----start-----")
while True:
    print("---listen----")
    conn, addr = sock.accept()    
    # print(conn)
    # print(addr)
    
    # ------------------------
    # получит все данные
    data = conn.recv(1024).decode()
    print(data)
    conn.send(f"Данные получены - {data[::-1]}".encode())    
    
    # ----------------------------
    # получит только 4 байта, неважно send или sendall
    # data = conn.recv(4).decode()
    # print(data)
    # conn.send(f"Данные получены - {data[::-1]}".encode())    
    
    
    # # -----------------------------    
    # # для получения данных частями например по 2 байта    
    # while True:
    #     data = conn.recv(2) # если соединение не закрыто клиентом залипает на этой строчке                
    #     if not data:            
    #         break
    #     print(data)
    
    

    if data == 'stop':
        break
    
    

print("end")





