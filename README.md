# 🏥 Actuaria Analytics - Pipeline de Dados Atuariais

## 📌 Sobre o Projeto

O **Actuaria Analytics** é uma solução de engenharia de dados voltada para processamento, transformação e análise de informações atuariais, utilizando uma arquitetura de pipeline automatizada baseada em **Apache Airflow**, **PostgreSQL**, **Docker** e **Streamlit**.

O projeto tem como objetivo construir um fluxo completo de dados capaz de transformar informações históricas de mortalidade e população em indicadores estruturados para análise atuarial.

Do ponto de vista atuarial, a solução busca apoiar a avaliação de riscos relacionados à **mortalidade**, **longevidade** e **exposição populacional ao risco**, permitindo identificar padrões demográficos, variações de mortalidade por faixa etária e sexo, além da geração de métricas utilizadas em estudos atuariais.

Essas análises possuem aplicações em:

- seguros de vida;
- previdência complementar;
- estudos de longevidade;
- planejamento financeiro de longo prazo;
- gestão de riscos populacionais;
- modelagem atuarial.

A solução utiliza a arquitetura **Medallion Data Architecture**, separando o processamento dos dados em três camadas:

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

Essa abordagem permite:

- maior organização dos dados;
- rastreabilidade das informações;
- separação entre dados brutos e analíticos;
- controle de qualidade;
- facilidade de auditoria;
- possibilidade de reprocessamento.

---

# 🏗️ Arquitetura do Projeto

O ambiente é totalmente containerizado utilizando Docker Compose.

A arquitetura é composta pelos seguintes serviços:

| Serviço | Responsabilidade |
|---|---|
| 🐘 PostgreSQL Analytics | Armazenamento das informações atuariais |
| 🐘 PostgreSQL Airflow | Banco de metadados e controle do Airflow |
| 🔄 Apache Airflow | Orquestração e execução do pipeline |
| 📊 Streamlit | Dashboard para análise dos indicadores |
| 🐳 Docker Compose | Gerenciamento dos containers |

---

# 🥉 Bronze Layer - Dados Brutos

A camada Bronze representa a etapa inicial de ingestão dos dados.

Nesta camada os dados são armazenados preservando sua estrutura original, permitindo:

- auditoria;
- rastreamento da fonte;
- histórico de ingestão;
- reprocessamento do pipeline.

Principais tabelas:

```sql
bronze.mortality_table_raw

bronze.population_raw
```

Informações armazenadas:

```text
reference_year
state_code
sex
age_group
deaths
population
source
ingestion_timestamp
```

A camada Bronze representa a fonte oficial utilizada pelo restante do pipeline.

---

# 🥈 Silver Layer - Tratamento e Transformação

A camada Silver realiza o processo de preparação dos dados para análise atuarial.

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

Nesta etapa são calculados elementos fundamentais para análise atuarial:

- população exposta ao risco;
- mortalidade por grupo etário;
- expectativa de vida estimada;
- informações consolidadas por sexo e idade.

---

# 🥇 Gold Layer - Indicadores Atuariais

A camada Gold contém os dados finais utilizados para análise e visualização.

Nesta etapa são gerados indicadores atuariais consolidados a partir das informações tratadas nas camadas anteriores.

Principais tabelas:

```sql
gold.actuarial_indicators

gold.mortality_indicators
```

Os dados desta camada são utilizados pelo dashboard Streamlit.

---

# 📈 Indicadores Atuariais Gerados e Metodologia Aplicada

Os indicadores atuariais são calculados utilizando conceitos tradicionais de análise de mortalidade e risco populacional.

A metodologia aplicada considera a relação entre:

- quantidade de eventos observados (óbitos);
- população exposta ao risco;
- grupos etários;
- histórico temporal.

---

# ⚕️ Taxa de Mortalidade

A taxa de mortalidade representa a probabilidade observada de ocorrência de óbito em determinado grupo populacional.

A metodologia utilizada é:

\[
q_x = \frac{D_x}{E_x}
\]

Onde:

```text
q_x = taxa de mortalidade do grupo etário x

D_x = quantidade de óbitos observados

E_x = população exposta ao risco
```

Esse indicador permite avaliar:

- evolução da mortalidade por idade;
- comparação entre grupos populacionais;
- comportamento histórico do risco.

É uma das principais métricas utilizadas em estudos de seguros de vida e previdência.

---

# 👥 Exposição Populacional ao Risco

A exposição ao risco representa a quantidade de indivíduos sujeitos ao evento atuarial durante determinado período.

Metodologia:

\[
E_x = População_{x,t}
\]

Onde:

```text
E_x = exposição ao risco

População_x,t = quantidade de indivíduos no grupo etário x no período t
```

A exposição é fundamental para evitar distorções, pois permite comparar eventos considerando o tamanho real da população analisada.

---

# 🧬 Mortalidade Média por Grupo Etário

Para análise histórica dos grupos populacionais é calculada a mortalidade média:

\[
\bar{q_x} = \frac{\sum q_{x,t}}{n}
\]

Onde:

```text
q̄_x = mortalidade média do grupo etário

q_x,t = taxa de mortalidade observada no período

n = quantidade de períodos analisados
```

Esse indicador permite identificar tendências e padrões de mortalidade ao longo dos anos.

---

# ⏳ Expectativa de Vida Estimada

A expectativa de vida é estimada utilizando o conceito atuarial de sobrevivência.

A probabilidade de sobrevivência é calculada por:

\[
S_x = \prod_{i=x}^{n}(1-q_i)
\]

Onde:

```text
S_x = probabilidade de sobrevivência a partir da idade x

q_i = taxa de mortalidade em cada idade

x = idade inicial analisada
```

Esse conceito permite avaliar:

- longevidade populacional;
- comportamento futuro esperado;
- impacto da mortalidade sobre riscos atuariais.

---

# 📊 Indicadores Disponibilizados no Dashboard

Os indicadores calculados na camada Gold são disponibilizados através do dashboard analítico desenvolvido em Streamlit.

O usuário poderá visualizar informações como:

- 📈 evolução dos indicadores de mortalidade;
- 👥 distribuição populacional por faixa etária;
- ⚕️ taxas de mortalidade por grupo;
- ⏳ expectativa de vida estimada;
- 🧬 análise de risco populacional.

Principais campos atuariais apresentados:

```text
mortality_rate
    → taxa de mortalidade calculada para cada grupo populacional

avg_mortality_rate
    → média histórica da taxa de mortalidade

avg_life_expectancy
    → expectativa média de vida estimada

population_exposure
    → população exposta ao risco atuarial

age_group_risk
    → agrupamento do risco conforme faixa etária
```

---

# 🚀 Execução do Projeto

## 1️⃣ Clonar o repositório

Execute:

```bash
git clone https://github.com/VtRodrigues96/actuaria-analytics.git

cd actuaria-analytics
```

---

# 2️⃣ Preparação dos diretórios do Airflow

O Apache Airflow executa internamente utilizando o usuário com **UID 50000**.

Antes da inicialização do ambiente, configure as permissões dos diretórios utilizados para persistência dos logs e plugins:

```bash
mkdir -p logs plugins

sudo chown -R 50000:0 logs plugins

sudo chmod -R 775 logs plugins
```

Essas permissões permitem que o Airflow consiga criar e gerenciar:

- logs das DAGs;
- registros de execução;
- arquivos temporários;
- informações internas de processamento.

---

# 3️⃣ Construção das imagens Docker

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

# 4️⃣ Inicialização do ambiente Airflow

Execute:

```bash
docker compose up airflow-init
```

Nesta etapa o ambiente realiza:

- criação do banco de metadados do Airflow;
- execução das migrations;
- criação do usuário administrador;
- preparação inicial do ambiente.

Ao finalizar corretamente, o container:

```
airflow-init
```

deverá apresentar:

```
Exited (0)
```

indicando inicialização concluída com sucesso.

---

# 5️⃣ Inicialização dos serviços

Execute:

```bash
docker compose up -d
```

Após essa etapa todos os serviços estarão disponíveis.

Validação:

```bash
docker ps
```

O usuário deverá visualizar containers ativos:

```
airflow_webserver

airflow_scheduler

actuaria_streamlit

actuaria_postgres

airflow_postgres
```

---

# 👀 O que o usuário deverá visualizar

Após a execução correta do projeto, estarão disponíveis três ambientes principais.

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

O usuário visualizará a DAG:

```
actuaria_pipeline
```

Fluxo de processamento:

```
init_database
        ↓
bronze.load_mortality_table
        ↓
bronze.load_population
        ↓
silver.transform_mortality
        ↓
silver.transform_population
        ↓
silver.build_mortality_age_group
        ↓
gold.build_indicators
        ↓
quality_check
```

Após executar a DAG, todas as tarefas deverão apresentar:

```
🟢 SUCCESS
```

---
# 🗄️ Consulta do Banco de Dados Analítico

O projeto utiliza o **PostgreSQL** como banco responsável pelo armazenamento dos dados processados através das camadas Bronze, Silver e Gold.

O banco analítico contém todas as informações utilizadas pelo dashboard e permite consultas SQL para validação dos dados, auditoria do pipeline e análises complementares.

Configuração de acesso:

```
Host:
localhost

Porta:
5432

Database:
analytics

Usuário:
actuaria

Senha:
actuaria
```

---

## 🔌 Acessando o PostgreSQL via Terminal

Para acessar o banco analítico através do container PostgreSQL:

```bash
docker exec -it actuaria_postgres psql -U actuaria -d analytics
```

Após a conexão, o usuário estará dentro do banco:

```
analytics=#
```

---

# 📚 Estrutura dos Schemas

O banco está organizado utilizando a arquitetura Medallion:

```
bronze
 |
 ↓
silver
 |
 ↓
gold
```

---

## 🥉 Consultando Dados Brutos (Bronze)

As tabelas Bronze armazenam os dados originais após ingestão.

Consultar tabelas disponíveis:

```sql
\dt bronze.*
```

Principais tabelas:

```sql
bronze.mortality_table_raw

bronze.population_raw
```

Exemplo de consulta:

```sql
SELECT *
FROM bronze.mortality_table_raw
LIMIT 10;
```

---

## 🥈 Consultando Dados Tratados (Silver)

As tabelas Silver apresentam os dados após limpeza, padronização e transformação.

Consultar tabelas:

```sql
\dt silver.*
```

Principais tabelas:

```sql
silver.mortality_clean

silver.population_clean

silver.mortality_age_group
```

Exemplo:

```sql
SELECT *
FROM silver.mortality_age_group
LIMIT 10;
```

Campos atuariais disponíveis:

```
age_min
age_max
sex
avg_mortality_rate
avg_life_expectancy
processing_timestamp
```

---

## 🥇 Consultando Indicadores Atuariais (Gold)

A camada Gold contém os indicadores finais utilizados para análise.

Consultar tabelas:

```sql
\dt gold.*
```

Principais tabelas:

```sql
gold.actuarial_indicators

gold.mortality_indicators
```

Exemplo:

```sql
SELECT *
FROM gold.actuarial_indicators
LIMIT 10;
```

---

# 📊 Validação da Carga de Dados

Após a execução completa da DAG, o usuário pode validar o volume processado:

```sql
SELECT 'bronze.mortality_table_raw' AS tabela, COUNT(*) 
FROM bronze.mortality_table_raw

UNION ALL

SELECT 'bronze.population_raw', COUNT(*) 
FROM bronze.population_raw

UNION ALL

SELECT 'silver.mortality_clean', COUNT(*) 
FROM silver.mortality_clean

UNION ALL

SELECT 'silver.population_clean', COUNT(*) 
FROM silver.population_clean

UNION ALL

SELECT 'gold.actuarial_indicators', COUNT(*) 
FROM gold.actuarial_indicators;
```

O resultado esperado demonstra:

- dados ingeridos na camada Bronze;
- dados tratados na camada Silver;
- indicadores calculados na camada Gold.

Essa validação garante que o pipeline foi executado corretamente antes da visualização no dashboard.

---

---
# 📊 Dashboard Streamlit

Acesse:

```
http://localhost:8501
```

O dashboard apresenta os dados provenientes da camada Gold.

O usuário poderá analisar:

- indicadores atuariais;
- mortalidade por faixa etária;
- expectativa de vida;
- distribuição populacional;
- métricas consolidadas de risco.

---

# 🗄️ Banco PostgreSQL Analytics

Banco responsável pelo armazenamento dos dados analíticos.

Configuração:

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

# 🧪 Validação da Execução

Para verificar se o pipeline foi executado corretamente:

## Listar DAGs disponíveis:

```bash
docker exec -it airflow_scheduler airflow dags list
```

Resultado esperado:

```
actuaria_pipeline
```

---

## Verificar execuções:

```bash
docker exec -it airflow_scheduler airflow dags list-runs -d actuaria_pipeline
```

Uma execução concluída deve apresentar:

```
state: success
```

---

## Verificar status das tarefas:

```bash
docker exec -it airflow_scheduler airflow tasks states-for-dag-run actuaria_pipeline RUN_ID
```

Resultado esperado:

```
success
```

para todas as tarefas.

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
├── logs/
│
├── plugins/
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

O projeto contempla:

✅ Pipeline automatizado utilizando Apache Airflow  
✅ Arquitetura Medallion (Bronze / Silver / Gold)  
✅ Processamento reprodutível via Docker Compose  
✅ Banco analítico PostgreSQL  
✅ Banco separado para metadados do Airflow  
✅ Controle de qualidade dos dados  
✅ Transformações atuariais automatizadas  
✅ Indicadores de mortalidade e longevidade  
✅ Dashboard analítico em Streamlit  
✅ Persistência dos dados processados  
✅ Ambiente preparado para reprocessamento  
✅ Logs e rastreabilidade das execuções  

---

# 🎓 Aplicação Atuarial

O projeto demonstra como técnicas modernas de engenharia de dados podem ser aplicadas à ciência atuarial, permitindo transformar volumes de dados populacionais em informações estratégicas para avaliação de riscos.

A solução aproxima o processo tradicional de análise atuarial de uma arquitetura moderna de dados, possibilitando maior automação, confiabilidade e escalabilidade dos estudos de mortalidade e longevidade.

---

# 👨‍💻 Autor

**Vitor Rodrigues**

Projeto acadêmico desenvolvido para a disciplina de:

**Orquestração de Workflows**
