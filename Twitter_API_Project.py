# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:31:36 2021

@author: t_zim
"""

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


# # # # TWITTER AUTHENTICATOR # # # #
        # Authenticates your dev account through twitter.  Uses twitter_credentials.py.
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
        # Only makes sure there is data coming in, and errors if not

class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['tweet'] = np.array([tweet.text for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


    # # # # OUPUT DATASETS # # # #
class OutputTweets():
    """
    Functionality for outputting data to files in specified location.
    """

    def __init__(self):
        pass

    def output_trending_topics(self,filepath):
        pass

    def output_search_tweets(self,filepath):
        pass


    # # # # TWITTER CLIENT # # # #
class TwitterClient():

    def __init__(self, twitter_user=None, location=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user
        self.location = location


    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets



    def get_trending_tweets(self,num_tweets):
        trending_tweets = []
        for tweet in Cursor(self.twitter_client.trends_closest, lat='38.8899', long='77.0091').items(num_tweets):
            trending_tweets.append(tweet)
        return trending_tweets

    # Grab most recent tweets from a given location and query criteria
    # # # # TWITTER CLIENT # # # #
class GeoSearchTweets():

    def __init__(self, twitter_user=None, location=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user
        self.location = location


    def get_geo_tweets(self, num_tweets):
        geo_tweets = []
        for tweet in Cursor(self.twitter_client.search).items(num_tweets):
            geo_tweets.append(tweet)
        return geo_tweets

    # Grab Trends and their Tweet Volume for a specified location



#%%
if __name__ == '__main__':


# # # # Initialize and authenticate # # # #

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    geo_search_tweets = GeoSearchTweets()

    api = twitter_client.get_twitter_client_api()


# # # # Trending Tweet Operations # # # #

    """
    The result of this section is a DataFrame with all trending topics from a location of interest
        1. Identify location's Yahoo ID
        2. Use the Yahoo ID to create a list of trending topics and tweet volume for that location
    """

    # SET UP VARIABLES

    # Geolocation
    latitude = '38.8899'
    longitude = '-77.0091'
    radius = '10mi'
    yahoo_id = '2514815'

    # US Capitol for 2021 Presidential Inaguration (lat/long)
    place = api.trends_closest(lat=latitude,long=longitude)
    print(place) # Look for the Yahoo Where In the World identifier for the location you want to search

    # Use Yahoo identifier for US Capitol to query trending topics for that location
    trends = api.trends_place(id=yahoo_id)

    # Build Dataframe with Trends and Tweet Volumes for the specified location
    for value in trends:
        trends_in_location = pd.DataFrame(data=[trend['name'] for trend in value['trends']], columns=['name'])
        trends_in_location['tweet_volume'] = np.array([trend['tweet_volume'] for trend in value['trends']])

    trends_in_location.set_index('name',inplace=True)
    # # # # # SHOULD SORT THESE TWEETS BY Tweet_Volume # # # # #

    # Display the dataframe
    print('Trends in Location')
    trends_in_location.head(25)

    len(trends_in_location)

# # # # Geo Location Operations # # # #
    """
    Use the search function to query twitter for tweets meeting specific criteria.
    Current criteria: Recent tweets for trending topics at a specified location in the world
        1. Use the trend dataframe (above) to specify query terms for your search and the Yahoo location id
        2. Use Trending Topics as search terms to compile tweets that match the topics to build a corpus (IN CONSTRUCTION)
        3. Do descriptive analytics on these tweets - sentiment, frequency graphs (IN CONSTRUCTION)
    """

    # SET UP VARIABLES

    # Geolocation
    latitude = '38.8899'
    longitude = '-77.0091'
    radius = '10mi'
    # Mixed, recent, popular
    result_type = 'recent'
    # Terms to query.  Currently, top 5 trending topics in the location.
    query_terms = [trends_in_location.index[0:5]]
    # End date (query will go back 7 days from this date)
    date = '2021-01-23'

    geo_tweets = api.search(q=query_terms,
                            geo_code=[latitude,longitude,radius],
                            result_type = result_type,
                            until=date,
                            num_tweets=10)
# geo_search_tweets



    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])


   #%%
# TESTING PLAYGROUND

print(trends_in_location)





#%%
"""
    NOT IN USE

if __name__ == '__main__':


    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
"""