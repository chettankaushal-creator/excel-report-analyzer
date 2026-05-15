import json
import os
from datetime import datetime

class FeedbackHandler:
    """
    यह है Agent का LEARNING MECHANISM
    Users के feedback को process करता है और model को improve करता है
    """
    
    def __init__(self):
        self.feedback_file = "data/feedback_log.json"
        self.correction_file = "data/corrections.json"
        
    def process_user_feedback(self, user_email_body: str):
        """
        User के email reply से feedback निकालो
        Example: "The percentage was wrong. Sales actually increased by 15%, not 10%"
        """
        
        # TODO: Use LLM to extract structured feedback from email
        # For now, manual structure
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "raw_feedback": user_email_body,
            "processed": False
        }
        
        with open(self.feedback_file, 'a') as f:
            json.dump(feedback, f)
            f.write('\n')
    
    def get_improvement_suggestions(self) -> list:
        """पिछले feedback से सीखो और improvement suggestions बनाओ"""
        if not os.path.exists(self.feedback_file):
            return []
        
        suggestions = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                fb = json.loads(line)
                if "wrong" in fb.get("raw_feedback", "").lower():
                    suggestions.append(fb["raw_feedback"])
        
        return suggestions
