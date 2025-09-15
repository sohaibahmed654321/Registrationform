import os
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

# Service account key1.json ka path
cred = credentials.Certificate(os.path.join(BASE_DIR, "myproject", "key1.json"))

# Agar app pehle initialize nahi hua to hi initialize karo
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# ✅ Firestore client create karo
db = firestore.client()
