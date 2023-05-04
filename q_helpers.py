import pymongo
import time_helpers
import twitter_helpers
import openai_helpers
import numpy as np
import random
import twitter_helpers
import openai_helpers
import datetime
import pytz

def execute_action(qtable,action_table, alpha, gamma, epsilon, client, client_bearer, openai_key, username):
    """
    Chooses an action based on the Q-values in the Q-table and performs the action on Twitter. Updates the action
    table with the details of the action performed.

    Parameters:
    -----------
    qtable: pymongo.collection.Collection
        MongoDB collection containing Q-values for all state-action pairs.
    action_table: pymongo.collection.Collection
        MongoDB collection containing details of all actions performed by the agent.
    alpha: float
        Learning rate or step size. Used to control the rate at which the agent learns from new experiences.
    gamma: float
        Discount factor. Determines the relative importance of immediate and future rewards.
    epsilon: float
        Probability of choosing a random action instead of the one with the highest Q-value. Used to balance exploration
        and exploitation.
    client: twitter.Api
        Instance of the Tweepy API client used to perform Twitter actions.
    client_bearer: TwitterBearerClient
        Instance of the Tweepy BearerToken client used to access Twitter API endpoints that require authentication.
    openai_key: str
        OpenAI API key used to access GPT-3 for tweet generation.
    username: str
        Twitter username of the agent.

    Returns:
    --------
    None
    """
    state = time_helpers.get_state()
    print(state)
    qtable_doc = qtable.find_one({'time_bucket': state})
    possible_actions = ['tweet', 'like', 'retweet', 'follow']
    query = 'motivation -is:retweet lang:en'
    lr_count = twitter_helpers.get_total_lr(client_bearer, username)
    lr_count = lr_count['likes'] + lr_count['retweets']
    follow_count = int(twitter_helpers.get_follower_count(client_bearer,username))
    interaction_count = lr_count + follow_count
    if np.random.random() < epsilon:
        # Choose a random action
        action = random.choice(possible_actions)
    else:
        max_value = max(qtable_doc['actions'].values())
        tied_actions = [key for key, value in qtable_doc['actions'].items() if value == max_value]
        action = random.choice(tied_actions)

    if action == 'tweet':
        model_engine = "text-davinci-003"
        prompt = "Write a motivational tweet"
        tweet = openai_helpers.generate_tweet(openai_key,model_engine, prompt)
        sent_tweet = twitter_helpers.send_tweet(client, tweet)
        action_table.insert_one({'datetime':datetime.datetime.now(pytz.timezone('America/New_York')),'state':state, 'action': action, 'interactions': interaction_count})
    elif action == 'like':
        like = twitter_helpers.like_motavational_tweet(client, client_bearer, query)
        action_table.insert_one({'datetime':datetime.datetime.now(pytz.timezone('America/New_York')),'state':state, 'action': action, 'interactions': interaction_count})
    elif action == 'retweet':
        retweet = twitter_helpers.retweet_motavational_tweet(client, client_bearer, query)
        action_table.insert_one({'datetime':datetime.datetime.now(pytz.timezone('America/New_York')),'state':state, 'action': action, 'interactions': interaction_count})
    else:
        follow = twitter_helpers.follow_account(client, client_bearer, query)
        action_table.insert_one({'datetime':datetime.datetime.now(pytz.timezone('America/New_York')), 'state':state, 'action': action, 'interactions': interaction_count})
    return

def get_results(qtable,action_table, alpha, gamma, epsilon, client, client_bearer, openai_key, username):
    """Calculates and updates Q-values based on the most recent action taken.

    Args:
        qtable (pymongo.collection.Collection): The MongoDB collection that stores Q-values.
        action_table (pymongo.collection.Collection): The MongoDB collection that stores previous actions.
        alpha (float): The learning rate, which determines how much the new Q-value is influenced by the reward.
        gamma (float): The discount factor, which determines the weight of future rewards.
        epsilon (float): The exploration-exploitation trade-off factor.
        client (tweepy.api.API): The Tweepy API client object.
        client_bearer (tweepy.bearer.Bearer): The Tweepy Bearer object.
        openai_key (str): The OpenAI API key.
        username (str): The Twitter username of the account being used.

    Returns:
        None
    """
    if(list(action_table.find())):
        prev_action = action_table.find().sort('datetime', -1).limit(1)[0]
        lr_count = twitter_helpers.get_total_lr(client_bearer,username)
        lr_count = lr_count['likes'] + lr_count['retweets']
        follow_count = int(twitter_helpers.get_follower_count(client_bearer,username))
        interaction_count = lr_count + follow_count
        reward = interaction_count - prev_action['interactions']
        qval_prev = qtable.find_one({'time_bucket': prev_action['state']})
        print(qval_prev)
        qval_prev = qval_prev['actions'][prev_action['action']]
        q_value = (1 - alpha) * qval_prev + alpha * (reward + gamma *50)
        update_spot = 'actions.' + prev_action['action']
        qtable.update_one({'time_bucket':prev_action['state']}, {'$set':{update_spot:q_value}})
    else:
        return








