# DOC 01: Setup Inicial e Modelagem de Dados (Backend)

**Status:** Ambiente configurado, estrutura modular criada e primeira modelagem de banco de dados aplicada.
**Stack:** Python 3, Django, SQLite (Desenvolvimento) / PostgreSQL (Produção futura).
**Arquitetura:** Monolito Modular.

## 1. Estrutura de Módulos (Apps)
O projeto foi dividido em três módulos independentes dentro da pasta `/backend/apps/` para garantir a separação de responsabilidades:
* `evo_integration`: Responsável por receber os Webhooks da catraca (check-in/check-out) e espelhar os dados dos alunos.
* `nps_engine`: Responsável pela lógica de cálculo de tempo, gatilhos de saída e integração com a API do WhatsApp.
* `realtime`: Responsável pela conexão WebSocket (Django Channels) para atualizar a "Torre de Controle" (TV).

## 2. Modelagem de Dados Inicial (`evo_integration`)
Para suportar o recebimento dos eventos da EVO sem duplicar informações, criamos as duas primeiras entidades no banco de dados.

**Arquivo:** `/backend/apps/evo_integration/models.py`

* **Tabela `Member` (Aluno):**
    * `evo_id` (CharField, Unique): ID original do aluno no sistema EVO.
    * `name` (CharField): Nome do aluno.
    * `created_at` (DateTimeField): Data de registro no nosso sistema.

* **Tabela `WorkoutSession` (Sessão de Treino):**
    * `member` (ForeignKey -> Member): Vínculo com o aluno.
    * `check_in_time` (DateTimeField): Timestamp exato da entrada (recebido via Webhook).
    * `check_out_time` (DateTimeField, Null/Blank): Timestamp exato da saída.
    * `is_active` (BooleanField): Status da sessão (True para treino em andamento).

## 3. Estado das Migrations
* O banco de dados local (`db.sqlite3`) já possui as tabelas `evo_integration_member` e `evo_integration_workoutsession`.