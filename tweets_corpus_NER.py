from json import loads, dump
from requests import get
import tweepy
from urllib.parse import urlencode

def oauth(secrets):
    auth = tweepy.OAuthHandler(secrets["api_key"], secrets["api_key_secret"])
    auth.set_access_token(secrets["access_token"], secrets["access_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)
    return api

def getTitles():
    titles = list()
    for endpoint in ['movie', 'tv']:
        for page in range(1, 500):
            query = urlencode({
                'api_key': <API_KEY>,
                'language': 'es-ES',
                'page': page,
                'sort_by': 'popularity.desc'
            })
            api_response = get(f'https://api.themoviedb.org/3/discover/{endpoint}?{query}').text
            results = loads(api_response)['results']
            try:
                film_titles = [result['title'] for result in results]
                titles.extend(film_titles)
            except:
                tv_titles = [result['name'] for result in results]
                titles.extend(tv_titles)
    return titles

secrets = {
    "api_key": "<API_KEY>",
    "api_key_secret": "<API_KEY_SECRET>",
    "access_token": "<ACCESS_TOKEN>",
    "access_token_secret": "<ACCESS_TOKEN_SECRET>"
}

api = oauth(secrets)
titles = getTitles()
tweet_cache = list()

with open('tweets.jsonl', 'w') as w:
    for title in titles:
        tweets = tweepy.Cursor(api.search, q=f'"{title}"', lang='es', tweet_mode="extended").items(100)
        for tweet in tweets:
            status = tweet._json
            if "retweeted_status" in status:
                status = status["retweeted_status"]
            if status["id"] not in tweet_cache:
              data = {
                  'id': status["id"],
                  'text': repr(status["full_text"]),
                  'title': title
              }
              dump(data, w, ensure_ascii=False)
              w.write('\n')
              tweet_cache.append(status["id"])
