from flask import Flask, render_template, request
import pandas as pd
from flask import Blueprint

# Define a blueprint for searchcourses model
searchcourses_bp = Blueprint('searchcourses', __name__)

app = Flask(__name__)
courses = pd.read_csv('modified_Highly_detailed_file.csv')

def search_courses(courses, keyword):
    # Remove null values
    courses.dropna(inplace=True)
    courses = courses.reset_index()
    result_courses = courses[courses['course_title'].str.contains(keyword, case=False)]
    results = result_courses['course_title'].tolist()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = search_courses(courses, keyword)

        if results: 
            search_results = []
            for title in results:
                course_data = courses[courses['course_title'] == title].iloc[0]
                search_results.append({
                    'name': title,
                    'course_img': course_data['course_img'],
                    'course_duration': course_data['course_duration'],
                    'course_url': course_data['course_url']
                })
            
            return render_template('index_det.html', keyword=keyword, searches=search_results)
        else:
            error_message = "No Searches found for the given input."
            return render_template('index_det.html', error_message=error_message)
        
    return render_template('index_det.html')

@app.route('/details/<title>', methods=['GET'])
def details(title):
    course_data = courses[courses['course_title'] == title].iloc[0]
    return render_template('details.html', course_data=course_data)

if __name__ == '__main__':
    app.run(debug=True)
