from celery import Celery

from celery.exceptions import So

app = Celery('example', broker='redis')


@app.task
def add1(a, b):
    return a + b


@app.task(ignore_result=True)
def add2(x, y):
    return x + y


@app.task(rate_limit='10/m')
def add3(x, y):
    return x + y



@app.task(bind=True, max_retries=3, default_retry_delay=60)
def add(self, x, y):
    
    
result = add.delay(4, 4)        



#apply_async() предлагает больше гибкости, позволяя указать различные 
# параметры выполнения: время и приоритет выполнения, а также колбэки и errbacks:
result = add.apply_async((4, 4), countdown=10)



#chain() позволяет соединить несколько задач в одну последовательность, 
# где результат одной задачи передается в качестве аргумента следующей:
from celery import chain
# (4 + 4) -> (8 * 10)
res = chain(add.s(4, 4), multiply.s(10))()



#group() используется для параллельного выполнения набора задач. 
# Он возвращает специальный объект GroupResult, который позволяет отслеживать выполнение группы задач:
from celery import group

# выполняет add(2, 2) и add(4, 4) параллельно
group_result = group(add.s(2, 2), add.s(4, 4))()



#chord() — это комбинация group() и chain(), позволяющая выполнить группу задач параллельно 
# и затем вызвать callback-задачу с результатами группы:
from celery import chord
# cначала выполняет add(2, 2) и add(4, 4) параллельно, затем результаты передаются в multiply()
result = chord([add.s(2, 2), add.s(4, 4)])(multiply.s(2))