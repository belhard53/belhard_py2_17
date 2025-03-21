# Сервер (server.py)
import socket
import turtle

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print("Сервер запущен. Ожидание подключения...")

conn, addr = sock.accept()
print(f"Подключение от {addr}")

screen = turtle.Screen()
screen.setup(600, 600)
server_turtle = turtle.Turtle('turtle')
server_turtle.speed(0)
server_turtle.color('red')

while True:
    print(1)
    try:
        data = conn.recv(5)
        if not data:
            break
        command = data.decode()
        if command == 'UP':
            server_turtle.setheading(90)
            server_turtle.forward(10)
        elif command == 'DOWN':
            server_turtle.setheading(270)
            server_turtle.forward(10)
        elif command == 'LEFT':
            server_turtle.setheading(180)
            server_turtle.forward(10)
        elif command == 'RIGHT':
            server_turtle.setheading(0)
            server_turtle.forward(10)
    except:
        break

conn.close()
sock.close()
