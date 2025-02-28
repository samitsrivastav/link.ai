import streamlit as st
import pandas as pd
from util import logo


with st.sidebar:
    logo()

# Load dataset
df = pd.read_csv("mentors_dataset.csv")

# Ensure column names are clean
df.columns = df.columns.str.strip()

def recommend_mentors(user_skill_level, specialization):
    """Recommend top 5 mentors based on skill level, specialization & rating."""
    
    # Filter mentors based on level and specialization
    filtered_mentors = df[(df["Level Taught"] == user_skill_level) & (df["Specialization"] == specialization)]
    
    if filtered_mentors.empty:
        return "No mentors available for this selection."
    
    # Sort by highest rating and experience
    top_mentors = filtered_mentors.sort_values(by=["Rating", "Experience (yrs)"], ascending=[False, False]).head(5)
    
    return top_mentors

def show_mentors(recommended_mentors):
    pass

def main():
    st.title("Mentor Recommendation System")
    
    # User selects skill level
    levels = ["Beginner", "Intermediate", "Advanced"]
    selected_level = st.selectbox("Select your skill level:", levels)

    # User selects specialization
    specializations = df["Specialization"].unique()
    selected_specialization = st.selectbox("Select your specialization:", specializations)

    if st.button("Find Mentors"):
        recommended_mentors = recommend_mentors(selected_level, selected_specialization)

        if isinstance(recommended_mentors, str):
            st.warning(recommended_mentors)
        else:
            st.write("### Recommended Mentors")
            st.dataframe(recommended_mentors)
            # show_mentors(recommended_mentors)

if __name__ == "__main__":
    main()
