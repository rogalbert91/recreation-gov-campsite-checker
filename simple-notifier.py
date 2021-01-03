import json
import sys
import twitter

from hashlib import md5

from camping import SUCCESS_EMOJI

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

    resp = api.PostUpdate(tweet)

    print("The following was tweeted:")
    print(lengthLimitedTweet)

def create_custom_tweet():
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

def create_campsite_tweet():
    first_line = next(sys.stdin)
    first_line_hash = md5(first_line.encode("utf-8")).hexdigest()

    available_site_strings = []
    for line in sys.stdin:
        line = line.strip()
        if SUCCESS_EMOJI in line:
            name = " ".join(line.split(":")[0].split(" ")[1:])
            available = line.split(":")[1][1].split(" ")[0]
            s = "{} site(s) available in {}".format(available, name)
            available_site_strings.append(s)

    if available_site_strings:
        tweet = ""
        tweet += first_line.rstrip()
        tweet += " 🏕🏕🏕\n"
        tweet += "\n".join(available_site_strings)
        create_tweet(tweet)
        sys.exit(0)
    else:
        print("No campsites available, not tweeting 😞")
        sys.exit(1)


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
