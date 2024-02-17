

# Read Data
import sys
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
    # Transform the keyword into a vector
    keyword_vector = cv.transform([keyword]).toarray()

    # Calculate cosine similarity between keyword vector and all course title vectors
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]

    # Get indices of courses with highest similarity scores
    top_indices = similarity_scores.argsort()[::-1][:10]

     # Retrieve and return recommended courses
    recommended_courses = [new_courses.iloc[idx]['title'] for idx in top_indices]
  
    # for element in recommended_courses:
    #     print(element)

    # Print recommended courses
    for course in recommended_courses:
        try:
            print(course.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        except Exception as e:
            print(e) 



recommed('HTML')
