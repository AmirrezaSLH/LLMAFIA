from openai import OpenAI

class ChatGPTClient:
    def __init__(self, api_key, model='gpt-4o-mini'):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def call_llm(self, query):
        """Calls the OpenAI API with the given query and returns the response."""
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=self.model,
        )

        response = chat_completion.choices[0].message.content
        return response
