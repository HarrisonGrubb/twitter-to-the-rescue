from datetime import datetime
import os
from pprint import pprint
import json
from dotenv import load_dotenv
import tweepy
import pandas as pd
import pytz
from dateutil import tz
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
load_dotenv()


CONSUMER_KEY = os.environ.get("TWITTER_API_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
sgclient = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID")
# AUTHENTICATE

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

# INITIALIZE API CLIENT

client = tweepy.API(auth)

# ISSUE REQUEST(S)

user = client.me() # get information about the currently authenticated user

data = client.user_timeline('NYCTSubway', exclude_replies = True , include_rts = False)

#timezone fix
utc = pytz.timezone('UTC')

#function for later
def email_out(reciever, delays):
        template_data = {
                "firstName" : reciever,
                "delay": delays}  
    
        sgclient = SendGridAPIClient(SENDGRID_API_KEY)
        from_email = MY_ADDRESS
        to_email = MY_ADDRESS
        message = Mail(from_email, to_email)
        print("MESSAGE:", type(message))

        message.template_id = SENDGRID_TEMPLATE_ID # see receipt.html for the template's structure
        message.dynamic_template_data = template_data        
        try:
                response = sgclient.send(message)
                print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
                print(response.status_code) #> 202 indicates SUCCESS
                print(response.body)
                print(response.headers)

        except Exception as e:
                print("OOPS", e)




tweet_list = []
for t in range(0, len(data)):
    tweet_list.append({
        'text' : data[t].text,
        'time' : data[t].created_at,
        'id' : data[t].id})
tweet_id = [ids['id'] for ids in tweet_list]

#call to get the most recent tweet > then from that tweet update the max id
max_id = tweet_list[-1]['id']
while len(tweet_list) < 20:
        while_data = client.user_timeline('NYCTSubway',max_id = max_id, exclude_replies = True , include_rts = False)
        for t in range(0, len(while_data)):
                if while_data[t].id in tweet_id:
                        pass
                else:
                        tweet_list.append({ # put an if statment before this to check for duplicate
                                'text' : while_data[t].text,
                                'time' : while_data[t].created_at.astimezone(utc),
                                'id' : while_data[t].id})
                        tweet_id.append(while_data[t].id)
        max_id = tweet_list[-1]['id']



# all totally useless changing the time so far
# [ts['time'].to('UTC') for ts in tweet_list]


# [datetime.strptime(str(ts['time']), "%Y-%m-%d %H:%M:%S") for ts in tweet_list]
# [ts['time'].replace(tzinfo = timezone('UTC')) for ts in tweet_list]

# [print(type(ts['time'])) for ts in tweet_list]
# [print(ts['time'].strftime("%Y-%m-%d %H:%M:%S %Z%z")) for ts in tweet_list]


user_travel = [{'user' : 'harrison', 'commutes' : {
        '0' : ['6 train', '7 train', 'Northbound E', 'Southbound E', 'Southbound A', 'Northbound A'],
        '1' : ['7 train', '6 train'],
        '2' : ['6 train', '7 train', 'Northbound E', 'Southbound E', 'Southbound A', 'Northbound A'],
        '3' : ['7 train', '6 train'],
        '4' : ['7 train', '6 train'],}},
              {'user' : 'user2', 'commutes' : {'6' : ['3 train', '2 train'], '5' : ['a train', 'c train']}}]

delay_word = ['delay', 'slow', 'maintenance', 'brakes']

# .weekday() to get day of week 0 is monday 6 is sunday
today = str(datetime.now().weekday())
users_to_email = []
list_count = -1


for user in user_travel:
        if today not in list(user['commutes'].keys()):
                pass
        else:
                list_count += 1
                for twit in tweet_list:
                        for commute in user['commutes'][today]:
                                if commute in twit['text']and any(delay in twit['text'] for delay in delay_word):
                                        users_to_email.append({'user' : user['user'], 'tweet_text' : []})
                                        users_to_email[list_count]['tweet_text'].append(twit['text'])


for recipient in users_to_email:
        reciever = recipient['user']
        delays = recipient['tweet_text']
        reciever = str(reciever)        
        email_out(reciever, delays)






# writing data to file
# new_tweet_data = pd.DataFrame.from_dict(tweet_list)

# csv_file_path = os.path.join(os.path.dirname(__file__), "data", 'data.csv')
# old_tweet_data = pd.read_csv(csv_file_path)

# tweet_data = new_tweet_data.append(old_tweet_data)
# tweet_data.drop_duplicates()

# tweet_data.to_csv(csv_file_path, index= False)

#https://www.afternerd.com/blog/python-string-contains/
# timezone question
#https://stackoverflow.com/questions/6935225/twitter-time-date-stamp-which-time-zone-is-it


# convert to dict
# data[0].__dict__
#data[0].text accessing elements


###### ROADMAP


# 3.) parse time of tweets to ensure that they're relevant

# Fix template at this point 

limit = client.rate_limit_status()
print(limit['resources']['statuses']['/statuses/user_timeline'])

# breakpoint()


# for twit in tweet_list:
#         for user in user_travel:
#                 if today not in list(user['commutes'].keys()):
#                         pass
#                 else:
#                         for commute in user['commutes'][today]:
#                                 if commute in twit['text']and any(delay in twit['text'] for delay in delay_word):
#                                         users_to_email.append({'user' : user['user'], 'tweet_text' : twit['text']})
# ^  original for loop to find compare travelers and delay tweets works but is jenky
