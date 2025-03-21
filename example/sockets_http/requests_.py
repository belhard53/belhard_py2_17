import requests

# бомбим наш сервер запросами
# ответ должен быть HTTP - иначе выдаст ошибку
for i in range(10):
    url = 'http://127.0.0.1:7771/users.json'
    # res = requests.post(url, params={'q':'qq'}, data=f"HELO", headers={"h1":"hh12"})
    res = requests.get(url, params={'q1':'123'})
    text = res.text
    print(res, text)