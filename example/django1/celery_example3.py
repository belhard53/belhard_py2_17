from celery import Celery
import time

app = Celery('reports', broker='pyamqp://guest@localhost//')

@app.task
def generate_report(report_id, parameters):
    # операции по извлечению данных, их обработке и анализе
    time.sleep(60) # имитация длительной операции
    # сохранение или отправка отчета
    return f"Report {report_id} generated with parameters {parameters}"

# использование
generate_report.delay("report_123", {"param1": "value1", "param2": "value2"})