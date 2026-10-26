class EngagementAnalyzer:
    def compute_session_statistics(self, video_metrics, audio_metrics):
        stability = video_metrics.get("head_stability", 80)
        speech = audio_metrics.get("speech_probability", 0.5)
        
        engagement_score = round((stability * 0.6) + (speech * 40 * 0.4), 2)
        engagement_score = min(max(engagement_score, 0.0), 100.0)
        
        return {
            "engagement_score": engagement_score,
            "status_label": "High Engagement" if engagement_score > 75 else ("Moderate" if engagement_score > 50 else "Low Activity")
        }