from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, model: str, temperature: float = 0.1, max_tokens: int = 1000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = self._load_api_key()
    
    @abstractmethod
    def _load_api_key(self) -> str:
        """Load API key from environment variables"""
        pass
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider"""
    
    def _load_api_key(self) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        return api_key
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("openai package not installed. Please install it with 'pip install openai'")
        
        client = AsyncOpenAI(api_key=self.api_key)
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_provider_name(self) -> str:
        return "openai"


class QwenProvider(LLMProvider):
    """Qwen LLM provider"""
    
    def _load_api_key(self) -> str:
        api_key = os.getenv("QWEN_API_KEY")
        if not api_key:
            raise ValueError("QWEN_API_KEY environment variable not set")
        return api_key
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("openai package not installed. Please install it with 'pip install openai'")
        
        # Qwen uses OpenAI-compatible API
        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_provider_name(self) -> str:
        return "qwen"


class DeepSeekProvider(LLMProvider):
    """DeepSeek LLM provider"""
    
    def _load_api_key(self) -> str:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        return api_key
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("openai package not installed. Please install it with 'pip install openai'")
        
        # DeepSeek uses OpenAI-compatible API
        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_provider_name(self) -> str:
        return "deepseek"
