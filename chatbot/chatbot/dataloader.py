from typing import List
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import os

CHROMA_PERSIST_DIR = f'{os.getcwd()}/datas/upload/chroma-persist'
CHROMA_COLLECTION_NAME = "dosu-bot"

class EmbeddingDB:
    def __init__(self):
        self._db = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function = OpenAIEmbeddings(),
            collection_name=CHROMA_COLLECTION_NAME,
        )
        self._retriever = self._db.as_retriever()

    def _upload_embedding_from_file(self, file_path):
        documents = TextLoader(file_path).load()

        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        print(f'Uploading {file_path} to chroma..')
        self._db.from_documents(
            persist_directory=CHROMA_PERSIST_DIR,
            documents=docs,
            embedding=OpenAIEmbeddings(),
            collection_name=CHROMA_COLLECTION_NAME,
        )
        print(f'Upload complete!! {file_path=}')

    def document_embedding(self, file_lists: List[str]):
        for file in file_lists:
            self._upload_embedding_from_file(file)

    def get_page_contents(self, query: str, use_retriever: bool = False) -> list[str]:
        if use_retriever:
            docs = self._retriever.get_relevant_documents(query)
        else:
            docs = self._db.similarity_search(query)

        str_docs = [doc.page_content for doc in docs]
        return str_docs

if __name__ == '__main__':
    embedding = EmbeddingDB()
    print(embedding.get_page_contents('카카오싱크', True))