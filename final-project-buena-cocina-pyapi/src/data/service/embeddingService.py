import data.service.indexing as indexing
from core.botCore import  *
import logging


logging.basicConfig(level=logging.DEBUG)


def find_products(q: str, top_k: int = 10):
    query = normalize_query(q)

    index = indexing.PRODUCT_INDEX
    products_data = indexing.PRODUCTS_DATA

    # Debug por si no hay datos
    if index is None or index.ntotal == 0:
        return []

    # Extraer filtros de la pregunta (que le interesa saber al cliente)
    min_price, max_price, category = extract_filters_from_query(query)
    print(min_price, max_price )


    # En base a los filtros obtner los ids
    filtered_ids = filter_products(products_data, min_price, max_price, category)
    print(filtered_ids)

    # Realizar la búsqueda por descripción utilizando FAISS si es necesario
    description_results = search_by_description_fallback(query, products_data)

    # Combina los resultados de los filtros con los resultados por descripción
    combined_ids = set(filtered_ids) | set(description_results)

    # Filtrar productos según los ids combinados
    result = [products_data[prod_id] for prod_id in combined_ids]

    order = sort_by_filter(min_price, max_price)


    if order == "asc":
        result.sort(key=lambda p: p["price"])
    elif order == "desc":
        result.sort(key=lambda p: p["price"], reverse=True)

    if not result:
        return get_confused_message()

    return result[:top_k]



def find_stores(query: str, top_k: int = 10) -> None | list | str:
    index = indexing.STORE_INDEX
    stores_data = indexing.STORES_DATA

    # Debug por si no hay datos
    if index is None or index.ntotal == 0:
        return []

    query_type = type_question_about_store(query)

    if query_type == "open_now":
        # Filtrar tiendas abiertas en este momento
        open_now_stores = get_open_stores(stores_data)

        if open_now_stores:
            return open_now_stores[:top_k]
        else:
            return no_open_stores_message()

    elif query_type == "opening_hours":
        # Horarios especificos
        return handle_schedule_query(query, stores_data)

    elif query_type == "ranking":
        # Filtrar tiendas por rankings
        return get_stores_by_rating(query, stores_data)

    elif query_type == "description":
        pass
    else:
        return "unknown"

