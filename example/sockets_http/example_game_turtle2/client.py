# нужен пайтон 3.12 и меньше т.к. в этой потоки работают с ошибкой

import socket
import json
import turtle
import threading
import time



HOST = '127.0.0.1'
PORT = 12345
size, x, y = (620,420), 0, 1

class TurtleClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))        
        data = json.loads(self.sock.recv(1024).decode())        
        err = data.get('err')        
        if err:
            self.running = False
            print(err)
        else:
            print(data.get('ok'))
            
            self.setup_turtle()
            self.running = True
            

    def setup_turtle(self):
        data = self.sock.recv(1024).decode().split("%^%")[0]
        data = json.loads(data)
        print(data)
        turtle.setup(width=size[0], height=size[1])
        self.turtle_id = data['id']
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.color(data['color'])
        self.t.shape('turtle')
        self.t.pu()
        self.t.goto(data['posx'], data['posy'])
        self.t.pd()
        self.t.showturtle()
        self.other_turtles = {}
        self.pen = True
        
        
        

        
        

    def send_updates(self):
        
            pos = list(map(int,self.t.position()))
            data = json.dumps({'x': pos[0], 'y': pos[1],
                               'angle':self.t.heading()})
            try:
                
                data+="%^%"
                self.sock.send(data.encode())
            except Exception as e:          
                print(1, e)
                

    def receive_updates(self):
        while self.running:
            try:
                data = self.sock.recv(4096).decode().split("%^%")[0]
                print(data)                
                data = json.loads(data)
                print(data)
                self.update_all(data)
            except Exception as e:
                print(2, e)
                # break
    
    def update_all(self, data):
        for tid, state in data.items():
            if tid not in self.other_turtles and tid != self.turtle_id:
                # Создаем новую черепаху для других клиентов
                t = turtle.Turtle()
                t.color(state['color'])
                t.shape('turtle')
                t.speed(0)
                t.penup()
                t.hideturtle()
                self.other_turtles[tid] = t
            if tid in self.other_turtles:
                # Обновляем позицию
                if tid != self.turtle_id:
                    self.other_turtles[tid].goto(state['x'], state['y'])
                    self.other_turtles[tid].setheading(state['angle'])
                    self.other_turtles[tid].pd()
                    self.other_turtles[tid].showturtle()
            
    
    
    def go_up(self):
         self.t.setheading(90)
         self.t.fd(5)
         self.send_updates()
    def go_down(self):
         self.t.setheading(270)
         self.t.fd(5)
         self.send_updates()
    def go_left(self):
         self.t.setheading(180)
         self.t.fd(5)
         self.send_updates()
    def go_right(self):
         self.t.setheading(0)
         self.t.fd(5)
         self.send_updates()
        
    def change_pen(self):
        if self.pen:
            self.t.pd()            
        else:
            self.t.pu()
        self.pen = not self.pen

    def key_controls(self):
        screen = turtle.Screen()
        screen.onkey(self.go_up, 'Up')
        screen.onkey(self.go_left, 'Left')
        screen.onkey(self.go_right, 'Right')
        screen.onkey(self.go_down, 'Down')        
        screen.onkey(self.go_down, 'Down')        
        screen.listen()

    def run(self):
        send_thread = threading.Thread(target=self.send_updates)
        recv_thread = threading.Thread(target=self.receive_updates)
        
        send_thread.daemon = True
        recv_thread.daemon = True
        
        send_thread.start()
        recv_thread.start()
        
        self.key_controls()
        
        turtle.mainloop()
        # turtle.done()
        print('----------------end---------------')
        self.running = False
        self.sock.close()

if __name__ == "__main__":
    try:
        client = TurtleClient()
        if client.running:
            client.run()
    except Exception as e:
        print(e)
