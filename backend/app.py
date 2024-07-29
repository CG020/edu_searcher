from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import os
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Use environment variable for API key
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    logging.error("YouTube API key not found. Please set the YOUTUBE_API_KEY environment variable.")

RESULTS_PER_PAGE = 10

@app.route('/api/search', methods=['GET'])
def search_resources():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    
    logging.info(f"Received search request. Query: {query}, Page: {page}")
    
    if not query:
        logging.warning("No query provided")
        return jsonify({'error': 'No query provided'}), 400

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            youtube_future = executor.submit(search_youtube, query)
            khan_academy_future = executor.submit(search_khan_academy, query)
        
        youtube_results = youtube_future.result()
        khan_academy_results = khan_academy_future.result()
        
        logging.info(f"YouTube results: {len(youtube_results)}, Khan Academy results: {len(khan_academy_results)}")
        
        all_results = youtube_results + khan_academy_results
        
        # Paginate results
        start = (page - 1) * RESULTS_PER_PAGE
        end = start + RESULTS_PER_PAGE
        paginated_results = all_results[start:end]
        
        response = {
            'results': paginated_results,
            'total_results': len(all_results),
            'has_more': end < len(all_results)
        }
        logging.info(f"Sending response: {len(paginated_results)} results")
        return jsonify(response)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

def search_youtube(query):
    if not YOUTUBE_API_KEY:
        logging.error("YouTube API key not available")
        return []

    youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}%20course&type=video&key={YOUTUBE_API_KEY}&maxResults=50'
    try:
        response = requests.get(youtube_url)
        response.raise_for_status()
        youtube_results = response.json().get('items', [])
        logging.info(f"YouTube API returned {len(youtube_results)} results")
        return [{
            'title': item['snippet']['title'],
            'link': f'https://www.youtube.com/watch?v={item["id"]["videoId"]}',
            'description': item['snippet']['description'],
            'source': 'YouTube'
        } for item in youtube_results]
    except requests.RequestException as e:
        logging.error(f"Error fetching YouTube results: {str(e)}")
        return []

def search_khan_academy(query):
    try:
        page = requests.get(f'https://www.khanacademy.org/search?page_search_query={query}')
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        results = []
        for item in soup.select('.search-result-item'):
            title = item.select_one('.search-result-title').text if item.select_one('.search-result-title') else 'No Title'
            link = item.select_one('a')['href'] if item.select_one('a') else ''
            description = item.select_one('.description').text if item.select_one('.description') else ''
            results.append({
                'title': title,
                'link': f'https://www.khanacademy.org{link}' if link else '',
                'description': description,
                'source': 'Khan Academy'
            })
        logging.info(f"Khan Academy search returned {len(results)} results")
        return results
    except requests.RequestException as e:
        logging.error(f"Error fetching Khan Academy results: {str(e)}")
        return []

if __name__ == '__main__':
    app.run(debug=True)