from pymongo import MongoClient
from bson import Binary
import pandas as pd

# Connect to MongoDB
mongo_client = MongoClient('mongodb://localhost:27017')
db = mongo_client.users  # Database name 'users'
collection = db.users  # Collection name 'users'

def getuserdata(email):
    # Find user document in MongoDB based on email
    user_document = collection.find_one({"email": email})

    if user_document:
        # Extract user details from the document
        user_details = {
            'email': user_document['email'],
            'password': user_document['password'],
            'interests': user_document['interests']
        }

        # Check if the user document contains the 'fullName' field
        if 'fullName' in user_document:
            user_details['fullName'] = user_document['fullName']

        # Check if the user document contains the 'moreAboutUser' field
        if 'moreAboutUser' in user_document:
            user_details['moreAboutUser'] = user_document['moreAboutUser']

        # Check if the user document contains the 'userPhoto' field
        if 'userPhoto' in user_document:
            user_details['userPhoto'] = user_document['userPhoto']

        # Check if the user document contains the 'education' field
        if 'education' in user_document:
            user_details['education'] = user_document['education']

        return user_details  # Return user details as a list containing a dictionary
    else:
        return []  # Return an empty list if user not found
    
def insert_user_fullName(email, fullName):
    # Update user document in MongoDB to insert fullName
    collection.update_one({"email": email}, {"$set": {"fullName": fullName}})

def insert_user_moreAboutUser(email, moreAboutUser):
    # Update user document in MongoDB to insert moreAboutUser
    collection.update_one({"email": email}, {"$set": {"moreAboutUser": moreAboutUser}})

def insert_user_userPhoto(email, userPhoto):
    # Update user document in MongoDB to insert userPhoto
    collection.update_one({"email": email}, {"$set": {"userPhoto": userPhoto}}) 

def insert_user_interests(email, interests):
    # Update user document in MongoDB to insert interests
    collection.update_one({"email": email}, {"$push": {"interests": interests}}) 

def delete_user_interests(email, selected_interests):
    # Delete selected interests from user document in MongoDB
    collection.update_one({"email": email}, {"$pull": {"interests": {"$in": selected_interests}}})

def insert_user_education(email, collegeName, specialization, grade):
    # Create education document
    education_det = {
        "collegeName": collegeName,
        "specialization": specialization,
        "grade": grade
    }
    
    # Find user document by email and update education field
    collection.update_one({"email": email}, {"$push": {"education": education_det}})

def delete_user_education(email, collegeName):
     collection.update_one(
        {"email": email},
        {"$pull": {"education": {"collegeName": collegeName}}}
    )
