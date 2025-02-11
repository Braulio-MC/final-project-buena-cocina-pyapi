import pandas as pd
import re
from core.firebaseHelper import db

def clean_text(text):
    """Limpia el texto eliminando caracteres especiales y espacios innecesarios."""
    if not isinstance(text, str):
        return ""  # Si es NaN u otro tipo, devolver cadena vacía
    text = text.lower().strip()  # Convertir a minúsculas y eliminar espacios extra
    text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios por uno solo
    text = re.sub(r'[^a-zA-Z0-9áéíóúüñ ]', '', text)  # Eliminar caracteres especiales
    return text


def create_features_df():
    """
        Carga los datos de productos, los limpia y crea una representación de texto.
        Retorna un DataFrame con las columnas: ['id', 'text_features'].
    """
    # Carga los datos desde firestor
    products_ref = db.collection("products").stream()
    products = []

    for doc in products_ref:
        data = doc.to_dict()
        product_id = doc.id
        name = clean_text(data.get("name", ""))
        description = clean_text(data.get("description", ""))
        category = clean_text(" ".join(data.get("category", [])))  # Concatenar categorías en una sola string
        store = clean_text(data.get("store", {}).get("name", ""))  # Nombre de la tienda si existe
        price = str(data.get("price", ""))  # Convertir el precio a string

        # 🔹 **Crear una representación de texto útil**
        text_features = f"{name} {description} {category} {store} {price}"

        products.append({"id": product_id, "text_features": text_features})

        # 🔹 **Convertir a DataFrame**
    df = pd.DataFrame(products)

    return df
