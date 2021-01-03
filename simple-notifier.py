import json
import sys
import twitter
import re

from hashlib import md5

from camping import SUCCESS_EMOJI, FAILURE_EMOJI

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

def create_tweet(tweet):
    lengthLimitedTweet = tweet[:MAX_TWEET_LENGTH]
    resp = api.PostUpdate(lengthLimitedTweet)

    print("The following was tweeted: \n")
    print(lengthLimitedTweet)

def create_custom_tweet():
    tweet = ""
    # optional direct mention a user
    if len(sys.argv) == 4 and sys.argv[3][0] == "@":
        user = sys.argv[3]
        tweet = "{}, ".format(user)
    tweet += "{}".format(sys.argv[2])

    create_tweet(tweet)

def parse_first_line():
    first_line = next(sys.stdin)
    while FAILURE_EMOJI in first_line:
        first_line = next(sys.stdin)
    return first_line

def create_campsite_tweet():
    first_line = parse_first_line()

    for line in sys.stdin:
        line = line.strip()
        if line == "eof":
            break
        elif SUCCESS_EMOJI in line:
            name = " ".join(line.split(":")[0].split(" ")[1:])
            available = line.split(":")[1][1].split(" ")[0]
            site_output = "{} site(s) available in {}".format(available, name)

            first_available_date = (re.search(r'\[.*\]', first_line)).group()
            date_output = "Next Available: {}".format(first_available_date)

            create_tweet(site_output + "\n" + date_output + "🏕")

            first_line = parse_first_line()

    sys.exit(0)

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
    create_campsite_tweet()
elif sys.argv[1] == "custom_tweet":
    create_custom_tweet()
elif sys.argv[1] == "dm":
    send_DM()
else:
    print("The command was not understood. Please either 'tweet' or 'dm', "
            + "followed by the message content and the user information for whom "
            + "you would like to contact.")
sys.exit(0)
