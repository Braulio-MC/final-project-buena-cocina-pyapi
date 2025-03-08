from core.firebaseHelper import db
from core.constants import table_stores

def get_stores_by_ids(store_ids: list) -> list:
    stores = []
    for store_id in store_ids:
        doc = db.collection(table_stores).document(store_id).get()
        if doc.exists:
            store = doc.to_dict()
            store["id"] = doc.id  # Agregar el ID al diccionario si es necesario
            stores.append(store)
    return stores