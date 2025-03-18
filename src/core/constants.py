ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_NAME = "HF_HUB_DISABLE_SYMLINKS_WARNING"
ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_VALUE = "1"
SENTIMENT_ANALYZER_MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
SENTIMENT_ANALYZER_LABEL_VERY_NEGATIVE = "muy negativo"
SENTIMENT_ANALYZER_LABEL_NEGATIVE = "negativo"
SENTIMENT_ANALYZER_LABEL_NEUTRAL = "neutral"
SENTIMENT_ANALYZER_LABEL_POSITIVE = "positivo"
SENTIMENT_ANALYZER_LABEL_VERY_POSITIVE = "muy positivo"
BIGQUERY_PROJECT_NAME = "buena-cocina-fp"
BIGQUERY_DATASET_NAME = "firestore_export_buena_cocina"
BIGQUERY_SP_CALC_SALES_BY_DAY_OF_WEEK_NAME = "calculate_sales_by_day_of_week"
BIGQUERY_SP_GET_TOP_LOCATIONS_ON_MAP_NAME = "get_top_locations_on_map"
BIGQUERY_SP_GET_TOP_SOLD_PRODUCTS_NAME = "get_top_sold_products"
REDIS_CACHE_PREFIX = "fastapi:bc:pyapi:cache"
INSIGHT_ROUTES_GET_TOP_LOCATIONS_ON_MAP_CACHE_EXPIRE = 60 * 60 * 24 # 24 hours
INSIGHT_ROUTES_CALCULATE_SALES_BY_DAY_OF_WEEK_CACHE_EXPIRE = 60 * 60 * 3 # 3 hours
PRODUCT_REVIEW_ROUTES_GET_ALL_CACHE_EXPIRE = 60 * 10 # 10 minutes
PRODUCT_REVIEW_ROUTES_PAGING_BY_PRODUCT_ID_WITH_RANGE_CACHE_EXPIRE = 60 * 5 # 5 minutes
PRODUCT_REVIEW_ROUTES_PAGING_BY_USER_ID_WITH_RANGE_CACHE_EXPIRE = 60 * 3 # 3 minutes
STORE_REVIEW_ROUTES_GET_ALL_CACHE_EXPIRE = 60 * 10 # 10 minutes
STORE_REVIEW_ROUTES_PAGING_BY_STORE_ID_WITH_RANGE_CACHE_EXPIRE = 60 * 5 # 5 minutes
STORE_REVIEW_ROUTES_PAGING_BY_USER_ID_WITH_RANGE_CACHE_EXPIRE = 60 * 3 # 3 minutes
EMBEDDINGS_MODEL = "intfloat/multilingual-e5-large"
SENTENCE_TRANSFORMERS_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2" # Modelo en español
table_products = 'products'
table_stores = 'stores'

# Ayuda para el bot
CATEGORY_SYNONYMS = {
    "italiana": ["pizza", "pasta", "spaghetti", "lasagna"],
    "mexicana": ["tacos", "burros", "quesadillas", "nachos"],
    "china": ["rollitos", "arroz", "pollo", "dim sum"],
    "argentina": ["asado", "empanadas", "choripán", "parrilla"],
    "internacional": ["francesa", "europea"],
    "comida rápida": ["fast food", "hamburguesas", "snacks", "hotdogs", "sandwich", "lonches", "pizza"],
    "pizza": ["pizzería", "pizzas", "italiano"],
    "bebidas": ["refrescos", "jugos", "cócteles", "cafe", "preparados"],
    "postres": ["dulces", "pasteles", "helados", "galletas", "pan", "roles"],
    "saludable": ["ensalada", "jugos", "batidos", "baguette", "vegetariano"]
}


# Ayuda para correguir palabras
VALID_WORDS = ["pizza", "pasta", "hamburguesa", "tacos", "cafe", 'botana', "papas", "pastes", "postres" "tienes", "alguien",
               "vender", "bebidas", "venden", "sandwiches", 'baggete', 'sopa', 'ramen', 'bebidas', 'quien']

VALID_WORDS_ABOUT_QUESTIONS = ['este momento', 'ahora', 'ahorita', 'hoy' 'esta hora']

CATEGORY_DESCRIPTIONS = {
    "italiana": "pizza, pasta, comida de Italia, lasaña, risotto",
    "mexicana": "tacos, burritos, comida mexicana, enchiladas, quesadillas",
    "china": "comida china, arroz frito, dumplings, rollitos primavera",
    "comida rápida": "fast food, hamburguesas, hot dogs, papas fritas pizza",
    "saludable": "ensaladas, batidos, comida saludable, jugos naturales bajo en calorias",
    "postres": "pasteles, helados, dulces, panadería, chocolates",
    "argentina": "asado, empanadas, choripán, milanesa, bife de chorizo, parrilla, matambre, chimichurri, comida argentina",
    "internacional": "comida francesa, sushi, hamburguesas, platillos internacionales",
}


open_now_examples = [
    "¿Quién está abierto ahora?",
    "¿Qué tiendas están abiertas ahorita?",
    "¿Dónde puedo comprar algo en este momento?",
    "¿Qué lugares están disponibles ahora?",
    "¿Puedo ir a una tienda ahorita?",
]

opening_hours_examples = [
    "¿A qué hora abre la tienda?",
    "¿Hasta qué hora están abiertos?",
    "¿Cuál es el horario de atención?",
    "¿Cuándo cierra este negocio?",
    "¿A qué hora puedo ir?",
]

# Ejemplos de consultas sobre tiendas
store_examples = [
    "¿Dónde puedo encontrar una tienda?",
    "Quiero saber qué tiendas están abiertas",
    "¿Dónde hay un restaurante?",
    "¿Cuáles son los horarios de los negocios?",
    "A qué hora cierra la cafetería",
    "Quisiera conocer los restaurantes disponibles",
    "¿Qué tiendas están abiertas ahora?",
    "¿Cuáles son los lugares para comer?"
]

# Ejemplos de consultas sobre productos
product_examples = [
    "Quiero una hamburguesa",
    "¿Tienen pizza disponible?",
    "Quisiera pedir un café",
    "Dime qué postres tienes",
    "Estoy buscando bebidas frías",
    "Me gustaría un platillo mexicano",
    "¿Qué comida tienen?",
    "¿Tienen alguna bebida especial?"
]