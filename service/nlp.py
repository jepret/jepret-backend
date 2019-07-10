import requests

def sentiment_analyze(text):
    PROSA_API_KEY = 'i1kN9ZP1ngILFlScL7dSz7O9oQlledxrcaLpAg5F'
    url = 'https://api.prosa.ai/v1/sentiments'
    headers = {'x-api-key':PROSA_API_KEY}
    data = {'text':text}
    r = requests.post(url,json=data,headers=headers)
    sentiment = r.json()['sentiment']
    if sentiment=='positive':
        return 1
    elif sentiment=='negative':
        return -1
    else:
        return 0
