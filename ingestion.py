# Loads using readthedocs loader, chunk everything to smaller pieces, embedd everything, then index to pinecone
# load, split, embed, store
from dotenv import load_dotenv
load_dotenv()
import os
from bs4 import BeautifulSoup
from langchain.docstore.document import Document

# chunkify HTML loaded documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
# loads doc into langchain doc object
from langchain_community.document_loaders import ReadTheDocsLoader
# embed all documents
from langchain_openai import OpenAIEmbeddings
# vector store object
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

class CustomHTMLLoader:
    def __init__(self, path):
        self.path = path
    
    def load(self):
        documents = []
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        page_content = self.extract_content(content)
                        documents.append(Document(metadata={'source': file_path}, page_content=page_content))
        return documents

    def extract_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.find(id='main-content')
        
        if not main_content:
            return soup.get_text(separator='\n', strip=True)
        
        return main_content.get_text(separator='\n', strip=True)

def ingest_docs():
    loader = CustomHTMLLoader(path="ebay-docs/www.ebayinc.com")
    # loader = CustomHTMLLoader(path="langchain-docs/api.python.langchain.com/en/latest/caches")

    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents")
    # for i, doc in enumerate(raw_documents):
    #     print(f"Document {i+1} length before splitting: {len(doc.page_content)}")  # Assuming 'page_content' holds the text

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ",""])

    # # chunks
    documents = text_splitter.split_documents(raw_documents)
    

    for doc in documents:
        new_url = doc.metadata.get("source", "")
        new_url = new_url.replace("ebay-docs", "https:/").replace("\\", "/")
        doc.metadata.update({"source": new_url})
    
    # for doc in documents:
    #     print(doc.metadata)
    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embeddings, index_name= os.environ.get("EBAY_INDEX_NAME"))
    print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
    # file_path = 'langchain-docs/api.python.langchain.com/en/latest/caches/index.html'
    # try:
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         content = file.read()
    #         print("File content preview:")
    #         print(content[:1000])  # Print the first 1000 characters to verify content
    # except FileNotFoundError:
    #     print(f"File not found: {file_path}")
    # except UnicodeDecodeError as e:
    #     print(f"UnicodeDecodeError: {e}")