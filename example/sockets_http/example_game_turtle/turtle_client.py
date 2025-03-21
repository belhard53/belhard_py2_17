# Клиент (client.py)
import socket
import turtle

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

screen = turtle.Screen()
screen.setup(600, 600)

t = turtle.Turtle('turtle')
t.speed(0)
t.color('blue')

def move_up():
    t.setheading(90)
    t.forward(10)
    sock.sendall(b'UP')

def move_down():
    t.setheading(270)
    t.forward(10)
    sock.sendall(b'DOWN')

def move_left():
    t.setheading(180)
    t.forward(10)
    sock.sendall(b'LEFT')

def move_right():
    t.setheading(0)
    t.forward(10)
    sock.sendall(b'RIGHT')

screen.onkey(move_up, 'Up')
screen.onkey(move_down, 'Down')
screen.onkey(move_left, 'Left')
screen.onkey(move_right, 'Right')
screen.listen()


screen.mainloop()
sock.close()
