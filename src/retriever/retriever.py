from src.vector_store.models import SearchResult


class Retriever:
    """Document retriever class"""

    def __init__(self, vector_store, embedding):

        self.vector_store = vector_store
        self.embedding = embedding

    def embed_query(self, query: str) -> list[float]:
        """Text embedding function

        Args:
            query (str): a query text

        Return:
            list (float): embedded text
        """

        return self.embedding.embed_text(query)

    def retrieve(self, query: str, top_k=5) -> list[SearchResult]:
        """A function for vector store retriever

        Args:
            query (str): a query text
            top_k (int): maximum number of similar results to retrieve
        Return:
            list (SearchResult): top similar text from the vector store
        """

        embedding = self.embed_query(query)

        return self.vector_store.search(query_embedding=embedding, top_k=top_k)
