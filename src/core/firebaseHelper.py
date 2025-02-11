from firebase_admin import initialize_app, firestore
from datetime import datetime

app = initialize_app()
db = firestore.client(app)

