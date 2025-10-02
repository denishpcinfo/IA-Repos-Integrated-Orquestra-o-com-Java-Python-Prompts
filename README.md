# 🔗 IA Repos Integrated – Orquestração com Java + Python + Prompts
Este repositório integra três aplicações complementares para demonstrar orquestração de políticas de negócio usando Spring Boot (Java), FastAPI (Python) e um Catálogo de Prompts.

📂 Estrutura do Repositório

<img width="288" height="126" alt="image" src="https://github.com/user-attachments/assets/70621907-533b-40ae-ba69-92644666c439" />


# ⚙️ Pré-requisitos

Java 17+

Maven 3.9+

Python 3.11+

Poetry (ou pip + venv)

Docker (opcional) para rodar ambientes isolados

cURL + jq para testes de linha de comando

# 🚀 Como rodar os serviços
1. 🔹 Catálogo de Prompts

  Os prompts ficam no diretório:
  prompt-engineering-catalog/prompts/

2. 🔹 Python – Engine Multiagente

  cd multiagent-autogen-demo
  poetry install
  poetry run uvicorn src.app:app --reload --port 8000
  
  Endpoints principais:
  
  GET /health → Healthcheck
  
  POST /plan → Gera um plano a partir de um objetivo
  
  POST /execute → Executa um plano e retorna relatório
  
  POST /echo → Endpoint auxiliar para debug/offline
  
  GET /plan-q → Planejamento via query params
  
  Configuração opcional:
  export HTTP_TOOL_URL=http://127.0.0.1:8000/echo

3. 🔹 Java – Orquestrador
  cd semantic-kernel-java-bank
  mvn spring-boot:run
  
  Endpoints:
  
  GET /orchestrate/plan → Consulta plano (Java → Python)
  
  POST /orchestrate/execute → Aplica política (ALLOW/DENY) e orquestra com Python

# 🔄 Fluxo de Orquestração

Java (Spring Boot) recebe uma requisição → ex: Reemitir cartão.

Política de negócio é aplicada (ex.: negar quando há disputa).

Se ALLOW, o Java encaminha para o Python.

O Python consulta os prompts e executa o fluxo.

A resposta retorna para o Java, que a expõe ao cliente.

# 🔎 Correlation ID

Toda requisição recebe um X-Correlation-Id (UUID).

O Java gera/propaga → o Python reutiliza.

O cid aparece em logs, headers e no JSON.

Exemplo log:

2025-10-01 19:22:12 INFO  cid=ba826f3f-... com.example.sk.web.OrchestrationController - Executing plan...
2025-10-01 19:22:12 INFO  multiagent - cid=ba826f3f-... POST /execute -> 200

# 📡 Exemplos de Teste

Ver plano (Java → Python)

curl -i "http://localhost:8080/orchestrate/plan?goal=Resumir%20politica&template=policy_summary"

Orquestração ALLOW

curl -i -X POST \
"http://localhost:8080/orchestrate/execute?goal=Reemitir%20cartao&template=policy_summary&tier=VIP&dispute=false"

Orquestração DENY

curl -i -X POST \
"http://localhost:8080/orchestrate/execute?goal=Reemitir%20cartao&template=policy_summary&tier=STD&dispute=true"

Política isolada

curl -i -X POST "http://localhost:8080/policy/reissue?tier=VIP&dispute=false"





![Screenshot_20251001_203354_Chrome](https://github.com/user-attachments/assets/20fe50f9-5a0a-492c-95ec-a80f581e3a99)

