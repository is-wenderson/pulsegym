import urllib.request
import json

url = 'http://127.0.0.1:8000/api/evo/webhook/'

print("===================================")
print("🏋️  CATRACA SIMPLIFICADA 🏋️")
print("===================================")
print("[1] Professor CHEGOU")
print("[2] Professor SAIU")
print("[3] Aluno CHEGOU")
print("[4] Aluno SAIU")
print("===================================")

opcao = input("O que aconteceu na catraca? (Digite o número): ")
payload = {}

if opcao == '1':
    nome = input("Qual o nome do Professor que CHEGOU? ")
    # Cria um ID único baseado no nome (ex: PROF-CARLOS)
    id_prof = f"PROF-{nome.upper().replace(' ', '')}"
    payload = {"usuario_id": id_prof, "nome": nome, "evento": "checkin", "tipo_usuario": "instrutor"}

elif opcao == '2':
    nome = input("Qual o nome do Professor que SAIU? ")
    id_prof = f"PROF-{nome.upper().replace(' ', '')}"
    payload = {"usuario_id": id_prof, "nome": nome, "evento": "checkout", "tipo_usuario": "instrutor"}

elif opcao == '3':
    nome = input("Qual o nome do Aluno que CHEGOU? ")
    # Cria um ID único baseado no nome (ex: ALU-WENDERSON)
    id_aluno = f"ALU-{nome.upper().replace(' ', '')}"
    payload = {"usuario_id": id_aluno, "nome": nome, "evento": "checkin", "tipo_usuario": "aluno"}

elif opcao == '4':
    nome = input("Qual o nome do Aluno que SAIU? ")
    id_aluno = f"ALU-{nome.upper().replace(' ', '')}"
    payload = {"usuario_id": id_aluno, "nome": nome, "evento": "checkout", "tipo_usuario": "aluno"}

else:
    print("Opção inválida. Encerrando.")
    exit()

# Envia os dados para o backend
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print(f"\nGirando a catraca para: {nome}...")
try:
    response = urllib.request.urlopen(req)
    print("Resposta do Sistema:", response.read().decode('utf-8'))
except Exception as e:
    print("Erro na comunicação:", e)