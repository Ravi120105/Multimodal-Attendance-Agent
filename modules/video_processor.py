import numpy as np

class VideoProcessor:
    def __init__(self):
        self.active_tracker = True

    def analyze_frame_simulation(self, frame_index=0):
        head_stability = float(np.clip(85 + 10 * np.sin(frame_index * 0.2), 50, 100))
        movement_index = float(np.clip(1.5 + 0.8 * np.cos(frame_index * 0.3), 0.1, 5.0))
        return {
            "head_stability": round(head_stability, 2),
            "movement_index": round(movement_index, 2)
        }