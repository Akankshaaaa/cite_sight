from typing import Dict, List
from src.tools.search_tool import SearchTool
from src.tools.content_retriever import ContentRetriever
from src.tools.summarizer import Summarizer
import time
import json

class ResearchAgent:
    def __init__(self):
        self.search_tool = SearchTool()
        self.content_retriever = ContentRetriever()
        self.summarizer = Summarizer()
        self.research_log = []

    def log_step(self, step: str, details: Dict):
        """Log each step of the research process"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.research_log.append({
            "timestamp": timestamp,
            "step": step,
            "details": details
        })

    def break_down_question(self, question: str) -> List[str]:
        """
        Break down a complex question into sub-questions
        Currently using a simple approach - in a production environment,
        this would use an LLM to generate more sophisticated sub-questions
        """
        # For now, we'll just use the main question
        return [question]

    def research(self, question: str) -> Dict:
        """
        Conduct research on a given question
        
        Args:
            question (str): The research question
            
        Returns:
            Dict: Research results including summaries and citations
        """
        try:
            # Step 1: Break down the question
            sub_questions = self.break_down_question(question)
            self.log_step("question_breakdown", {"sub_questions": sub_questions})

            all_summaries = []
            all_sources = []

            # Step 2: Research each sub-question
            for sub_q in sub_questions:
                # Search for relevant content
                search_results = self.search_tool.search(sub_q)
                self.log_step("search", {
                    "sub_question": sub_q,
                    "num_results": len(search_results)
                })

                # Fetch and process content for each search result
                for result in search_results:
                    content = self.content_retriever.fetch_content(result["link"])
                    
                    if content:
                        # Generate summary
                        summary = self.summarizer.summarize(
                            content["content"],
                            context=sub_q
                        )
                        
                        if summary:
                            all_summaries.append(summary)
                            all_sources.append({
                                "title": content["title"],
                                "url": content["url"]
                            })

                        self.log_step("content_processing", {
                            "url": result["link"],
                            "success": bool(summary)
                        })

            # Step 3: Cross-validate information
            if len(all_summaries) > 1:
                cross_validation = self.summarizer.cross_validate(all_summaries)
            else:
                cross_validation = {"cross_validation": "Not enough sources for cross-validation"}

            # Step 4: Compile final report
            report = {
                "question": question,
                "summaries": all_summaries,
                "sources": all_sources,
                "cross_validation": cross_validation,
                "research_log": self.research_log
            }

            return report

        except Exception as e:
            error_report = {
                "error": str(e),
                "research_log": self.research_log
            }
            return error_report

    def get_research_log(self) -> List[Dict]:
        """Return the research log"""
        return self.research_log 