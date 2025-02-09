from sentence_transformers import  SentenceTransformer
import joblib
from constants import SENTENCE_TRANSFORMERS_MODEL_NAME, EMBEDDINGS_JOBLIB, PRODUCTS_IDS_CSV
from dataPreprocessing import create_features_df

model = SentenceTransformer(SENTENCE_TRANSFORMERS_MODEL_NAME)

def generate_embeddings(df):

    """
        Esta funcio crea embeddings:
        Los embeddings son una tecnica fundamental de IA para transformar en este caso categorias a listas de
        numeros capturando asi el significado, contexto o relaciones de datos en matrices premitiendo que las maquinas
        entiendan y puedan hacer operaciones como comparaciones.
    """

    text_data = df['text_features'].tolist()
    embeddings = model.encode(text_data, show_progress_bar=True)
    return embeddings

# Obtener y procesar datos
df = create_features_df()
embeddings = generate_embeddings(df)

# Guardar embeddings y IDs para su posterior uso
joblib.dump(embeddings, EMBEDDINGS_JOBLIB)
df[["id"]].to_csv(PRODUCTS_IDS_CSV, index=False)
