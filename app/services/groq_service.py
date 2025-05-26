import os
from typing import Dict, Any, Optional
from .api_manager import APIManager

class GroqService:
    def __init__(self, api_key: Optional[str] = None, api_manager: Optional[APIManager] = None):
        """
        Initialize the Groq service.
        
        Args:
            api_key (str, optional): Groq API key. If not provided, will look for GROQ_API_KEY environment variable.
            api_manager (APIManager, optional): API manager for making requests. If not provided, will use direct API key.
        """
        self.api_manager = api_manager
        if not api_manager:
            self.api_key = api_key or os.getenv('GROQ_API_KEY')
            if not self.api_key:
                raise ValueError("Groq API key is required when not using an API manager. Either pass it to the constructor or set GROQ_API_KEY environment variable.")

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Groq's API.
        
        Args:
            prompt (str): The prompt to generate text from
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            str: The generated text
        """
        if self.api_manager:
            # Use the API manager to make the request
            response = self.api_manager.post('v1/chat/completions', {
                'prompt': prompt,
                **kwargs
            })
            return response['choices'][0]['text']
        else:
            # TODO: Implement direct API call using self.api_key
            raise NotImplementedError("Direct API integration not yet implemented") 