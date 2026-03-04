# DOC 02: Rotas e Recebimento de Webhook (EVO)

**Status:** Endpoint criado e testado com sucesso.
**Módulo:** `evo_integration`

## 1. O Endpoint (Porta de Entrada)
Criamos a rota principal que ficará aguardando os disparos (POST) do sistema da catraca da EVO.
* **URL:** `/api/evo/webhook/`
* **Método Permitido:** `POST`
* **Proteção:** O token CSRF foi desativado (`@csrf_exempt`) especificamente para esta view, pois a requisição virá de um servidor de terceiros (EVO).

## 2. Lógica Atual (`views.py`)
O arquivo `/backend/apps/evo_integration/views.py` já possui a estrutura base para decodificar o payload JSON que chega no corpo da requisição.
* Atualmente, a função lê o JSON e imprime o resultado no console para fins de debug.
* Retorna um `JsonResponse` com status HTTP 200 em caso de sucesso, ou status 400 em caso de erro no formato JSON.

## 3. Simulador de Testes
Foi criado um script na raiz do backend chamado `simulador_evo.py`.
Este script utiliza a biblioteca nativa `urllib` do Python para disparar requisições POST para a rota do webhook, simulando o envio de dados pela EVO. É útil para o desenvolvedor testar a rota localmente.

## 4. Próximos Passos (Para o Desenvolvedor)
1. **Mapear o JSON Oficial:** Analisar a documentação da API/Webhooks da EVO para mapear exatamente quais chaves virão no JSON real (ex: `id_membro`, `tipo_evento`, `data_hora`).
2. **Salvar no Banco (Models):** Substituir o `print()` atual em `views.py` pela lógica do Django ORM que verifica se o aluno já existe (tabela `Member`) e cria/encerra uma `WorkoutSession`.