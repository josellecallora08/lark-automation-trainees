import os
from typing import Dict, Any, Optional
import requests

class APIManager:
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the API Manager.
        
        Args:
            base_url (str, optional): Base URL for API requests. If not provided, will look for API_BASE_URL environment variable.
        """
        self.base_url = base_url or os.getenv('API_BASE_URL')
        if not self.base_url:
            raise ValueError("API base URL is required. Either pass it to the constructor or set API_BASE_URL environment variable.")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint (str): API endpoint to call
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            Dict[str, Any]: API response
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint (str): API endpoint to call
            data (Dict[str, Any], optional): Request body
            
        Returns:
            Dict[str, Any]: API response
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json() 