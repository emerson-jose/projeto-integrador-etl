# -Projeto-Integrador---ETL-e-An-lise-de-Dados
Repositório do Projeto Integrador Aplicado em CD &amp; IA
# 📊 Análise Preditiva e Desempenho de Vendas (CRM)

![Status](https://img.shields.io/badge/Status-Concluído-green)
![Linguagem](https://img.shields.io/badge/Linguagem-Python%20%7C%20SQL-blue)
![Visualização](https://img.shields.io/badge/Visualização-Power%20BI-yellow)

## 🎯 Entendimento do Negócio

**Definição do Problema:**
O projeto visa analisar o pipeline de vendas de uma empresa B2B de hardware de computadores. O objetivo principal é responder à seguinte pergunta de negócio: *"Quais são os padrões e tendências no pipeline de vendas que podem ser alavancados para otimizar as estratégias comerciais e maximizar a receita?"*

**Matriz de KPIs Estabelecida:**
1. Receita Total (Faturamento)
2. Taxa de Conversão (Win Rate)
3. Ticket Médio por Conta
4. Faturamento por Setor (Indústria)
5. Eficiência do Funil (Ciclo de Vendas em dias)
6. Ranking de Performance das Equipes de Vendas

## 📂 Fonte de Dados
O conjunto de dados utilizado é o **"Predictive Analytics for CRM Sales Performance"**, extraído do Kaggle. Ele contém dados estruturados sobre contas (clientes corporativos), produtos, equipes de vendas e oportunidades de negócios (prospects).
- Link da base: [Kaggle Dataset](https://www.kaggle.com/datasets/agungpambudi/predictive-analytics-for-crm-sales-performance)

## ⚙️ Arquitetura e Processo ETL
Para garantir a integridade e escalabilidade da análise, o seguinte processo foi executado:
1. **Extração:** Coleta dos arquivos `.csv` (accounts, products, sales_teams, sales_pipeline).
2. **Transformação (Limpeza e Modelagem):**
   - Tratamento de valores nulos e inconsistências sistêmicas.
   - Padronização de tipos de dados (datas, valores monetários).
   - Criação de chaves estrangeiras lógicas para relacionamento.
3. **Carga:** Estruturação de um banco de dados relacional [ex: PostgreSQL / SQLite] utilizando modelagem Star Schema (Tabela Fato de Vendas e Dimensões de Contas, Produtos e Equipes).

## 🛠️ Tecnologias Utilizadas
- **Banco de Dados / SQL:** [Ex: PostgreSQL, DBeaver] para estruturação e consultas.
- **Linguagem / Scripts:** [Ex: Python, Pandas, SQLAlchemy] para o processo de ETL.
- **Visualização de Dados:** [Ex: Power BI ou Metabase] para construção do Dashboard executivo.

## 📈 Resultados e Insights (Em Breve/Concluído)
*(Descreva aqui 2 ou 3 grandes descobertas que você teve após a análise. Ex: "Identificou-se que o setor de Tecnologia tem a conversão mais rápida, enquanto o setor Financeiro gera o maior Ticket Médio...")*

---
*Desenvolvido por [Seu Nome] - Conecte-se comigo no [LinkedIn](seu_link).*
