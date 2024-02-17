#falsk integration
from flask import Flask, render_template, request
app = Flask(__name__)


# Read Data
import numpy as np
import pandas as pd
courses = pd.read_csv('udemywithlink_2.csv')
# Remove null values
courses.dropna(inplace=True)
courses = courses.reset_index()
courses = courses[['id','title','desc','by','image_url','duration','course_url']]

#function to remove all odd characters
import re

def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]","",title)

courses['desc'] = courses['desc'].apply(clean_title)
courses['by'] = courses['by'].apply(clean_title)

#Convert string(sentence) to lists
courses['desc'] =  courses['desc'].apply(lambda x:x.split())
courses['by'] =  courses['by'].apply(lambda x:x.split())
courses['temp_title'] = courses['title']
courses['temp_title'] = courses['temp_title'].apply(clean_title)
courses['temp_title'] =  courses['temp_title'].apply(lambda x:x.split())

#the ultimate concatenation
courses['tags'] = courses['temp_title'] + courses['desc'] + courses['by'] 
new_courses = courses[['id','title','tags']]


# Converting tags from lists to strings
new_courses['tags'] = new_courses['tags'].apply(lambda x:" ".join(x))
new_courses['tags'] = new_courses['tags'].str.lower()


#Using scikit learn module to use CountVectorizer for vectorisation
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2000,stop_words='english')
vectors = cv.fit_transform(new_courses['tags']).toarray()


#using cosine similarity for finding distance between vectors
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

#Final logic for recommendation
def recommed(keyword):

    keyword_vector = cv.transform([keyword]).toarray()
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]
    top_indices = similarity_scores.argsort()[::-1][:10]

     # Retrieve and return recommended courses
    recommended_courses = [new_courses.iloc[idx]['title'] for idx in top_indices]
    return recommended_courses



# recommed('GIT and Visual Studio with Azure DevOps Repos for Developers')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_title = request.form['course_title']
        recommendations = recommed(input_title)

        if recommendations:
            # Get course data including image URL and price
            recommended_courses = []
            for title in recommendations:
                course_data = courses[courses['title'] == title].iloc[0]
                recommended_courses.append({
                    'name': title,
                    'image_url': course_data['image_url'],
                    'duration': course_data['duration'],
                    'course_url' : course_data['course_url']
                })
            
            return render_template('index_im.html', input_title=input_title, recommendations=recommended_courses)
        else:
            error_message = "No recommendations found for the given input."
            return render_template('index_im.html', error_message=error_message)

    return render_template('index_im.html')

if __name__ == '__main__':
    app.run(debug=True)
























