from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
import pandas as pd
import json
import os

default_args = {
    'owner': 'admin',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

def validate_data(file_path, suite_name):
    """
    Valida um arquivo CSV usando Great Expectations.
    """
    
    context = gx.get_context(
        context_root_dir=os.path.expanduser('~/Dev/MigraData/great_expectations')
    )
    
    
    df = pd.read_csv(file_path)
    
    
    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_datasource",
        data_connector_name="default_runtime_data_connector",
        data_asset_name=os.path.basename(file_path).replace('.csv', ''),
        runtime_parameters={"batch_data": df},
        batch_identifiers={
            "default_identifier_name": "default_identifier"
        }
    )
    
    
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    results = validator.validate()
    
    
    result_path = f"/tmp/ge_results_{os.path.basename(file_path)}.json"
    with open(result_path, "w") as f:
        json.dump(results.to_json_dict(), f, indent=2)
    
    
    if not results.success:
        error_msg = f"Validação falhou para {file_path}. Verifique {result_path}"
        raise ValueError(error_msg)
    
    return f"Validação bem-sucedida para {file_path}"

with DAG(
    'validate_migration_data',
    default_args=default_args,
    description='Valida dados de migração com Great Expectations',
    schedule_interval=None,
    catchup=False,
    tags=['validation']
) as dag:

    validate_old_data = PythonOperator(
        task_id='validate_old_data',
        python_callable=validate_data,
        op_kwargs={
            'file_path': os.path.expanduser('~/Dev/MigraData/great_expectations/data/old_data.csv'),
            'suite_name': 'migration_suite'
        }
    )

    validate_new_data = PythonOperator(
        task_id='validate_new_data',
        python_callable=validate_data,
        op_kwargs={
            'file_path': os.path.expanduser('~/Dev/MigraData/great_expectations/data/new_data.csv'),
            'suite_name': 'migration_suite'
        }
    )

    
    validate_old_data >> validate_new_data
