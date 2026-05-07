import os
import json
from groq import Groq
from typing import Dict, Any, Optional

class AIService:
    """
    AI Service using Groq API for intelligent data extraction.
    IMPORTANT: Only extract structured data, don't use for routing.
    """
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def extract_order_data(self, message: str) -> Dict[str, Any]:
        """
        Extract manufacturing order data from natural language.
        
        Returns:
        {
            "success": True/False,
            "part_name": "name or null",
            "material": "material or null",
            "quantity": int or null,
            "deadline": "deadline or null"
        }
        """
        
        prompt = f"""Extract manufacturing order data from this message.
Return ONLY valid JSON, no markdown, no explanation:

Message: "{message}"

Return exactly this structure:
{{
    "part_name": "extracted part name or null",
    "material": "extracted material or null",
    "quantity": extracted quantity as integer or null,
    "deadline": "extracted deadline or null",
    "success": true
}}

If insufficient data for an order, set success to false."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                # Try to extract JSON from response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end > start:
                    data = json.loads(response_text[start:end])
                    return data
                return {"success": False, "error": "Could not parse Groq response"}
        
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_quality_type(self, message: str) -> str:
        """
        Extract quality check type from message.
        Returns: THERMAL, TENSILE, DIMENSION, PRESSURE, INSPECTION, OTHER
        """
        
        prompt = f"""What quality check type is mentioned? Return ONLY one word:

Message: "{message}"

Options: THERMAL, TENSILE, DIMENSION, PRESSURE, INSPECTION, VERIFICATION, OTHER

Reply with EXACTLY one word from the options."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip().upper()
        except:
            return "INSPECTION"
    
    def generate_conversational_response(self, message: str, context: str = "") -> str:
        """
        Generate a conversational response for UI display.
        Light-weight for conversational feel.
        """
        
        prompt = f"""You are a manufacturing operations assistant. 
Respond naturally and concisely (1-2 sentences max).

{context}

User: {message}

Response:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except:
            return "Processing your request..."
