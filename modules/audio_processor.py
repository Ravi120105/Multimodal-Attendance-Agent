import numpy as np

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050

    def analyze_audio_segment(self, dummy_signal=None):
        if dummy_signal is None:
            db_level = float(np.random.uniform(-45.0, -20.0))
            speech_prob = float(np.random.uniform(0.1, 0.9))
        else:
            db_level = -30.0
            speech_prob = 0.5
        return {
            "decibel_level": round(db_level, 2),
            "speech_probability": round(speech_prob, 2)
        }