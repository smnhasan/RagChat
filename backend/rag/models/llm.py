import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from huggingface_hub import hf_hub_download
import torch

try:
    from llama_cpp import Llama
except ImportError:
    raise ImportError(
        "llama-cpp-python is required. Install with: "
        "pip install llama-cpp-python or "
        "pip install llama-cpp-python[cublas] for GPU support"
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for the llama-cpp-python model."""
    model_id: str = os.getenv("LLAMA_MODEL_ID", "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF")
    model_basename: str = os.getenv("LLAMA_MODEL_BASENAME", "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
    context_window_size: int = int(os.getenv("CONTEXT_WINDOW_SIZE", 8096))
    max_new_tokens: int = int(os.getenv("MAX_NEW_TOKENS", 2048))
    n_gpu_layers: int = int(os.getenv("N_GPU_LAYERS", -1))  # -1 means use all layers on GPU
    n_batch: int = int(os.getenv("N_BATCH", 512))
    n_threads: int = int(os.getenv("N_THREADS", os.cpu_count() or 4))
    temperature: float = float(os.getenv("TEMPERATURE", 0.8))
    top_p: float = float(os.getenv("TOP_P", 0.9))
    top_k: int = int(os.getenv("TOP_K", 40))
    repeat_penalty: float = float(os.getenv("REPEAT_PENALTY", 1.1))
    verbose: bool = os.getenv("VERBOSE", "False").lower() == "true"
    model_directory: str = os.getenv("MODEL_DIRECTORY", "models/llm/models")
    resume_download: bool = True
    # GPU memory settings
    main_gpu: int = int(os.getenv("MAIN_GPU", 0))
    tensor_split: Optional[List[float]] = None
    rope_scaling_type: Optional[str] = None
    rope_freq_base: float = float(os.getenv("ROPE_FREQ_BASE", 0.0))
    rope_freq_scale: float = float(os.getenv("ROPE_FREQ_SCALE", 0.0))


class LlamaModel:
    """Manages loading and interaction with the llama-cpp-python model."""

    def __init__(self, config: ModelConfig):
        """
        Initialize the llama-cpp-python model with the given configuration.

        Args:
            config (ModelConfig): Configuration for the model.

        Raises:
            RuntimeError: If model loading fails.
        """
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

        # Check GPU availability and CUDA support
        if torch.cuda.is_available():
            logger.info(f"CUDA available with {torch.cuda.device_count()} GPU(s)")
            logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA version: {torch.version.cuda}")
        else:
            logger.info("CUDA not available, using CPU")

        self.llm = self._load_model()

    def _load_model(self) -> Optional[Llama]:
        """
        Load the llama-cpp-python model from Hugging Face Hub.

        Returns:
            Optional[Llama]: Loaded llama-cpp-python model instance or None if loading fails.

        Raises:
            RuntimeError: If model downloading or initialization fails.
        """
        try:
            # Download model from Hugging Face Hub
            model_path = hf_hub_download(
                repo_id=self.config.model_id,
                filename=self.config.model_basename,
                resume_download=self.config.resume_download,
                cache_dir=self.config.model_directory,
            )
            logger.info(f"Model downloaded to: {model_path}")

            # Prepare model initialization parameters
            model_params = {
                "model_path": model_path,
                "n_ctx": self.config.context_window_size,
                "n_batch": self.config.n_batch,
                "n_threads": self.config.n_threads,
                "verbose": self.config.verbose,
            }

            # GPU-specific settings
            if self.device.type == "cuda" and torch.cuda.is_available():
                model_params.update({
                    "n_gpu_layers": self.config.n_gpu_layers,
                    "main_gpu": self.config.main_gpu,
                })

                if self.config.tensor_split:
                    model_params["tensor_split"] = self.config.tensor_split

                logger.info(f"Configuring GPU with {self.config.n_gpu_layers} layers")
                logger.info(f"Main GPU: {self.config.main_gpu}")
            else:
                # CPU-only mode
                model_params["n_gpu_layers"] = 0
                logger.info("Running in CPU-only mode")

            # Optional ROPE scaling parameters
            if self.config.rope_freq_base > 0:
                model_params["rope_freq_base"] = self.config.rope_freq_base
            if self.config.rope_freq_scale > 0:
                model_params["rope_freq_scale"] = self.config.rope_freq_scale

            # Initialize the model
            llm = Llama(**model_params)
            logger.info("Model loaded successfully")
            return llm

        except Exception as e:
            logger.error(f"Failed to load llama-cpp-python model: {str(e)}")
            raise RuntimeError(f"Model loading failed: {str(e)}")

    def generate(
            self,
            text: str,
            max_tokens: Optional[int] = None,
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            top_k: Optional[int] = None,
            repeat_penalty: Optional[float] = None,
            stop: Optional[List[str]] = None,
            stream: bool = False
    ) -> str:
        """
        Generate a response for a given prompt using the llama-cpp-python model.

        Args:
            text (str): Input prompt for the model.
            max_tokens (Optional[int]): Maximum number of tokens to generate.
            temperature (Optional[float]): Sampling temperature.
            top_p (Optional[float]): Top-p sampling parameter.
            top_k (Optional[int]): Top-k sampling parameter.
            repeat_penalty (Optional[float]): Repetition penalty.
            stop (Optional[List[str]]): Stop sequences.
            stream (bool): Whether to stream the response.

        Returns:
            str: Generated response text.

        Raises:
            ValueError: If the prompt is empty or invalid.
            RuntimeError: If generation fails.
        """
        if not isinstance(text, str) or not text.strip():
            logger.error(f"Invalid text: must be a non-empty string. Got: {text}")
            raise ValueError("Text must be a non-empty string")

        try:
            # Use provided parameters or fall back to config defaults
            generation_params = {
                "prompt": text,
                "max_tokens": max_tokens or self.config.max_new_tokens,
                "temperature": temperature if temperature is not None else self.config.temperature,
                "top_p": top_p if top_p is not None else self.config.top_p,
                "top_k": top_k if top_k is not None else self.config.top_k,
                "repeat_penalty": repeat_penalty if repeat_penalty is not None else self.config.repeat_penalty,
                "stop": stop or ["<|eot_id|>", "<|end_of_text|>"],
                "echo": False,  # Don't include the prompt in output
            }

            logger.debug(f"Generation parameters: {generation_params}")

            if stream:
                # Streaming generation
                response_text = ""
                for output in self.llm(**generation_params, stream=True):
                    token = output["choices"][0]["text"]
                    response_text += token
                    yield token
                return response_text
            else:
                # Non-streaming generation
                response = self.llm(**generation_params)
                generated_text = response["choices"][0]["text"].strip()
                logger.info("Successfully generated response")
                return generated_text

        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise RuntimeError(f"Generation failed: {str(e)}")

    def generate_with_chat_template(
            self,
            messages: List[Dict[str, str]],
            **kwargs
    ) -> str:
        """
        Generate response using chat message format.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'.
            **kwargs: Additional generation parameters.

        Returns:
            str: Generated response.
        """
        try:
            # Create chat completion
            response = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.config.max_new_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                top_p=kwargs.get("top_p", self.config.top_p),
                top_k=kwargs.get("top_k", self.config.top_k),
                repeat_penalty=kwargs.get("repeat_penalty", self.config.repeat_penalty),
                stop=kwargs.get("stop", ["<|eot_id|>"]),
            )

            return response["choices"][0]["message"]["content"].strip()

        except Exception as e:
            logger.error(f"Chat completion failed: {str(e)}")
            raise RuntimeError(f"Chat completion failed: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.llm:
            return {}

        try:
            return {
                "model_path": self.llm.model_path if hasattr(self.llm, 'model_path') else "Unknown",
                "context_size": self.config.context_window_size,
                "gpu_layers": self.config.n_gpu_layers,
                "device": str(self.device),
                "cuda_available": torch.cuda.is_available(),
                "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            }
        except Exception as e:
            logger.error(f"Failed to get model info: {str(e)}")
            return {"error": str(e)}


def get_chat_prompt(user_input: str) -> str:
    """
    Create a formatted chat prompt with system instructions and user input.

    Args:
        user_input (str): User's input text.

    Returns:
        str: Formatted prompt string.

    Raises:
        ValueError: If user_input is empty or invalid.
    """
    if not isinstance(user_input, str) or not user_input.strip():
        logger.error("Invalid user input: must be a non-empty string")
        raise ValueError("User input must be a non-empty string")

    today_date = datetime.today().strftime("%d %B %Y")
    prompt = (
        "<|start_header_id|>system<|end_header_id|>\n\n"
        f"Cutting Knowledge Date: December 2023\n"
        f"Today Date: {today_date}\n\n"
        "You are an assistant. You always provide correct information.\n"
        "<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n\n{user_input}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    logger.debug("Generated chat prompt")
    return prompt


def get_chat_messages(user_input: str) -> List[Dict[str, str]]:
    """
    Create chat messages format for the model.

    Args:
        user_input (str): User's input text.

    Returns:
        List[Dict[str, str]]: List of message dictionaries.
    """
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("User input must be a non-empty string")

    today_date = datetime.today().strftime("%d %B %Y")

    return [
        {
            "role": "system",
            "content": (
                f"Cutting Knowledge Date: December 2023\n"
                f"Today Date: {today_date}\n\n"
                "You are an assistant. You always provide correct information."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    