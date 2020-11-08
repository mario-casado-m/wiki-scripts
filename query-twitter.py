import tweepy


def oauth(secrets):
    auth = tweepy.OAuthHandler(secrets["api_key"], secrets["api_key_secret"])
    auth.set_access_token(secrets["access_token"], secrets["access_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)
    return api


secrets = {
    "api_key": "<API_KEY>",
    "api_key_secret": "<API_KEY_SECRET>",
    "access_token": "<ACCESS_TOKEN>",
    "access_token_secret": "<ACCESS_TOKEN_SECRET>"
}
api = oauth(secrets)
# api.update_status('Hello, world!')
tweets = tweepy.Cursor(api.search, q='"desde que"', tweet_mode="extended").items()
with open("tweets.tsv", "w") as w:
    w.write("tweet_id\tdate\ttext\tuser_id\n")
    for tweet in tweets:
        status = tweet._json
        if "retweeted_status" in status:
            status = status["retweeted_status"]
        w.write(
            "{tweet_id}\t{date}\t{text}\t{user_id}\n".format(
                tweet_id=status["id"],
                date=status["created_at"],
                text=repr(status["full_text"]),
                user_id=status["user"]["id_str"],
            )
        )
