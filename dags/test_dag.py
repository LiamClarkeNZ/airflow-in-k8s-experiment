from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import logging

# try:
#     from .libs import FOO
# except Exception as e:
#     logging.warning(e)
#     logging.warning(__file__)
#     logging.warning(__name__)
#     logging.warning(__package__)
#     import sys
#     logging.warning(sys.path)
#
# try:
#     from libs import FOO
# except Exception as e:
#     logging.warning(e)
#     logging.warning(__file__)
#     logging.warning(__name__)
#     logging.warning(__package__)
#     import sys
#     logging.warning(sys.path)
# try:
#     from dags.libs import FOO
#     logging.warning("dags.libs.imported")
# except Exception as e:
#     logging.warning(e)
#     logging.warning(__file__)
#     logging.warning(__name__)
#     logging.warning(__package__)
#     import sys
#     logging.warning(sys.path)
#
#
# try:
#     from dags import libs
#     logging.warning("dags.libs.only.imported")
#     logging.warning(libs.FOO)
# except Exception as e:
#     logging.warning(e)
#     logging.warning(__file__)
#     logging.warning(__name__)
#     logging.warning(__package__)
#     import sys
#     logging.warning(sys.path)
#
#
# try:
#     from repo.dags.libs import FOO
#     logging.warning("repo.dags.libs.imported")
# except Exception as e:
#     logging.warning(e)
#     logging.warning(__file__)
#     logging.warning(__name__)
#     logging.warning(__package__)
#     import sys
#     logging.warning(sys.path)


import os
import sys

logging.warning(os.listdir("/opt/airflow/dags/repo/dags/"))
logging.warning(os.listdir("/opt/airflow/dags/repo/dags/libs"))
logging.warning(os.listdir("/opt/airflow/dags/repo/dags/libs2"))

try:
    print("XXXXXX")
    print(os.getcwd())
    sys.path.insert(0, os.path.dirname(__file__))
    from libs2.test import da_func
    logging.warning("da_func.imported")
except Exception as e:
    logging.warning(e)
    logging.warning(__file__)
    logging.warning(__name__)
    logging.warning(__package__)



default_args = {
    'owner': 'jeff',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'dag-from-git',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)


def print_context(ds, **kwargs):
    print(kwargs)
    print(ds)
    print(FOO)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 30',
    retries=3,
    dag=dag,
)
dag.doc_md = __doc__

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)

run_this >> t1 >> [t2, t3]
