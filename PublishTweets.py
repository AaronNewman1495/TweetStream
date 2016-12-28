import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
from kafka.errors import KafkaError
from TweetParser import TweetParser
import yaml

with open('Secrets.yml', 'r') as f:
	secrets = yaml.load(f)
with open('Settings.yml', 'r') as g:
	settings = yaml.load(g)

access_token = secrets["Twitter"]["accessToken"]
access_token_secret = secrets["Twitter"]["accessTokenSecret"]
consumer_key = secrets["Twitter"]["apiKey"]
consumer_secret = secrets["Twitter"]["apiSecret"]

kafka_host = secrets["Kafka"]["host"]
kafka_port = secrets["Kafka"]["port"]
kafka_topic = settings["Kafka"]["topic"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def init_producer():
	tcp_string = kafka_host + ':' + str(kafka_port)
	return KafkaProducer(bootstrap_servers=[tcp_string])

api = tweepy.API(auth)

producer = init_producer()

tweet_parser = TweetParser()

for status in tweepy.Cursor(api.home_timeline).items(10):
	tweet_message = tweet_parser.parse(status._json)
	if tweet_message is not None:
		producer.send(kafka_topic, tweet_message)


