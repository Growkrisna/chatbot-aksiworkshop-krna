from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        query = request.form.get('query')
    else:
        query = request.args.get('q')
        
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    params = {
        "q": query,
        "key": GOOGLE_BOOKS_API_KEY,
        "maxResults": 5,
        "langRestrict": "id"
    }
    
    try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=10)
        response.raise_for_status()
        
        books = []
        for item in response.json().get('items', []):
            book_info = {
                "title": item['volumeInfo'].get('title', 'No title'),
                "authors": ", ".join(item['volumeInfo'].get('authors', ['Unknown'])),
                "thumbnail": item['volumeInfo'].get('imageLinks', {}).get('thumbnail', 
                           url_for('static', filename='images/book-placeholder.jpg')),
                "preview_link": item['volumeInfo'].get('previewLink', '#')
            }
            books.append(book_info)
            
        return jsonify(books)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    
    # Untuk handle static files di Vercel
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('static/'):
        return send_from_directory('', path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()