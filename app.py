from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key dari .env

app = Flask(__name__)
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search')
def search_books():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    # Panggil Google Books API
    params = {
        "q": query,
        "key": GOOGLE_BOOKS_API_KEY,
        "maxResults": 5,
        "langRestrict": "id"  # Filter bahasa Indonesia
    }
    response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    
    # Format respons
    books = []
    for item in response.json().get('items', []):
        book_info = {
            "title": item['volumeInfo'].get('title', 'No title'),
            "authors": ", ".join(item['volumeInfo'].get('authors', ['Unknown'])),
            "thumbnail": item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            "preview_link": item['volumeInfo'].get('previewLink', '#')
        }
        books.append(book_info)
    
    return jsonify(books)

if __name__ == '__main__':
    app.debug = True
    app.run()
    
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)