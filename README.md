# PulseGym - Sistema de Gestão e NPS

Bem-vindo ao repositório do PulseGym. Esta é uma solução projetada para academias, focada em monitorar o atendimento, gerenciar a jornada de treinos via integração com catracas (EVO), balancear a carga do salão em tempo real e disparar pesquisas de satisfação (NPS) automatizadas no WhatsApp.

## 🏗️ Estrutura Geral do Projeto (Raiz)

O projeto foi organizado em diretórios principais para separar claramente as responsabilidades de software e infraestrutura:

* **/backend/:** Contém a API e as regras de negócio. Construído em Python (Django). É o "Cérebro" do sistema.
* **/frontend/:** Destinado à interface visual (Torre de Controle/TV e Dashboards). Atualmente contém o protótipo em HTML/JS isolado, preparado para receber o ecossistema Node.js (React/Vue).
* **/docs/:** Central de conhecimento. Guarda a documentação de arquitetura, PDFs de requisitos funcionais e não funcionais.
* **/infra/:** Reservado para arquivos de infraestrutura (Dockerfiles, docker-compose, scripts de CI/CD e deploy).

## ⚙️ Arquitetura do Backend (Monolito Modular)

A estrutura interna do backend está dividida em módulos independentes (apps):

* **`evo_integration`:** Core do sistema. Recebe webhooks da catraca EVO, gerencia o turno dos professores, executa o algoritmo de roleta (balanceamento de salão) e fornece a API de "Raio-X" para a TV.
* **`nps_engine`:** *(Na fila)* Monitora o tempo de treino e aciona a integração com a API do WhatsApp para enviar a pesquisa de NPS baseada no vínculo histórico.
* **`realtime`:** *(Na fila)* Utilizará WebSockets (Django Channels) para substituir o *polling* atual da TV, empurrando dados em tempo real para o frontend.

## 🚀 Como rodar o Laboratório Localmente (PoC)

O ambiente foi configurado com uma arquitetura desacoplada (Frontend separado do Backend). Você precisará de **3 terminais** abertos:

**1. O Cérebro (Backend):**
```bash
# Clone e ative o ambiente
git clone [https://github.com/is-wenderson/pulsegym.git](https://github.com/is-wenderson/pulsegym.git)
cd pulsegym
python -m venv venv
venv\Scripts\activate.bat # (No Linux/Mac: source venv/bin/activate)

# Instale as dependências (Django, CorsHeaders) e rode o servidor
pip install django django-cors-headers
cd backend
python manage.py migrate
python manage.py runserver
