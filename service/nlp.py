import os
import requests


def analyze_sentiment(text):
    PROSA_API_KEY = os.getenv("PROSA_API_KEY")
    url = 'https://api.prosa.ai/v1/sentiments'
    headers = {'x-api-key': PROSA_API_KEY}
    data = {'text': text}
    r = requests.post(url, json=data, headers=headers)
    sentiment = r.json()['sentiment']
    if sentiment == 'positive':
        return 1
    elif sentiment == 'negative':
        return -1
    else:
        return 0
