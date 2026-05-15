import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class AnalysisAgent:
    """
    Agent 2: LLM से analysis करवाता है + पिछले feedback से सीखता है
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.feedback_history = self.load_feedback()
        self.model = "gpt-4o-mini"  # सस्ता और तेज़
        
    def load_feedback(self) -> list:
        """पिछले feedback लोड करो (Learning का मुख्य तंत्र)"""
        feedback_file = "data/feedback_log.json"
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_feedback(self, feedback: dict):
        """नया feedback सेव करो"""
        self.feedback_history.append(feedback)
        with open("data/feedback_log.json", 'w') as f:
            json.dump(self.feedback_history[-100:], f)  # Last 100 feedbacks only
    
    def analyze(self, excel_summary: dict, changes: dict = None) -> str:
        """
        Excel data का analysis करो - WITH LEARNING FROM PAST FEEDBACK
        """
        
        # Learning Prompt: पिछली गलतियों से सीखो
        learning_context = ""
        if self.feedback_history:
            recent_feedback = self.feedback_history[-5:]  # पिछले 5 feedback
            learning_context = f"""
            📚 LEARNING FROM PAST FEEDBACK:
            Based on previous corrections, you should improve on:
            {json.dumps(recent_feedback, indent=2)}
            
            Make sure you don't repeat the same mistakes. If feedback said "percentage was wrong", 
            double-check your percentage calculations this time.
            """
        
        prompt = f"""
        You are an expert Data Analyst AI Agent.
        
        {learning_context}
        
        Here is today's Excel report summary:
        {json.dumps(excel_summary, indent=2)}
        
        Changes from yesterday:
        {json.dumps(changes, indent=2)}
        
        Please provide a professional analysis with:
        1. EXECUTIVE SUMMARY (2-3 lines - what's the main story?)
        2. KEY METRICS (top 5 most important numbers)
        3. WHAT CHANGED (compared to yesterday - include percentages)
        4. INSIGHTS (2-3 actionable insights)
        5. ANOMALIES (anything unusual - if nothing, say "None detected")
        6. CONFIDENCE SCORE (0-100% - how confident are you in this analysis?)
        
        Format your response as clean markdown with bullet points.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # कम temperature = ज्यादा consistent
        )
        
        analysis = response.choices[0].message.content
        
        # Log this analysis for future learning
        self.log_analysis(analysis, excel_summary)
        
        return analysis
    
    def log_analysis(self, analysis: str, summary: dict):
        """Analysis को log करो ताकि future learning हो सके"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "data_summary": summary,
            "analysis": analysis[:500]  # Truncate for storage
        }
        
        # Store in vector DB for semantic search (next version)
        with open("logs/analysis_history.json", 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
