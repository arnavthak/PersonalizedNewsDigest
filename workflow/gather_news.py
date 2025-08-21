from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils import embedding_functions

load_dotenv(override=True)

def gather_news():
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        print("NEWS_API_KEY environment variable not set.")

    newsapi = NewsApiClient(api_key=news_api_key)

    top_headlines = newsapi.get_top_headlines(country='us', language='en', page_size=100)

    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-large"
    )

    chroma_client = chromadb.PersistentClient()

    # chroma_client.reset() # clear DB of previous day's news headlines

    # collection = chroma_client.create_collection(name="headlines", embedding_function=ef)

    # Check if the collection exists before trying to delete it
    collection_name = "headlines"
    try:
        chroma_client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        # This might fail if the collection doesn't exist, which is fine
        print(f"Could not delete collection '{collection_name}': {e}")
        
    # Create a new collection
    collection = chroma_client.create_collection(name=collection_name, embedding_function=ef)

    print("Created collection headlines!")

    articles = top_headlines["articles"]

    print(articles)

    for article in articles:
        collection.add(
            ids=[article["url"]],
            documents=[f"{article['title']}\n\n{article['description']}"]
        )

    print("Done!")

if __name__ == "__main__":
    gather_news()