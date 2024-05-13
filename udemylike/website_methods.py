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
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1uhykbiHnFEOf-PmVlUdJ_hadvkktirbFE7hAc4gKvmM/edit#gid=0")
worksheet = sheet.get_worksheet(0)  # Assuming the data is in the first worksheet
# Read websites data into a pandas DataFrame
websites_sheets = worksheet.get_all_records()
websites = pd.DataFrame(websites_sheets)

###
###
###

# Data Cleaning
# Remove null values
websites.dropna(inplace=True)
websites = websites.reset_index()
websites = websites[['web_id','web_url','web_img','web_platform','web_title','web_short_desc','web_language']]

# Function to clean title
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

# Convert string(sentence) to lists
websites['temp_web_platform'] = websites['web_platform']
websites['temp_web_platform'] = websites['temp_web_platform'].apply(clean_title)
websites['temp_web_platform'] = websites['temp_web_platform'].apply(lambda x: x.split())
websites['temp_web_title'] = websites['web_title']
websites['temp_web_title'] = websites['temp_web_title'].apply(clean_title)
websites['temp_web_title'] = websites['temp_web_title'].apply(lambda x: x.split())
websites['temp_web_short_desc'] = websites['web_short_desc']
websites['temp_web_short_desc'] = websites['temp_web_short_desc'].apply(clean_title)
websites['temp_web_short_desc'] = websites['temp_web_short_desc'].apply(lambda x: x.split())

# Creating tags
# The ultimate concatenation
websites['tags'] = websites['temp_web_platform'] + websites['temp_web_title'] + websites['temp_web_short_desc']

# Converting tags from lists to strings
websites['tags'] = websites['tags'].apply(lambda x: " ".join(x))
websites['tags'] = websites['tags'].str.lower()

# Using CountVectorizer for vectorization
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(websites['tags']).toarray()

# Using cosine similarity for finding distance between vectors
similarity = cosine_similarity(vectors)

# Final logic for recommendation
def recommend_websites(keyword):
    keyword_vector = cv.transform([keyword]).toarray()
    similarity_scores = cosine_similarity(keyword_vector, vectors)[0]
    top_indices = similarity_scores.argsort()[::-1][:10]
    
    recommended_websites_list = []   # list bcz it returns list of dictionaries
    for idx in top_indices:
        website_details = {
            'web_id': websites.iloc[idx]['web_id'],
            'web_url': websites.iloc[idx]['web_url'],
            'web_img': websites.iloc[idx]['web_img'],
            'web_title': websites.iloc[idx]['web_title'],
            'web_platform': websites.iloc[idx]['web_platform'],
            'web_short_desc': websites.iloc[idx]['web_short_desc'],
            'web_language': websites.iloc[idx]['web_language']
        }
        recommended_websites_list.append(website_details)
    
    return recommended_websites_list








