from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.activityStore
collection = db.activity_coll_1

# Default route
@app.route('/')
def index():
    document = collection.find_one()
    repeated_strings = document.get("Repeated string", []) if document else []
    return render_template('search.html', repeated_strings=repeated_strings)

# Store and check route
@app.route('/store', methods=['POST'])
def store_and_check():
    search_term = request.form['search_term']
    # Update the Search string field in the database
    collection.update_one({}, {'$push': {'Search string': search_term}}, upsert=True)

    document = collection.find_one()
    search_strings = document.get('Search string', []) if document else []

    if len(search_strings) >= 20:
        check_for_repeat(search_strings)
        # Clear the Search string field
        collection.update_one({}, {'$set': {'Search string': []}})

    return redirect(url_for('index'))

# Check for repeated words
def check_for_repeat(search_strings):
    stop_words = set(stopwords.words('english'))
    words = [word for search_term in search_strings for word in nltk.word_tokenize(search_term) if word.isalnum() and word.lower() not in stop_words]
    
    counter = Counter(words)
    print("Word counts:", counter)  # Debugging line to print word counts
    # Only consider words that have repeated more than 2 times
    repeated = [word for word, count in counter.items() if count > 5]

    # Get the current list of repeated strings from the database
    document = collection.find_one()
    current_repeated_strings = document.get("Repeated string", []) if document else []

    # Only insert words that are not already present in the Repeated string field
    words_to_insert = [word for word in repeated if word.lower() not in map(str.lower, current_repeated_strings)]

    if words_to_insert:
        collection.update_one({}, {'$push': {'Repeated string': {'$each': words_to_insert}}}, upsert=True)

if __name__ == '__main__':
    app.run(debug=True)
