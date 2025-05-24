import streamlit as st
import pandas as pd
from login import login, get_current_user
from editor.kb_editor import run_admin_editor
from engine.advisor import CourseAdvisor
st.set_page_config(page_title="AIU CSE Course Advisor", layout="wide")
st.title("🎓 AIU CSE Course Advisor")
st.sidebar.image("logo.png", width=200)
# 🔐 Handle Login
if "user" not in st.session_state or st.session_state.user is None:
    login()
else:
    user = get_current_user()
    if user is None:
        st.error("User session expired. Please log in again.")
        st.stop()
    st.sidebar.success(f"Logged in as {user['username']} ({user['role']})")
    # 🛠️ Admin Interface
    if user['role'] == "admin":
        run_admin_editor()
    # 🎓 Student Advisor
    elif user['role'] == "student":
        st.subheader("🎓 Personalized Course Advisor")
        df = pd.read_csv("data/courses.csv")
        cgpa = st.number_input("Enter your CGPA", min_value=0.0, max_value=4.0, step=0.1)
        semester = st.selectbox("Upcoming Semester", ["Fall", "Spring"])
        passed = st.multiselect("Select Passed Courses", df["coursecode"].dropna().unique().tolist())
        failed = st.multiselect("Select Failed Courses", [c for c in df["coursecode"].dropna().unique().tolist() if c not in passed])
        if st.button("Get Recommendations"):
            engine = CourseAdvisor({
                "cgpa": cgpa,
                "semester": semester,
                "passed": passed,
                "failed": failed
            }, df)
            engine.run_engine()
            if engine.recommendations:
                st.markdown("### ✅ Recommended Courses")
                rec_df = pd.DataFrame(engine.recommendations)
                # 👇 Rename for better display and fix missing 'name'
                rec_df_display = rec_df.rename(columns={"coursename": "Course Name"})
                st.dataframe(rec_df_display[["code", "Course Name", "credit_hours"]])
                st.success(f"**Total Credit Hours:** {engine.total_credits}")
            else:
                st.warning("⚠️ No suitable courses found based on your input.")
            # 💬 Explanation Output
            st.markdown("### 💬 Explanation for Each Recommendation")
            for exp in engine.explanations:
                st.info(exp)
    else:
        st.error("🚫 Unauthorized role.")
    # 🔓 Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
