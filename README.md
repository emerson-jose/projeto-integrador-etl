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

---

# 🚀 Implementação Técnica: Pipeline Cloud-Native

Este projeto implementa um pipeline de dados completo (Extração, Transformação e Carga) com uma interface gráfica moderna e armazenamento em nuvem (Supabase). Abaixo, detalhamos a arquitetura e o fluxo de dados.

## 📊 Fluxograma do Processo (Pipeline ETL)

```mermaid
flowchart TD
    %% Fontes de Entrada
    Kaggle([Kaggle API - Dataset Externo])
    Web([Web Scraping - Playwright])

    %% Pasta de Dados Brutos
    Raw[(dados_analise - Arquivos CSV)]

    subgraph Transform [Camada de Processamento Polars Engine]
        direction TB
        PQT[Conversão Parquet - Compactação]
        Clean[Tratamento de Dados - Tipagem e Renomeação]
    end

    %% Pasta de Dados Tratados
    Tratados[(arquivos_tratados - Arquivos Otimizados)]

    subgraph Output [Entrega e Visualização]
        direction TB
        DB[(Supabase Cloud - PostgreSQL)]
        UI{Interface Gráfica - PySide6}
        PDF[[Relatórios PDF]]
    end

    %% Conexões
    Kaggle & Web ==> Raw
    Raw ==> PQT
    PQT --> Clean
    Clean ==> Tratados
    Tratados ==> DB
    DB <--> UI
    UI --- PDF

    %% Estilos de Cores e Formas (Garantindo contraste do texto)
    style Kaggle fill:#bbdefb,stroke:#1976d2,color:#000
    style Web fill:#bbdefb,stroke:#1976d2,color:#000
    style Raw fill:#e3f2fd,stroke:#2196f3,stroke-dasharray: 5 5,color:#000
    
    style Transform fill:#fff9c4,stroke:#fbc02d,color:#000
    style Clean fill:#fffde7,stroke:#fdd835,color:#000
    style PQT fill:#fffde7,stroke:#fdd835,color:#000
    
    style Tratados fill:#c8e6c9,stroke:#4caf50,stroke-width:2px,color:#000
    style DB fill:#a5d6a7,stroke:#2e7d32,color:#000
    style UI fill:#2b5278,stroke:#1e3d59,color:#fff
    style PDF fill:#ffcdd2,stroke:#d32f2f,color:#000
```

---

## 🏗️ Estrutura da Árvore de Diretórios

```text
PROJETO-ETL/
├── backend/                    # Núcleo de Processamento (Engine)
│   ├── analytics.py            # Análise de dados e métricas de desempenho
│   ├── conecao_supar.py        # Configuração da conexão com Supabase
│   ├── converter_parquet.py    # Conversão de CSV para Parquet (Otimização)
│   ├── db_manager.py           # Gestão de banco de dados e operações CRUD
│   ├── extracao_dados_web.py   # Coleta de dados via Web Scraping (Playwright)
│   ├── extracao_teste.py       # Scripts de teste para validação de extração
│   ├── funcoes.py              # Funções auxiliares e utilitárias do sistema
│   ├── gerador_pdf.py          # Motor de geração de relatórios exportáveis
│   ├── graficos_interativos.py # Geração de visualizações dinâmicas
│   ├── graficos.py             # Visualizações estáticas (Matplotlib/Seaborn)
│   ├── inserir_dados.py        # Lógica de carga (Load) no banco de dados
│   ├── main.py                 # Orquestrador central do pipeline ETL
│   └── tratando.py             # Limpeza e transformação profunda (Polars)
├── frontend/                   # Interface do Usuário (Desktop GUI)
│   ├── app_gui.py              # Janela principal e ponto de entrada da UI
│   ├── componentes_interface.py # Widgets e componentes customizados
│   ├── estilos_visuais.py      # Definições de temas e estilização (QSS)
│   ├── janela_edicao.py        # Interface para edição de registros
│   ├── painel_admin.py         # Módulo de administração e controle
│   └── painel_dashboard.py     # Painel visual com indicadores e KPIs
├── dados_analise/              # Raw Data (Arquivos CSV originais)
├── dados_convertidos_prt/      # Cold Storage (Arquivos Parquet brutos)
├── arquivos_tratados/          # Staging Area (Parquet processado e limpo)
├── .env.example                # Template de variáveis de ambiente
├── requirements.txt            # Dependências Python do projeto
├── run.py                      # Atalho para execução do sistema completo
└── organizar_projeto.py        # Script utilitário para organização de pastas
```

---

## ⚙️ Arquitetura e Processo ETL (Implementação)
1. **Extração:** Coleta híbrida via **Kaggle API** e **Playwright** (Web Scraping).
2. **Transformação (Polars Engine):**
   - Conversão para **Parquet** para máxima performance.
   - Tratamento de nulos, tipagem e renomeação de colunas.
3. **Carga:** Sincronização direta com **Supabase (PostgreSQL Cloud)** utilizando SQLAlchemy.
4. **Visualização:** Dashboard BI desenvolvido em **PySide6** com integração Matplotlib e exportação para PDF.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Manipulação:** Polars, Pandas, NumPy.
- **Banco de Dados:** Supabase (Nuvem).
- **Interface:** PySide6.
- **Relatórios:** ReportLab, Plotly.

---
*Desenvolvido por Emerson José - Projeto Integrador ETL.*
