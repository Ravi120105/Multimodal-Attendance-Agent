import streamlit as st
import pandas as pd
import time
from database.db_manager import init_db, create_session, get_active_sessions, register_participant, get_participants, get_attendance_records, log_attendance
from modules.attendance import AttendanceTracker
from modules.video_processor import VideoProcessor
from modules.audio_processor import AudioProcessor
from modules.engagement_analyzer import EngagementAnalyzer
from modules.recommendation_engine import RecommendationEngine
from modules.report_generator import ReportGenerator


st.set_page_config(page_title="Multimodal Attendance & Engagement Agent", page_icon="🎓", layout="wide")

init_db()

st.title("🎓 Multimodal Attendance & Engagement Agent")
st.markdown("Privacy-conscious classroom intelligence system with local processing fallbacks and AI recommendations.")

st.sidebar.header("Navigation")
menu = st.sidebar.selectbox("Choose Module", ["Dashboard Overview", "Live Session Control", "Participant Enrollment", "Analytics & AI Insights", "Demo & Simulation Mode"])

tracker = AttendanceTracker()
video_proc = VideoProcessor()
audio_proc = AudioProcessor()
engagement_analyzer = EngagementAnalyzer()
rec_engine = RecommendationEngine()

if menu == "Dashboard Overview":
    st.subheader("📊 System Overview & Active Status")
    sessions = get_active_sessions()
    participants = get_participants()
    records = get_attendance_records()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registered Participants", len(participants))
    col2.metric("Total Sessions Hosted", len(sessions))
    col3.metric("Total Attendance Logs", len(records))

    st.markdown("---")
    st.markdown("### 📋 Recent Attendance Records")
    if records:
        df_rec = pd.DataFrame(records)
        st.dataframe(df_rec[["session_id", "full_name", "enrollment_number", "timestamp", "status", "confidence"]], use_container_width=True)
        csv_data = ReportGenerator.export_attendance_csv(records)
        st.download_button("📥 Download Attendance CSV", data=csv_data, file_name="attendance_report.csv", mime="text/csv")
    else:
        st.info("No attendance records available yet. Start a session or use Demo Mode.")

elif menu == "Live Session Control":
    st.subheader("🔴 Live Classroom Session Management")
    sessions = get_active_sessions()
    session_options = {s['session_name'] + f" ({s['session_id']})": s['session_id'] for s in sessions}

    with st.form("new_session_form"):
        st.markdown("#### Create New Session")
        s_name = st.text_input("Session Name", "Advanced AI Lecture - Unit 3")
        c_code = st.text_input("Course Code", "CSE-402")
        submit_session = st.form_submit_button("Initialize Session")
        if submit_session:
            new_id = f"sess_{int(time.time())}"
            create_session(new_id, s_name, c_code)
            st.success(f"Session '{s_name}' successfully created!")
            st.rerun()

    if session_options:
        selected_name = st.selectbox("Select Active Session", list(session_options.keys()))
        active_sess_id = session_options[selected_name]

        st.markdown(f"### Monitoring Session: `{active_sess_id}`")
        participants = get_participants()

        if st.button("🚀 Run Live Multimodal Scan Simulation"):
            if participants:
                sample_pids = [p['participant_id'] for p in participants[:3]]
                tracker.process_frame_detections(active_sess_id, sample_pids)
                st.success("Scanned frame batch successfully! Sustained presence verified.")
                st.rerun()
            else:
                st.warning("Please register participants first.")

        st.markdown("#### Manual Attendance Override")
        if participants:
            p_map = {f"{p['full_name']} ({p['enrollment_number']})": p['participant_id'] for p in participants}
            selected_p_str = st.selectbox("Select Participant", list(p_map.keys()))
            manual_status = st.selectbox("Status", ["Present", "Late", "Absent"])
            if st.button("Record Manual Attendance"):
                log_attendance(active_sess_id, p_map[selected_p_str], status=manual_status, confidence=1.0)
                st.success(f"Manually recorded {manual_status} for {selected_p_str}")
                st.rerun()

elif menu == "Participant Enrollment":
    st.subheader("👤 Participant Consent & Enrollment")
    st.markdown("Enroll participants under privacy compliance standards. No facial embeddings or biometric vectors are stored permanently.")

    with st.form("enroll_form"):
        fname = st.text_input("Full Name")
        enrol = st.text_input("Enrollment Number (e.g. 0157CS241115)")
        consent = st.checkbox("Participant Consent Granted for Local Attendance Logging", value=True)
        submit_reg = st.form_submit_button("Register Participant")

        if submit_reg:
            if fname and enrol and consent:
                pid = f"p_{enrol}"
                success = register_participant(pid, fname, enrol)
                if success:
                    st.success(f"Successfully registered {fname}!")
                else:
                    st.warning("Enrollment number already exists.")
            else:
                st.error("Please fill in all details and confirm consent.")

    st.markdown("### Registered Roster")
    roster = get_participants()
    if roster:
        st.dataframe(pd.DataFrame(roster), use_container_width=True)
    else:
        st.info("No participants registered yet.")

elif menu == "Analytics & AI Insights":
    st.subheader("📈 Multimodal Activity Analysis & Teaching Recommendations")
    
    v_metrics = video_proc.analyze_frame_simulation(int(time.time()) % 10)
    a_metrics = audio_proc.analyze_audio_segment()
    engagement = engagement_analyzer.compute_session_statistics(v_metrics, a_metrics)

    col1, col2, col3 = st.columns(3)
    col1.metric("Head Stability Index", f"{v_metrics['head_stability']}%")
    col2.metric("Audio Decibel Level", f"{a_metrics['decibel_level']} dB")
    col3.metric("Composite Engagement Score", f"{engagement['engagement_score']}/100", engagement['status_label'])

    st.markdown("---")
    st.markdown("### 🤖 Teaching Recommendations Engine")
    recommendation = rec_engine.generate_recommendations(engagement['engagement_score'], 15)
    st.info(recommendation)

elif menu == "Demo & Simulation Mode":
    st.subheader("🧪 Sandbox Demonstration Mode")
    st.markdown("Test all system features using pre-configured simulated classroom data.")

    if st.button("Load Demo Dataset & Run Simulation"):
        init_db()
        create_session("demo_session_101", "Demo AI Lecture", "CS-DEMO")
        register_participant("demo_p1", "Himanshi Ahuja", "0157CS241085")
        register_participant("demo_p2", "Manthan Rai", "0157CS241114")
        register_participant("demo_p3", "Manvi Rajput", "0157CS241115")
        log_attendance("demo_session_101", "demo_p1", "Present", 0.98)
        log_attendance("demo_session_101", "demo_p2", "Present", 0.95)
        log_attendance("demo_session_101", "demo_p3", "Late", 0.90)
        st.success("Demo dataset loaded successfully! Navigate to Dashboard Overview or Live Session Control to explore.")