import datetime
import os
from pprint import pprint
import json
from dotenv import load_dotenv
import tweepy
import pandas as pd
from pytz import timezone
from dateutil import tz
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

data = client.user_timeline('NYCTSubway', exclude_replies = True , include_rts = False)


tweet_list = []
for t in range(0, len(data)):
    tweet_list.append({
        'text' : data[t].text,
        'time' : data[t].created_at,
        'id' : data[t].id})
tweet_id = [ids['id'] for ids in tweet_list]

#call to get the most recent tweet > then from that tweet update the max id
max_id = tweet_list[-1]['id']
while len(tweet_list) < 4:
        while_data = client.user_timeline('NYCTSubway',max_id = max_id, exclude_replies = True , include_rts = False)
        for t in range(0, len(while_data)):
                if while_data[t].id in tweet_id:
                        pass
                else:
                        tweet_list.append({ # put an if statment before this to check for duplicate
                                'text' : while_data[t].text,
                                'time' : while_data[t].created_at,
                                'id' : while_data[t].id})
                        tweet_id.append(while_data[t].id)
        max_id = tweet_list[-1]['id']

x = 'y'

# [ts['time'].replace(tzinfo = 'UTC') for ts in tweet_list]
# [ts['time'].astimezone(timezone('US/Eastern')) for ts in tweet_list]


# my key words to search for as well as my trains on days traveled        
delay_word = ['delay', 'slow', 'maintenance', 'brakes']
travel_dict = [
        {'Monday' : 0, 'trains' : ['6 train', '7 train', 'e train', 'c train']},
        {'Tuesday' : 1, 'trains': ['6 train', '7 train']},
        {'Wednesday' : 2, 'trains': ['6 train', '7 train', 'e train', 'c train']},
        {'Thursday' : 3, 'trains': ['6 train', '7 train']},
        {'Friday' : 4, 'trains' : ['6 train', '7 train']},
]

for twit in tweet_list:
        if any()        

# .weekday() to get day of week 0 is monday 6 is sunday
# need to adjust for new dict style and filter based on day of week (super hard date time filter)
# for t in tweet_list:
#     if any(delay in t['text'] for delay in delay_word) and any(train in t['text'] for train in trains):
#         late_count += 1
#         if any(day in t['Day'] for day in Days):
#             late_date_count += 1

new_tweet_data = pd.DataFrame.from_dict(tweet_list)

csv_file_path = os.path.join(os.path.dirname(__file__), "data", 'data.csv')
old_tweet_data = pd.read_csv(csv_file_path)

tweet_data = new_tweet_data.append(old_tweet_data)
tweet_data.drop_duplicates()

tweet_data.to_csv(csv_file_path, index= False)

#https://www.afternerd.com/blog/python-string-contains/
# timezone question
#https://stackoverflow.com/questions/6935225/twitter-time-date-stamp-which-time-zone-is-it


# convert to dict
# data[0].__dict__
#data[0].text accessing elements


###### ROADMAP

# 2.) parse the text to test if my train and delay is in the text

# 3.) parse time of tweets to ensure that they're relevant

# next message me abou the delay

# 4.) deploy to heroku > schedule to run

limit = client.rate_limit_status()
print(limit['resources']['statuses']['/statuses/user_timeline'])

breakpoint()