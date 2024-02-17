from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def search_courses(keyword):
    courses = pd.read_csv('modified_Highly_detailed_file.csv')
    # Remove null values
    courses.dropna(inplace=True)
    courses = courses.reset_index()
    result_courses = courses[courses['course_title'].str.contains(keyword, case=False)]

    # Extract course titles from the DataFrame
    results = result_courses['course_title'].tolist()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        result_courses = search_courses(keyword)
        return render_template('index.html', keyword=keyword, results=result_courses)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)