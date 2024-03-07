# Flask integration
from flask import Flask, render_template, request
from flask import Blueprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)

# Read Data
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# # Read CSV file into DataFrame
# courses = pd.read_csv('modified_Highly_detailed_file.csv')

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
