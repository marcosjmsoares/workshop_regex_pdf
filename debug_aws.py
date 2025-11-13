import os
from pathlib import Path
from dotenv import load_dotenv
import boto3

print("=" * 60)
print("TESTE COMPLETO DE DEBUG")
print("=" * 60)

# 1. Verificar localização do .env
print("\n1. LOCALIZAÇÃO DO .ENV")
env_path = Path('.env')
print(f"   Caminho: {env_path.absolute()}")
print(f"   Existe: {env_path.exists()}")

if env_path.exists():
    print(f"\n   Conteúdo do .env:")
    with open('.env', 'r') as f:
        for line in f:
            if 'SECRET' in line or 'PASSWORD' in line:
                parts = line.split('=')
                print(f"   {parts[0]}=***")
            else:
                print(f"   {line.strip()}")

# 2. Carregar .env
print("\n2. CARREGANDO .ENV")
load_result = load_dotenv(verbose=True)
print(f"   Resultado: {load_result}")

# 3. Verificar variáveis
print("\n3. VARIÁVEIS CARREGADAS")
print(f"   QUEUE_NAME: '{os.getenv('QUEUE_NAME')}'")
print(f"   AWS_REGION: '{os.getenv('AWS_REGION')}'")
print(f"   AWS_BUCKET: '{os.getenv('AWS_BUCKET')}'")
print(f"   AWS_ACCESS_KEY_ID: {'***' if os.getenv('AWS_ACCESS_KEY_ID') else 'None'}")
print(f"   AWS_SECRET_ACCESS_KEY: {'***' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'None'}")

# 4. Testar conexão SQS
print("\n4. TESTANDO CONEXÃO SQS")
queue_name = os.getenv('QUEUE_NAME')
region = os.getenv('AWS_REGION')

if queue_name and region:
    try:
        sqs = boto3.client('sqs', region_name=region)
        print(f"   Cliente SQS criado para região: {region}")
        
        # Listar todas as filas
        print(f"\n   Listando todas as filas na região {region}:")
        list_response = sqs.list_queues()
        if 'QueueUrls' in list_response:
            for url in list_response['QueueUrls']:
                queue_name_from_url = url.split('/')[-1]
                print(f"   - {queue_name_from_url}")
                if queue_name_from_url == queue_name:
                    print(f"     ✅ MATCH com QUEUE_NAME do .env")
        else:
            print("   Nenhuma fila encontrada")
        
        # Tentar pegar a URL da fila específica
        print(f"\n   Buscando fila específica: '{queue_name}'")
        response = sqs.get_queue_url(QueueName=queue_name)
        print(f"   ✅ SUCESSO! URL: {response['QueueUrl']}")
        
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
else:
    print("   ❌ QUEUE_NAME ou AWS_REGION não configuradas")

print("\n" + "=" * 60)
