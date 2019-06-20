import datetime
import os
from pprint import pprint
import json
from dotenv import load_dotenv
import tweepy
import pandas as pd

load_dotenv()


CONSUMER_KEY = os.environ.get("TWITTER_API_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# AUTHENTICATE

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# INITIALIZE API CLIENT

client = tweepy.API(auth)

# ISSUE REQUEST(S)

user = client.me() # get information about the currently authenticated user

data = client.user_timeline('NYCTSubway', count = 60,max_id = 1141476562350563329, exclude_replies = True , include_rts = False)

tweet_list = []
for t in range(0, len(data)):
    tweet_list.append({
        'text' : data[t].text,
        'time' : data[t].created_at,
        'id' : data[t].id})

# dynamically update the max id in my api call to move the starting point back to the end of my call

tweet_data = pd.DataFrame.from_dict(tweet_list)

csv_file_path = os.path.join(os.path.dirname(__file__), "data", 'data.csv')

tweet_data.to_csv(csv_file_path, index= False)

#https://www.afternerd.com/blog/python-string-contains/


# convert to dict
# data[0].__dict__
#data[0].text accessing elements


###### ROADMAP
# 1.) get longer duration of tweets

# 2.) parse the text to test if my train and delay is in the text

# 3.) message me that it is

# 4.) deploy to heroku > schedule to run

# limit = client.rate_limit_status()
