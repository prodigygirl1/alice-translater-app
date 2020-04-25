from flask import Flask, request
import logging
import json
import requests


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:

        res['response']['text'] = 'Я Алиса. Я могу сказать перевод слова на английский язык. ' \
                                  'Скажи: Переведи слово <слово>'

        return
    translate = get_translate(req['request']['original_utterance'])
    if translate:
        res['response']['text'] = translate
    else:
        res['response']['text'] = 'Я вас не поняла. Повторите еще раз.'


def get_translate(word):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': '',
        'text': word,
        'lang': 'en'
    }
    response = requests.get(url, params=params)
    if response:
        js_resp = response.json()
        return js_resp['text']
    return None


if __name__ == '__main__':
    app.run()