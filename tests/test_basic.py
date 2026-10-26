import pytest
from database.db_manager import init_db, create_session, register_participant, get_participants
from modules.engagement_analyzer import EngagementAnalyzer
from modules.recommendation_engine import RecommendationEngine

def test_database_flow():
    init_db()
    create_session("test_sess_01", "AI Lecture", "CS401")
    register_participant("p999", "Test Student", "0157CS999")
    participants = get_participants()
    assert len(participants) > 0

def test_engagement_computation():
    analyzer = EngagementAnalyzer()
    stats = analyzer.compute_session_statistics({"head_stability": 90}, {"speech_probability": 0.8})
    assert "engagement_score" in stats
    assert stats["engagement_score"] > 0

def test_local_recommendation():
    engine = RecommendationEngine()
    engine.gemini_enabled = False
    rec = engine.generate_recommendations(55.0, 25)
    assert "Low engagement" in rec