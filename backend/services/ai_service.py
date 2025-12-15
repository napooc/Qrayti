"""AI service for quiz and summary generation."""
import json
import logging
from typing import List, Optional
from config import settings

logger = logging.getLogger(__name__)


class AIService:
    """
    AI service that handles quiz and summary generation.
    Supports multiple backends: OpenAI API, local models, etc.
    """
    
    def __init__(self):
        """Initialize the AI service based on configuration."""
        self.model_type = settings.model_type
        self.ready = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the appropriate model based on configuration."""
        try:
            if self.model_type == "openai":
                self._initialize_openai()
            elif self.model_type == "local":
                self._initialize_local_model()
            else:
                logger.warning(f"Unknown model type: {self.model_type}, defaulting to OpenAI")
                self._initialize_openai()
            
            self.ready = True
            logger.info(f"AI Service initialized with model type: {self.model_type}")
        
        except Exception as e:
            logger.error(f"Error initializing AI service: {str(e)}")
            self.ready = False
    
    def _initialize_openai(self):
        """Initialize OpenAI API client."""
        try:
            from openai import OpenAI
            
            if not settings.openai_api_key:
                logger.warning("OpenAI API key not found. Set OPENAI_API_KEY in .env file.")
                self.client = None
            else:
                self.client = OpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI client initialized successfully")
        
        except ImportError:
            logger.error("OpenAI package not installed. Run: pip install openai")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {str(e)}")
            self.client = None
    
    def _initialize_local_model(self):
        """Initialize local model (Hugging Face, etc.)."""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            model_name = settings.local_model_name
            logger.info(f"Loading local model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            
            logger.info(f"Local model {model_name} loaded successfully")
        
        except ImportError:
            logger.error("transformers or torch not installed. Run: pip install transformers torch")
            self.model = None
            self.tokenizer = None
        except Exception as e:
            logger.error(f"Error loading local model: {str(e)}")
            self.model = None
            self.tokenizer = None
    
    async def is_ready(self) -> bool:
        """Check if the AI service is ready."""
        return self.ready and (
            (self.model_type == "openai" and self.client is not None) or
            (self.model_type == "local" and self.model is not None)
        )
    
    async def generate_quiz(self, content: str, num_questions: int = 5) -> List[dict]:
        """
        Generate quiz questions from content.
        
        Args:
            content: The text content to generate questions from
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with options and explanations
        """
        if not await self.is_ready():
            raise Exception("AI service is not ready. Please check your configuration.")
        
        if self.model_type == "openai":
            return await self._generate_quiz_openai(content, num_questions)
        else:
            return await self._generate_quiz_local(content, num_questions)
    
    async def _generate_quiz_openai(self, content: str, num_questions: int) -> List[dict]:
        """Generate quiz using OpenAI API."""
        prompt = f"""Tu es un assistant éducatif pour des étudiants marocains. Génère {num_questions} questions à choix multiples basées sur le contenu suivant.

CONTENU:
{content[:4000]}

INSTRUCTIONS:
- Crée {num_questions} questions pertinentes et de difficulté progressive
- Chaque question doit avoir 4 options de réponse
- Fournis une explication en français
- Fournis une explication en darija marocaine (dialecte arabe marocain)
- Les explications en darija doivent utiliser l'alphabet latin (translittération)

Réponds UNIQUEMENT avec un JSON valide dans ce format exact:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question en français?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 1,
      "explanation": "Explication détaillée en français",
      "explanationDarija": "Explication en darija (translittération latine)"
    }}
  ]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # or gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "Tu es un assistant éducatif expert pour les étudiants marocains. Tu réponds toujours avec du JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            questions = result.get("questions", [])
            
            # Ensure questions have proper IDs
            for i, q in enumerate(questions):
                q["id"] = i + 1
            
            logger.info(f"Generated {len(questions)} questions using OpenAI")
            return questions
        
        except Exception as e:
            logger.error(f"Error generating quiz with OpenAI: {str(e)}")
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    async def _generate_quiz_local(self, content: str, num_questions: int) -> List[dict]:
        """Generate quiz using local model."""
        # This is a placeholder for local model implementation
        # You would implement this based on your local model choice
        logger.warning("Local model quiz generation not fully implemented yet")
        raise NotImplementedError("Local model quiz generation coming soon")
    
    async def generate_summary(self, content: str) -> List[dict]:
        """
        Generate a structured summary from content.
        
        Args:
            content: The text content to summarize
            
        Returns:
            List of summary sections with key terms and essential points
        """
        if not await self.is_ready():
            raise Exception("AI service is not ready. Please check your configuration.")
        
        if self.model_type == "openai":
            return await self._generate_summary_openai(content)
        else:
            return await self._generate_summary_local(content)
    
    async def _generate_summary_openai(self, content: str) -> List[dict]:
        """Generate summary using OpenAI API."""
        prompt = f"""Tu es un assistant éducatif pour des étudiants marocains. Crée un résumé structuré du contenu suivant.

CONTENU:
{content[:4000]}

INSTRUCTIONS:
- Divise le contenu en 3-5 sections logiques
- Pour chaque section:
  * Fournis un titre clair
  * Écris un résumé concis du contenu
  * Identifie 2-4 termes clés avec leurs définitions
  * Liste 2-4 points essentiels à retenir
- Les définitions doivent être en français ET en darija (translittération latine)

Réponds UNIQUEMENT avec un JSON valide dans ce format exact:
{{
  "sections": [
    {{
      "title": "Titre de la section",
      "content": "Résumé de la section en 2-3 phrases",
      "keyTerms": [
        {{
          "term": "Terme important",
          "definition": "Définition en français",
          "definitionDarija": "Définition en darija (translittération latine)"
        }}
      ],
      "essentialPoints": [
        "Point essentiel 1",
        "Point essentiel 2"
      ]
    }}
  ]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # or gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "Tu es un assistant éducatif expert pour les étudiants marocains. Tu réponds toujours avec du JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            sections = result.get("sections", [])
            
            logger.info(f"Generated {len(sections)} summary sections using OpenAI")
            return sections
        
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    async def _generate_summary_local(self, content: str) -> List[dict]:
        """Generate summary using local model."""
        # This is a placeholder for local model implementation
        logger.warning("Local model summary generation not fully implemented yet")
        raise NotImplementedError("Local model summary generation coming soon")

