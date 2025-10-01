# import os
# import firebase_admin
# from firebase_admin import credentials, firestore
#
# # Project root ka path
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# # Service account key file ka name (tumhari nayi file)
# cred_path = os.path.join(BASE_DIR, "keys1.json")
#
# # Firebase initialize
# if not firebase_admin._apps:
#     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)
#
# # Firestore client
# db = firestore.client()
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("hello.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
firebase_auth = auth
