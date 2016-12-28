import json

class TweetParser:

	def parse(self, tweet):
		result = {}
#		print(tweet.__class__.__name__)

		result['tweet_id'] = tweet['id']
		result['coordinates'] = tweet['coordinates']
		result['text'] = tweet['text']
		result['hashtags'] = tweet['entities']['hashtags']

		if result['coordinates'] is None:
			return None
		else:
			result['coordinates'] = result['coordinates']['coordinates']
			return json.dumps(result)
