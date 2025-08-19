from typing import List, Optional, Dict

def process_chroma_query_result(chroma_result: dict) -> List[Dict[str, str]]:
    """
    Transforms the output of a ChromaDB collection.query() call into a
    list of dictionaries, with each dictionary containing 'id' and 'text'.

    Args:
        chroma_result (dict): The dictionary returned by the collection.query() call.
                              Expected to have 'ids' and 'documents' keys, each
                              containing a nested list.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary has
                    the keys 'id' and 'text'.
    """
    processed_list = []
    ids = chroma_result.get('ids', [[]])[0]
    documents = chroma_result.get('documents', [[]])[0]

    if len(ids) != len(documents):
        print("Warning: Mismatch between number of IDs and documents. Check the query result.")
        return []

    for unique_id, text in zip(ids, documents):
        processed_list.append({"url": unique_id, "text": text})

    return processed_list

def get_fetch_params():
    params = {"command": "uvx", "args": ["mcp-server-fetch"]}
    return params