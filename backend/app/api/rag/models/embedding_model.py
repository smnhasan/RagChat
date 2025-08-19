import os
import asyncio
import requests
import aiohttp
from typing import List, Optional
from langchain_core.embeddings import Embeddings
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()
BASE_URL = 'https://chatbot.staging.nascenia.com'


class Embedding(Embeddings):
    """
    Custom Embeddings class for interfacing with a local embedding API endpoint.

    Attributes:
        api_url (str): The URL of the local embedding API endpoint
        api_key (Optional[str]): API key for authentication (if required)
    """

    def __init__(
        self,
        api_url: str = f"{BASE_URL}/api/v1/embed",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the Embedding class.

        Args:
            api_url (str): URL of the embedding API endpoint
            api_key (Optional[str]): API key for authentication
        """
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self.counter = 0

        print(f"Embedding API URL: {self.api_url}", flush=True)

    @retry(
        stop=stop_after_attempt(3),  # Retry up to 3 times
        wait=wait_fixed(2),  # Wait 2 seconds between retries
        retry=retry_if_exception_type(
            requests.RequestException
        ),  # Retry only on RequestException
    )
    def _embed_text(self, text: str) -> List[float]:
        """
        Internal method to embed a single piece of text with retry logic.

        Args:
            text (str): Input text to embed

        Returns:
            List[float]: Embedding vector
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {"text": text}
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for non-200 responses
        embeddings = response.json().get("embedding", [])
        return embeddings

    @retry(
        stop=stop_after_attempt(3),  # Retry up to 3 times
        wait=wait_fixed(2),  # Wait 2 seconds between retries
        retry=retry_if_exception_type(aiohttp.ClientError),  # Retry only on ClientError
    )
    async def _async_embed_text(
        self, session: aiohttp.ClientSession, text: str
    ) -> List[float]:
        """
        Internal asynchronous method to embed a single piece of text with retry logic.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for requests
            text (str): Input text to embed

        Returns:
            List[float]: Embedding vector
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # self.counter += 1
        # print(f'<<Calling Embedding:  {self.counter}>>', flush=True)

        async with session.post(
            self.api_url, json={"text": text}, headers=headers
        ) as response:
            if response.status != 200:
                raise aiohttp.ClientError(f"HTTP Error: {response.status}")
            json_data = await response.json()
            return json_data.get("embedding", [])

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Asynchronous method to embed multiple documents with retry logic.

        Args:
            texts (List[str]): List of text to embed.

        Returns:
            List[List[float]]: List of embeddings.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._async_embed_text(session, text) for text in texts]
            return await asyncio.gather(*tasks)

    async def aembed_query(self, text: str) -> List[float]:
        """
        Asynchronous method to embed a single query with retry logic.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding vector.
        """
        async with aiohttp.ClientSession() as session:
            return await self._async_embed_text(session, text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents synchronously with retry logic.

        Args:
            texts (List[str]): List of text to embed.

        Returns:
            List[List[float]]: List of embeddings.
        """
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query synchronously with retry logic.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding vector.
        """
        return self._embed_text(text)
    
    