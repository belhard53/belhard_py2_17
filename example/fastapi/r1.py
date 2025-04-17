import requests
# param = {'q':123}
# res = requests.get("http://127.0.0.1:8000/", params=param)

for i in range(1000):
    p = {'name':f"user_{i}", 'age':33, 'phone':f'123456{i}'}
    res = requests.post("http://127.0.0.1:8200/users", params=p)
    print(res.text)