import os
import asyncio
import pandas as pd
import time
import logging

KAFKA_CONNECTION_STRING = os.environ.get('KAFKA_CONNECTION_STRING', 'kafka-broker:9092')
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME', 'us-election-tweet')
SPEED_UP = os.environ.get('SPEED_UP', 1000)
ENV = os.environ.get('ENV', 'dev')

ENV = 'dev' if ENV == '' else ENV
KAFKA_CONNECTION_STRING = 'kafka-broker:9092' if ENV == 'dev' else KAFKA_CONNECTION_STRING


def main():

    logging.info(f'Loaded environment variables:' +
                 f'\nENV: {ENV}' +
                 f'\nKAFKA_CONNECTION_STRING: {KAFKA_CONNECTION_STRING}' +
                 f'\nKAFKA_TOPIC_NAME: {KAFKA_TOPIC_NAME}' +
                 f'\nSPEED_UP: {SPEED_UP}')

    data_dir = "./data"
    biden_data = pd.read_csv(os.path.join(data_dir, "hashtag_joebiden.csv"), lineterminator='\n')
    trump_data = pd.read_csv(os.path.join(data_dir, "hashtag_donaldtrump.csv"), lineterminator='\n')

    logging.info(f'Loaded data from {data_dir}.')

    biden_data['person'] = 'biden'
    trump_data['person'] = 'trump'

    df = biden_data.append(trump_data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    df.sort_values(by='created_at', inplace=True)

    df['time_to_sleep'] = df['created_at'].diff().apply(lambda x: x.seconds / SPEED_UP).fillna(0)

    logging.info('Preprocessed data by combining.')

    if (KAFKA_CONNECTION_STRING.lower().startswith('endpoint')) and (ENV == 'prod'):
        # lazy import
        from azure.eventhub.aio import EventHubProducerClient
        from azure.eventhub import EventData

        async def run():

            client = EventHubProducerClient.from_connection_string(conn_str=KAFKA_CONNECTION_STRING,
                                                                   eventhub_name=KAFKA_TOPIC_NAME)
            async with client:
                for _, row in df.iterrows():
                    event_data_batch = await client.create_batch()
                    event_data_batch.add(EventData(row.to_json()))
                    await asyncio.sleep(row['time_to_sleep'])
                    await client.send_batch(event_data_batch)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

    else:
        # lazy import
        from kafka import KafkaProducer
        from kafka.errors import NoBrokersAvailable

        # retry every 5 seconds to wait until broker is set up
        while True:
            try:
                producer = KafkaProducer(bootstrap_servers=[KAFKA_CONNECTION_STRING])

                for _, row in df.iterrows():
                    time.sleep(row['time_to_sleep'])
                    producer.send(KAFKA_TOPIC_NAME, row.to_json().encode())

                break
            except NoBrokersAvailable:
                time.sleep(5)
                continue

    logging.info('All data has been sent to Kafka.')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
