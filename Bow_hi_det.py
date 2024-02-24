# Flask integration
from flask import Flask, render_template, request
from flask import Blueprint
app = Flask(__name__)

# Read Data
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Read CSV file into DataFrame
courses = pd.read_csv('modified_Highly_detailed_file.csv')

# Remove null values
courses.dropna(inplace=True)
courses = courses.reset_index()
courses = courses[['course_id','course_url', 'course_img', 'course_duration', 'course_price',
       'course_price_original', 'course_instrutor', 'course_title',
       'course_short_desc', 'course_rating', 'course_date', 'course_language',
       'course_outcome_text', 'course_outcome_html', 'course_about_text',
       'course_about_html']]

# Function to clean title
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

courses['course_short_desc'] = courses['course_short_desc'].apply(clean_title)
courses['course_instrutor'] = courses['course_instrutor'].apply(clean_title)

# Convert string(sentence) to lists
courses['course_short_desc'] = courses['course_short_desc'].apply(lambda x: x.split())
courses['course_instrutor'] = courses['course_instrutor'].apply(lambda x: x.split())
courses['temp_title'] = courses['course_title']
courses['temp_title'] = courses['temp_title'].apply(clean_title)
courses['temp_title'] = courses['temp_title'].apply(lambda x: x.split())

# The ultimate concatenation
courses['tags'] = courses['temp_title'] + courses['course_short_desc'] + courses['course_instrutor']
new_courses = courses[['course_id', 'course_title', 'tags']]

# Converting tags from lists to strings
new_courses['tags'] = new_courses['tags'].apply(lambda x: " ".join(x))
new_courses['tags'] = new_courses['tags'].str.lower()

# Using CountVectorizer for vectorization
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(new_courses['tags']).toarray()

# Using cosine similarity for finding distance between vectors
similarity = cosine_similarity(vectors)

# Final logic for recommendation
def recommend(keyword):
    keyword_vector = cv.transform([keyword]).toarray()
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]
    top_indices = similarity_scores.argsort()[::-1][:10]
    recommended_courses = [new_courses.iloc[idx]['course_title'] for idx in top_indices]
    return recommended_courses

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_title = request.form['course_title']
        recommendations = recommend(input_title)

        if recommendations:
            recommended_courses = []
            for title in recommendations:
                course_data = courses[courses['course_title'] == title].iloc[0]
                recommended_courses.append({
                    'name': title,
                    'course_img': course_data['course_img'],
                    'course_duration': course_data['course_duration'],
                    'course_url': course_data['course_url']
                })
            return render_template('index_im.html', input_title=input_title, recommendations=recommended_courses)
        else:
            error_message = "No recommendations found for the given input."
            return render_template('index_im.html', error_message=error_message)

    return render_template('index_im.html')

@app.route('/details/<title>', methods=['GET'])
def details(title):
    course_data = courses[courses['course_title'] == title].iloc[0]
    return render_template('base_details.html', course_data=course_data)

if __name__ == '__main__':
    app.run(debug=True)
