from agents import function_tool
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from utils import process_chroma_query_result
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

load_dotenv(override=True)

@function_tool
def get_headlines(query: str) -> List[Dict[str, str]]:
    """
    Retrieve the top 5 most relevant headlines from the Chroma database
    based on a semantic search using the provided query string.

    Args:
        query (str): The natural language query to search against stored headlines.

    Returns:
        List[Dict[str, str]]: A list of the top 5 matching headlines, where each
                              headline is represented as {'id': str, 'text': str}.
    """

    # Initialize embedding function
    ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-large"
    )

    # Connect to Chroma persistent client
    chroma_client = chromadb.PersistentClient()

    # Load the headlines collection with embeddings
    headlines = chroma_client.get_collection(
        name="headlines",
        embedding_function=ef
    )

    # Query the collection
    results = headlines.query(
        query_texts=[query],
        n_results=5
    )

    # Process results into clean structured list
    return process_chroma_query_result(results)

@function_tool
def send_html_email(subject: str, html_body: str, recipient: str) -> Dict[str, str]:
    """
    Send an HTML email using SendGrid.

    Args:
        subject (str): The subject line of the email.
        html_body (str): The HTML content of the email.
        recipient (str): Recipient email address.

    Returns:
        Dict[str, str]: Status of the email sending operation.
    """
    try:
        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            return {"status": "error", "message": "SendGrid API key not set in environment"}

        sg_client = sendgrid.SendGridAPIClient(api_key=api_key)
        from_email = Email("arnav.thakrar@gmail.com")  # Must be verified in SendGrid
        to_email = To(recipient)
        content = Content("text/html", html_body)

        mail = Mail(from_email, to_email, subject, content)
        response = sg_client.client.mail.send.post(request_body=mail.get())

        if 200 <= response.status_code < 300:
            return {"status": "success", "message": f"Email sent to {recipient}"}
        else:
            return {
                "status": "error",
                "message": f"SendGrid responded with status {response.status_code}",
                "body": response.body.decode() if hasattr(response.body, 'decode') else str(response.body)
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}