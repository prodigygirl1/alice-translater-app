from flask import Flask, request
import logging
import json
import requests
import os


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
    translate = get_translate(req['request']['original_utterance'].split()[-1])
    if translate:
        res['response']['text'] = translate
    else:
        res['response']['text'] = 'Я вас не поняла. Повторите еще раз.'


def get_translate(word):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': 'trnsl.1.1.20200425T170742Z.c6acc154e47a990b.85895b23d7a7dd9dfc83aaee290497558530ca78',
        'text': word,
        'lang': 'en'
    }
    response = requests.get(url, params=params)
    if response:
        js_resp = response.json()
        print('ПЕРЕВОД:', js_resp['text'])
        return js_resp['text']
    return None


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run()
