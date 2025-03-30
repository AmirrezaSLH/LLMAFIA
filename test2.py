
from api_key import get_api_key
from gpt_client import ChatGPTClient
from context_manager import ContextManager

cxt_manager = ContextManager()
rules = cxt_manager.get_rules()

api_key = get_api_key()

agent = ChatGPTClient(api_key=api_key)
query = "What are these?"
test_rules = agent.process_question(query + rules)
print(test_rules)
'''
test_query = "What is the capital of the moon?"
what_model = "What model are you? Specify the model name and version."

test_model = agent.process_question(what_model)
#response = agent.process_question(test_query)

#print(response)
print(test_model)
'''