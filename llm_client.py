"""
LLM Client for generating status messages using multiple providers
"""

import requests
import random
import logging
from typing import Optional
from config import (
    LLM_PROVIDER, LOCAL_MODEL_NAME, 
    OLLAMA_BASE_URL, OLLAMA_MODEL, STATUS_TEMPLATES, 
    PROMPT_TEMPLATE, UNPROFESSIONAL_WORDS
)

# Try to import optional dependencies
try:
    from config import OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = None

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.session = requests.Session()
        
        # Initialize provider-specific clients
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "local":
            self._init_local()
        elif self.provider == "ollama":
            self._init_ollama()
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}, using templates only")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if not OPENAI_API_KEY:
            logger.warning("OpenAI API key not found, will use templates only")
            return
        try:
            import openai
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
            logger.info("✅ OpenAI client initialized")
        except ImportError:
            logger.warning("OpenAI library not installed, will use templates only")
            self.openai_client = None
    
    def _init_local(self):
        """Initialize local HuggingFace model"""
        try:
            from transformers import pipeline
            self.local_model = pipeline(
                "text-generation",
                model=LOCAL_MODEL_NAME,
                device="cpu"  # Use CPU for compatibility
            )
            logger.info(f"✅ Local model '{LOCAL_MODEL_NAME}' initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize local model: {e}, will use templates only")
            self.local_model = None
    
    def _init_ollama(self):
        """Initialize Ollama client"""
        self.ollama_url = OLLAMA_BASE_URL
        self.ollama_model = OLLAMA_MODEL
        logger.info(f"✅ Ollama client initialized for {self.ollama_model}")
    
    def generate_status(self, status_type: str) -> str:
        """
        Generate a funny status message for the given status type.
        Falls back to template messages if LLM is unavailable or slow.
        """
        # For templates provider, use templates directly
        if self.provider == "templates":
            return self._get_template_status(status_type)
        
        try:
            # Try to generate with LLM first (with timeout)
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("LLM generation timed out")
            
            # Set a 10-second timeout for LLM generation
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)
            
            try:
                llm_response = self._generate_with_llm(status_type)
                signal.alarm(0)  # Cancel the alarm
                
                if llm_response and self._is_appropriate(llm_response):
                    return llm_response
            except (TimeoutError, Exception) as e:
                signal.alarm(0)  # Cancel the alarm
                logger.warning(f"LLM generation failed or timed out: {e}")
                
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")
        
        # Fallback to template messages
        return self._get_template_status(status_type)
    
    def _generate_with_llm(self, status_type: str) -> Optional[str]:
        """Generate status message using the configured LLM provider"""
        if self.provider == "openai":
            return self._generate_with_openai(status_type)
        elif self.provider == "local":
            return self._generate_with_local(status_type)
        elif self.provider == "ollama":
            return self._generate_with_ollama(status_type)
        elif self.provider == "templates":
            return None  # Will fall back to templates
        else:
            return None
    
    def _generate_with_openai(self, status_type: str) -> Optional[str]:
        """Generate status message using OpenAI"""
        if not hasattr(self, 'openai_client') or self.openai_client is None:
            return None
            
        try:
            prompt = PROMPT_TEMPLATE.format(
                status_type=status_type,
                context=f"User wants a {status_type} status message",
                avoid_words=", ".join(UNPROFESSIONAL_WORDS[:5])
            )
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional but funny status message generator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.8
            )
            
            generated_text = response.choices[0].message.content.strip()
            return self._clean_response(generated_text)
            
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {e}")
            return None
    
    def _generate_with_local(self, status_type: str) -> Optional[str]:
        """Generate status message using local HuggingFace model"""
        if not hasattr(self, 'local_model') or self.local_model is None:
            return None
            
        try:
            prompt = f"Generate a funny {status_type} status message: "
            
            response = self.local_model(
                prompt,
                max_length=len(prompt.split()) + 10,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.local_model.tokenizer.eos_token_id
            )
            
            generated_text = response[0]['generated_text']
            # Extract only the new part
            new_text = generated_text[len(prompt):].strip()
            return self._clean_response(new_text)
            
        except Exception as e:
            logger.error(f"Error generating with local model: {e}")
            return None
    
    def _generate_with_ollama(self, status_type: str) -> Optional[str]:
        """Generate status message using Ollama LLM"""
        try:
            # Simplified prompt for faster generation
            prompt = f"Generate a funny {status_type} status message (max 50 chars): "
            
            logger.info(f"Attempting to generate with Ollama model: {self.ollama_model}")
            
            response = self.session.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.8,
                        "num_predict": 20,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=15
            )
            
            logger.info(f"Ollama response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                logger.info(f"Ollama generated: {generated_text}")
                return self._clean_response(generated_text)
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            logger.error(f"Error generating with Ollama: {e}")
            return None
    
    def _clean_response(self, text: str) -> str:
        """Clean and format the generated response"""
        if not text:
            return ""
        
        # Remove quotes if present
        text = text.strip('"\'')
        # Take only the first line
        text = text.split('\n')[0]
        # Limit length
        if len(text) > 50:
            text = text[:47] + "..."
        
        return text.strip()
    
    def _get_template_status(self, status_type: str) -> str:
        """Get a random template status message"""
        templates = STATUS_TEMPLATES.get(status_type)
        if not templates:
            return "No template found for this status type"
        return random.choice(templates)
    
    def _is_appropriate(self, text: str) -> bool:
        """Check if the generated text is appropriate"""
        text_lower = text.lower()
        
        # Check for unprofessional words
        for word in UNPROFESSIONAL_WORDS:
            if word.lower() in text_lower:
                return False
        
        # Check for empty or very short responses
        if len(text.strip()) < 3:
            return False
        
        return True
    
    def test_connection(self) -> bool:
        """Test if the configured LLM provider is accessible"""
        if self.provider == "openai":
            return self._test_openai_connection()
        elif self.provider == "local":
            return self._test_local_connection()
        elif self.provider == "ollama":
            return self._test_ollama_connection()
        else:
            return False
    
    def _test_openai_connection(self) -> bool:
        """Test OpenAI connection"""
        if not hasattr(self, 'openai_client') or self.openai_client is None:
            return False
        try:
            # Simple test call
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
    
    def _test_local_connection(self) -> bool:
        """Test local model connection"""
        return hasattr(self, 'local_model') and self.local_model is not None
    
    def _test_ollama_connection(self) -> bool:
        """Test if Ollama is running and accessible"""
        try:
            response = self.session.get(f"{self.ollama_url}/api/tags", timeout=20)
            if response.status_code == 200:
                models = response.json().get("models", [])
                logger.info(f"✅ Ollama connection successful. Available models: {[m.get('name', 'unknown') for m in models]}")
                
                # Check if our model is available
                model_names = [m.get('name', '') for m in models]
                if self.ollama_model in model_names:
                    logger.info(f"✅ Model {self.ollama_model} is available")
                    return True
                else:
                    logger.warning(f"⚠️ Model {self.ollama_model} not found. Available: {model_names}")
                    return False
            else:
                logger.warning(f"Ollama returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Ollama connection test failed: {e}")
            return False 