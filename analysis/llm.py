import openai


class Client:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key='sk-qIkc-8Pi2zZR4NSVBYTYlg',
            base_url=(
                'https://chatapi.akash.network'
                '/api/v1'
            )
        )

    def chat(self, role, content):
        return self.client.chat.completions.create(
            model='DeepSeek-R1',
            messages=[
                {
                    'role': role,
                    'content': content
                }
            ],
        )