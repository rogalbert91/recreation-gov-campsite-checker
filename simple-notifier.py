import json
import sys
import twitter

MAX_TWEET_LENGTH = 279
CREDENTIALS_FILE = "twitter_credentials.json"

with open(CREDENTIALS_FILE) as f:
    tc = json.load(f)

api = twitter.Api(
    consumer_key=tc["consumer_key"],
    consumer_secret=tc["consumer_secret"],
    access_token_key=tc["access_token_key"],
    access_token_secret=tc["access_token_secret"],
)

def create_tweet():
    tweet = ""
    # optional direct mention a user
    if len(sys.argv) == 4 and sys.argv[3][0] == "@":
        user = sys.argv[3]
        tweet = "{}, ".format(user)
    tweet += "{}".format(sys.argv[2])

    lengthLimitedTweet = tweet[:MAX_TWEET_LENGTH]
    resp = api.PostUpdate(lengthLimitedTweet)

    print("The following was tweeted: \n")
    print(lengthLimitedTweet)

def send_DM():
    if sys.argv[3] == None:
        print("You must provide a user ID as the third argument.")
        exit(1)
    user = sys.argv[3]
    text = sys.argv[2]

    resp = api.PostDirectMessage(user_id=user, text=text, return_json=True)

    print("\nAPI Response:")
    print(resp)
    print("\nThe following message was sent to {}:".format(user))
    print(text)

if sys.argv[1] == "tweet":
    create_tweet()
elif sys.argv[1] == "dm":
    send_DM()
else:
    print("The command was not understood. Please either 'tweet' or 'dm', "
            + "followed by the message content and the user information for whom "
            + "you would like to contact.")
sys.exit(0)
