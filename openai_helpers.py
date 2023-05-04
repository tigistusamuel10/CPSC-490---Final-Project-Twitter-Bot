import openai
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_KEY')






# Generate a motivational tweet
prompt = "Write a motivational tweet"


def generate_tweet(api_key, model_engine:str, prompt:str):
    """
    The function that will be used to access the OpenAI API to generate tweets

    api_key:
        User api_key from OpenAi
    
    model_engine:
        The GPT model being used(most likely "text-davinci-003")
    
    prompt:
        The prompt for what you want the GPT model to generate(most likely "Write a motivational tweet")
    """
    openai.api_key = api_key
    # Set up OpenAI API authentication

    # Choose the GPT-3 model to use
    model_engine = model_engine

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=240,
        n=1,
        stop=None,
        temperature=1,
    )

    tweet = response.choices[0].text.strip()
    tweet = tweet.replace('"','')
    return tweet


