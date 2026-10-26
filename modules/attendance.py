from database.db_manager import log_attendance

class AttendanceTracker:
    def __init__(self):
        self.sustained_counters = {}
        self.threshold_frames = 3

    def process_frame_detections(self, session_id, detected_participant_ids):
        timestamped_records = []
        for pid in detected_participant_ids:
            self.sustained_counters[pid] = self.sustained_counters.get(pid, 0) + 1
            if self.sustained_counters[pid] >= self.threshold_frames:
                log_attendance(session_id, pid, status="Present", confidence=0.95)
                timestamped_records.append({"participant_id": pid, "status": "Present"})
        return timestamped_records