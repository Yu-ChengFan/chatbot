import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"), environment=os.environ.get('PINECONE_ENVIRONMENT_REGION'))  # Replace with your Pinecone API key and environment


index_name = os.environ.get("EBAY_INDEX_NAME")
index = pc.Index(index_name)

index.delete(delete_all=True)

print(f"All vectors in the index '{index_name}' have been deleted.")