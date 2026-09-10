import pickle
import numpy as np
from src.vector_store.models import SearchResult
from src.embedding.models import TextEmbed
from pathlib import Path


class VectorStore:
    """Store the texts embeded list in a retrievable file"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.embedding_records = []

    def add_many(self, records: list[TextEmbed]) -> None:
        """
        Add the embedding text to the records
        Args:
            records(list): embedded texts list
        Return:
            None
        """
        for record in records:
            self.embedding_records.append(record)

    def store(self) -> None:
        """
        function for storing the text embeded list in a file
        Return:
            list: stored the embedded text list in the file path
        """

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            self.file_path,
            "wb",
        ) as file:
            pickle.dump(self.embedding_records, file)

    def load(self):
        """load the stored text embedded list from the file"""

        if not self.file_path.exists():
            raise FileNotFoundError(f"vector file in the {self.file_path} not found!")

        with open(self.file_path, "rb") as file:
            self.embedding_records = pickle.load(file)
            print("Vector store file loaded successfully!")
            return self.embedding_records

    def search(self, query_embedding: list[float], top_k=5) -> list[SearchResult]:
        """
        search and return the top simillar text embedded with the query

        Args:
            query: text query
            top_k: number of search return
        Return:
            list(float): top embedded text with the highest similarity score
        """
        if top_k <= 0:
            raise ValueError("top_k value should be greater than 0")

        results = []

        for record in self.embedding_records:
            similarity = self.cosine_similarity(
                vector1=query_embedding, vector2=record.embedding
            )

            results.append(SearchResult(text_embed=record, similarity_score=similarity))

        results.sort(key=lambda x: x.similarity_score, reverse=True)

        return results[:top_k]

    def cosine_similarity(self, vector1, vector2) -> float:
        """
        cosine similarity between two vectors

        Args:
            vector1: first vector
            vector2: secondd vector
        Return:
            float: similarity score of the two vectors
        """

        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        dot_product = np.dot(
            vector1,
            vector2,
        )

        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)

        return dot_product / (magnitude1 * magnitude2)
