import socket
import threading
import json
from random import randint 
import time

HOST = '127.0.0.1'
PORT = 12345
MAX_PLAYERS = 15
size, x, y = (600,400), 0, 1
colors = [
    'orange',       # Чёрный
    'darkslategrey', # Темно-серый
    'darkslateblue', # Темно-синий
    'indigo',      # Индиго
    'darkred',     # Темно-красный
    'darkmagenta', # Темно-фиолетовый
    'darkgrey',    # Глубокий серый
    'darkslategrey', # Почти чёрный
    'maroon',      # Темно-красный
    'navy',        # Морской синий
    'darkred',     # Темно-красный
    'darkblue',    # Темно-синий
    'darkgrey',    # Глубокий серый
    'darkslategrey', # Почти чёрный
    'darkblue'     # Темно-синий
]


class TurtleServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.turtles = {}
        self.connections = {}  # Храним соединения по ID
        self.lock = threading.Lock()
        self.client_num = 0
        print(f"Сервер запущен на {HOST}:{PORT}")

    def handle_client(self, conn, addr, client_n):
        turtle_id = f"{addr[0]}:{addr[1]}"
        color = colors[client_n-1]
        posx = randint(int(-size[x]/2), int(size[x]/2))
        posy = randint(int(-size[y]/2), int(size[y]/2))
        
        with self.lock:
            self.turtles[turtle_id] = {
                    'x': posx, 'y': posy, 
                    'color': color,
                    'angle': 0}
            self.connections[turtle_id] = conn  # Сохраняем соединение
        
        data = json.dumps({
            'id': turtle_id,
            'posx': posx, 'posy':posy,
            'color': color})
        data += "%^%"
        conn.send(data.encode())
        
        while True:
            try:
                data = conn.recv(1024).decode().split("%^%")[0] 
                # Обновляем позицию текущей черепахи
                if data :
                    print(11, client_n, data)               
                    with self.lock:
                        self.turtles[turtle_id].update(json.loads(data))
                        # Рассылаем обновления всем клиентам
                        broadcast_data = json.dumps(self.turtles)
                        for client_id in self.connections:
                            # if client_id != turtle_id:
                                try:
                                    broadcast_data += "%^%"
                                    self.connections[client_id].send(broadcast_data.encode())
                                    print(22, broadcast_data)
                                    
                                except:
                                    pass
            except Exception as e:
                print(e)
                break
        
        with self.lock:
            del self.turtles[turtle_id]
            del self.connections[turtle_id]
        conn.close()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            if self.client_num < MAX_PLAYERS:
                self.client_num += 1
                print(f'------- {self.client_num} -------',addr)
                client_thread = threading.Thread(target=self.handle_client, 
                                             args=(conn, addr, self.client_num))
                conn.send(json.dumps({"ok":"Вы подключены", "num":self.client_num}).encode())
                client_thread.start()
            else:
                conn.send(json.dumps({"err":"Больше нельзя. Сервер заполнен"}).encode())
                conn.close()


if __name__ == "__main__":
    server = TurtleServer()
    server.run()