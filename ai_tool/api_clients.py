"""
API Clients for Multiple AI Providers
Supports OpenAI, Anthropic, Google Gemini, Cohere, and Hugging Face APIs
"""

import requests
import json
from typing import Dict, Any, Optional, Iterator, Union, List
from abc import ABC, abstractmethod

from .config import ConfigManager
from .utils import handle_error


class BaseAIClient(ABC):
    """Base class for all AI API clients."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from the AI API."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        pass


class OpenAIClient(BaseAIClient):
    """OpenAI API client."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
        self.default_model = "gpt-3.5-turbo"
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from OpenAI API."""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens')
        stream = kwargs.get('stream', False)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'stream': stream
        }
        
        if max_tokens:
            data['max_tokens'] = max_tokens
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                result = response.json()
                return result['choices'][0]['message']['content']
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def _handle_stream_response(self, response) -> Iterator[str]:
        """Handle streaming response from OpenAI."""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        json_data = json.loads(data)
                        if 'choices' in json_data and json_data['choices']:
                            delta = json_data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue
    
    def get_available_models(self) -> List[str]:
        """Get available OpenAI models."""
        return [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]


class AnthropicClient(BaseAIClient):
    """Anthropic Claude API client."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.anthropic.com/v1"
        self.default_model = "claude-3-sonnet-20240229"
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from Anthropic API."""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 1000)
        stream = kwargs.get('stream', False)
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'stream': stream
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                result = response.json()
                return result['content'][0]['text']
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API error: {e}")
    
    def _handle_stream_response(self, response) -> Iterator[str]:
        """Handle streaming response from Anthropic."""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # Remove 'data: ' prefix
                    if data == '[DONE]':
                        break
                    try:
                        json_data = json.loads(data)
                        if json_data.get('type') == 'content_block_delta':
                            delta = json_data.get('delta', {})
                            if 'text' in delta:
                                yield delta['text']
                    except json.JSONDecodeError:
                        continue
    
    def get_available_models(self) -> List[str]:
        """Get available Anthropic models."""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0"
        ]


class GeminiClient(BaseAIClient):
    """Google Gemini API client."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.default_model = "gemini-pro"
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from Gemini API."""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        stream = kwargs.get('stream', False)
        
        # Convert messages format for Gemini
        gemini_messages = self._convert_messages_format(messages)
        
        params = {'key': self.api_key}
        headers = {'Content-Type': 'application/json'}
        
        data = {
            'contents': gemini_messages,
            'generationConfig': {
                'temperature': temperature
            }
        }
        
        endpoint = "streamGenerateContent" if stream else "generateContent"
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}:{endpoint}",
                params=params,
                headers=headers,
                json=data,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini API error: {e}")
    
    def _convert_messages_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Convert messages format for Gemini API."""
        gemini_messages = []
        for msg in messages:
            role = "user" if msg['role'] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg['content']}]
            })
        return gemini_messages
    
    def _handle_stream_response(self, response) -> Iterator[str]:
        """Handle streaming response from Gemini."""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    if 'candidates' in json_data and json_data['candidates']:
                        candidate = json_data['candidates'][0]
                        if 'content' in candidate:
                            parts = candidate['content'].get('parts', [])
                            for part in parts:
                                if 'text' in part:
                                    yield part['text']
                except json.JSONDecodeError:
                    continue
    
    def get_available_models(self) -> List[str]:
        """Get available Gemini models."""
        return [
            "gemini-pro",
            "gemini-pro-vision"
        ]


class CohereClient(BaseAIClient):
    """Cohere API client."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.cohere.ai/v1"
        self.default_model = "command"
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from Cohere API."""
        model = kwargs.get('model', self.default_model)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 1000)
        stream = kwargs.get('stream', False)
        
        # Convert messages to single prompt for Cohere
        prompt = self._convert_messages_to_prompt(messages)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': stream
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers=headers,
                json=data,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                result = response.json()
                return result['generations'][0]['text']
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cohere API error: {e}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to single prompt for Cohere."""
        prompt = ""
        for msg in messages:
            role = msg['role'].capitalize()
            content = msg['content']
            prompt += f"{role}: {content}\n"
        prompt += "Assistant:"
        return prompt
    
    def _handle_stream_response(self, response) -> Iterator[str]:
        """Handle streaming response from Cohere."""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    if 'text' in json_data:
                        yield json_data['text']
                except json.JSONDecodeError:
                    continue
    
    def get_available_models(self) -> List[str]:
        """Get available Cohere models."""
        return [
            "command",
            "command-light",
            "command-nightly"
        ]


class HuggingFaceClient(BaseAIClient):
    """Hugging Face Inference API client."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api-inference.huggingface.co/models"
        self.default_model = "microsoft/DialoGPT-medium"
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from Hugging Face API."""
        model = kwargs.get('model', self.default_model)
        
        # Convert messages to input text
        input_text = self._convert_messages_to_text(messages)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {'inputs': input_text}
        
        try:
            response = requests.post(
                f"{self.base_url}/{model}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get('generated_text', '')
            return str(result)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Hugging Face API error: {e}")
    
    def _convert_messages_to_text(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to text for Hugging Face."""
        return messages[-1]['content']  # Use last message as input
    
    def get_available_models(self) -> List[str]:
        """Get available Hugging Face models."""
        return [
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-large",
            "facebook/blenderbot-400M-distill",
            "gpt2"
        ]


class AIClientManager:
    """Manager for all AI API clients."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all available AI clients."""
        client_configs = {
            'openai': ('openai_api_key', OpenAIClient),
            'anthropic': ('anthropic_api_key', AnthropicClient),
            'gemini': ('gemini_api_key', GeminiClient),
            'cohere': ('cohere_api_key', CohereClient),
            'huggingface': ('huggingface_api_key', HuggingFaceClient),
        }
        
        for provider, (key_name, client_class) in client_configs.items():
            api_key = self.config_manager.get(key_name)
            if api_key:
                try:
                    self.clients[provider] = client_class(api_key)
                except Exception as e:
                    print(f"Warning: Failed to initialize {provider} client: {e}")
    
    def get_response(self, provider: str, messages: List[Dict[str, str]], **kwargs) -> Union[str, Iterator[str]]:
        """Get response from specified AI provider."""
        if provider not in self.clients:
            available_providers = list(self.clients.keys())
            if not available_providers:
                raise Exception("No AI providers configured. Please set API keys using --config-set")
            raise Exception(f"Provider '{provider}' not available. Available providers: {available_providers}")
        
        return self.clients[provider].get_response(messages, **kwargs)
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for specified provider."""
        if provider not in self.clients:
            raise Exception(f"Provider '{provider}' not available")
        
        return self.clients[provider].get_available_models()
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers."""
        return list(self.clients.keys())