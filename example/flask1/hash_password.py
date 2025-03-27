
import os 
import hashlib


# вариант с рандомной солью
salt = os.urandom(32) # возвращает случайные байты - после этого соль сохраняется вместе с паролем
password = 'pas1234'
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
saved_pas = salt + key
# print(saved_pas)

# проверка
send_pas = 'pas1234'
right_pas = saved_pas[32:]
new_kew = hashlib.pbkdf2_hmac('sha256', 
                    password=send_pas.encode('utf-8'), salt=saved_pas[:32], 
                    iterations=100000)
if new_kew == right_pas:
    print('Ok')



# -------------------------------------------
# вариант с одинаковой солью 
password = 'pas1234'
salt = 'salt1234'
password += salt
saved_pas = hashlib.sha256(password.encode('utf-8')).hexdigest()
# print(saved_pas) # Выводим зашифрованный пароль

# проверка
send_pas = 'pas1234'
salt = 'salt1234'
password += salt
hash = hashlib.sha256(f"{send_pas}{salt}".encode('utf-8')).hexdigest()
if hash==saved_pas:
    print('Ok')