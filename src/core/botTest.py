import numpy as np
from data.service.EmbeddingService import generate_embedding
from core.firebaseHelper import db
from data.service.EmbeddingService import find_similar_products



query = "tienes pizza"
product_ids = find_similar_products(query)

print(f"Productos encontrados: {product_ids}")  # Verifica si devuelve IDs