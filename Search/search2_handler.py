from flask import Flask, render_template, request
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fuzzywuzzy import process

app = Flask(__name__)

# Load the courses data
courses = pd.read_csv('udemywithlink_2.csv')

# Remove NaN values
courses.dropna(inplace=True)
courses = courses.reset_index()

# Clean title function
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

courses["cleaned_title"] = courses["title"].apply(clean_title)

# Use of TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(courses["cleaned_title"])

# Search Function
def search(title):
    title = clean_title(title)
    # Perform fuzzy string matching to find the closest match
    closest_match, _ = process.extractOne(title, ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "TypeScript",
                            "HTML", "CSS", "Bootstrap", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Express.js",
                            "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle",
                            "Windows", "macOS", "Linux", "Unix",
                            "TCP/IP", "DNS", "DHCP", "HTTP", "HTTPS", "SSL/TLS", "VPN",
                            "AWS", "Azure", "Google Cloud Platform",
                            "Git", "GitHub", "GitLab", "Jenkins", "Docker", "Kubernetes", "Ansible", "Terraform",
                            "Algorithm", "Data Structure", "Object-Oriented Programming", "Functional Programming", "Design Patterns", "Big O Notation",
                            "Agile", "Scrum", "Kanban", "Waterfall", "SDLC",
                            "Firewall", "Encryption", "Penetration Testing", "Vulnerability", "Malware", "Phishing", "Two-Factor Authentication"])
    query_vec = vectorizer.transform([closest_match])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argsort(-similarity)[:20]  # Sort in descending order
    results = courses.iloc[indices][::-1]
    return results["title"].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = search(query)

        if results:
            result_details = []
            for title in results:  # Corrected variable name
                course_data = courses[courses['title'] == title].iloc[0]
                result_details.append({
                    'name': title,
                    'image_url': course_data['image_url'],
                    'duration': course_data['duration'],
                    'course_url' : course_data['course_url']
                })
            return render_template('searchpage.html', results=result_details)  # Corrected variable name
        else:
            error_message = "No Search results"
            return render_template('searchpage.html', error_message=error_message)
    
    return render_template('searchpage.html')


if __name__ == '__main__':
    app.run(debug=True)
