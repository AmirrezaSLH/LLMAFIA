

import os
from dotenv import load_dotenv

import gpt_client

def read_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: api_key.txt file not found")
        return None
    except Exception as e:
        print(f"Error reading API key: {str(e)}")
        return None



load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

agent = gpt_client.ChatGPTClient(api_key=api_key)

test_query = "What is the capital of the moon?"
what_model = "What model are you? Specify the model name and version."

test_model = agent.process_question(what_model)
#response = agent.process_question(test_query)

#print(response)
print(test_model)
