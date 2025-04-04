import pandas as pd
import re
from core.firebaseHelper import db
from core.constants import table_products

def clean_text(text):
    """Limpia el texto eliminando caracteres especiales y espacios innecesarios."""
    if not isinstance(text, str):
        return ""  # Si es NaN u otro tipo, devolver cadena vacía
    text = text.lower().strip()  # Convertir a minúsculas y eliminar espacios extra
    text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios por uno solo
    text = re.sub(r'[^a-zA-Z0-9áéíóúüñ ]', '', text)  # Eliminar caracteres especiales
    return text if text else "sin_informacion"  # Rellenar si queda vacío


def create_features_df():
    """
    Carga los datos de productos, los limpia y crea una representación de texto.
    Retorna un DataFrame con las columnas: ['id', 'text_features'].
    """
    # Carga los datos desde Firestore
    products_ref = db.collection(table_products).stream()
    products = []

    for doc in products_ref:
        data = doc.to_dict()
        product_id = doc.id
        name = clean_text(data.get("name", ""))
        description = clean_text(data.get("description", ""))
        category = clean_text(" ".join(data.get("category", [])))
        store = clean_text(data.get("store", {}).get("name", ""))
        price = str(data.get("price", ""))

        # Crear representación de texto
        text_features = f"{name} {description} {category} {store} {price}".strip()

        # Añadir al listado
        products.append({"id": product_id, "text_features": text_features})

    # Convertir a DataFrame
    df = pd.DataFrame(products)

    # Filtrar productos con text_features vacíos
    df = df[df['text_features'].str.strip() != ""]

    if df.empty:
        raise ValueError("Todos los productos tienen 'text_features' vacíos después de limpiar los datos.")

    return df