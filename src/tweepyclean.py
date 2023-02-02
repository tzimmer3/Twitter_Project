import re
import string
import numpy as np
import pandas as pd


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['tweet'] = np.array([tweet.text for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

    ## FUNCTIONS
    def clean_special_chars(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def extract_hashtags(tweet):
        regex = "#(\w+)"
        hashtag_list = re.findall(regex, tweet)
        return hashtag_list

    def extract_mentions(tweet):
        regex = "@(\w+)"
        mentions_list = re.findall(regex, tweet)
        return mentions_list

    def count_caption_words(tweet):
        return sum([i.strip(string.punctuation).isalpha() for i in tweet.split()])

    def remove_stopwords(tweet, stopwords):
        tweet = [word for word in tweet if word not in stopwords]
        return tweet


## APPENDIX

"""
# Remove stop words
## NOT NEEDED AT THIS TIME.  Not using stopword removal.  Should work if eventually needed.
#df['tweet_nostops'] = df['tweet'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
"""