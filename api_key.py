import os

def get_api_key():
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')