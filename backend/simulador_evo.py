import urllib.request
import json

# URL da nossa porta de entrada (webhook)
url = 'http://127.0.0.1:8000/api/evo/webhook/'

# Dados falsos simulando a catraca da EVO
payload = {
    "aluno_id": 12345,
    "nome": "Wenderson - Teste PulseGym"
}

# Convertendo para o formato de envio (JSON)
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print("Disparando webhook para o servidor...")

try:
    response = urllib.request.urlopen(req)
    print("✅ Sucesso! Resposta do Servidor:", response.read().decode('utf-8'))
except Exception as e:
    print("❌ Erro ao enviar:", e)