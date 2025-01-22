from firebase_admin import initialize_app, firestore

app = initialize_app()
db = firestore.client(app)