import streamlit as st
import pandas as pd
COURSE_CSV_PATH = "data/courses.csv"
def load_courses():
    return pd.read_csv(COURSE_CSV_PATH)
def save_courses(df):
    df.to_csv(COURSE_CSV_PATH, index=False)
def run_admin_editor():
    st.subheader("📋 Course Knowledge Base Editor")
    df = load_courses()

    # Show existing courses
    st.markdown("### 📄 Current Courses")
    st.dataframe(df)

    st.markdown("---")
    st.markdown("### ➕ Add New Course")
    with st.form("add_course_form"):
        coursecode = st.text_input("Course Code")
        coursename = st.text_input("Course Name")
        description = st.text_area("Description")
        prerequisites = st.text_input("Prerequisites (comma-separated course codes)")
        corequisites = st.text_input("Corequisites (comma-separated course codes)")
        credithours = st.number_input("Credit Hours", min_value=1, step=1)
        semester = st.selectbox("Semester Offered", ["Fall", "Spring", "Both"])
        submitted = st.form_submit_button("Add Course")
        if submitted:
            if coursecode in df["coursecode"].values:
                st.error("Course code already exists.")
            else:
                new_row = pd.DataFrame([{
                    "coursecode": coursecode,
                    "coursename": coursename,
                    "description": description,
                    "prerequisites": prerequisites,
                    "corequisites": corequisites,
                    "credithours": credithours,
                    "semester": semester
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_courses(df)
                st.success(f"✅ Added course: {coursecode}")

    st.markdown("---")
    st.markdown("### 📝 Edit Existing Course")
    edit_code = st.selectbox("Select Course Code to Edit", options=df["coursecode"].unique().tolist())
    if edit_code:
        course_row = df[df["coursecode"] == edit_code].iloc[0]

        with st.form("edit_course_form"):
            coursename = st.text_input("Course Name", value=course_row["coursename"])
            description = st.text_area("Description", value=course_row["description"])
            prerequisites = st.text_input("Prerequisites (comma-separated)", value=course_row["prerequisites"])
            corequisites = st.text_input("Corequisites (comma-separated)", value=course_row["corequisites"])
            credithours = st.number_input("Credit Hours", min_value=1, step=1, value=int(course_row["credithours"]))
            semester = st.selectbox("Semester Offered", ["Fall", "Spring", "Both"], index=["Fall", "Spring", "Both"].index(course_row["semester"]))
            update = st.form_submit_button("Update Course")
            if update:
                df.loc[df["coursecode"] == edit_code, :] = [edit_code, coursename, description, prerequisites, corequisites, credithours, semester]
                save_courses(df)
                st.success(f"✅ Updated course: {edit_code}")

    st.markdown("---")
    st.markdown("### 🗑️ Delete Course")
    delete_code = st.text_input("Enter Course Code to Delete")
    if st.button("Delete Course"):
        if delete_code in df["coursecode"].values:
            df = df[df["coursecode"] != delete_code]
            save_courses(df)
            st.success(f"🗑️ Deleted course: {delete_code}")
        else:
            st.error("Course code not found.")
