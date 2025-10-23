"""
Model management system for English Assistant
Handles loading, caching, and health checking of HuggingFace models
"""
import logging
import os
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import threading
from functools import lru_cache

import torch
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification,
    pipeline, Pipeline
)
from language_tool_python import LanguageTool

from config import settings
from utils.error_handler import ModelErrorHandler


class ModelManager:
    """Centralized model management for offline HuggingFace models"""
    
    def __init__(self):
        self.logger = logging.getLogger("model_manager")
        self.models: Dict[str, Any] = {}
        self.tokenizers: Dict[str, Any] = {}
        self.pipelines: Dict[str, Pipeline] = {}
        self.model_configs = self._get_model_configs()
        self.cache_dir = Path(settings.models_cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._lock = threading.Lock()
        
        # Initialize LanguageTool
        self.language_tool = None
        self._init_language_tool()
    
    def _get_model_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get configuration for all models"""
        return {
            # Translation models
            "nllb-200": {
                "model_name": "facebook/nllb-200-distilled-600M",
                "type": "translation",
                "task": "translation",
                "languages": ["es", "en"],
                "priority": 1
            },
            "opus-mt-es-en": {
                "model_name": "Helsinki-NLP/opus-mt-es-en",
                "type": "translation", 
                "task": "translation",
                "languages": ["es", "en"],
                "priority": 2
            },
            "m2m100": {
                "model_name": "facebook/m2m100_418M",
                "type": "translation",
                "task": "translation", 
                "languages": ["es", "en"],
                "priority": 3
            },
            
            # Grammar correction model
            "t5-grammar": {
                "model_name": "vennify/t5-base-grammar-correction",
                "type": "correction",
                "task": "text2text-generation",
                "priority": 1
            }
        }
    
    def _init_language_tool(self):
        """Initialize LanguageTool for grammar checking"""
        try:
            self.logger.info("Initializing LanguageTool...")
            self.language_tool = LanguageTool('en-US')
            self.logger.info("LanguageTool initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize LanguageTool: {e}")
            self.language_tool = None
    
    @lru_cache(maxsize=10)
    def load_model(self, model_key: str, force_reload: bool = False) -> Optional[Any]:
        """Load a model with caching and error handling"""
        if model_key not in self.model_configs:
            self.logger.error(f"Unknown model key: {model_key}")
            return None
        
        with self._lock:
            # Check if model is already loaded
            if model_key in self.models and not force_reload:
                self.logger.info(f"Using cached model: {model_key}")
                return self.models[model_key]
            
            config = self.model_configs[model_key]
            model_name = config["model_name"]
            
            try:
                self.logger.info(f"Loading model: {model_name}")
                start_time = time.time()
                
                # Set cache directory
                os.environ["HF_HOME"] = str(self.cache_dir)
                os.environ["TRANSFORMERS_CACHE"] = str(self.cache_dir)
                
                # Load tokenizer
                tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    cache_dir=self.cache_dir,
                    local_files_only=False  # Allow download if not cached
                )
                
                # Load model based on type
                if config["type"] in ["translation", "correction"]:
                    model = AutoModelForSeq2SeqLM.from_pretrained(
                        model_name,
                        cache_dir=self.cache_dir,
                        local_files_only=False,
                        torch_dtype=torch.float32  # CPU-friendly
                    )
                else:
                    model = AutoModelForSequenceClassification.from_pretrained(
                        model_name,
                        cache_dir=self.cache_dir,
                        local_files_only=False,
                        torch_dtype=torch.float32
                    )
                
                # Store in cache
                self.models[model_key] = model
                self.tokenizers[model_key] = tokenizer
                
                load_time = time.time() - start_time
                self.logger.info(f"Model {model_key} loaded successfully in {load_time:.2f}s")
                
                return model
                
            except Exception as e:
                self.logger.error(f"Failed to load model {model_key}: {e}")
                return None
    
    def get_pipeline(self, model_key: str, task: Optional[str] = None) -> Optional[Pipeline]:
        """Get or create a pipeline for the specified model"""
        if model_key in self.pipelines:
            return self.pipelines[model_key]
        
        model = self.load_model(model_key)
        if model is None:
            return None
        
        tokenizer = self.tokenizers.get(model_key)
        if tokenizer is None:
            self.logger.error(f"No tokenizer found for model: {model_key}")
            return None
        
        config = self.model_configs[model_key]
        pipeline_task = task or config.get("task", "text2text-generation")
        
        try:
            # Create pipeline without return_full_text for translation models
            if config["type"] == "translation":
                pipe = pipeline(
                    pipeline_task,
                    model=model,
                    tokenizer=tokenizer,
                    device=-1  # CPU only
                )
            else:
                pipe = pipeline(
                    pipeline_task,
                    model=model,
                    tokenizer=tokenizer,
                    device=-1,  # CPU only
                    return_full_text=False
                )
            
            
            self.pipelines[model_key] = pipe
            self.logger.info(f"Pipeline created for {model_key}")
            return pipe
            
        except Exception as e:
            self.logger.error(f"Failed to create pipeline for {model_key}: {e}")
            return None
    
    def get_translation_models(self) -> List[str]:
        """Get list of available translation models"""
        return [key for key, config in self.model_configs.items() 
                if config["type"] == "translation"]
    
    def get_correction_models(self) -> List[str]:
        """Get list of available correction models"""
        return [key for key, config in self.model_configs.items() 
                if config["type"] == "correction"]
    
    def health_check(self, model_key: str) -> Dict[str, Any]:
        """Perform health check on a model"""
        if model_key not in self.model_configs:
            return {"status": "error", "message": "Unknown model"}
        
        try:
            model = self.load_model(model_key)
            if model is None:
                return {"status": "error", "message": "Failed to load model"}
            
            # Simple inference test
            pipeline = self.get_pipeline(model_key)
            if pipeline is None:
                return {"status": "error", "message": "Failed to create pipeline"}
            
            # Test with simple input
            test_input = "Hello world"
            start_time = time.time()
            
            try:
                result = pipeline(test_input, max_length=50, num_return_sequences=1)
                inference_time = time.time() - start_time
                
                return {
                    "status": "healthy",
                    "model_key": model_key,
                    "inference_time": round(inference_time, 3),
                    "test_successful": True
                }
            except Exception as e:
                return {
                    "status": "error", 
                    "message": f"Inference test failed: {str(e)}"
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_language_tool(self) -> Optional[LanguageTool]:
        """Get LanguageTool instance"""
        return self.language_tool
    
    def preload_models(self, model_keys: Optional[List[str]] = None):
        """Preload specified models or all models"""
        if model_keys is None:
            model_keys = list(self.model_configs.keys())
        
        self.logger.info(f"Preloading models: {model_keys}")
        
        for model_key in model_keys:
            try:
                self.load_model(model_key)
                self.get_pipeline(model_key)
            except Exception as e:
                self.logger.error(f"Failed to preload model {model_key}: {e}")
    
    def clear_cache(self, model_key: Optional[str] = None):
        """Clear model cache"""
        with self._lock:
            if model_key:
                # Clear specific model
                self.models.pop(model_key, None)
                self.tokenizers.pop(model_key, None)
                self.pipelines.pop(model_key, None)
                self.logger.info(f"Cleared cache for model: {model_key}")
            else:
                # Clear all models
                self.models.clear()
                self.tokenizers.clear()
                self.pipelines.clear()
                self.logger.info("Cleared all model caches")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about all configured models"""
        info = {
            "total_models": len(self.model_configs),
            "loaded_models": len(self.models),
            "cache_directory": str(self.cache_dir),
            "models": {}
        }
        
        for key, config in self.model_configs.items():
            info["models"][key] = {
                "name": config["model_name"],
                "type": config["type"],
                "task": config["task"],
                "loaded": key in self.models,
                "has_pipeline": key in self.pipelines
            }
        
        return info
    
    def shutdown(self):
        """Cleanup resources"""
        self.logger.info("Shutting down ModelManager...")
        
        # Clear all caches
        self.clear_cache()
        
        # Close LanguageTool
        if self.language_tool:
            try:
                self.language_tool.close()
            except Exception as e:
                self.logger.error(f"Error closing LanguageTool: {e}")
        
        self.logger.info("ModelManager shutdown complete")


# Global model manager instance
model_manager = ModelManager()


def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    return model_manager