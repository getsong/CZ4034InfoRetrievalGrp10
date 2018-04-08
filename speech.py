import requests

headers = {
    'Content-Type': 'application/json',
}

params = (
    ('key', 'AIzaSyDcCAo3go_japc1chDWbAgNCdHZxz4nXu4'),
)

data = open('sync-request.json', 'rb').read()
response = requests.post('https://speech.googleapis.com/v1beta1/speech:syncrecognize', headers=headers, params=params, data=data)

print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://speech.googleapis.com/v1beta1/speech:syncrecognize?key=AIzaSyDcCAo3go_japc1chDWbAgNCdHZxz4nXu4', headers=headers, data=data)