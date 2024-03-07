from flask import Flask, render_template, request
import pandas as pd
from flask import Blueprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from fuzzywuzzy import process
from datetime import datetime
import json
import random
from Bow_hi_det import recommend  # Import the recommend function from recommendations.py

# Define a blueprint for searchcourses model
searchcourses_bp = Blueprint('searchcourses', __name__)

app = Flask(__name__)

# Data Connection to docs
    # courses = pd.read_csv('modified_Highly_detailed_file.csv')
# Define the scope of access (can be readonly or readwrite)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# Path to your credentials JSON file
credentials ={
  "type": "service_account",
  "project_id": "guidesphere",
  "private_key_id": "1149cc64b75a7ef6345b783fbe7729a82d40be19",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCd6X9VmPUeADi1\nVX1sI1Tz8shoco7SW/9mgYOnHpcO/dRBWF3CkEzXbuABX8jtlknRasgB6SGxyrmX\nXdfsNFS++14WQuRJsLUXHOlcAES6EOtwTpY0NX368CARQh72on8r0zmu13y5SRRc\nhH3bpvvqX3aaD8TMihZe2RtvuEDGWGxefVyfZIVjJBfpa1UR7F/Q9UzXX71zv2EG\naMb8dIt6md7xJAn7+hFKjVpIfYA3+8c5lBI/8uONuo5WoZxeFdLsRzaYYlsDz7dz\n0QwniQiEFe3XS33z8SavfXvQNg7hJqaQjBXB6dVBoAWz4mAjbjDi955Gqbib2eEg\nVkqCJYmFAgMBAAECggEADKZh3veL20VlRZF9pKYH7irqxwM2Ub+w7ANACqk2rKrE\n0B9GE4n/vdpR84o6zF2XuED3mL+WRWnaCDgqTe+7QjlcxifBpe2T9DAKuaYD22vz\nkGGbQr9uQiXuS7OiS1ulGFupaUo14ZnrGaY7dtcfoxzWoWzV9RSyyhJWUlLOTZUz\nje2i27KDJ1MnXJupM+S4OSL0aKIfHiJ46a1RjgAKrZ2QufTxcKT/nvwbF31EUPfr\nHoQSrIrKqP3z6/hVD/I92sUiJDK+6fhpYzFCxcSb+BUa7VSLeXKjDmsv9C3zkIbN\nBRevP07tLGA/UM7G7wkL9aer3vUwn8e/0lBctLpjwQKBgQDP7DABNIa0+Zvt2456\nmHDjo4HVONmr98I/grad7Tdke8tJPRBdX5eu61AP2skm66+Fx1oNsdNzCW37apBc\nDLZIcrEWEMSRY7089W7rJl06rpt/EZMdAgsIOwni8bSDQOVFBJ79tOo97JIgf4SE\nddR2t+TSJOWQGJo6fc3OdI+CSQKBgQDCbPpTc/eE1tdR8/gSYJ4Zr32IzbMJ9may\nuFj2rEWak+i0WWVUwxRzJZ288PQ8hFzUlqR0rXQ6AvPhVcVTzx2G6i2idsyLd7ru\n9NfXhNu/86iDIjLUUOG0sAbXBdAQhxORJLYr5bAV88D2zg9EO5ibHxiTDL80dfeZ\nqUDaNTmNXQKBgQC0h8ealEfOBNhtqu/H5GpITKSjRMxCs0l2qYD0GI668X2tZpa5\n7BEgsHIAgh+bapIpHtFDCL6mqG5VGM6lDeiLeQHnPcHe1vHtZtDa3aGfHRIoP1Mz\noZ2AlPpdkS4BtKwcxAlkEdw8zhaGnxGpjUFfnwXPrHeiKKpo1OiINM6R+QKBgQDA\niTMMWZcQUcFBQxyy9kMapJLoWuumPgBNlAllngv/m+GiV7TlT5p8vQ+MAAGdvGZB\nkDyj3vFuUWY6C7ox2LUg2d7/OC4vHw5bfNQSdVs4p46E7eTwJHifeoILhZIaC+nw\nni5ZIkhSNOUug7jSlUH2u8CWPtVKmlfsL5Qtgu/PcQKBgC2YOnZBEXrybwi/ipAv\nSIShjih+F6oAYubdIwdPsBKsjA4twn+PPlIhCKNAPlD37/zOkLXVA/e2eqqYS6cP\nzLi6WBuMkoNXA3KBXN69X7YmRtpXH7J6RNpfJB1DOSYkMKEAVg8IP3my9QGvFXem\nrfZ6qUERkYXa3SXE58Mn8Vlc\n-----END PRIVATE KEY-----\n",
  "client_email": "guide-sphere-vivek-2292@guidesphere.iam.gserviceaccount.com",
  "client_id": "116909885100955444844",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/guide-sphere-vivek-2292%40guidesphere.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# Authenticate using service account credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(credentials)
# Open the Google Sheets document

# Courses
sheet1 = client.open_by_url("https://docs.google.com/spreadsheets/d/1FelQDvbaIFUhLUNsY0SrWazFCywDdrjhj5fI1t9gMBM/edit#gid=1389387669")
worksheet1 = sheet1.get_worksheet(0)  # Assuming the data is in the first worksheet
# Read courses data into a pandas DataFrame
course_data = worksheet1.get_all_records()
courses = pd.DataFrame(course_data)
# Books
sheet2 = client.open_by_url("https://docs.google.com/spreadsheets/d/1qrsUN1inO_baBz_RVBu8g7cCiH0JA2496agoOEN4G5c/edit#gid=83392491")
worksheet2 = sheet2.get_worksheet(0)  # Assuming the data is in the first worksheet
# Read books data into a pandas DataFrame
book_data = worksheet2.get_all_records()
books = pd.DataFrame(book_data)
# Data import ends here

def search_courses(courses, keyword,  threshold=0):
    # Remove null values
    courses.dropna(inplace=True)
    courses = courses.reset_index()
    result_courses = courses[courses['course_title'].str.contains(keyword, case=False)]
    results = result_courses['course_title'].tolist()

    # Using fuzzy words
        # Remove null values
    # courses.dropna(inplace=True)
    # courses = courses.reset_index()
    
    # # Create a list of course titles for fuzzy matching
    # course_titles = courses['course_title'].tolist()
    
    # # Use fuzzy matching to find matches to the keyword
    # matches = process.extract(keyword, course_titles)
    
    # # Filter matches based on threshold
    # results = [match[0] for match in matches if match[1] >= threshold]
    
    # # Ensure results is always a list
    # results = results if results else []
    return results

def search_books(books, keyword):
    # Remove null values
    books.dropna(inplace=True)
    books = books.reset_index()
    result_books = books[books['book_title'].str.contains(keyword, case=False)]
    results = result_books['book_title'].tolist()
    return results

def format_date(date):
    # Extract year and month from the datetime object
    year = str(date.year)
    month = str(date.month).zfill(2)  # Zero-padding for single-digit months
    # Format the date as 'mm/yyyy'
    formatted_date = f"{month}/{year}"
    return formatted_date

def clean_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%m/%Y')
    except ValueError:
        return pd.NaT  # Return NaT for invalid dates

def get_recent_courses(courses):
    # Convert 'course_date' to datetime
    courses['course_date'] = pd.to_datetime(courses['course_date'], format='%m/%Y') 
    # Get current month and year
    current_date = datetime.now() 
    # Filter courses that are nearest or in the same month and year as the current month and year
    recent_courses = courses[courses['course_date'].dt.strftime('%m/%Y') <= current_date.strftime('%m/%Y')].sort_values(by='course_date', ascending=False).head(10)
    # Convert 'course_date' back to the original format
    courses['course_date'] = courses['course_date'].apply(format_date)
    courses['course_date'] = courses['course_date'].apply(clean_date)
    # Get the course titles of the recent courses
    recent_course_titles = recent_courses['course_title'].tolist()
    return recent_course_titles

# Persnoalised recommendations
# Load data from students.json file
with open('students.json', 'r') as file:
    students_data = json.load(file)

def get_personalized_recommendations(username):
    # Find the corresponding student data based on the username
    student_data = next((student for student in students_data if student['name'] == username), None)
    if not student_data:
        return "Username not found"
    # Extract interests from the student data
    interests = student_data['interests']
    # Initialize array to store personalized recommendations
    personalized_recommendations = []
    # Pass each interest keyword to the recommend function and add recommended courses to the array
    for interest in interests:
        recommended_courses = recommend(interest)  # Assuming recommend function is defined elsewhere
        personalized_recommendations.extend(recommended_courses[:5])  # Add top 5 recommended courses for each interest
    # Shuffle the list of personalized recommendations
    random.shuffle(personalized_recommendations)
    return personalized_recommendations

@app.route('/')
def welcome():
    recent_course_titles = get_recent_courses(courses)
    personalized_recommendations = get_personalized_recommendations("Vishwa")
    if recent_course_titles and personalized_recommendations:
        # recent courses part
        recent_courses = []
        for title in recent_course_titles:
            recent_course_data = courses[courses['course_title'] == title].iloc[0]
            recent_courses.append({
                'name': title,
                'course_img': recent_course_data['course_img'],
                'course_duration': recent_course_data['course_duration'],
                'course_url': recent_course_data['course_url']
            })
        # recommendations part
        personalized_rec = []
        for title in personalized_recommendations:
            personalized_rec_data = courses[courses['course_title'] == title]
            if not personalized_rec_data.empty:
                rec_data = personalized_rec_data.iloc[0]
                personalized_rec.append({
                    'name': title,
                    'course_img': rec_data['course_img'],
                    'course_duration': rec_data['course_duration'],
                    'course_url': rec_data['course_url']
                })
        return render_template('welcome.html', recent_courses_list=recent_courses, recommended_courses=personalized_rec)
    else:
        error_message = "No recent/recommeded courses"
        return render_template('welcome.html', error_message=error_message)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        
        if 'search_course' in request.form:
            results = search_courses(courses, keyword)
            search_type = 'course'
        elif 'search_book' in request.form:
            results = search_books(books, keyword)
            search_type = 'book'

        if results:
            search_results = []
            for title in results:
                if search_type == 'course':
                    course_data = courses[courses['course_title'] == title].iloc[0]
                    search_results.append({
                        'type': 'course',  # Add a 'type' key to differentiate course and book data
                        'name': title,
                        'course_img': course_data['course_img'],
                        'course_duration': course_data['course_duration'],
                        'course_url': course_data['course_url']
                    })
                elif search_type == 'book':
                    book_data = books[books['book_title'] == title].iloc[0]
                    search_results.append({
                        'type': 'book',  # Add a 'type' key to differentiate course and book data
                        'name': title,
                        'book_author': book_data['book_author'],
                        'book_img': book_data['book_img'],
                        'book_long_desc': book_data['book_long_desc']
                    })
            
            return render_template('index_det.html', keyword=keyword, searches=search_results)
        else:
            error_message = f"No {search_type}s found for the given input."
            return render_template('index_det.html', error_message=error_message)
        
    return render_template('index_det.html')


@app.route('/details/<title>', methods=['GET'])
def details(title):
    course_data = courses[courses['course_title'] == title].iloc[0]
    recommendations = recommend(title)  # Get recommended courses for the selected course
    if recommendations:
        recommended_courses = []
        first_recommendation_skipped = False
        for title in recommendations:
            if not first_recommendation_skipped:
                first_recommendation_skipped = True
                continue  # Skip the first recommended course
            rec_course_data = courses[courses['course_title'] == title]
            if not rec_course_data.empty:
                rec_course_data = rec_course_data.iloc[0]
                recommended_courses.append({
                    'name': title,
                    'course_img': rec_course_data['course_img'],
                    'course_duration': rec_course_data['course_duration'],
                    'course_url': rec_course_data['course_url']
                }) 

    return render_template('details.html', course_data=course_data, recommended_courses=recommended_courses)

@app.route('/book_details/<title>', methods=['GET'])
def book_details(title):
    book_data = books[books['book_title'] == title].iloc[0]
    return render_template('book_details.html', book_data=book_data)


if __name__ == '__main__':
    app.run(debug=True)
