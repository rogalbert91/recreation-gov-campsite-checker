import json
import sys
import twitter

MAX_TWEET_LENGTH = 279
CREDENTIALS_FILE = "twitter_credentials.json"

with open(CREDENTIALS_FILE) as f:
    tc = json.load(f)

def create_tweet(tweet):
    tweet = tweet[:MAX_TWEET_LENGTH]
    api = twitter.Api(
        consumer_key=tc["consumer_key"],
        consumer_secret=tc["consumer_secret"],
        access_token_key=tc["access_token_key"],
        access_token_secret=tc["access_token_secret"],
    )
    resp = api.PostUpdate(tweet)
    print("The following was tweeted: \n")
    print(tweet)

tweet = ""
# optional direct mention a user
if len(sys.argv) == 3 and sys.argv[2][0] == "@":
    user = sys.argv[2]
    tweet = "{}, ".format(user)

tweet += "{}".format(sys.argv[1])

create_tweet(tweet)
sys.exit(0)
