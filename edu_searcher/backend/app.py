from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEYS = {
    'edx': 'YOUR_EDX_API_KEY',
    'khan_academy': 'YOUR_KHAN_ACADEMY_API_KEY',
    'udacity': 'YOUR_UDACITY_API_KEY',
    'futurelearn': 'YOUR_FUTURELEARN_API_KEY',
    'codecademy': 'YOUR_CODEC_ACADEMY_API_KEY',
}

API_ENDPOINTS = {
    'edx': 'https://api.edx.org/catalog/v1/courses',
    'khan_academy': 'https://www.khanacademy.org/api/v1/topic/DOMAIN/courses',
    'udacity': 'https://catalog-api.udacity.com/v1/courses',
    'futurelearn': 'https://www.futurelearn.com/api/v1/courses',
    'codecademy': 'https://www.codecademy.com/api/v1/courses'
}

@app.route('/api/fetch_resources', methods=['GET'])
def fetch_resources():
    query = request.args.get('query')
    source_type = request.args.get('sourceType')
    level = request.args.get('level')

    results = []

    # edX
    edx_response = requests.get(API_ENDPOINTS['edx'], params={'search': query, 'api_key': API_KEYS['edx']})
    if edx_response.status_code == 200:
        results += edx_response.json().get('results', [])

    # Khan Academy
    khan_response = requests.get(API_ENDPOINTS['khan_academy'].replace('DOMAIN', query))
    if khan_response.status_code == 200:
        results += khan_response.json()

    # Udacity
    udacity_response = requests.get(API_ENDPOINTS['udacity'])
    if udacity_response.status_code == 200:
        results += udacity_response.json().get('courses', [])

    # FutureLearn
    futurelearn_response = requests.get(API_ENDPOINTS['futurelearn'], params={'search': query, 'api_key': API_KEYS['futurelearn']})
    if futurelearn_response.status_code == 200:
        results += futurelearn_response.json().get('courses', [])

    # Codecademy
    codecademy_response = requests.get(API_ENDPOINTS['codecademy'])
    if codecademy_response.status_code == 200:
        results += codecademy_response.json().get('courses', [])

    # Filter results if needed
    if source_type:
        results = [result for result in results if result.get('source') == source_type]
    if level:
        results = [result for result in results if result.get('level') == level]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
