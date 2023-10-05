import openai
from KitchenGuru import settings

openai.api_key = settings.CHATGPT_API_KEY


def send_code_to_api(code):
    res = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are an experienced developer."},
            {"role": "user", "content": f"Tell me what language is this code written? {code}"},
        ]
    )
    return res["choices"][0]["message"]["content"]