import pandas as pd

class ReportGenerator:
    @staticmethod
    def export_attendance_csv(records):
        df = pd.DataFrame(records)
        return df.to_csv(index=False).encode('utf-8')