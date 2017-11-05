#Vinh Luong
#Github Link: https://github.com/vinhluong274/hw8

# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching.
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

## [PART 1]

def get_tweets():
    data = api.search('umsi')#searches twitter feed for tweets including UMSI
    if 'umsi' in CACHE_DICTION:
        print("Data was in the cache \n")
        return CACHE_DICTION['umsi']
    else:
        print("Making a request for new data...\n")
        data = api.search('umsi')
        CACHE_DICTION['umsi'] = data
        dumped_json_cache = json.dumps(CACHE_DICTION)#stores the search in json file named CACHE_DICTION
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION["umsi"]

tweet_result = get_tweets()
for a in tweet_result["statuses"]:# iterates through the 5 most recent tweets
    print("TEXT: ", a['text'])
    print("CREATED AT: : ", a['created_at'])
    print("USERNAME: ", a['user']['screen_name'])#this is a nested dictionary so we must have two indices to reference two keys
    print("\n")

## [PART 2]
# 1 - Make a connection to a new database tweets.sqlite, and create a variable to hold the database cursor.
connection = sqlite3.connect('twitterDB.sqlite')
cursor = connection.cursor()

# 2 - Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
cursor.execute("DROP TABLE IF EXISTS Tweets")
cursor.execute("CREATE TABLE Tweets (tweet_id TEXT, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets INTEGER)")

# 3 - Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweets.
umsi_tweets = get_tweets()

# 4 - Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.
for a in umsi_tweets["statuses"]:
    tup = a["id"], a["user"]["screen_name"], a["created_at"], a["text"], a["retweet_count"]
    cursor.execute("INSERT INTO Tweets (tweet_id, author, time_posted, tweet_text, retweets) VALUES (?,?,?,?,?)", tup)

#  5- Use the database connection to commit the changes to the database
connection.commit()

## [PART 3] - SQL statements
for line in cursor.execute("SELECT * FROM Tweets ORDER BY time_posted DESC"):
    print(line[2], line[3] + "\n") #indexes 2 and 3 are respectively the Timestamp and tweet

# Select the author of all of the tweets (the full rows/tuples of information) that have been retweeted MORE
# than 2 times, and fetch them into the variable more_than_2_rts.
# Print the results
more_than_2_rts = []

for row in cursor.execute("SELECT * FROM Tweets WHERE retweets >= 2"): #SQL statement that selects all tweets where retweets column is greater than 2
    more_than_2_rts.append(row[1])

print("These users have had at least 2 RTs on their UMSI Tweets: ")
for name in more_than_2_rts:
    print(name + "\n")



if __name__ == "__main__":
    unittest.main(verbosity=2)
