import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Configure Streamlit page settings
st.set_page_config(
    page_title="Arthritis Diagnosis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/arthritisdiagnosis',
        'About': 'Arthritis Diagnosis System - Created by Muhammad Junaid, Hamid Shehzad, and Aneeqa Sabir'
    }
)

st.markdown("""
    <style>
    /* Light theme with professional styling */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Enhanced text readability */
    p, li {
        color: #2D3748;
        font-size: 1.1rem;
        line-height: 1.7;
        letter-spacing: 0.3px;
    }
    
    /* Headers styling */
    h1 {
        color: #1A365D;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2, h3 {
        color: #2C5282;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Improved multiselect styling */
    .stMultiSelect {
        background-color: #F7FAFC;
        border-radius: 8px;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #4299E1, #63B3ED);
        border: none;
        border-radius: 20px;
        padding: 6px 16px;
        margin: 3px;
        color: white;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4299E1, #63B3ED);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(66, 153, 225, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px -1px rgba(66, 153, 225, 0.3);
    }
    
    /* Enhanced boxes */
    .diagnosis-box, .medication-box {
        background-color: #F7FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Warning text */
    .warning {
        color: #E53E3E;
        font-size: 0.95rem;
    }
    
    /* Risk level indicators */
    .risk-high {
        color: #E53E3E;
        font-weight: bold;
    }
    
    .risk-medium {
        color: #D69E2E;
        font-weight: bold;
    }
    
    .risk-low {
        color: #38A169;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# [Rest of your existing code remains the same until the modifications below]

# Add new function for risk assessment
def assess_risk(symptoms, age_group):
    risk_factors = {
        "fever": 3,
        "joint_pain": 2,
        "morning_stiffness": 2,
        "swelling": 2,
        "fatigue": 1,
        "age_50+": 3
    }
    
    risk_score = sum(risk_factors.get(symptom, 1) for symptom in symptoms)
    if age_group == "65+":
        risk_score += 3
    elif age_group == "50-64":
        risk_score += 2
    
    if risk_score > 12:
        return "High", "risk-high"
    elif risk_score > 8:
        return "Medium", "risk-medium"
    return "Low", "risk-low"

# Add at the beginning of tab1
with tab1:
    # Add age group selection
    age_group = st.selectbox(
        "Age Group",
        ["18-34", "35-49", "50-64", "65+"],
        help="Select your age group"
    )
    
    # Add pain intensity slider
    pain_intensity = st.slider(
        "Pain Intensity (0-10)",
        0, 10, 5,
        help="Rate your pain level from 0 (no pain) to 10 (severe pain)"
    )

    # [Previous symptom selection code remains here]

    # After diagnosis generation, add risk assessment
    if st.button("Generate Diagnosis", help="Click to analyze your symptoms"):
        if not selected_symptoms:
            st.error("⚠️ Please select at least one symptom for diagnosis.")
        else:
            risk_level, risk_class = assess_risk(selected_symptoms, age_group)
            st.markdown(f"""
                <div class="diagnosis-box">
                    <h3>Risk Assessment</h3>
                    <p>Risk Level: <span class="{risk_class}">{risk_level}</span></p>
                    <p>Pain Level: {pain_intensity}/10</p>
                </div>
            """, unsafe_allow_html=True)
            
            # [Rest of your diagnosis code]

# Add new Pain Tracker tab
tab1, tab2, tab3, tab4 = st.tabs(["Diagnosis", "Information", "History", "Pain Tracker"])

with tab4:
    st.markdown("### Pain Tracking Journal")
    
    # Add pain tracking form
    with st.form("pain_tracker"):
        date = st.date_input("Date")
        location = st.multiselect(
            "Pain Location",
            ["Knees", "Hands", "Shoulders", "Ankles", "Back", "Hips", "Other"]
        )
        intensity = st.slider("Pain Level", 0, 10, 5)
        weather = st.selectbox(
            "Weather Conditions",
            ["Sunny", "Rainy", "Cold", "Hot", "Humid"]
        )
        notes = st.text_area("Additional Notes")
        
        if st.form_submit_button("Save Entry"):
            if "pain_history" not in st.session_state:
                st.session_state.pain_history = []
            
            st.session_state.pain_history.append({
                "date": date.strftime("%Y-%m-%d"),
                "location": location,
                "intensity": intensity,
                "weather": weather,
                "notes": notes
            })
            st.success("Pain entry recorded successfully!")
    
    # Display pain history
    if "pain_history" in st.session_state and st.session_state.pain_history:
        st.markdown("### Pain History")
        pain_df = pd.DataFrame(st.session_state.pain_history)
        st.line_chart(pain_df.set_index("date")["intensity"])
        st.dataframe(pain_df)
