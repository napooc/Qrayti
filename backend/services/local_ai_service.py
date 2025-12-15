"""Local AI service for quiz and summary generation using local models."""
import json
import logging
import re
from typing import List, Dict, Optional

# Ensure numpy is available before importing torch/transformers
try:
    import numpy
    logging.info(f"✅ numpy version: {numpy.__version__}")
except ImportError:
    logging.error("❌ numpy is not installed. Run: pip install numpy")
    raise ImportError("numpy is required. Install it with: pip install numpy")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import settings

logger = logging.getLogger(__name__)


class LocalAIService:
    """
    AI service that uses local models (Hugging Face) for generation.
    No API keys required - everything runs on your machine.
    """
    
    def __init__(self):
        """Initialize the local AI service."""
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.ready = False
        self.model_name = settings.local_model_name
        
        logger.info(f"Initializing Local AI Service with model: {self.model_name}")
    
    def load_model(self):
        """Load the model and tokenizer."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info("This may take a few minutes on first run (downloading model)...")
            
            # Determine device
            if settings.device == "auto":
                device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                device = settings.device
            
            logger.info(f"Using device: {device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Set padding token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
            }
            
            if settings.load_in_8bit and device == "cuda":
                model_kwargs["load_in_8bit"] = True
                model_kwargs["device_map"] = "auto"
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )
            
            if not settings.load_in_8bit:
                self.model = self.model.to(device)
            
            # Create text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if device == "cuda" else -1,
                max_length=settings.max_length,
                temperature=settings.temperature,
                do_sample=True,
                top_p=0.95,
            )
            
            self.ready = True
            logger.info(f"✅ Model loaded successfully: {self.model_name}")
            logger.info(f"   Device: {device}")
            logger.info(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB" if device == "cuda" else "   CPU Mode")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            logger.error(f"   Model: {self.model_name}")
            logger.error(f"   Try a smaller model like 'gpt2' or 'microsoft/phi-2'")
            self.ready = False
            raise
    
    def is_ready(self) -> bool:
        """Check if the model is loaded and ready."""
        return self.ready
    
    def generate_text(self, prompt: str, max_new_tokens: int = 400) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input prompt
            max_new_tokens: Maximum number of new tokens to generate
            
        Returns:
            Generated text
        """
        import time
        gen_start = time.time()
        
        if not self.ready:
            raise Exception("Model not loaded. Call load_model() first.")
        
        try:
            logger.info(f"Generating text, prompt length: {len(prompt)}, max_tokens: {max_new_tokens}")
            
            # Generate with optimized settings for speed
            outputs = self.pipeline(
                prompt,
                max_new_tokens=max_new_tokens,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
            )
            
            gen_time = time.time() - gen_start
            logger.info(f"Text generation took {gen_time:.2f} seconds")
            
            # Extract generated text (remove prompt)
            generated = outputs[0]['generated_text']
            result = generated[len(prompt):].strip()
            
            logger.info(f"Generated {len(result)} characters")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generating text: {str(e)}")
            logger.error(f"   Prompt length: {len(prompt)}")
            logger.error(f"   Max tokens: {max_new_tokens}")
            raise
    
    def extract_json_from_text(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from text that may contain markdown or other formatting.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Parsed JSON dict or None
        """
        # Try to find JSON in code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # Try to find JSON without code blocks
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        
        # Try parsing the whole text
        try:
            return json.loads(text)
        except:
            return None
    
    async def generate_quiz(self, content: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate quiz questions from content.
        
        Args:
            content: The text content to generate questions from
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with options and explanations
        """
        if not self.ready:
            raise Exception("Model not loaded")
        
        import time
        start_time = time.time()
        
        # ULTRA aggressive truncation - only 300 chars for MAXIMUM speed!
        max_content_length = 300
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
            logger.info(f"Content truncated to {max_content_length} chars for maximum speed")
        
        logger.info(f"Generating {num_questions} quiz questions from {len(content)} characters...")
        
        # Ultra-short prompt for maximum speed
        prompt = f"""Crée {num_questions} questions:

{content}

JSON:{{"questions":[{{"id":1,"question":"Q?","options":["A","B","C","D"],"correctIndex":0,"explanation":"E","explanationDarija":"D"}}]}}"""

        try:
            # Generate with model - minimal tokens for maximum speed
            logger.info("Starting AI generation...")
            generated = self.generate_text(prompt, max_new_tokens=400)
            
            elapsed = time.time() - start_time
            logger.info(f"AI generation completed in {elapsed:.2f} seconds")
            
            # Try to extract JSON
            result = self.extract_json_from_text(generated)
            
            if result and "questions" in result:
                questions = result["questions"]
                
                # Ensure IDs are set
                for i, q in enumerate(questions):
                    q["id"] = i + 1
                    # Ensure all required fields exist
                    if "explanationDarija" not in q:
                        q["explanationDarija"] = q.get("explanation", "")
                
                logger.info(f"✅ Generated {len(questions)} questions")
                return questions[:num_questions]
            else:
                # No fallback - retry with even shorter prompt
                logger.warning("Could not parse JSON from model output, retrying with shorter prompt")
                # Retry with minimal prompt
                retry_prompt = f"Crée {num_questions} questions sur: {content[:200]}\nJSON:"
                generated = self.generate_text(retry_prompt, max_new_tokens=300)
                result = self.extract_json_from_text(generated)
                if result and "questions" in result:
                    questions = result["questions"]
                    for i, q in enumerate(questions):
                        q["id"] = i + 1
                        if "explanationDarija" not in q:
                            q["explanationDarija"] = q.get("explanation", "")
                    logger.info(f"✅ Generated {len(questions)} questions (retry)")
                    return questions[:num_questions]
                else:
                    raise Exception("Failed to generate valid quiz after retry")
                
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    async def generate_summary(self, content: str) -> List[Dict]:
        """
        Generate a structured summary from content.
        
        Args:
            content: The text content to summarize
            
        Returns:
            List of summary sections with key terms and essential points
        """
        import time
        start_time = time.time()
        
        if not self.ready:
            raise Exception("Model not loaded")
        
        # ULTRA aggressive truncation - only 300 chars for MAXIMUM speed!
        max_content_length = 300
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
            logger.info(f"Content truncated to {max_content_length} chars for maximum speed")
        
        logger.info(f"Generating summary from {len(content)} characters...")
        
        # Ultra-short prompt for maximum speed
        prompt = f"""Résume:

{content}

JSON:{{"sections":[{{"title":"T","content":"C","keyTerms":[{{"term":"T","definition":"D","definitionDarija":"DD"}}],"essentialPoints":["P1"]}}]}}"""

        try:
            # Generate with model - minimal tokens for maximum speed
            logger.info("Starting AI generation...")
            generated = self.generate_text(prompt, max_new_tokens=300)
            
            elapsed = time.time() - start_time
            logger.info(f"AI generation completed in {elapsed:.2f} seconds")
            
            # Try to extract JSON
            result = self.extract_json_from_text(generated)
            
            if result and "sections" in result:
                sections = result["sections"]
                logger.info(f"✅ Generated {len(sections)} summary sections")
                return sections
            else:
                # No fallback - retry with even shorter prompt
                logger.warning("Could not parse JSON from model output, retrying with shorter prompt")
                # Retry with minimal prompt
                retry_prompt = f"Résume: {content[:200]}\nJSON:"
                generated = self.generate_text(retry_prompt, max_new_tokens=250)
                result = self.extract_json_from_text(generated)
                if result and "sections" in result:
                    sections = result["sections"]
                    logger.info(f"✅ Generated {len(sections)} summary sections (retry)")
                    return sections
                else:
                    raise Exception("Failed to generate valid summary after retry")
                
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def _get_fallback_quiz(self, num_questions: int) -> List[Dict]:
        """Return fallback quiz data."""
        return [
            {
                "id": 1,
                "question": "Qu'est-ce que le DOC (Dahir des Obligations et Contrats)?",
                "options": [
                    "Un document administratif",
                    "Le texte fondamental du droit civil marocain",
                    "Un contrat commercial",
                    "Une loi fiscale"
                ],
                "correctIndex": 1,
                "explanation": "Le DOC est le texte fondamental qui régit le droit civil au Maroc depuis 1913.",
                "explanationDarija": "DOC هو القانون الأساسي للقانون المدني المغربي من 1913"
            }
        ][:num_questions]
    
    def _get_fallback_summary(self) -> List[Dict]:
        """Return fallback summary data."""
        return [
            {
                "title": "Résumé du contenu",
                "content": "Le contenu traite des concepts juridiques importants pour les étudiants marocains.",
                "keyTerms": [
                    {
                        "term": "Concept clé",
                        "definition": "Définition en français",
                        "definitionDarija": "Ta3rif bel darija"
                    }
                ],
                "essentialPoints": [
                    "Point important du contenu",
                    "Deuxième point essentiel"
                ]
            }
        ]

