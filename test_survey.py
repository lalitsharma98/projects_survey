import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

# Project List
projects = [
    "Anomaly Detection - Phase 1", "Model Validation - Phase 1", "Language Prioritization",
    "Automated WP Notes - Phase 1", "Data Extraction: MS Excel - Phase 1"
]

# Users and their project involvement matrix
users_projects = {
    "Adrian": [1, 1, "", 1, ""],
    "Chetan": ["", "", "", "", 1],
    "Claudio": [1, 1, "", 1, ""],
    "Danish": ["", "", "", "", 1],
    "Gabi": [1, 1, "", 1, ""],
    "Isaias": [1, 1, "", 1, ""],
    "Jesse": [1, 1, 1, 1, ""],
    "Joel": [1, 1, "", 1, ""],
    "Lalit": ["", "", "", "", 1],
    "Laurie": [1, 1, 1, 1, ""],
    "Maricela": [1, 1, "", 1, ""],
    "Mario": [1, 1, "", 1, ""],
    "Paul": [1, 1, "", 1, ""],
    "Vibhor": [1, 1, "", 1, ""]
}

# Admin credentials
ADMIN_USERS = {"Jesse": "admin123", "Chetan": "admin456"}

# App title
st.title("Project Survey")

# User selection dropdown
selected_user = st.selectbox("Select User", list(users_projects.keys()))

# Survey form for selected user and their projects
if selected_user:
    st.header(f"Projects for {selected_user}")
    survey_data = []
    projects_list = users_projects[selected_user]
    for i, project_status in enumerate(projects_list):
        if project_status == 1:
            st.subheader(projects[i])
            usage = st.radio(f"Usage Status for {projects[i]}", ["Not Used", "Started Exploring", "Started Utilizing", "Regularly Utilizing/Reaping Benefit"], key=f"usage_{selected_user}_{projects[i]}")
            feedback = st.radio(f"Feedback for {projects[i]}", ["Needs Improvement", "Somewhat Useful", "Very Useful"], key=f"feedback_{selected_user}_{projects[i]}")
            features = st.radio(f"Features Explored for {projects[i]}", ["Never", "Partial", "Fully"], key=f"features_{selected_user}_{projects[i]}")
            frequency = st.radio(f"Frequency of Use for {projects[i]}", ["Never", "Rarely (once a month)", "Occasionally (a few times a month)", "Frequently (a few times a week)", "Almost Daily"], key=f"frequency_{selected_user}_{projects[i]}")
            comments = st.text_area(f"Comments for {projects[i]}", key=f"comments_{selected_user}_{projects[i]}")
            survey_data.append([selected_user, projects[i], usage, feedback, features, frequency, comments])

    if st.button("Submit Survey"):
        # Create a DataFrame from the survey data
        df = pd.DataFrame(survey_data, columns=["User", "Project", "Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Comments"])
        df["Month Year"] = datetime.now().strftime("%B %Y")

        # File path
        file_path = "survey_results.xlsx"

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            for i, row in df.iterrows():
                condition = (
                    (existing_df["User"] == row["User"]) &
                    (existing_df["Project"] == row["Project"]) &
                    (existing_df["Month Year"] == row["Month Year"])
                )
                if condition.any():
                    existing_df.loc[condition, ["Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Comments"]] = row[["Usage Status", "Feedback", "Features Explored", "Frequency of Use", "Comments"]].values
                else:
                    existing_df = pd.concat([existing_df, pd.DataFrame([row])], ignore_index=True)
            existing_df.to_excel(file_path, index=False)
        else:
            df.to_excel(file_path, index=False)

        st.success("Survey submitted successfully!")

# Show Admin Panel only for Jesse and Chetan
if selected_user in ADMIN_USERS:
    st.sidebar.header("Admin Panel")
    admin_password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Download Survey Data"):
        if ADMIN_USERS.get(selected_user) == admin_password:
            if os.path.exists("survey_results.xlsx"):
                df = pd.read_excel("survey_results.xlsx")
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name="Survey Data")
                output.seek(0)

                st.sidebar.download_button(
                    label="📥 Download Survey Data",
                    data=output,
                    file_name="survey_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.sidebar.error("No survey data found.")
        else:
            st.sidebar.error("Invalid admin credentials!")
