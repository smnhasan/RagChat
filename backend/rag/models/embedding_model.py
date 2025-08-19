import torch
import asyncio
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    """Configuration for the embedding model."""
    model_id: str = "hkunlp/instructor-large"
    device_type: str = "cuda" if torch.cuda.is_available() else "cpu"
    test_query: str = "This is a test."


def build_embedding_model(config: EmbeddingConfig):
    """Build and initialize the embedding model."""
    embeddings = HuggingFaceInstructEmbeddings(
        model_name=config.model_id,
        model_kwargs={"device": config.device_type},
    )
    # Warm up the model by embedding a test query
    _ = embeddings.embed_query(config.test_query)
    return embeddings


class Embedding(Embeddings):
    """
    Custom Embeddings class using a local embedding model.

    Attributes:
        model: The loaded embedding model
    """

    def __init__(
        self,
        config: EmbeddingConfig = EmbeddingConfig(),
    ):
        """
        Initialize the Embedding class.

        Args:
            config (EmbeddingConfig): Configuration for the embedding model
        """
        super().__init__()
        self.model = build_embedding_model(config)

    def _embed_text(self, text: str) -> List[float]:
        """
        Internal method to embed a single piece of text.

        Args:
            text (str): Input text to embed

        Returns:
            List[float]: Embedding vector
        """
        try:
            return self.model.embed_query(text)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    async def _async_embed_text(
        self, text: str
    ) -> List[float]:
        """
        Internal asynchronous method to embed a single piece of text.

        Args:
            text (str): Input text to embed

        Returns:
            List[float]: Embedding vector
        """
        try:
            return await self.model.aembed_query(text)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Asynchronous method to embed multiple documents.

        Args:
            texts (List[str]): List of text to embed.

        Returns:
            List[List[float]]: List of embeddings.
        """
        tasks = [self._async_embed_text(text) for text in texts]
        return await asyncio.gather(*tasks)

    async def aembed_query(self, text: str) -> List[float]:
        """
        Asynchronous method to embed a single query.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding vector.
        """
        return await self._async_embed_text(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents synchronously.

        Args:
            texts (List[str]): List of text to embed.

        Returns:
            List[List[float]]: List of embeddings.
        """
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query synchronously.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding vector.
        """
        return self._embed_text(text)
