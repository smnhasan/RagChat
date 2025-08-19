import requests
import os
from typing import Any, Dict, List, Optional
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import Generation, LLMResult
from pydantic import Field, BaseModel as PydanticBaseModel
from dotenv import load_dotenv

load_dotenv()
BASE_URL = 'https://chatbot.staging.nascenia.com'
counter = 0


class LLM(BaseLLM, PydanticBaseModel):
    """
    Custom LLM class for interfacing with a local API endpoint.

    Attributes:
        api_url (str): The URL of the local API endpoint
        api_key (Optional[str]): API key for authentication (if required)
    """

    api_url: str = Field(default=f"{BASE_URL}/api/v1/generate")
    api_key: Optional[str] = Field(default=None)

    def __init__(
        self,
        api_url: str = f"{BASE_URL}/api/v1/generate",
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the LocalAPILLM.

        Args:
            api_url (str): URL of the API endpoint
            api_key (Optional[str]): API key for authentication
        """
        # Use Pydantic's model_construct to properly initialize fields
        super().__init__(api_url=api_url, api_key=api_key, **kwargs)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Call the local API with the given prompt.

        Args:
            prompt (str): The input prompt
            stop (Optional[List[str]]): Optional list of stop sequences
            run_manager (Optional[CallbackManagerForLLMRun]): Callback manager

        Returns:
            str: Generated text from the API
        """
        global counter
        # counter += 1
        # print(f'<<Calling LLM: {counter}>>', flush=True)

        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Prepare payload
        payload = {"query": prompt}

        try:
            # Make API request
            response = requests.post(self.api_url, json=payload, headers=headers)

            # Raise an exception for bad responses
            response.raise_for_status()

            # Extract prediction
            result = response.json().get("prediction", "")

            return result

        except requests.RequestException as e:
            raise ValueError(f"API request failed: {e}")

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """
        Generate responses for multiple prompts.

        Args:
            prompts (List[str]): List of input prompts
            stop (Optional[List[str]]): Optional list of stop sequences
            run_manager (Optional[CallbackManagerForLLMRun]): Callback manager

        Returns:
            LLMResult: Generated responses
        """
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop, run_manager, **kwargs)
            generations.append([Generation(text=text)])

        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        """
        Return the type of LLM.

        Returns:
            str: Type identifier for the LLM
        """
        return "local_api_llm"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """
        Return identifying parameters for the LLM.

        Returns:
            Dict[str, Any]: Dictionary of identifying parameters
        """
        return {"api_url": self.api_url}
    
    
    