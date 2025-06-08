import requests
import json
from typing import Dict, List
from src.config.config import (
    OPENROUTER_API_KEY, 
    MODEL_NAME, 
    TEMPERATURE, 
    MAX_TOKENS,
    OPENROUTER_API_URL,
    SITE_URL,
    SITE_NAME
)

class Summarizer:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": SITE_URL,
            "X-Title": SITE_NAME,
        }

    def _parse_json_response(self, text: str) -> Dict:
        """Try to parse JSON from the response text, or create a structured response"""
        try:
            return json.loads(text)
        except:
            # If JSON parsing fails, create a structured format
            return {
                "summary": text,
                "key_points": [],
                "quotes": [],
                "confidence_level": "medium"
            }

    def summarize(self, content: str, context: str = "") -> Dict[str, str]:
        """
        Summarize content using OpenRouter's LLM
        
        Args:
            content (str): Content to summarize
            context (str): Additional context or specific instructions
            
        Returns:
            Dict[str, str]: Dictionary containing summary and key points
        """
        try:
            prompt = f"""
            Please analyze and summarize the following content. Provide your response in valid JSON format using this exact structure:
            {{
                "summary": "A concise summary of the content",
                "key_points": ["Key point 1", "Key point 2", ...],
                "quotes": ["Notable quote 1", "Notable quote 2", ...],
                "confidence_level": "high/medium/low"
            }}

            If provided, consider this context: {context}
            
            Content to analyze:
            {content}
            """
            
            response = requests.post(
                url=OPENROUTER_API_URL,
                headers=self.headers,
                data=json.dumps({
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                    "response_format": { "type": "json_object" }
                })
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract and parse the response text
            summary_text = response_data["choices"][0]["message"]["content"]
            parsed_summary = self._parse_json_response(summary_text)
            
            return {
                "summary": json.dumps(parsed_summary),
                "source_length": len(content)
            }
            
        except Exception as e:
            print(f"Error in summarization: {str(e)}")
            return {
                "summary": json.dumps({
                    "summary": "Error generating summary",
                    "key_points": [],
                    "quotes": [],
                    "confidence_level": "low"
                }),
                "source_length": len(content)
            }

    def cross_validate(self, summaries: List[Dict]) -> Dict:
        """
        Cross-validate information between multiple summaries
        
        Args:
            summaries (List[Dict]): List of summary dictionaries
            
        Returns:
            Dict: Analysis of agreements and disagreements
        """
        try:
            # Prepare the summaries for comparison
            parsed_summaries = []
            for s in summaries:
                try:
                    summary_data = json.loads(s['summary'])
                    parsed_summaries.append(summary_data)
                except:
                    continue
            
            summary_texts = "\n\n".join([
                f"Source {i+1}:\nSummary: {s.get('summary', '')}\nKey Points: {', '.join(s.get('key_points', []))}"
                for i, s in enumerate(parsed_summaries)
            ])
            
            prompt = f"""
            Please analyze these different source summaries and provide your response in valid JSON format using this exact structure:
            {{
                "agreements": ["Point of agreement 1", "Point of agreement 2", ...],
                "contradictions": ["Contradiction 1", "Contradiction 2", ...],
                "unique_points": ["Unique point 1", "Unique point 2", ...],
                "confidence": "high/medium/low"
            }}

            Sources to analyze:
            {summary_texts}
            """
            
            response = requests.post(
                url=OPENROUTER_API_URL,
                headers=self.headers,
                data=json.dumps({
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                    "response_format": { "type": "json_object" }
                })
            )
            
            response.raise_for_status()
            response_data = response.json()
            analysis_text = response_data["choices"][0]["message"]["content"]
            
            # Ensure the response is valid JSON
            try:
                json.loads(analysis_text)
                return {"cross_validation": analysis_text}
            except:
                return {
                    "cross_validation": json.dumps({
                        "agreements": [],
                        "contradictions": [],
                        "unique_points": [],
                        "confidence": "low"
                    })
                }
            
        except Exception as e:
            print(f"Error in cross-validation: {str(e)}")
            return {
                "cross_validation": json.dumps({
                    "agreements": [],
                    "contradictions": [],
                    "unique_points": [],
                    "confidence": "low"
                })
            } 