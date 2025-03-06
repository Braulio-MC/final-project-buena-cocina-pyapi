from core.firebaseHelper import db


def get_all_products():
    products_ref = db.collection("productos").stream()
    return [doc.to_dict() for doc in products_ref]


def update_product_embedding(product_id: str, embedding: list):
    db.collection("productos").document(product_id).update({"embedding": embedding})