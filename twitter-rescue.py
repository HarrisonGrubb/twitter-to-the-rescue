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

data = client.user_timeline('NYCTSubway', exclude_replies = True , include_rts = False)


tweet_list = []
for t in range(0, len(data)):
    tweet_list.append({
        'text' : data[t].text,
        'time' : data[t].created_at,
        'id' : data[t].id})

#call to get the most recent tweet > then from that tweet update the max id
max_id = tweet_list[-1]['id']
while len(tweet_list) < 20:
        while_data = client.user_timeline('NYCTSubway',max_id = max_id, exclude_replies = True , include_rts = False)
        for t in range(0, len(while_data)):
                tweet_list.append({ # put an if statment before this to check for duplicate
                        'text' : while_data[t].text,
                        'time' : while_data[t].created_at,
                        'id' : while_data[t].id})
        max_id = tweet_list[-1]['id']

# able to create list of tweets but not sure why I'm getting duplicates
# create if statement to check for duplicate
# may want to pull in the dict of other tweets id's for future reference
        




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
demo_text = [
        'southbound 6 trains are delayed'
        , 'southbound 3 trains are delayed'
        , 'northbound 6 trains have resumed service'
        , 'uptown f trains have resumed service'
        , 'southbound 6 trains have residual delays']

delay_catcher = 0
for text in demo_text:
        if '6 train' in text and 'delay' in text:
                delay_catcher += 1
                print(text)
        else:
                pass


# 3.) parse time of tweets to ensure that they're relevant

# next message me abou the delay

# 4.) deploy to heroku > schedule to run

# limit = client.rate_limit_status()
