# 🏥 Actuaria Analytics - Pipeline de Dados Atuariais

## 📌 Sobre o Projeto

O **Actuaria Analytics** é uma solução de engenharia de dados voltada para processamento e análise de informações atuariais, utilizando uma arquitetura de pipeline automatizada baseada em **Apache Airflow**, **PostgreSQL**, **Docker** e **Streamlit**.

Do ponto de vista atuarial, o objetivo deste projeto é construir um fluxo completo de dados para transformar dados históricos de mortalidade e população em informações estruturadas capazes de apoiar a avaliação de riscos relacionados à longevidade e mortalidade. A análise permite identificar padrões de comportamento demográfico, variações de mortalidade por faixa etária e sexo, além de estimar indicadores utilizados em estudos atuariais, como taxas de mortalidade, expectativa de vida e exposição ao risco. Essas informações são fundamentais para auxiliar processos de tomada de decisão em áreas como seguros de vida, previdência, planejamento financeiro de longo prazo e gestão de riscos populacionais.

A solução utiliza a arquitetura **Medallion Data Architecture**, separando o processamento em três camadas:

```
Dados Originais
       |
       ↓
🥉 Bronze Layer
       |
       ↓
🥈 Silver Layer
       |
       ↓
🥇 Gold Layer
       |
       ↓
📊 Dashboard Streamlit
```

Essa abordagem permite maior organização, rastreabilidade, qualidade dos dados e facilidade de reprocessamento.

---

# 🏗️ Arquitetura do Projeto

O ambiente é totalmente containerizado utilizando Docker Compose, contendo os seguintes serviços:

| Serviço | Responsabilidade |
|---|---|
| 🐘 PostgreSQL Analytics | Armazenamento dos dados atuariais |
| 🐘 PostgreSQL Airflow | Banco de metadados do Airflow |
| 🔄 Apache Airflow | Orquestração e execução do pipeline |
| 📊 Streamlit | Dashboard para visualização dos indicadores |
| 🐳 Docker Compose | Gerenciamento dos containers |

---

# 🥉 Bronze Layer - Dados Brutos

A camada Bronze representa a primeira etapa do pipeline.

Nesta camada os dados são armazenados preservando sua origem, permitindo:

- auditoria;
- rastreamento da fonte;
- reprocessamento;
- histórico de ingestão.

Principais tabelas:

```sql
bronze.mortality_table_raw

bronze.population_raw
```

Informações armazenadas:

- ano de referência;
- estado;
- sexo;
- faixa etária;
- população;
- quantidade de óbitos;
- origem dos dados;
- timestamp de ingestão.

---

# 🥈 Silver Layer - Tratamento e Transformação

A camada Silver realiza o processo de preparação dos dados para análise.

Nesta etapa são executados:

✅ limpeza dos dados;  
✅ padronização dos campos;  
✅ tratamento de inconsistências;  
✅ transformação das informações;  
✅ criação de agregações atuariais.

Principais tabelas:

```sql
silver.mortality_clean

silver.population_clean

silver.mortality_age_group
```

São geradas informações como:

- mortalidade média por grupo etário;
- expectativa de vida estimada;
- exposição populacional;
- dados preparados para cálculos atuariais.

---

# 🥇 Gold Layer - Indicadores Atuariais

A camada Gold contém os dados finais utilizados para análise.

Nesta etapa são calculados indicadores consolidados para apoiar análises atuariais.

Principais tabelas:

```sql
gold.actuarial_indicators

gold.mortality_indicators
```

---

# 📈 Indicadores Atuariais Gerados

O projeto gera métricas relacionadas ao comportamento populacional e risco atuarial.

## 👥 Mortalidade por Faixa Etária

Permite avaliar:

- evolução da mortalidade conforme a idade;
- diferença entre grupos populacionais;
- comportamento histórico dos riscos.

Principais campos:

```text
age_min
age_max
sex
avg_mortality_rate
avg_life_expectancy
```

---

## 👨‍👩‍👧 Indicadores Populacionais

Permitem analisar:

- distribuição da população;
- exposição ao risco;
- comportamento demográfico.

Principais campos:

```text
reference_year
state_code
sex
age_group
population
```

---

## ⚕️ Indicadores de Risco Atuarial

As métricas permitem análises como:

- projeção de mortalidade;
- avaliação de longevidade;
- análise de risco populacional;
- suporte para estudos atuariais.

Exemplos de indicadores:

```text
mortality_rate

life_expectancy

population_exposure

age_group_risk
```

---

# 🚀 Execução do Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/VtRodrigues96/actuaria-analytics.git

cd actuaria-analytics
```

---

## 2️⃣ Preparar permissões dos volumes do Airflow

O Apache Airflow utiliza internamente o usuário com **UID 50000**.

Antes da inicialização do ambiente, execute:

```bash
mkdir -p logs plugins

sudo chown -R 50000:0 logs plugins

sudo chmod -R 775 logs plugins
```

Esses comandos garantem que o Airflow tenha permissão para criar:

- logs das DAGs;
- arquivos temporários;
- registros de execução;
- arquivos internos de processamento.

---

## 3️⃣ Construir as imagens Docker

Execute:

```bash
docker compose build
```

Serão criadas as imagens:

```
actuaria-airflow:2.10.5

actuaria-streamlit:latest
```

---

## 4️⃣ Inicializar o Airflow

Execute:

```bash
docker compose up airflow-init
```

Essa etapa realiza:

- criação do banco de metadados do Airflow;
- execução das migrations;
- criação do usuário administrador;
- preparação do ambiente inicial.

---

## 5️⃣ Subir todos os serviços

Execute:

```bash
docker compose up -d
```

Após a inicialização, todos os containers estarão ativos.

---

# 👀 O que o usuário deverá visualizar

Após executar corretamente o projeto, o usuário terá acesso aos seguintes serviços.

---

# 🔄 Apache Airflow

Acesse:

```
http://localhost:8080
```

Credenciais:

```
Usuário:
admin

Senha:
admin
```

No Airflow será apresentada a DAG:

```
actuaria_pipeline
```

O fluxo deverá apresentar as seguintes tarefas:

```
init_database

bronze.load_mortality_table

bronze.load_population

silver.transform_mortality

silver.transform_population

silver.build_mortality_age_group

gold.build_indicators

quality_check
```

Após a execução completa, todas as tarefas deverão apresentar:

```
🟢 SUCCESS
```

---

# 📊 Dashboard Streamlit

Acesse:

```
http://localhost:8501
```

O usuário visualizará:

- indicadores atuariais;
- análises populacionais;
- métricas de mortalidade;
- informações agrupadas por faixa etária;
- dados consolidados da camada Gold.

---

# 🗄️ Banco de Dados PostgreSQL

Banco analítico:

```
Host:
localhost

Porta:
5432

Database:
analytics

Usuário:
actuaria
```

Schemas criados:

```
bronze

silver

gold

metadata
```

---

# 📂 Estrutura do Projeto

```
actuaria-analytics/

├── dags/
│   └── actuaria_pipeline.py
│
├── src/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── database/
│   └── quality/
│
├── sql/
│
├── streamlit_app/
│
├── config/
│
├── docker-compose.yml
│
├── Dockerfile
│
├── Dockerfile.streamlit
│
├── requirements.txt
│
└── README.md
```

---

# 🔁 Características Implementadas

O projeto possui:

✅ Pipeline automatizado com Apache Airflow  
✅ Execução reproduzível via Docker Compose  
✅ Arquitetura Medallion (Bronze/Silver/Gold)  
✅ Persistência em PostgreSQL  
✅ Separação entre banco analítico e banco de metadados  
✅ Controle de qualidade dos dados  
✅ Dashboard analítico em Streamlit  
✅ Ambiente preparado para reprocessamento  
✅ Logs e monitoramento das execuções  

---

# 👨‍💻 Autor

**Vitor Rodrigues**

Projeto acadêmico desenvolvido para a disciplina de **Orquestração de Workflows**.
