import pymongo
import time_helpers
import twitter_helpers
import openai_helpers
import datetime
import pytz
import os
from dotenv import load_dotenv
import q_helpers

load_dotenv()

mongo_client = pymongo.MongoClient(os.getenv('MONGO_PASS'), tlsInsecure=True)

#get Twitter info
twitter_ck = os.getenv('TWITTER_CONSUMER_KEY')
twitter_cs = os.getenv('TWITTER_CONSUMER_SECRET')
twitter_at = os.getenv('TWITTER_ACCESS_TOKEN')
twitter_ats = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
twitter_bt = os.getenv('TWITTER_BEARER_TOKEN')
client_bearer = twitter_helpers.generate_client(bt_present=True,bearer_token= twitter_bt)
client = twitter_helpers.generate_client(twitter_ck, twitter_cs, twitter_at, twitter_ats)
username = 'motivater247'

#OpenAI API access info preparation
openai_key = os.getenv('OPENAI_KEY')



db = mongo_client['Qbase']

#instantite the MongoDB Qtable
qtable = db.qtable
#instantiate MongoDB action table
action_table = db.action_table
alpha = 0.1
gamma = 0.9
epsilon = 0.8
q_helpers.get_results(qtable,action_table,alpha,gamma,epsilon,client,client_bearer,openai_key,username)
q_helpers.execute_action(qtable,action_table,alpha,gamma,epsilon,client,client_bearer,openai_key,username)


 





























# import numpy as np

# '''
# Big questiopn is how should I define my states? Major lead right now is dividing states by time of day.
# I am thinking maybe having 24 states for each hour of the day. You then have the bot take different actions
# at different times of the day. However, I am confused on
# '''

# # Define the Q-table as a matrix with dimensions equal to the number of states and actions
# num_states = 3
# num_actions = 3
# Q = np.zeros((num_states, num_actions))

# # Define the parameters of the algorithm
# alpha =0.1
# gamma = 0.9
# epsilon = 0.9

# # Define the initial state of the algorithm
# state = # initial state

# # Define the number of episodes to run
# num_episodes = # number of episodes

# # Loop through the episodes
# for episode in range(num_episodes):
#     # Reset the environment to the initial state
#     state = # initial state
#     done = False

#     # Loop through the steps of the episode
#     while not done:
#         # Choose the next action based on the Q-values and exploration rate
#         if np.random.random() < epsilon:
#             # Choose a random action
#             action = np.random.randint(num_actions)
#         else:
#             # Choose the action with the highest Q-value for the current state
#             action = np.argmax(Q[state])

#         # Take the action and observe the new state and reward
#         next_state, reward, done = # function that takes action and returns next state and reward

#         # Update the Q-value for the current state and action using the Q-learning formula
#         Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]))

#         # Move to the next state
#         state = next_state
