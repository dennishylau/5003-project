import os
import asyncio
import json
import pandas as pd
import time
import logging


def main():

    biden_data = pd.read_csv("./data/hashtag_joebiden.csv", lineterminator='\n')
    trump_data = pd.read_csv("./data/hashtag_donaldtrump.csv", lineterminator='\n')

    biden_data['person'] = 'biden'
    trump_data['person'] = 'trump'

    df = biden_data.append(trump_data)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    df.sort_values(by='created_at', inplace=True)

    CONNECTION_STRING = os.environ.get('CONNECTION_STRING', 'localhost:9092')
    EVENTHUB_NAME = os.environ.get('EVENTHUB_NAME', 'us-election-tweet')
    SPEED_UP = os.environ.get('SPEED_UP', 1000)

    time_pointer = df.iloc[0]['created_at']
    for i, row in df.iterrows():
        time_to_sleep = time_pointer - row['created_at']
        time.sleep(time_to_sleep.seconds / SPEED_UP)
        time_pointer = row['created_at']
        print(row['created_at'])

    if CONNECTION_STRING.lower().startswith('endpoint'):
        from azure.eventhub.aio import EventHubProducerClient
        from azure.eventhub import EventData

        async def run():

            producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STRING, eventhub_name=EVENTHUB_NAME)
            async with producer:
                event_data_batch = await producer.create_batch()

                json_data = json.dumps({"message": "Hello World 1"})
                event_data_batch.add(EventData(json_data))

                await producer.send_batch(event_data_batch)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

    else:
        from kafka import KafkaProducer
        producer = KafkaProducer(bootstrap_servers=[CONNECTION_STRING],
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        for _ in range(100):

            producer.send('fizzbuzz', {'foo': 'bar'})



if __name__ == "__main__":
    main()
