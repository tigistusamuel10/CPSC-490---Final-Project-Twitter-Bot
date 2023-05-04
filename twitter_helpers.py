import tweepy

import os
import dotenv
from dotenv import load_dotenv
import random

load_dotenv()


def generate_client(consumer_key = None, consumer_secret = None, access_token = None, access_token_secret = None, bt_present = False, bearer_token = None):
    """
    This function generates a Tweepy Client object to perform actions on Twitter.
    The function can create a client using either the authentication credentials for an app or a bearer token.

    Args:
        consumer_key (str): The consumer key for your Twitter app.
        consumer_secret (str): The consumer secret for your Twitter app.
        access_token (str): The access token for your Twitter app.
        access_token_secret (str): The access token secret for your Twitter app.
        bt_present (bool): A flag indicating whether or not a bearer token is being used.
        bearer_token (str): The bearer token for a Twitter app, used if bt_present is True.

    Returns:
        tweepy.Client: A Tweepy Client object used for performing actions on Twitter.

    Note:
        - If bt_present is True, then the consumer_key, consumer_secret, access_token, and access_token_secret
        parameters will be ignored, and only the bearer_token parameter will be used.
        - If bt_present is False, then the consumer_key, consumer_secret, access_token, and access_token_secret
        parameters are required, and the bearer_token parameter will be ignored.
    """
    if(bt_present):
        client = tweepy.Client(bearer_token = bearer_token)
    else:

        client = tweepy.Client(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token = access_token, access_token_secret = access_token_secret)
    return client


def send_tweet(client: tweepy.Client, tweet:str):
    """
    Sends a tweet using the specified Twitter API client.

    Parameters:
        client (tweepy.Client): A Tweepy client object that is authorized to make requests to the Twitter API.
        tweet (str): The text of the tweet to be sent.

    Returns:
        response: The response object returned by the Twitter API after creating the tweet.
    """
    response = client.create_tweet(text = tweet)
    return response

def get_tweets(client_bearer, query):
    """
    Retrieves a collection of recent tweets that match a specified search query.
    
    Parameters:
        client (tweepy.ClientBearer): A bearer token-authenticated Tweepy client.
        query (str): The search query for which to retrieve recent tweets.
    
    Returns:
        tweets (tweepy.Tweet): A collection of recent tweets that match the specified search query.
    """
    tweets = client_bearer.search_recent_tweets(query = query, tweet_fields = ['context_annotations','author_id', 'public_metrics'])
    return tweets

def like_motavational_tweet(client, client_bearer,query):
    """
    Likes a motivational tweet from a given query using the Twitter API.

    Parameters:
    - client: A Twitter API client object for making API requests.
    - client_bearer: A bearer token for the Twitter API authentication.
    - query: A string representing the query to search for tweets.

    Returns:
    - A like object representing the successful like action.

    This function first uses the `get_tweets()` function to retrieve a list of tweets from the given query.
    It then selects a random tweet from the list and likes it using the `client.like()` method. The function 
    returns the like object as a confirmation of the successful like action.

    Note: The `get_tweets()` function should be defined separately to retrieve tweets based on a given query.
    """
    tweets = get_tweets(client_bearer,query)
    num_tweets = len(tweets.data)
    selected_index = random.randrange(0,num_tweets)
    selected_tweet = tweets.data[selected_index]
    like = client.like(tweet_id = selected_tweet.id)
    return like

def retweet_motavational_tweet(client, client_bearer,query):
    """
    Retrieves a random tweet containing a given query from the Twitter API using the specified client bearer token, and then retweets it using the specified client. Returns the retweet object if successful, or raises a Tweepy error if unsuccessful.

    Args:
        client: A Tweepy client object that the retweet will be made on.
        client_bearer: A string representing the Twitter API bearer token to use for authentication.
        query: A string representing the query to search for in the tweets.

    Returns:
        A Tweepy retweet object if the retweet was successful, otherwise a Tweepy error is raised.

    Raises:
        Tweepy error: If the retweet was unsuccessful for any reason.
    """

    tweets = get_tweets(client_bearer,query)
    num_tweets = len(tweets.data)
    selected_index = random.randrange(0,num_tweets)
    selected_tweet = tweets.data[selected_index]
    retweet = client.retweet(tweet_id = selected_tweet.id)
    return retweet

def follow_account(client, client_bearer,query):
    """
    Follows a random user who has tweeted using the given query term.

    Args:
        client: A tweepy Client object representing the authenticated Twitter API client.
        client_bearer: A string representing the bearer token used to authenticate the Twitter API client.
        query: A string representing the search term to be used to find relevant tweets.

    Returns:
        A tweepy Follow object representing the newly created follow relationship.
    """

    tweets = get_tweets(client_bearer,query)
    num_tweets = len(tweets.data)
    selected_index = random.randrange(0,num_tweets)
    selected_tweet = tweets.data[selected_index]
    tweet_author = selected_tweet.author_id
    follow = client.follow_user(target_user_id = tweet_author)
    return follow

def get_user(client_bearer, username):
    """
    Retrieves information about a given Twitter user using the provided Twitter API bearer token.
    
    Args:
        client_bearer: A tweepy Client object with a bearer token.
        username: A string representing the username of the Twitter user to retrieve information for.
        
    Returns:
        A tweepy User object representing the requested Twitter user, with information including the user's ID and public metrics.
    """
    user = client_bearer.get_user(username = username, user_fields = ['id','public_metrics'])
    return user

def get_follower_count(client_bearer,username):
    """
    Retrieves the number of followers for a given user on Twitter.

    Args:
        client_bearer: A Twitter API client with bearer token authentication.
        username: A string representing the username of the user to retrieve the follower count for.

    Returns:
        An integer representing the number of followers for the specified user.
    """
    user = get_user(client_bearer, username)
    count = user.data.data['public_metrics']['followers_count']
    return count

def get_total_likes(client_bearer, username):
    """
    This function takes in a Tweepy client authenticated with a bearer token and a Twitter username, and returns the total number of likes received by the user's tweets.

    Parameters:
    - client_bearer: Tweepy client authenticated with a bearer token
    - username: Twitter username (string) for the user whose total like count is to be retrieved

    Returns:
    - Total number of likes received by the user's tweets (integer)
    """
    like_count = 0
    user = get_user(client_bearer, username)
    user_id = user.data.data['id']
    tweet_count = user.data.data['public_metrics']['tweet_count']
    if tweet_count < 5:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = 5, tweet_fields = ['context_annotations','author_id', 'public_metrics'], exclude = ['retweets'])
        for tweet in tweets.data:
            like_count += int(tweet.data['public_metrics']['like_count'])
    else:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = tweet_count, tweet_fields = ['context_annotations','author_id', 'public_metrics'])
        for tweet in tweets.data:
            like_count += int(tweet.data['public_metrics']['like_count'])
    return like_count

def get_total_retweets(client_bearer, username):
    """
    This function takes a Twitter API v2 client object with a bearer token
    and a Twitter username and returns the total number of retweets for
    all tweets posted by the user.

    Parameters:
    -----------
    client_bearer : tweepy.Client
        A Twitter API v2 client object with a bearer token.
    username : str
        The username (i.e., handle) of the Twitter user.

    Returns:
    --------
    retweet_count : int
        The total number of retweets for all tweets posted by the user.
    """
    retweet_count = 0
    user = get_user(client_bearer, username)
    user_id = user.data.data['id']
    tweet_count = user.data.data['public_metrics']['tweet_count']
    if tweet_count < 5:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = 5, tweet_fields = ['context_annotations','author_id', 'public_metrics'], exclude = ['retweets'])
        for tweet in tweets.data:
            retweet_count += int(tweet.data['public_metrics']['retweet_count'])
    else:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = tweet_count, tweet_fields = ['context_annotations','author_id', 'public_metrics'])
        for tweet in tweets.data:
            retweet_count += int(tweet.data['public_metrics']['retweet_count'])
    return retweet_count

def get_total_lr(client_bearer, username):
    """
    Retrieve the total number of likes and retweets of a given user's tweets.

    Args:
    - client_bearer: An instance of the tweepy.ClientBearer class authorized with a bearer token.
    - username: A string representing the username of the target user.

    Returns:
    A dictionary with two keys: 'likes' and 'retweets', each holding the respective count of the target user's likes and retweets.
    """
    like_count = 0
    retweet_count = 0
    user = get_user(client_bearer, username)
    user_id = user.data.data['id']
    tweet_count = user.data.data['public_metrics']['tweet_count']
    if tweet_count < 5:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = 5, tweet_fields = ['context_annotations','author_id', 'public_metrics'], exclude = ['retweets'])
        if(tweets.data):
            for tweet in tweets.data:
                like_count += int(tweet.data['public_metrics']['like_count'])
                retweet_count += int(tweet.data['public_metrics']['retweet_count'])
        else:
            like_count += 0 
            retweet_count += 0
    else:
        tweets = client_bearer.get_users_tweets(id = user_id, max_results = tweet_count, tweet_fields = ['context_annotations','author_id', 'public_metrics'])
        if(tweets.data):
            for tweet in tweets.data:
                like_count += int(tweet.data['public_metrics']['like_count'])
                retweet_count += int(tweet.data['public_metrics']['retweet_count'])
        else:
            like_count += 0 
            retweet_count += 0
    total_counts = {'likes': like_count, 'retweets': retweet_count}
    return total_counts 