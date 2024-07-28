from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import concurrent.futures

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = 'AIzaSyA5JnpIy971dH9CjieCZscjBxX8JlKNZ_s'
RESULTS_PER_PAGE = 10  # Adjust this number as needed

@app.route('/api/search', methods=['GET'])
def search_resources():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        youtube_future = executor.submit(search_youtube, query)
        khan_academy_future = executor.submit(search_khan_academy, query)
    
    all_results = youtube_future.result() + khan_academy_future.result()
    
    # Paginate results
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    paginated_results = all_results[start:end]
    
    return jsonify({
        'results': paginated_results,
        'total_results': len(all_results),
        'has_more': end < len(all_results)
    })

def search_youtube(query):
    youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}%20course&type=video&key={YOUTUBE_API_KEY}&maxResults=50'
    response = requests.get(youtube_url)
    results = []
    if response.status_code == 200:
        youtube_results = response.json().get('items', [])
        for item in youtube_results:
            title = item['snippet']['title']
            link = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
            description = item['snippet']['description']
            results.append({
                'title': title,
                'link': link,
                'description': description,
                'source': 'YouTube'
            })
    return results

def search_khan_academy(query):
    page = requests.get(f'https://www.khanacademy.org/search?page_search_query={query}')
    results = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        for item in soup.select('.search-result-item'):
            title = item.select_one('.search-result-title').text
            link = item.select_one('a')['href']
            description = item.select_one('.description').text if item.select_one('.description') else ''
            results.append({
                'title': title,
                'link': f'https://www.khanacademy.org{link}',
                'description': description,
                'source': 'Khan Academy'
            })
    return results

if __name__ == '__main__':
    app.run(debug=True)