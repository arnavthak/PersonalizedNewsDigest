import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv(override=True)

ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-large"
)

chroma_client = chromadb.PersistentClient()

collection = chroma_client.get_collection(name="headlines", embedding_function=ef)

results = collection.query(
    query_texts=["celebrity news"],
    n_results=5
)

print(results)