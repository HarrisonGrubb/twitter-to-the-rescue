# Twitter to the Rescue
----
### Saving your commute one tweet at a time

By parsing through the MTA's twitter account at scheduled times.  This project can give you an advanced notice subway delays.  

## Setup

You can clone this repo to your own Github page either through the web-based GUI or through GIT commands.

After you've forked the repo ensure you download a local copy to your machine.  From there you can navigate to your repo via the below command.

``` cd /you_repo_name ```

From there you'll want to create a new virtual enviroment to install the necessary third party pacakges.  Follow the commands below if you need help setting up your virtual enviroment.

 
```conda create -n name-of-your-env python = 3.7```
```conda activate name-of-your-env```

Now that you've got a working virtual enviroment you can use pip to install the third party packages via the command below.

``` pip install -r requirments.txt```

Finally, this program requires registering for three services: 
* Twitter: source of the Tweets :)
* Sendgrid: makes sending email notices easy
* Heroku: to PAAS company that will allow you to schedule the program

## Security Steps

After signing up for Twitter, Sendgrid, and if you want to schedule the program Heroku.  You'll need to store these variables in a .env file.  In your directory you can run the following command.

``` touch .env```

Open that file and fill in the below variables with your own unique login credentials.

* CONSUMER_KEY = your-key-here
* CONSUMER_SECRET = your-key-here
* ACCESS_TOKEN = your-key-here
* ACCESS_TOKEN_SECRET = your-key-here
* SENDGRID_API_KEY = your-key-here
* MY_ADDRESS = your-email-address-here
* SENDGRID_TEMPLATE_ID = name-of-the-sendgrid-template

## About to run

Before you can run this code you'll want to make sure you have a copy of the sendgrid email template saved into your sendgrid profile.  I've included a copy of mine with this repo.

Additionally in line 108 of the twitter-rescue.py you'll need to update your own train schedule to make it relevant for you.  If you made any adjustments look for the data named user_travel.  

Navigate through the nested dictionary replacing my name with yours.  The day index is listed below so you can make sure the days you care about are included in the data.  

* 0 = Monday
* 1 = Tuesday
* 2 = Wednesday
* 3 = Thursday
* 4 = Friday
* 5 = Saturday
* 7 = Sunday

Additionally, if you take a train with letters in it, for example the A Train, include both directions (example below).  This is particularly relevant for people who take the A Train.  The program will pick up every instance of the following passage as a delay: "6 trains are running express after **a train's** brakes were activated".  

* This is good: "Northbound E", "Southbound E"
* This will have too many false positives: "E train"

If you'd like for the tweets you've captured to be stored locally you can uncomment the code after the comment writing data to file.

## Running the code

If you've opted to run this locally make sure you're still in the project's local repo.  You can run the code with the below command.

``` python twitter-rescue.py ```

If you've followed the above steps correctly **and** there is a delay you'll get a 202 response from sendgrid :D.  If there is no delay but you see a Twitter API call count the program also ran correctly. 

You will also get a notice of how many Twitter API calls you have left.  You have a maximum of 900 per 15 minutes. Unless you dramatically alter the amount of tweets you want in the variable tweet_list you won't run out of API calls.  

## Deploying to Heroku

If you would like to deploy this to Heroku please follow the instructions below from my professor.  You can simply replace the example app with this one and you'll be up in the cloud in no time.

https://github.com/prof-rossetti/nyu-info-2335-201905/tree/master/exercises/deploying-services


## Future Roadmap

There are some items I'm working on that may or may not make it into the submitted version of this project.  They're listed below in order of importance.

* Adjusting the time of the tweets: I can't get pendulum installed
* Integrating with Google Sheets to store the tweets in the cloud
* Through Google Sheets and Forms I'd like to be able to adjust my travel schedule without touching my code
* Occasionally I will get multiple emails from a single run