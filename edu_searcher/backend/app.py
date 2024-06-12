from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = 'TEMP'
GOOGLE_CX = 'TEMP'
UDEMY_CLIENT_ID = 'TEMP'
UDEMY_CLIENT_SECRET = 'TEMP'

@app.route('/api/fetch_resources', methods=['GET'])
def fetch_resources():
    query = request.args.get('query')
    source_type = request.args.get('sourceType')
    level = request.args.get('level')

    google_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={GOOGLE_CX}&key={GOOGLE_API_KEY}"
    udemy_url = f"https://www.udemy.com/api-2.0/courses/?search={query}"

    google_response = requests.get(google_url)
    google_results = google_response.json().get('items', [])

    udemy_response = requests.get(udemy_url, headers={
        'Authorization': f'Basic {GOOGLE_API_KEY}:{UDEMY_CLIENT_SECRET}'
    })
    udemy_results = udemy_response.json().get('results', [])

    combined_results = google_results + udemy_results

    if source_type:
        combined_results = [result for result in combined_results if result.get('source') == source_type]
    if level:
        combined_results = [result for result in combined_results if result.get('level') == level]

    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(debug=True)
