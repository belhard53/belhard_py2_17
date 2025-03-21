import select
import socket
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0) # Неблокирующийся сокет
server.bind(('localhost', 7771))
server.listen()

sockets = [server]
message_queues = {}

def close_connection(con):
    sockets.remove(con)
    if con in message_queues:
        del message_queues[con]
    con.close()


# Пока есть хоть один сокет
while sockets:
    # Опрашиваем сокеты на готовность к чтению, записи, ошибки.
    # С таймаутом в 1 секунду для того, чтобы программа реагировала
    # на другие события.
    readable, writable, exceptional = select.select(sockets, sockets, sockets, 1)

    for s in readable: # Для каждого сокета готового к чтению
        if s is server: # Если это сокет принимающий соединения
            connection, client_address = s.accept()
            connection.setblocking(0) # Этот клиентский сокет тоже будет неблокируемым
            sockets.append(connection) # Добавляем клиентский сокет в список сокетов
            message_queues[connection] = queue.Queue() # Создаём очередь сообщений для сокета
        else:
            try:
                data = s.recv(1024) # Читаем без блокировки
            except:
                close_connection(s) # В случае ошибки закрываем этот сокет и удаляем
            else: # Если ошибка не произошла
                if data: # И данные получены
                    for c in message_queues: # Обходим все очереди сообщений
                        if c != s: # Кроме очереди текущего сокета
                            message_queues[c].put(data) # Отправляем данные в каждую очередь
                else:
                    # Если данных нет в сокете готовом для чтения
                    # значит он в состоянии закрытия на клиентской
                    # стороне. Закрываем его на стороне сервера.
                    close_connection(s)

    for s in writable: # Для каждого сокета готового к записи
        try:
            next_msg = message_queues[s].get_nowait() # Получаем сообщение из очереди
        except queue.Empty:
            pass # Игнорируем пустые очереди
        except KeyError:
            pass # Игнорируем очереди удалённые до того, как до них дошла очередь обработки
        else:
            s.send(next_msg) # Отправляем без блокировки

    for s in exceptional: # Для каждого сбойного сокета
        close_connection(s) # Закрываем сбойный сокет