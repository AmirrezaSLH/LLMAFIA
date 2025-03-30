from openai import OpenAI

class ChatGPTClient:
    def __init__(self, api_key, model = 'gpt-4o-mini'):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def prompt_engineer(self, user_query='', context='', general_context='', historical_context = ''):
        
        """Creates a structured prompt for better AI responses."""
        
        prompt = (
            f"GPT (You) Role: {general_context}\n"
            f"Information (About Amirreza Salehi, remember more recent life experiences are more relevant as answers): {context}\n"
            f"History of The Converstation (Between GPT and User): {historical_context}\n"
            f"Answer this question (from the User) in a way that aligns with your role, taking into account the provided information and the context of the previous conversation: {user_query}"
        )
        
        return prompt

    def call_chatgpt(self, query):
        
        """Calls the OpenAI API with the given query."""
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=self.model,
        )
        
        return chat_completion

    def process_question(self, user_query='', context='', general_context='', history = [ ('', '') ]):
        
        """Handles full query processing, including prompt engineering and API call."""
        
        #historical_context = self.historical_context_engineer(history)
        historical_context = ''
        prompt = self.prompt_engineer(user_query, context, general_context, historical_context)
        gpt_response = self.call_chatgpt(prompt)
        
        response = gpt_response.choices[0].message.content
        
        return response    
