from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/borough', methods=['POST'])
def borough():
    year = request.form['year']
    r = requests.get('https://api.tfl.gov.uk/AccidentStats/{year}')
    json_object = r.json()
    neigbourhood = float(json_object['borough'])
    return str(neighbourhood)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)