import requests
# param = {'q':123}
# res = requests.get("http://127.0.0.1:8000/", params=param)
res = requests.post("http://127.0.0.1:8600/quizes/1/link?question_id=q")
print(res.text)

# for i in range(100):
#     p = {'name':f"user_{i}", 'age':33, 'phone':f'123456{i}'}
#     res = requests.post("http://127.0.0.1:8300/users", params=p)
#     print(res.text)