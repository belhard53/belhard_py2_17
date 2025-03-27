import asyncio
import time
from aiohttp import ClientSession
import requests

n_step:int = 0

async def aget_weather(city:str, n_city):
    '''
    асинхронная функция получения погоды
    '''
    global n_step
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()            
            
            # принт не асинхронный,  но это конечная точка и выполняется очень быстро            
            n_step += 1 
            print(f'{n_step} - {n_city} {city}: {weather_json["weather"][0]["main"]}')
    

def get_weather(city):    
    '''
    синхронная функция получения погоды
    '''
    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
    res = requests.get(url, params) # делаем GET запрос
    # res.content
    # res.text
    res = res.json() # так как возвращают json, конвертируем его в словарь
    # pprint(res)        
    print(f'{city}: {res["weather"][0]["main"]}')

# import pprint
# pprint.pprint()    


async def async_main(cities_):
    tasks = []
    for i, city in enumerate(cities_):
        tasks.append(asyncio.create_task(aget_weather(city, i)))

    for task in tasks:
        await task
        

def main(cities_):    
    for city in cities_:
        get_weather(city)

    


cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
          'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']


t = time.time()


# 2 варианта на выбор
asyncio.run(async_main(cities*4)) # асинхронный вариант
# main(cities) # синхронный вариант

print(time.time() - t)