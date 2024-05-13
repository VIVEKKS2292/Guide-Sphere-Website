import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json
import random

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
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PiDB-S1DIm4jxsNfpIQbZ6OWsA2yg14cpHkqqqeyakY/edit#gid=0")
worksheet = sheet.get_worksheet(0)  # Assuming the data is in the first worksheet
# Read data into a pandas DataFrame
youtube_sheets = worksheet.get_all_records()
youtube_data = pd.DataFrame(youtube_sheets)

###
###
###

# Data Cleaning
# Remove null values
youtube_data.dropna(inplace=True)
youtube_data = youtube_data.reset_index()
youtube_data = youtube_data[['yt_img','yt_url','yt_duration','yt_price','yt_origianl_price','yt_instructor',
                             'yt_title','yt_short_desc','yt_course_rating','yt_date','yt_language','yt_subject','yt_class',
                             'yt_about','yt_id']]

# Function to clean title
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

# Convert string(sentence) to lists
youtube_data['temp_yt_instructor'] = youtube_data['yt_instructor']
youtube_data['temp_yt_instructor'] = youtube_data['temp_yt_instructor'].apply(clean_title)
youtube_data['temp_yt_instructor'] = youtube_data['temp_yt_instructor'].apply(lambda x: x.split())
youtube_data['temp_yt_title'] = youtube_data['yt_title']
youtube_data['temp_yt_title'] = youtube_data['temp_yt_title'].apply(clean_title)
youtube_data['temp_yt_title'] = youtube_data['temp_yt_title'].apply(lambda x: x.split())
youtube_data['temp_yt_short_desc'] = youtube_data['yt_short_desc']
youtube_data['temp_yt_short_desc'] = youtube_data['temp_yt_short_desc'].apply(clean_title)
youtube_data['temp_yt_short_desc'] = youtube_data['temp_yt_short_desc'].apply(lambda x: x.split())
youtube_data['temp_yt_subject'] = youtube_data['yt_subject']
youtube_data['temp_yt_subject']  = youtube_data['temp_yt_subject'].apply(clean_title)
youtube_data['temp_yt_subject']  = youtube_data['temp_yt_subject'].apply(lambda x: x.split())
youtube_data['temp_yt_class'] = youtube_data['yt_class'].astype(str)
youtube_data['temp_yt_about'] = youtube_data['yt_about']
youtube_data['temp_yt_about']  = youtube_data['temp_yt_about'].apply(clean_title)
youtube_data['temp_yt_about']  = youtube_data['temp_yt_about'].apply(lambda x: x.split())

###
###
###

# Recommendation function
# The ultimate concatenation
youtube_data['tags'] =  youtube_data['temp_yt_title'] + youtube_data['temp_yt_instructor'] + youtube_data['temp_yt_short_desc'] 

# Converting tags from lists to strings
youtube_data['tags'] = youtube_data['tags'].apply(lambda x: " ".join(x))
youtube_data['tags'] = youtube_data['tags'].str.lower()

# Using CountVectorizer for vectorization
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(youtube_data['tags']).toarray()

# Using cosine similarity for finding distance between vectors
similarity = cosine_similarity(vectors)

# Final logic for recommendation
def recommend_yts(keyword):
    keyword_vector = cv.transform([keyword]).toarray()
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]
    top_indices = similarity_scores.argsort()[::-1][:10]
    
    recommended_yts_list = []   # list bcz it returns list of dictionaries
    for idx in top_indices:
        yt_details = {
            'yt_img': youtube_data.iloc[idx]['yt_img'],
            'yt_url': youtube_data.iloc[idx]['yt_url'],
            'yt_duration': youtube_data.iloc[idx]['yt_duration'],
            'yt_price': youtube_data.iloc[idx]['yt_price'],
            'yt_origianl_price': youtube_data.iloc[idx]['yt_origianl_price'],
            'yt_instructor': youtube_data.iloc[idx]['yt_instructor'],
            'yt_title': youtube_data.iloc[idx]['yt_title'],
            'yt_short_desc': youtube_data.iloc[idx]['yt_short_desc'],
            'yt_course_rating': youtube_data.iloc[idx]['yt_course_rating'],
            'yt_date': youtube_data.iloc[idx]['yt_date'],
            'yt_language': youtube_data.iloc[idx]['yt_language'],
            'yt_subject': youtube_data.iloc[idx]['yt_subject'],
            'yt_class': youtube_data.iloc[idx]['yt_subject'],
            'yt_about': youtube_data.iloc[idx]['yt_about'],
            'yt_id': youtube_data.iloc[idx]['yt_id']
        }
        recommended_yts_list.append(yt_details)
  
    return recommended_yts_list

###
###
###

# Recently added Youtube Videos/ latest Playlists
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
    except (ValueError, TypeError):
        return pd.NaT  # Return NaT for invalid or missing dates
    
def get_recent_yts():
    # To prevent that date issue part
    youtube_data['yt_date'] = youtube_data['yt_date'].apply(clean_date)
    # Convert 'yt_date' to datetime
    youtube_data['yt_date'] = pd.to_datetime(youtube_data['yt_date'], format='%m/%Y') 
    # Get current month and year
    current_date = datetime.now() 
    # Filter Youtube Vidoes that are nearest or in the same month and year as the current month and year
    recent_yts = youtube_data[youtube_data['yt_date'].dt.strftime('%m/%Y') <= current_date.strftime('%m/%Y')].sort_values(by='yt_date', ascending=False).head(10)
    # Convert 'yt_date' back to the original format
    youtube_data['yt_date'] = youtube_data['yt_date'].apply(format_date)
    youtube_data['yt_date'] = youtube_data['yt_date'].apply(clean_date)
    
    recent_yts_list = []
    for idx, yt in recent_yts.iterrows():
        yt_details = {
            'yt_img': yt['yt_img'],
            'yt_url': yt['yt_url'],
            'yt_duration': yt['yt_duration'],
            'yt_price': yt['yt_price'],
            'yt_origianl_price': yt['yt_origianl_price'],
            'yt_instructor': yt['yt_instructor'],
            'yt_title': yt['yt_title'],
            'yt_short_desc': yt['yt_short_desc'],
            'yt_course_rating': yt['yt_course_rating'],
            'yt_date': yt['yt_date'],
            'yt_language': yt['yt_language'],
            'yt_subject': yt['yt_subject'],
            'yt_class': yt['yt_class'],
            'yt_about': yt['yt_about'],
            'yt_id': yt['yt_id']
        }
        recent_yts_list.append(yt_details)
    youtube_data['yt_date'] = youtube_data['yt_date'].apply(format_date)

    return recent_yts_list

###
###
###

# Persnoalised recommendations
# Load data from students.json file
with open('students.json', 'r') as file:
    students_data = json.load(file)

def get_personalized_yt_recommendations(username):
    # Find the corresponding student data based on the username
    student_data = next((student for student in students_data if student['name'] == username), None)
    if not student_data:
        return "Username not found"
    
    # Extract interests from the student data
    interests = student_data['interests']
    
    # Initialize array to store personalized recommendations
    personalized_yt_recommendations_list = []
    
    # Pass each interest keyword to the recommend function and add recommended courses to the array
    for interest in interests:
        recommended_yts = recommend_yts(interest) 
        for course in recommended_yts[:5]:  # Add top 5 recommended Youtube Playlists for each interest
            personalized_yt_recommendations_list.append(course)
    
    # Shuffle the list of personalized recommendations
    random.shuffle(personalized_yt_recommendations_list)
    
    return personalized_yt_recommendations_list

###
###
###

# Search Youtube Videos function
def search_yts(keyword):
    result_yts = youtube_data[youtube_data['tags'].str.contains(keyword, case=False)]

    result_yt_list = []
    for idx, yt in result_yts.iterrows():
        yt_details = {
            'yt_img': yt['yt_img'],
            'yt_url': yt['yt_url'],
            'yt_duration': yt['yt_duration'],
            'yt_price': yt['yt_price'],
            'yt_origianl_price': yt['yt_origianl_price'],
            'yt_instructor': yt['yt_instructor'],
            'yt_title': yt['yt_title'],
            'yt_short_desc': yt['yt_short_desc'],
            'yt_course_rating': yt['yt_course_rating'],
            'yt_date': yt['yt_date'],
            'yt_language': yt['yt_language'],
            'yt_subject': yt['yt_subject'],
            'yt_class': yt['yt_class'],
            'yt_about': yt['yt_about'],
            'yt_id': yt['yt_id']
        }
        result_yt_list.append(yt_details)
    
    return result_yt_list

###
###
###

# Youtube Video Details Function
def getYt(title):
    yt_data = youtube_data[youtube_data['yt_title'] == title]

    if yt_data.empty:
        return None
    else:
        yt_data = yt_data.iloc[0]
        yt_details = {
            'yt_img': yt_data['yt_img'],
            'yt_url': yt_data['yt_url'],
            'yt_duration': yt_data['yt_duration'],
            'yt_price': yt_data['yt_price'],
            'yt_origianl_price': yt_data['yt_origianl_price'],
            'yt_instructor': yt_data['yt_instructor'],
            'yt_title': yt_data['yt_title'],
            'yt_short_desc': yt_data['yt_short_desc'],
            'yt_course_rating': yt_data['yt_course_rating'],
            'yt_date': yt_data['yt_date'],
            'yt_language': yt_data['yt_language'],
            'yt_subject': yt_data['yt_subject'],
            'yt_class': yt_data['yt_class'],
            'yt_about': yt_data['yt_about'],
            'yt_id': yt_data['yt_id']
        }
        return yt_details
















