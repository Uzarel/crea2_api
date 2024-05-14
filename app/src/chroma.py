import chromadb
import os
import time

from chromadb.config import Settings
from langchain_chroma import Chroma


def get_chroma_client(timeout=60):
    client = None
    start_time = time.time()
    while not client:
        try:
            client = chromadb.HttpClient(
                host=os.environ["CHROMA_HOST"],
                port=os.environ["CHROMA_PORT"],
                settings=Settings(allow_reset=True),
            )
        except:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timed out while trying to connect to Chroma server.")
            time.sleep(1) # Sleep for 1 second before retrying
    client.reset()
    return client


def upload_documents_to_chroma(
    chroma_client, collection_name, embedding_function, docs
):
    # Do not upload if collection already exists
    if collection_name not in [
        collection.name for collection in chroma_client.list_collections()
    ]:
        ids = [doc.metadata["uuid"] for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        documents = [doc.page_content for doc in docs]
        embeddings = embedding_function.embed_documents(documents)
        collection = chroma_client.get_or_create_collection(name=collection_name)
        collection.add(
            ids=ids, metadatas=metadatas, documents=documents, embeddings=embeddings
        )


def get_chroma_vectorstore(chroma_client, collection_name, embedding_function):
    return Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )
