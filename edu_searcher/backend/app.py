from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
YOUTUBE_API_KEY = 'AIzaSyA5JnpIy971dH9CjieCZscjBxX8JlKNZ_s'
CORS(app)


@app.route('/api/search', methods=['GET'])
def search_resources():
    query = request.args.get('query')
    results = []

    youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}'
    response = requests.get(youtube_url)
    if response.status_code == 200:
        youtube_results = response.json().get('items', [])
        for item in youtube_results:
            title = item['snippet']['title']
            link = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
            results.append({'title': title, 'link': link, 'source': 'YouTube'})

    page = requests.get(f'https://www.khanacademy.org/search?page_search_query={query}')
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        for item in soup.select('.search-result-item'):
            title = item.select_one('.search-result-title').text
            link = item.select_one('a')['href']
            results.append({'title': title, 'link': f'https://www.khanacademy.org{link}', 'source': 'Khan Academy'})
    else:
        return jsonify({'error': 'Failed to retrieve data from Khan Academy'}), 500

    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)
