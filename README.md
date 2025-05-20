# Projeto de Validação de Dados com Airflow e Great Expectations

Este projeto implementa um pipeline de validação de dados para migrações, combinando **Apache Airflow** (orquestração) e **Great Expectations** (testes de qualidade). Valida diferenças entre dados pré e pós-migração (contagem, médias, nulidade).

## Configuração
1. **Dependências**:
   pip install apache-airflow great_expectations pandas faker
   
    Great Expectations:
    great_expectations init
    great_ expectations datasources new
    great_expectations suite new  # Crie 'migration_suite'

    airflow db init
    airflow users create --username admin --password admin --role Admin

## Resultados
1. Relatórios JSON em /tmp/ge_results_*.json

2. Data Docs HTML em great_expectations/uncommitted/data_docs/