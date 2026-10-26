import os
import google.generativeai as genai
from config import GEMINI_API_KEY

class RecommendationEngine:
    def __init__(self):
        if GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                self.gemini_enabled = True
            except Exception:
                self.gemini_enabled = False
        else:
            self.gemini_enabled = False

    def generate_recommendations(self, avg_engagement, active_count):
        if self.gemini_enabled:
            try:
                prompt = f"Classroom analytics: Average Engagement Score: {avg_engagement}/100, Active Participants: {active_count}. Provide 3 concise, actionable teaching recommendations for the instructor."
                response = self.model.generate_content(prompt)
                return f"[Gemini AI Insights]\n{response.text}"
            except Exception:
                pass 
        
        if avg_engagement < 60:
            return "⚠️ Low engagement detected. Recommendation: Introduce an interactive 5-minute Q&A poll, pivot to a live code demonstration, or call for a short 3-minute biological break."
        elif avg_engagement < 80:
            return "💡 Moderate participation observed. Recommendation: Pose an open-ended discussion question to encourage active chat/audio engagement."
        else:
            return "✅ Excellent engagement levels! Recommendation: Maintain current pacing and continue with planned collaborative activities."