from dotenv import load_dotenv
load_dotenv()
import os
from typing import Any, Dict, List
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

index_name = index_name = os.environ.get("EBAY_INDEX_NAME")

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    chat = ChatOpenAI(verbose = True, temperature=0, max_tokens=1500)
    # augmentation generation
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm = chat, retriever = docsearch.as_retriever(), prompt=rephrase_prompt
    )

    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_document": result["context"]
    }
    return new_result

if __name__ == "__main__":
    res = run_llm(query="what can you tell me about ebay Human I-T")
    print(res["result"])