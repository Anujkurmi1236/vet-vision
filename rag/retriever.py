from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


VECTOR_DB_PATH = "vectorstore/veterinary_guidelines"


def get_vectorstore():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name="veterinary_guidelines"
    )

    return vectorstore