import asyncio

clients = []

class SimpleChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print('Подключился: {}'.format(self.peername))
        clients.append(self)

    def data_received(self, data):
        print('{} отправил: {}'.format(self.peername, data.decode()))
        for client in clients:
            if client is not self:
                client.transport.write(data)

    def connection_lost(self, ex):
        print('Отключился: {}'.format(self.peername))
        clients.remove(self)


# Цикл событий невозможно прервать, если в нём
# не происходят события. Чтобы избежать этого
# регистрируем в цикле фунцию, которая будет 
# вызываться раз в секунду.
def wakeup():
    loop = asyncio.get_event_loop()
    loop.call_later(1, wakeup)


if __name__ == '__main__':
    print('Запуск...')

    # Получаем цикл событий
    loop = asyncio.get_event_loop()
    # Регистрируем "отлипатель"
    loop.call_later(1, wakeup)
    # Создаём асинхронную сопрограмму-протокол
    coro = loop.create_server(SimpleChatClientProtocol, host='localhost', port=7771)
    # Регистрируем её в цикле событий на выполнение
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        print('Сервер запущен на {}'.format(socket.getsockname()))
    print('Выход по Ctrl+C\n')

    try:
        loop.run_forever() # Запускаем бесконечный цикл событий
    except KeyboardInterrupt: # Программа прервана нажатием Ctrl+C
        pass
    finally:
        server.close() # Закрываем протокол
        loop.run_until_complete(server.wait_closed()) # Асинхронно ожидаем окончания закрытия
    loop.close() # Закрываем цикл событий