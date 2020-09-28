from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
from MarkovBot import MarkovBot

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'gb',
    'depends_on_past': False,
    'start_date': datetime(2016, 4, 15),
    'email_on_failure': ['baymeevag@gmail.com'],
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'schedule_interval': timedelta(hours=2)
}

dag = DAG('Helloworld', default_args=default_args)

def shitpost():
    topic = 'mathematics'
    bot = MarkovBot(topic)
    tweet = bot.get_tweet()
    bot.api.update_status(tweet) 

run_this = PythonOperator(
    task_id='shitpost',
    provide_context=True,
    python_callable=shitpost,
    dag=dag
)
