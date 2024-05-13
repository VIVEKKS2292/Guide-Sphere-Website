from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
from flask import Blueprint
from course_methods import recommend_courses
from course_methods import get_recent_courses
from course_methods import search_courses 
from course_methods import get_personalized_course_recommendations
from course_methods import getCourse 
from book_methods import recommend_books
from book_methods import search_books
from book_methods import getBook
from job_methods import recommend_jobs 
from job_methods import search_jobs
from job_methods import getJob  
from userdata_methods import getuserdata    
from userdata_methods import insert_user_fullName
from userdata_methods import insert_user_moreAboutUser
from userdata_methods import insert_user_userPhoto
from userdata_methods import insert_user_interests
from userdata_methods import delete_user_interests
from userdata_methods import insert_user_education
from userdata_methods import delete_user_education
from website_methods import recommend_websites

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

@app.route('/homepagesearchresults', methods=['GET'])
def homepagesearchresults():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        home_result_courses = search_courses(keyword)
        home_result_books = search_books(keyword)
        home_result_jobs = search_jobs(keyword)
        return render_template('homepagesearchresults.html', keyword=keyword, home_result_courses_list=home_result_courses,
                            home_result_books_list=home_result_books, home_result_jobs_list=home_result_jobs)
    
    return render_template('homepagesearchresults.html')

@app.route('/coursedetailspage/<title>', methods=['GET'])
def coursedetailspage(title):
    course = getCourse(title)
    similar_courses = recommend_courses(title)
    similar_books = recommend_books(title)
    similar_websites = recommend_websites(title)
    return render_template('coursedetailspage.html', course=course, similar_courses_list=similar_courses,
                           similar_books_list=similar_books, similar_websites_list=similar_websites)

@app.route('/bookdetailspage/<title>', methods=['GET'])
def bookdetailspage(title):
    book = getBook(title)
    similar_books = recommend_books(title)
    similar_websites = recommend_websites(title)
    return render_template('bookdetailspage.html', book=book, similar_books_list=similar_books,
                           similar_websites_list=similar_websites)

@app.route('/jobdetailspage/<title>', methods=['GET'])
def jobdetailspage(title):
    job = getJob(title)
    related_courses = recommend_courses(title)
    related_books = recommend_books(title)
    similar_websites = recommend_websites(title)
    return render_template('jobdetailspage.html', job=job, related_books_list=related_books, related_courses_list=related_courses,
                           similar_websites_list=similar_websites)

email = 'acd@gmail.com'
UPLOAD_FOLDER = r'D:\Coding\Guide Sphere\udemylike\static\uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSTIONS = set (['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSTIONS

@app.route('/myprofilepage/<section>', methods=['GET', 'POST'])
def myprofilepage(section):
    if section == 'userPhotoDetails' and request.method == 'POST':
        # Check if a file was uploaded
        if 'userPhoto' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['userPhoto']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            insert_user_userPhoto(email, filename)
            flash('successfully uploaded')
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

    if section == 'basicDetails' and request.method == 'POST':
        fullName = request.form.get('fullName')
        insert_user_fullName(email, fullName)

    if section == 'interestsDetails' and request.method == 'POST':
        interests = request.form.get('interests')
        insert_user_interests(email, interests)

    if section == 'deleteinterestsDetails' and request.method == 'POST':
        selected_interests = request.form.getlist('selected_interests[]')
        delete_user_interests(email, selected_interests)

    if section == 'moreAboutUserDetails' and request.method == 'POST':
        moreAboutUser = request.form.get('moreAboutUser')
        insert_user_moreAboutUser(email, moreAboutUser)
    
    if section == 'educationDetails' and request.method == 'POST':
        collegeName = request.form.get('collegeName')
        specialization = request.form.get('specialization')
        grade = request.form.get('grade')
        insert_user_education(email, collegeName, specialization, grade)
    
    if section == 'deleteducationDetails' and request.method == 'POST':
        selected_education = request.form.getlist('selected_education[]')
        delete_user_education(email, selected_education)

    user = getuserdata(email)
    return render_template('myprofilepage.html', user=user)

    
if __name__ == '__main__':
    app.run(debug=True)

