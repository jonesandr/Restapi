from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = 'http://restapi:5001/api'


@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == 'POST':
        requests.post(
            API_URL,
            json={
                'name': request.form['name'],
                'meaning': request.form['meaning']
            })
        data['message'] = "Word added"
    data['words'] = getWords()
    return render_template('index.html', data=data)


@app.route('/delete/<name>', methods=['GET'])
def delete(name):
    requests.delete(f'{API_URL}/{name}')
    data = {'message': 'Word deleted'}
    data['words'] = getWords()
    return render_template('index.html', data=data)


@app.route('/edit/<name>', methods=['GET'])
def edit(name):
    res = requests.get(f'{API_URL}/{name}').json()
    data = {'word': {'meaning': res['meaning'], 'name': name}}

    data['words'] = getWords()
    return render_template('index.html', data=data)


@app.route('/edit/<name>', methods=['POST'])
def edit2(name):
    requests.patch(
        f'{API_URL}/{name}',
        json={
            'meaning': request.form['meaning']
        })
    data = {'message': 'Word edited'}
    data['words'] = getWords()
    return render_template('index.html', data=data)


def getWords():
    res = requests.get(API_URL).json()
    return res['words']


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
