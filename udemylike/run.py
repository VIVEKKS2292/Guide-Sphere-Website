from flask import Flask, render_template, request
from flask import Blueprint
from course_methods import recommend_courses
from course_methods import get_recent_courses
from course_methods import search_courses 
from course_methods import get_personalized_course_recommendations
from book_methods import recommend_books
from book_methods import search_books
from job_methods import recommend_jobs 
from job_methods import search_jobs   

# Define a blueprint for searchcourses model
searchcourses_bp = Blueprint('searchcourses', __name__)

app = Flask(__name__)

@app.route('/')
def homepage():
    recent_courses = get_recent_courses()
    personalized_course_recommendations = get_personalized_course_recommendations("Vishwa")
    trending_books = recommend_books("Python")
    recent_job_postings = recommend_jobs("developer")
    return render_template('homepage.html', recent_courses_list=recent_courses,
                            personalized_course_recommendations_list=personalized_course_recommendations,
                            trending_books_list=trending_books,
                            recent_job_postings_list=recent_job_postings)

@app.route('/coursesearchpage')
def coursesearchpage():
    recent_courses = get_recent_courses()
    personalized_course_recommendations = get_personalized_course_recommendations("Vishwa")
    python_courses = recommend_courses("Python")
    git_courses = recommend_courses("GIT")
    apna_college_courses = recommend_courses("Apna College")
    return render_template('coursespage.html',recent_courses_list=recent_courses,
                           personalized_course_recommendations_list=personalized_course_recommendations,
                           python_courses_list=python_courses,git_courses_list=git_courses,
                           apna_college_courses_list=apna_college_courses)

@app.route('/booksearchpage')
def booksearchpage():
    python_books = recommend_books("Python")
    datastructures_books = recommend_books("Data Structures")
    ux_books = recommend_books("User Experience")
    software_books = recommend_books("Software Architecture")
    excel_books = recommend_books("Excel")
    return render_template('bookspage.html',python_books_list = python_books,datastructures_books_list = datastructures_books,
                           ux_books_list = ux_books,software_books_list = software_books,excel_books_list = excel_books)

@app.route('/jobsearchpage')
def jobsearchpage():
    developer_jobs = recommend_jobs("developer")
    associate_jobs = recommend_jobs("associate")
    business_jobs = recommend_jobs("business")
    digital_marketing_jobs = recommend_jobs("digital marketing")
    marketing_executive_jobs = recommend_jobs("marketing executive")
    return render_template('jobspage.html',developer_jobs_list = developer_jobs,associate_jobs_list = associate_jobs,
                           business_jobs_list = business_jobs,digital_marketing_jobs_list = digital_marketing_jobs,
                           marketing_executive_jobs_list = marketing_executive_jobs)

@app.route('/searchresults', methods=['GET'])
def searchresults():
    if request.method == 'GET':
        pageid = request.args.get('pageid')
        keyword = request.args.get('keyword')
        if pageid == '1':
            result_courses = search_courses(keyword)
            results = result_courses
        elif pageid == '2':
            result_books = search_books(keyword)
            results = result_books
        elif pageid == '3':
            result_jobs = search_jobs(keyword)
            results = result_jobs

        return render_template('searchresults.html', pageid=pageid, keyword=keyword, results_list=results)

    return render_template('searchresults.html')
    
if __name__ == '__main__':
    app.run(debug=True)

