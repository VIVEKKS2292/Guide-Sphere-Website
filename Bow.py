#falsk integration
from flask import Flask, render_template, request
app = Flask(__name__)


# Read Data
import numpy as np
import pandas as pd
courses = pd.read_csv('Vishwa_scrape_course_dataset(3000).csv')
# Remove null values
courses.dropna(inplace=True)
courses = courses.reset_index()
courses = courses[['id','title','desc','by']]

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

    ## Without Keyword Sensitivty

    # course_index = new_courses[new_courses['title'] == title].index[0]
    # distances = similarity[course_index]
    # courses_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    # recommended_courses = []
    # for i in courses_list:
    #     recommended_courses.append(new_courses.iloc[i[0]].title)

    # return recommended_courses

    ## With Keyword Sensitivity

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
        return render_template('index.html', input_title=input_title, recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
























