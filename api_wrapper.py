import requests
import json
from hashlib import sha256

class APIWrapper:
    def __init__(self, base_url="http://localhost:5000/v1"):
        self.base_url = base_url
        self.cache = {}

    def _cache_key(self, messages, max_tokens, temperature):
        #Encodes and hash the parameters to create a unique cache key
        key_data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        return sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
    
    def generate_chat(self, messages, max_tokens=64, temperature=0.7):
        try:
            # Check cache first
            cache_key = self._cache_key(messages, max_tokens, temperature)
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            payload = {
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }

            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=60)

            response.raise_for_status()
            # Store in cache
            self.cache[cache_key] = response.json()
            return response.json()
        
        except requests.RequestException as e:
            print(f"Error during API request: {e}")
            return None