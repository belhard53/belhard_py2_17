https://cloud.google.com/?hl=ru  
жмем  - Get started for free - отвечаем на вопросы, вводим карту  

создать ВМ  
создать правило фаервола на нужный порт  
открыть консоль SSH (можно открывать несколько консолей и в каждой что-то запустить)  

обновляем индексы пакетов(программ)  
`sudo apt update`  

далее устанавливает сразу все нужные пакеты  
`sudo apt install -y git python3-dev python3-venv python3-pip`  

клонируем свой проект flask с гитХаб  
переходим в папку с проектом  

создаем и активируем виртуальное окружение  
`python3 -m venv venv`  
`source venv/bin/activate`  

устанавливаем нужные библиотеки  
`pip install flask`  
`pip install gunicorn`  
или  
`pip install -r requirements.txt`  

убедиться в том что в главном файле flask нет строчки app.run()  

запускаем gunicorn  
`gunicorn main:app -w 4 -b 0.0.0.0:5000`  
    *где main - название главного файла, app - переменная в нем содержащая flask*

проверяем работу сайта















