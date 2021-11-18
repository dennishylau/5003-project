import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, TimestampType, StringType, DoubleType, LongType
from pyspark.sql.functions import udf, from_json, col, from_unixtime
from textblob import TextBlob

DATABASE_HOST = os.environ.get('DB_HOST', '')
DATABASE_PORT = os.environ.get('DB_PORT', '')
DATABASE_NAME = os.environ.get('DB_NAME', '')
DATABASE_USER = os.environ.get('DB_USER', '')
DATABASE_PASS = os.environ.get('DB_PASS', '')

ENV = os.environ.get('ENV', 'dev')
KAFKA_CONNECTION_STRING = os.environ.get('KAFKA_CONNECTION_STRING', 'kafka-broker:9092')
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME', 'us-election-tweet')

ENV = 'dev' if ENV == '' else ENV
KAFKA_CONNECTION_STRING = 'kafka-broker:9092' if ENV == 'dev' else KAFKA_CONNECTION_STRING

schema = (
    StructType()
    .add("created_at", LongType(), True)
    .add("tweet_id", DoubleType(), True)
    .add("tweet", StringType(), True)
    .add("likes", DoubleType(), True)
    .add("retweet_count", DoubleType(), True)
    .add("source", StringType(), True)
    .add("user_id", DoubleType(), True)
    .add("user_name", StringType(), True)
    .add("user_screen_name", StringType(), True)
    .add("user_description", StringType(), True)
    .add("user_join_date", TimestampType(), True)
    .add("user_followers_count", DoubleType(), True)
    .add("user_location", StringType(), True)
    .add("lat", DoubleType(), True)
    .add("long", DoubleType(), True)
    .add("city", StringType(), True)
    .add("country", StringType(), True)
    .add("continent", StringType(), True)
    .add("state", StringType(), True)
    .add("state_code", StringType(), True)
    .add("collected_at", TimestampType(), True)
    .add("person", StringType(), True)
    .add("time_to_sleep", DoubleType(), True)
)


def get_polarity(tweet):
    return TextBlob(tweet).sentiment.polarity


def timescale_sink(df, batch_id):
    url = f'jdbc:postgresql://{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?user={DATABASE_USER}&password={DATABASE_PASS}'
    df.filter(df['person'] == 'biden').write.jdbc(url, 'joebiden_tweets', mode='append')
    df.filter(df['person'] == 'trump').write.jdbc(url, 'donaldtrump_tweets', mode='append')


def main():

    spark = (
        SparkSession.builder
        .appName('5003-project')
        .master('spark://spark-master:7077')
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel('ERROR')

    udf_get_polarity = udf(get_polarity, DoubleType())

    df = (spark
          .readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", KAFKA_CONNECTION_STRING)
          .option("subscribe", KAFKA_TOPIC_NAME)
          .option("startingOffsets", "earliest")
          .load()
          .select(from_json(col("value").cast("string"), schema).alias("data"))
          .select("data.*")
          .withColumn('created_at', from_unixtime(col("created_at") / 1000).cast("timestamp"))
          .withColumn("score", udf_get_polarity(col("tweet")))
          )

    write_table = (
        df
        .writeStream
        .outputMode("append")
        .foreachBatch(timescale_sink)
        .start()
        .awaitTermination()
    )


if __name__ == '__main__':
    main()
