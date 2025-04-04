from core.firebaseHelper import db
from core.constants import table_products, table_stores


def get_all_products():
    products_ref = db.collection(table_products).stream()
    return [doc.to_dict() for doc in products_ref]


def update_product_embedding_product(product_id: str, embedding: list):
    db.collection(table_products).document(product_id).update({"embedding": embedding})


def update_product_embedding_store(store_id: str, embedding: list):
    db.collection(table_stores).document(store_id).update({"embedding_stores": embedding})