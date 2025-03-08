import Levenshtein

palabra_usuario = "pizza"
palabras_validas = ["pasta", "pizzas", "piso"]

# Encontrar la palabra más cercana
sugerencia = min(palabras_validas, key=lambda x: Levenshtein.distance(palabra_usuario, x))
print(f"¿Quisiste decir '{sugerencia}'?")