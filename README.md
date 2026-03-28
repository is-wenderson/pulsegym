PulseGym - Sistema de Gestão e NPS
Bem-vindo ao repositório do PulseGym. Esta é uma solução projetada para academias, focada em monitorar o atendimento, gerenciar a jornada de treinos via integração com catracas (EVO), balancear a carga do salão em tempo real e disparar pesquisas de satisfação (NPS) automatizadas no WhatsApp.

🏗️ Estrutura Geral do Projeto (Raiz)
O projeto foi organizado em diretórios principais para separar claramente as responsabilidades de software e infraestrutura:

/backend/: Contém a API e as regras de negócio. Construído em Python (Django). É o "Cérebro" do sistema.

/frontend/: Destinado à interface visual (Torre de Controle/TV e Dashboards). Atualmente contém o protótipo em HTML/JS isolado, preparado para receber o ecossistema Node.js (React/Vue).

/docs/: Central de conhecimento. Guarda a documentação de arquitetura, PDFs de requisitos funcionais e não funcionais.

/infra/: Reservado para arquivos de infraestrutura (Dockerfiles, docker-compose, scripts de CI/CD e deploy).

⚙️ Arquitetura do Backend (Monolito Modular)
A estrutura interna do backend está dividida em módulos independentes (apps):

evo_integration: Core do sistema. Recebe webhooks da catraca EVO, gerencia o turno dos professores, executa o algoritmo de roleta (balanceamento de salão) e fornece a API de "Raio-X" para a TV.

nps_engine: (Na fila) Monitora o tempo de treino e aciona a integração com a API do WhatsApp para enviar a pesquisa de NPS baseada no vínculo histórico.

realtime: (Na fila) Utilizará WebSockets (Django Channels) para substituir o polling atual da TV, empurrando dados em tempo real para o frontend.

🚀 Como rodar o Laboratório Localmente (PoC)
O ambiente foi configurado com uma arquitetura desacoplada (Frontend separado do Backend). Você precisará de 3 terminais abertos:

1. O Cérebro (Backend):

Bash
# Clone e ative o ambiente
git clone https://github.com/is-wenderson/pulsegym.git
cd pulsegym
python -m venv venv
venv\Scripts\activate.bat # (No Linux/Mac: source venv/bin/activate)

# Instale as dependências (Django, CorsHeaders) e rode o servidor
pip install django django-cors-headers
cd backend
python manage.py migrate
python manage.py runserver
2. A Torre de Controle (Frontend/TV):
Abra um segundo terminal, vá para a raiz do projeto e inicie o servidor estático:

Bash
cd frontend
python -m http.server 5500
Acesse no navegador: http://localhost:5500/tv_simulador.html

3. A Catraca (Simulador):
Abra um terceiro terminal, ative o venv, vá para a pasta backend e rode o simulador interativo para testar as regras de negócio:

Bash
python simulador_evo.py
✅ O que já foi construído (Prova de Conceito Validada)
A fundação técnica das regras de negócio do salão já está codificada e validada:

Modelagem de Entidades: Tabelas Member (Aluno), Instructor (Professor) e WorkoutSession (Sessões históricas) criadas.

Automação de Turnos (RF09): O sistema identifica quando um professor passa na catraca e altera automaticamente o status dele para "Online no Salão" (is_on_shift).

Algoritmo de Balanceamento (RF06): No check-in de um aluno, o sistema varre os professores online, conta os alunos ativos de cada um e atribui o novo aluno ao professor com a menor fila.

Trava de Capacidade e Fila de Espera (RF04, RF07): Professores possuem um limite máximo (max_capacity). Se todos estiverem lotados, o aluno vai para a Fila de Espera sem professor vinculado (null).

Algoritmo de Órfãos (RF17): Se um professor bater o check-out, seus alunos ativos são reatribuídos automaticamente para outros professores disponíveis.

Torre de Controle (TV): Endpoint /api/evo/tv/ fornecendo dados e uma interface Frontend consumindo via polling com CORS liberado.

🎯 Próximos Passos (Para a Engenharia - Eduardo Job)
Fase 1: Transição do Laboratório para Produção

Conectar a API EVO Real: Mapear o payload real do webhook da W12, substituir as chaves do nosso views.py e trocar o banco SQLite pelo banco de produção (PostgreSQL).

Atualizar Infraestrutura de Tempo Real: Evoluir a TV (tv_simulador.html) para um framework moderno (React/Vue) e substituir o polling HTTP por WebSockets nativos (Django Channels / Socket.io) para atender ao RNF05.

Painel do Instrutor Chefe (RF05): Criar a rota na API e a interface no frontend para permitir arrastar/clicar e vincular manualmente os alunos da Fila de Espera a um instrutor.

Fase 2: Módulo NPS (WhatsApp)

Regra de Trava (RF11): Criar a verificação de 15/30 dias para evitar spam de pesquisas.

Integração Meta/Z-API (RF12): Desenvolver o webhook de saída para disparar a mensagem via WhatsApp assim que a WorkoutSession for encerrada.

Recepção de Notas (RF13): Criar o endpoint webhook para receber a resposta do WhatsApp e salvar a nota (0-10) vinculada ao Instrutor exato que atendeu o aluno.
