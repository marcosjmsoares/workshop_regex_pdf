import time
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv


# FORÇAR carregamento do .env da raiz do projeto
# Sobe um nível de src/ para chegar na raiz
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

print(f"Carregando .env de: {ENV_PATH}")
print(f"Arquivo existe: {ENV_PATH.exists()}")

load_dotenv(dotenv_path=ENV_PATH)

# Verificar se carregou
print(f"QUEUE_NAME carregado: '{os.getenv('QUEUE_NAME')}'")
print(f"AWS_REGION carregado: '{os.getenv('AWS_REGION')}'")


import schedule
from configs.tools.queue import HTMLSQSListener

# Função a ser executada a cada 2 minutos
def task_every_2_minutes():
    print(f"Tarefa a cada 2 minutos executada em {datetime.now()}")
    HTMLSQSListener().check_messages()


# Função para agendar a tarefa a cada 2 minutos
def schedule_2_min_task():
    schedule.every(10).seconds.do(task_every_2_minutes)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule_2_min_task()
