import pandas as pd
from firebaseHelper import db

def get_product_data():
    """
    Obtiene los datos de los productos desde Firebase Firestore.
    """
    productos = db.collection('products').stream()
    return [{
        "id": p.id,
        "name": p.get("name", ""),
        "description": p.get("description", ""),
        "category": p.get("category", []),
        "price": p.get("price", 0),
        "rating": p.get("rating", 0),
        "totalReviews": p.get("totalReviews", 0),
        "store_name": p.get("store", {}).get("name", ""),  # Nombre de la tienda
        "discount": p.get("discount", {}).get("percentage", 0)  # Porcentaje de descuento
    } for p in productos]

def create_features_df():
    """
    Convertir los dtos en un dataframe con caracterisitcas relevantes
    """

    data = get_product_data()
    df = pd.DataFrame(data)

    # Convertir categorias en una cadena de texto
    df["category"] = df["category"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")

    # Generar texto de características combinadas
    df["text_features"] = (
            df["name"] + " " + df["description"] + " " + df["category"] +
            " " + df["store_name"]  # Agregar tienda
    )

    return df[["id", "text_features", "category", "price", "rating", "totalReviews", "discount"]]
