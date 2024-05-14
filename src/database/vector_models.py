from typing import Dict, List

import numpy as np
from chromadb import HttpClient
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions import (
    HuggingFaceEmbeddingFunction,
    OpenCLIPEmbeddingFunction,
)
from PIL import Image

from src.config import (
    HUGGINGFACE_API_KEY,
    HUGGINGFACE_MODEL,
    VECTORDB_HOST,
    VECTORDB_NAME,
    VECTORDB_PORT,
)


class VectorDB:
    """
    A class for interacting with a vector database using chromadb library.

    This class provides methods to insert, query, and manage image data
    represented as embeddings in the vector database.
    """

    def __init__(self) -> None:
        """
        Initializes the VectorDB object.

        Sets up the embedding function, connects to the chromadb client,
        and creates or retrieves the specified collection.
        """
        self.embedding_function = HuggingFaceEmbeddingFunction(
            api_key=HUGGINGFACE_API_KEY,
            model_name=HUGGINGFACE_MODEL,
        )
        self.client = HttpClient(host=VECTORDB_HOST, port=VECTORDB_PORT)
        self.collection = self.client.get_or_create_collection(
            name=VECTORDB_NAME,
            metadata={"hnsw:space": "cosine"},
            embedding_function=OpenCLIPEmbeddingFunction(),
            data_loader=ImageLoader(),
        )

    def get_all_data(self) -> Dict:
        """
        Retrieves all data (IDs and metadata) from the vector
        database collection.

        Returns:
            A dictionary containing lists of IDs and metadata for all entries.
        """
        ids_results = self.collection.get()
        return ids_results

    def insert_data(self, image_info_dict: List) -> None:
        """
        Inserts image data into the vector database collection.

        Args:
            image_info_dict: A list of dictionaries containing
              image information (e.g., filepath, ID, metadata).
        """
        image_names = [img_info.filepath for img_info in image_info_dict]
        image_ids = [str(img_info.id) for img_info in image_info_dict]
        image_metadata = [{"title": img_info.id} for img_info in image_info_dict]
        self.collection.add(ids=image_ids, uris=image_names, metadatas=image_metadata)

    def query_with_text(self, query_text: str, n: int = 3) -> Dict:
        """
        Performs a text query against the vector database.

        Args:
            query_text: The text query to use for searching.
            n: The maximum number of results to return (default: 3).

        Returns:
            A dictionary containing query results (distances and URIs).
        """
        query_result = self.collection.query(query_texts=[query_text], include=["distances", "uris"], n_results=n)
        return query_result

    def query_with_image(self, query_image_path: str, n: int = 3) -> Dict:
        """
        Performs an image query against the vector database.

        Args:
            query_image_path: The path to the query image.
            n: The maximum number of results to return (default: 3).

        Returns:
            A dictionary containing query results (distances and URIs).
        """
        query_image = np.array(Image.open(query_image_path))
        query_results = self.collection.query(query_images=[query_image], include=["distances", "uris"], n_results=n)
        return query_results

    def number_of_vectors(self) -> int:
        """
        Returns the number of vectors (data entries) in the collection.

        Returns:
            The number of vectors stored in the vector database.
        """
        return self.collection.count()

    def delete_vector_storage(self) -> None:
        """
        Deletes all vectors from the collection.
        """
        all_ids = self.get_all_data()["ids"]
        if len(all_ids) > 0:
            print("Number of vectors", len(all_ids), self.number_of_vectors())
            print(min(all_ids), max(all_ids))
            self.client.delete_collection(VECTORDB_NAME)
            print("deleting collection in vectordb...")
        else:
            print("No vectors in DB.")


if __name__ == "__main__":
    vectordb = VectorDB()
    count = vectordb.number_of_vectors()
    print(f"number of vectors {count}")
    data = vectordb.get_all_data()
    print(data)
    vectordb.delete_vector_storage()
