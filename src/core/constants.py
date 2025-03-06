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
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"
SENTENCE_TRANSFORMERS_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2" # Modelo en español

# Ayuda para el bot
CATEGORY_SYNONYMS = {
    "comida rápida": ["fast food", "hamburguesas", "snacks, pizza, hotdogs, botana frituras, sanwich, lonches,"],
    "pizza": ["pizzería", "pizzas", "italiano"],
    "bebidas": ["refrescos", "jugos", "cócteles, cafe, preparados"],
    "postres": ["dulces", "pasteles", "helados"],
    "saludable": ['ensalda', 'jugos', 'batidos']
}

STORE_SYNONYMS = {
    "McDonald's": ["McD", "Mc Donalds", "McDonalds"],
    "Domino's": ["Dominos", "Domino"],
    "Starbucks": ["coffee shop", "café"]
}
