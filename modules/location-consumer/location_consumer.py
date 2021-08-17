import json
import os
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_Point

# Add environment variables in deployment
kafka_topic = os.environ["KAFKA_TOPIC"]
kafka_host = os.environ["KAFKA_HOST"]
db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_name = os.environ["DB_NAME"]

kafka_consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_host)

def write_location(location):
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, db_host, db_port, db_name), echo=True)
    with engine.connect() as connection:
        coordinate = ST_Point(location["latitude"], location["longitude"])
        sql_statement = "insert into public.location (person_id, coordinate) values ({}, {})".format(int(location["person_id"]), coordinate)
        connection.execute(sql_statement)

for location in kafka_consumer:
    print(location)
    location_json = json.loads(location)
    write_location(location_json)



