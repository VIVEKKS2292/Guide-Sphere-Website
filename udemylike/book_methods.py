import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Read Data
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
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qeudkzx5IIheQkRUMbOxorLPpSU6dmmKIp_zDZ2oS1I/edit#gid=410936179")
worksheet = sheet.get_worksheet(0)  # Assuming the data is in the first worksheet
# Read books data into a pandas DataFrame
books_sheets = worksheet.get_all_records()
books = pd.DataFrame(books_sheets)

###
###
###

# Data Cleaning
# Remove null values
books.dropna(inplace=True)
books = books.reset_index()
books = books[['book_id','book_url','book_img','book_title','book_author','book_desc_text','book_desc_html']]

# Function to clean title
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

# Convert string(sentence) to lists
books['temp_book_author'] = books['book_author']
books['temp_book_author'] = books['temp_book_author'].apply(clean_title)
books['temp_book_author'] = books['temp_book_author'].apply(lambda x: x.split())
books['temp_title'] = books['book_title']
books['temp_title'] = books['temp_title'].apply(clean_title)
books['temp_title'] = books['temp_title'].apply(lambda x: x.split())

###
###
###

# Recommendation function
# The ultimate concatenation
books['tags'] = books['temp_title'] + books['temp_book_author']

# Converting tags from lists to strings
books['tags'] = books['tags'].apply(lambda x: " ".join(x))
books['tags'] = books['tags'].str.lower()

# Using CountVectorizer for vectorization
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(books['tags']).toarray()

# Using cosine similarity for finding distance between vectors
similarity = cosine_similarity(vectors)

# Final logic for recommendation
def recommend_books(keyword):
    keyword_vector = cv.transform([keyword]).toarray()
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]
    top_indices = similarity_scores.argsort()[::-1][:10]
    
    recommended_books_list = []   # list bcz it returns list of dictionaries
    for idx in top_indices:
        book_details = {
            'book_id': books.iloc[idx]['book_id'],
            'book_url': books.iloc[idx]['book_url'],
            'book_img': books.iloc[idx]['book_img'],
            'book_title': books.iloc[idx]['book_title'],
            'book_author': books.iloc[idx]['book_author'],
            'book_desc_text': books.iloc[idx]['book_desc_text'],
            'book_desc_html': books.iloc[idx]['book_desc_html']
        }
        recommended_books_list.append(book_details)
    
    return recommended_books_list

###
###
###

# Search Books function
def search_books(keyword):
    result_books = books[books['tags'].str.contains(keyword, case=False)]

    result_books_list = []
    for idx, book in result_books.iterrows():
        book_details = {
            'book_id': book['book_id'],
            'book_url': book['book_url'],
            'book_img': book['book_img'],
            'book_title': book['book_title'],
            'book_author': book['book_author'],
            'book_desc_text': book['book_desc_text'],
            'book_desc_html': book['book_desc_html']
        }
        result_books_list.append(book_details)
    
    return result_books_list

###
###
###

# Book Details Function
def getBook(title):
    book_data = books[books['book_title'] == title]

    if book_data.empty:
        return None
    else:
        book_data = book_data.iloc[0]
        book_details = {
            'book_id': book_data['book_id'],
            'book_url': book_data['book_url'],
            'book_img': book_data['book_img'],
            'book_title': book_data['book_title'],
            'book_author': book_data['book_author'],
            'book_desc_text': book_data['book_desc_text'],
            'book_desc_html': book_data['book_desc_html']
        }
        return book_details





















