# PulseGym - Sistema de Gestão e NPS

Bem-vindo ao repositório do PulseGym. Esta é uma solução projetada para academias, focada em monitorar o atendimento, gerenciar a jornada de treinos via integração com catracas (EVO) e disparar pesquisas de satisfação (NPS) automatizadas no WhatsApp.

## 🏗️ Estrutura Geral do Projeto (Raiz)
O projeto foi organizado em diretórios principais para separar claramente as responsabilidades de software e infraestrutura:

* **`/backend/`**: Contém a API e o painel administrativo. Construído em Python (Django). É o cérebro do sistema.
* **`/frontend/`**: Destinado à interface visual (Torre de Controle/TV e Dashboards). Preparado para receber o ecossistema Node.js (React/Vue).
* **`/docs/`**: Central de conhecimento. Guarda toda a documentação de arquitetura, decisões técnicas e manuais de endpoints.
* **`/infra/`**: Reservado para arquivos de infraestrutura (Dockerfiles, docker-compose, scripts de CI/CD e deploy).

---

## ⚙️ Arquitetura do Backend (Monolito Modular)
A estrutura interna do backend está dividida em módulos independentes (`apps`):

* **`evo_integration`**: Recebe webhooks da catraca EVO (check-in/check-out) e registra a sessão do aluno no banco de dados.
* **`nps_engine`**: Monitora o tempo de treino e aciona a integração com a API do WhatsApp para enviar a pesquisa de NPS.
* **`realtime`**: Utiliza WebSockets (Django Channels) para avisar o `frontend` (TV) sempre que um aluno entra ou sai.

---

## 📖 Documentação Técnica Obrigatória
Antes de iniciar o desenvolvimento, leia os guias técnicos localizados na pasta `/docs/`:
* **[DOC 01: Setup Inicial e Modelagem de Dados](docs/01_setup_e_modelagem.md)**
* **[DOC 02: Rotas e Recebimento de Webhook (EVO)](docs/02_rotas_e_webhook.md)**

---

## 🚀 Como rodar o Backend localmente

**1. Clone e ative o ambiente:**
> git clone https://github.com/is-wenderson/pulsegym.git
> cd pulsegym
> python -m venv venv
> venv\Scripts\activate.bat

**2. Instale dependências e rode o servidor:**
> pip install django
> cd backend
> python manage.py migrate
> python manage.py runserver

*(Para testar requisições locais: rode `python simulador_evo.py` em um segundo terminal).*

---

## ✅ O que já foi construído (Status Atual)
A fundação técnica e a primeira via de entrada de dados estão prontas:
1. **Estrutura e Setup:** Diretórios base criados, ambiente configurado e projeto Django modularizado com sucesso.
2. **Modelagem de Dados (`evo_integration`):** Criação e migração das tabelas `Member` (Aluno) e `WorkoutSession` (Sessões de treino vinculadas ao ID da EVO).
3. **API de Entrada (Webhook):** Endpoint HTTP POST criado em `/api/evo/webhook/`, livre de bloqueios CSRF, capaz de receber e ler payloads JSON.
4. **Ferramentas de Teste:** Script simulador de catraca programado nativamente em Python para facilitar os testes locais.

## 🎯 Próximos Passos (Para o Desenvolvedor - Eduardo Job)
* **1. Mapear o JSON da EVO:** Analisar a documentação oficial da EVO, identificar as chaves do payload de entrada/saída e extraí-las na função `views.py` do `evo_integration`.
* **2. Lógica de Banco de Dados:** Substituir o `print` de debug no webhook pelas operações do ORM do Django (Criar/Atualizar o `Member` e abrir/fechar a `WorkoutSession`).
* **3. Iniciar o Módulo NPS:** Começar o desenvolvimento do `nps_engine`, desenhando a rotina que identifica os treinos encerrados para disparar as mensagens no WhatsApp.