import streamlit as st
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
from datetime import timedelta

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

# Light theme styling
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
    
    /* Custom card styling */
    .custom-card {
        background-color: #F7FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    knowledge_base = [
        {
            "if": ["joint_pain", "morning_stiffness", "swelling", "fatigue", "fever"],
            "then": "rheumatoid_arthritis",
            "confidence": 0.90,
            "exercise_recommendations": [
                "Gentle stretching exercises",
                "Low-impact aerobic activities",
                "Water aerobics"
            ],
            "diet_recommendations": [
                "Omega-3 rich foods",
                "Anti-inflammatory foods",
                "Limited processed foods"
            ]
        },
        {
            "if": ["joint_pain", "age_50+", "bone_spurs", "joint_crackling", "morning_stiffness"],
            "then": "osteoarthritis",
            "confidence": 0.88,
            "exercise_recommendations": [
                "Regular walking",
                "Swimming",
                "Strength training"
            ],
            "diet_recommendations": [
                "Calcium-rich foods",
                "Vitamin D supplements",
                "Collagen-rich foods"
            ]
        },
        # ... [Previous conditions remain the same]
    ]
    
    medications = {
        "rheumatoid_arthritis": [
            {
                "name": "Methotrexate",
                "description": "A disease-modifying drug that reduces inflammation and prevents joint damage.",
                "usage": "Taken weekly, preferably at the same time each week.",
                "schedule": "Weekly",
                "reminders": ["Take with food", "Avoid alcohol", "Regular blood tests required"]
            },
            {
                "name": "Biologics",
                "description": "Advanced medications that target specific parts of the immune system.",
                "usage": "Administered by injection or infusion as prescribed.",
                "schedule": "Varies",
                "reminders": ["Keep refrigerated", "Rotate injection sites", "Monitor for infections"]
            }
        ],
        # ... [Previous medications remain the same]
    }
    
    return knowledge_base, medications

def assess_risk(symptoms, age_group, pain_intensity):
    risk_factors = {
        "fever": 3,
        "joint_pain": 2,
        "morning_stiffness": 2,
        "swelling": 2,
        "fatigue": 1,
        "age_50+": 3
    }
    
    risk_score = sum(risk_factors.get(symptom, 1) for symptom in symptoms)
    
    # Add pain intensity to risk calculation
    risk_score += pain_intensity * 0.5
    
    # Age group factor
    age_factors = {
        "18-34": 0,
        "35-49": 1,
        "50-64": 2,
        "65+": 3
    }
    risk_score += age_factors.get(age_group, 0)
    
    if risk_score > 15:
        return "High", "risk-high", risk_score
    elif risk_score > 10:
        return "Medium", "risk-medium", risk_score
    return "Low", "risk-low", risk_score

def forward_chaining(knowledge_base, symptoms):
    inferred = set(symptoms)
    diagnoses = []
    
    for rule in knowledge_base:
        matching_symptoms = len(set(rule["if"]).intersection(inferred))
        total_symptoms = len(rule["if"])
        if matching_symptoms > 0:
            confidence = (matching_symptoms / total_symptoms) * rule["confidence"]
            if confidence >= 0.5:
                diagnoses.append({
                    "condition": rule["then"],
                    "confidence": confidence,
                    "matching_symptoms": matching_symptoms,
                    "total_symptoms": total_symptoms,
                    "exercise_recommendations": rule.get("exercise_recommendations", []),
                    "diet_recommendations": rule.get("diet_recommendations", [])
                })
    
    return sorted(diagnoses, key=lambda x: x["confidence"], reverse=True)

def initialize_session_state():
    if "pain_history" not in st.session_state:
        st.session_state.pain_history = []
    if "medication_schedule" not in st.session_state:
        st.session_state.medication_schedule = []
    if "diagnosis_history" not in st.session_state:
        st.session_state.diagnosis_history = []

# Initialize session state
initialize_session_state()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Arthritis Diagnosis System")
    st.markdown("### Project Team")
    st.markdown("- Muhammad Junaid\n- Hamid Shehzad\n- Aneeqa Sabir")
    
    # Add quick actions in sidebar
    st.markdown("### Quick Actions")
    if st.button("Export Data"):
        # Add export functionality here
        st.download_button(
            "Download Report",
            data=pd.DataFrame(st.session_state.diagnosis_history).to_csv(),
            file_name="arthritis_report.csv",
            mime="text/csv"
        )

# Main application
st.title("🏥 Arthritis Diagnosis System")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Diagnosis", 
    "Pain Tracker", 
    "Medication Manager",
    "Lifestyle & Exercise",
    "History"
])

# Diagnosis Tab
with tab1:
    st.markdown("### Patient Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox(
            "Age Group",
            ["18-34", "35-49", "50-64", "65+"]
        )
        pain_intensity = st.slider(
            "Pain Intensity (0-10)",
            0, 10, 5
        )
    
    with col2:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    
    st.markdown("### Symptom Selection")
    col3, col4 = st.columns(2)
    
    with col3:
        joint_symptoms = st.multiselect(
            "Joint Symptoms",
            ["joint_pain", "joint_crackling", "morning_stiffness", "swelling"]
        )
        systemic_symptoms = st.multiselect(
            "Systemic Symptoms",
            ["fever", "chills", "fatigue", "weight_loss", "night_sweats"]
        )
    
    with col4:
        skin_symptoms = st.multiselect(
            "Skin Symptoms",
            ["skin_rashes", "nail_pitting", "redness"]
        )
        other_symptoms = st.multiselect(
            "Other Symptoms",
            ["age_50+", "bone_spurs", "back_pain", "stiff_spine", "eye_inflammation"]
        )

    selected_symptoms = joint_symptoms + systemic_symptoms + skin_symptoms + other_symptoms

    if st.button("Generate Diagnosis"):
        if not selected_symptoms:
            st.error("⚠️ Please select at least one symptom for diagnosis.")
        else:
            risk_level, risk_class, risk_score = assess_risk(selected_symptoms, age_group, pain_intensity)
            
            st.markdown(f"""
                <div class="diagnosis-box">
                    <h3>Risk Assessment</h3>
                    <p>Risk Level: <span class="{risk_class}">{risk_level}</span></p>
                    <p>Risk Score: {risk_score:.1f}</p>
                    <p>Pain Level: {pain_intensity}/10</p>
                </div>
            """, unsafe_allow_html=True)
            
            knowledge_base, medications = load_data()
            diagnoses = forward_chaining(knowledge_base, selected_symptoms)
            
            if diagnoses:
                for diagnosis in diagnoses:
                    st.markdown(f"""
                        <div class="diagnosis-box">
                            <h3>{diagnosis["condition"].replace("_", " ").title()}</h3>
                            <p>Confidence: {diagnosis["confidence"]*100:.1f}%</p>
                            <p>Matching Symptoms: {diagnosis["matching_symptoms"]}/{diagnosis["total_symptoms"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add diagnosis to history
                    st.session_state.diagnosis_history.append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "condition": diagnosis["condition"],
                        "confidence": diagnosis["confidence"],
                        "risk_level": risk_level,
                        "pain_level": pain_intensity
                    })

# Pain Tracker Tab
with tab2:
    st.markdown("### Pain Tracking Journal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
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
                st.session_state.pain_history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "location": location,
                    "intensity": intensity,
                    "weather": weather,
                    "notes": notes
                })
                st.success("Pain entry recorded successfully!")
    
    with col2:
        st.markdown("### Quick Stats")
        if st.session_state.pain_history:
            pain_df = pd.DataFrame(st.session_state.pain_history)
            avg_pain = pain_df["intensity"].mean()
            st.metric("Average Pain Level", f"{avg_pain:.1f}/10")
            
            # Most painful locations
            if not pain_df.empty and "location" in pain_df:
                all_locations = [loc for locs in pain_df["location"] for loc in locs]
                if all_locations:
                    location_counts = pd.Series(all_locations).value_counts()
                    st.markdown("#### Most Affected Areas")
                    st.write(location_counts.head())

    # Display pain history visualization
    if st.session_state.pain_history:
        st.markdown("### Pain History Visualization")
        pain_df = pd.DataFrame(st.session_state.pain_history)
        
        # Line chart for pain intensity over time
        fig = px.line(pain_df, x="date", y="intensity", title="Pain Intensity Over Time")
        st.plotly_chart(fig)
        
        # Display detailed history
        st.markdown("### Detailed History")
        st.dataframe(pain_df)
# Medication Manager Tab
with tab3:
    st.markdown("### Medication Schedule")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("medication_scheduler"):
            med_name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage")
            frequency = st.selectbox(
                "Frequency",
                ["Daily", "Twice Daily", "Weekly", "Monthly"]
            )
            time = st.time_input("Reminder Time")
            start_date = st.date_input("Start Date")
            duration = st.number_input("Duration (days)", min_value=1, value=30)
            special_instructions = st.text_area("Special Instructions")
            
            if st.form_submit_button("Add Medication"):
                if "medication_schedule" not in st.session_state:
                    st.session_state.medication_schedule = []
                
                end_date = start_date + timedelta(days=duration)
                
                st.session_state.medication_schedule.append({
                    "medication": med_name,
                    "dosage": dosage,
                    "frequency": frequency,
                    "time": time.strftime("%H:%M"),
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "instructions": special_instructions,
                    "status": "Active"
                })
                st.success("Medication added successfully!")

    with col2:
        st.markdown("### Today's Schedule")
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        
        # Filter medications for today
        today_meds = [
            med for med in st.session_state.medication_schedule
            if datetime.strptime(med["start_date"], "%Y-%m-%d").date() <= current_date 
            and datetime.strptime(med["end_date"], "%Y-%m-%d").date() >= current_date
        ]
        
        if today_meds:
            for med in today_meds:
                med_time = datetime.strptime(med["time"], "%H:%M").time()
                status = "🔴 Pending" if med_time > current_time else "🟢 Due"
                
                st.markdown(f"""
                    <div class="custom-card" style="border-left: 4px solid {'#FF4B4B' if status == '🔴 Pending' else '#28A745'}">
                        <h4>{med["medication"]}</h4>
                        <p><strong>Dosage:</strong> {med["dosage"]}</p>
                        <p><strong>Time:</strong> {med["time"]} ({status})</p>
                        <p><strong>Frequency:</strong> {med["frequency"]}</p>
                        <p style="font-size: 0.9em; color: #666;">{med["instructions"]}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No medications scheduled for today")

    # Medication History and Management
    st.markdown("### Medication Management")
    
    # Create tabs for different medication views
    med_tab1, med_tab2, med_tab3 = st.tabs(["Active Medications", "Medication History", "Adherence Tracking"])
    
    with med_tab1:
        if "medication_schedule" in st.session_state and st.session_state.medication_schedule:
            active_meds = [
                med for med in st.session_state.medication_schedule
                if datetime.strptime(med["end_date"], "%Y-%m-%d").date() >= current_date
            ]
            
            if active_meds:
                for med in active_meds:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"""
                            <div style="padding: 10px;">
                                <h4>{med["medication"]}</h4>
                                <p>Dosage: {med["dosage"]} | Frequency: {med["frequency"]}</p>
                                <p>Schedule: {med["time"]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button(f"Edit {med['medication']}", key=f"edit_{med['medication']}"):
                            st.session_state.edit_med = med
                    with col3:
                        if st.button(f"Stop {med['medication']}", key=f"stop_{med['medication']}"):
                            med["status"] = "Stopped"
                            st.success(f"Stopped {med['medication']}")
                            st.rerun()
            else:
                st.info("No active medications")

    with med_tab2:
        if "medication_schedule" in st.session_state and st.session_state.medication_schedule:
            # Convert medication schedule to DataFrame for better display
            med_df = pd.DataFrame(st.session_state.medication_schedule)
            med_df["Duration"] = (
                pd.to_datetime(med_df["end_date"]) - pd.to_datetime(med_df["start_date"])
            ).dt.days
            
            # Display medication history with filters
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Active", "Stopped"]
            )
            
            filtered_df = med_df if status_filter == "All" else med_df[med_df["status"] == status_filter]
            st.dataframe(filtered_df)
            
            # Export medication history
            if st.button("Export Medication History"):
                st.download_button(
                    label="Download Medication History",
                    data=filtered_df.to_csv(index=False),
                    file_name="medication_history.csv",
                    mime="text/csv"
                )

    with med_tab3:
        st.markdown("### Medication Adherence Tracking")
        
        if "medication_adherence" not in st.session_state:
            st.session_state.medication_adherence = []
        
        # Add adherence tracking form
        with st.form("adherence_tracker"):
            track_date = st.date_input("Date")
            track_med = st.selectbox(
                "Medication",
                [med["medication"] for med in st.session_state.medication_schedule]
                if "medication_schedule" in st.session_state else []
            )
            taken = st.radio("Medication Taken?", ["Yes", "No", "Delayed"])
            if taken == "Delayed":
                delay_time = st.time_input("Time Taken")
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Record Adherence"):
                st.session_state.medication_adherence.append({
                    "date": track_date.strftime("%Y-%m-%d"),
                    "medication": track_med,
                    "taken": taken,
                    "time_taken": delay_time.strftime("%H:%M") if taken == "Delayed" else None,
                    "notes": notes
                })
                st.success("Adherence recorded successfully!")
        
        # Display adherence statistics
        if st.session_state.medication_adherence:
            adherence_df = pd.DataFrame(st.session_state.medication_adherence)
            
            # Calculate adherence rate
            total_records = len(adherence_df)
            taken_on_time = len(adherence_df[adherence_df["taken"] == "Yes"])
            adherence_rate = (taken_on_time / total_records) * 100
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Adherence Rate", f"{adherence_rate:.1f}%")
            with col2:
                st.metric("Total Doses", total_records)
            with col3:
                st.metric("Doses Taken On Time", taken_on_time)
            
            # Display adherence chart
            adherence_df["date"] = pd.to_datetime(adherence_df["date"])
            adherence_by_date = adherence_df.groupby("date")["taken"].value_counts().unstack()
            st.line_chart(adherence_by_date)
with tab4:
    st.markdown("### Exercise Tracking")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("exercise_tracker"):
            exercise_date = st.date_input("Exercise Date")
            exercise_type = st.selectbox(
                "Exercise Type",
                ["Walking", "Swimming", "Yoga", "Stretching", "Strength Training", "Other"]
            )
            duration = st.number_input("Duration (minutes)", min_value=5, max_value=180, value=30)
            intensity = st.select_slider(
                "Intensity",
                options=["Very Light", "Light", "Moderate", "Vigorous", "Very Vigorous"]
            )
            pain_during = st.slider("Pain During Exercise (0-10)", 0, 10, 0)
            
            if st.form_submit_button("Log Exercise"):
                if "exercise_history" not in st.session_state:
                    st.session_state.exercise_history = []
                
                st.session_state.exercise_history.append({
                    "date": exercise_date.strftime("%Y-%m-%d"),
                    "type": exercise_type,
                    "duration": duration,
                    "intensity": intensity,
                    "pain_level": pain_during
                })
                st.success("Exercise logged successfully!")

    with col2:
        st.markdown("### Exercise Stats")
        if "exercise_history" in st.session_state and st.session_state.exercise_history:
            exercise_df = pd.DataFrame(st.session_state.exercise_history)
            total_minutes = exercise_df["duration"].sum()
            avg_pain = exercise_df["pain_level"].mean()
            
            st.metric("Total Exercise Time", f"{total_minutes} minutes")
            st.metric("Average Pain During Exercise", f"{avg_pain:.1f}/10")

            # Display exercise type distribution
            st.markdown("#### Exercise Distribution")
            type_counts = exercise_df["type"].value_counts()
            st.bar_chart(type_counts)

    # Diet Tracking
    st.markdown("### Diet Tracking")
    col3, col4 = st.columns([2, 1])
    
    with col3:
        with st.form("diet_tracker"):
            diet_date = st.date_input("Meal Date")
            meal_type = st.selectbox(
                "Meal Type",
                ["Breakfast", "Lunch", "Dinner", "Snack"]
            )
            foods = st.multiselect(
                "Foods Consumed",
                ["Fruits", "Vegetables", "Whole Grains", "Lean Protein", "Dairy", 
                 "Anti-inflammatory foods", "Processed Foods", "High-sugar Foods"]
            )
            water_intake = st.number_input("Water Intake (glasses)", 0, 20, 8)
            notes = st.text_area("Meal Notes")
            
            if st.form_submit_button("Log Meal"):
                if "diet_history" not in st.session_state:
                    st.session_state.diet_history = []
                
                st.session_state.diet_history.append({
                    "date": diet_date.strftime("%Y-%m-%d"),
                    "meal_type": meal_type,
                    "foods": foods,
                    "water_intake": water_intake,
                    "notes": notes
                })
                st.success("Meal logged successfully!")

    with col4:
        st.markdown("### Diet Stats")
        if "diet_history" in st.session_state and st.session_state.diet_history:
            diet_df = pd.DataFrame(st.session_state.diet_history)
            
            # Calculate average water intake
            avg_water = diet_df["water_intake"].mean()
            st.metric("Average Daily Water Intake", f"{avg_water:.1f} glasses")
            
            # Show food type distribution
            if not diet_df.empty:
                all_foods = [food for foods_list in diet_df["foods"] for food in foods_list]
                food_counts = pd.Series(all_foods).value_counts()
                st.markdown("#### Most Common Foods")
                st.write(food_counts.head())

# History Tab
with tab5:
    st.markdown("### Comprehensive History")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    # Diagnosis History
    st.markdown("#### Diagnosis History")
    if st.session_state.diagnosis_history:
        diagnosis_df = pd.DataFrame(st.session_state.diagnosis_history)
        diagnosis_df["date"] = pd.to_datetime(diagnosis_df["date"])
        mask = (diagnosis_df["date"].dt.date >= start_date) & (diagnosis_df["date"].dt.date <= end_date)
        filtered_diagnosis = diagnosis_df[mask]
        st.dataframe(filtered_diagnosis)
        
        # Diagnosis distribution
        st.markdown("#### Diagnosis Distribution")
        condition_counts = filtered_diagnosis["condition"].value_counts()
        st.bar_chart(condition_counts)

    # Pain History Visualization
    st.markdown("#### Pain Trends")
    if st.session_state.pain_history:
        pain_df = pd.DataFrame(st.session_state.pain_history)
        pain_df["date"] = pd.to_datetime(pain_df["date"])
        mask = (pain_df["date"].dt.date >= start_date) & (pain_df["date"].dt.date <= end_date)
        filtered_pain = pain_df[mask]
        
        # Line chart for pain intensity
        fig = px.line(filtered_pain, x="date", y="intensity", 
                     title="Pain Intensity Over Time",
                     labels={"intensity": "Pain Level", "date": "Date"})
        st.plotly_chart(fig)
        
        # Pain locations heatmap
        if not filtered_pain.empty and "location" in filtered_pain:
            all_locations = [loc for locs in filtered_pain["location"] for loc in locs]
            location_counts = pd.Series(all_locations).value_counts()
            st.markdown("#### Most Affected Areas")
            st.bar_chart(location_counts)

    # Exercise Summary
    st.markdown("#### Exercise Summary")
    if "exercise_history" in st.session_state and st.session_state.exercise_history:
        exercise_df = pd.DataFrame(st.session_state.exercise_history)
        exercise_df["date"] = pd.to_datetime(exercise_df["date"])
        mask = (exercise_df["date"].dt.date >= start_date) & (exercise_df["date"].dt.date <= end_date)
        filtered_exercise = exercise_df[mask]
        
        # Exercise statistics
        if not filtered_exercise.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                total_duration = filtered_exercise["duration"].sum()
                st.metric("Total Exercise Duration", f"{total_duration} minutes")
            with col2:
                avg_intensity = filtered_exercise["intensity"].mode().iloc[0]
                st.metric("Most Common Intensity", avg_intensity)
            with col3:
                avg_pain = filtered_exercise["pain_level"].mean()
                st.metric("Average Pain During Exercise", f"{avg_pain:.1f}/10")

    # Diet Summary
    st.markdown("#### Diet Summary")
    if "diet_history" in st.session_state and st.session_state.diet_history:
        diet_df = pd.DataFrame(st.session_state.diet_history)
        diet_df["date"] = pd.to_datetime(diet_df["date"])
        mask = (diet_df["date"].dt.date >= start_date) & (diet_df["date"].dt.date <= end_date)
        filtered_diet = diet_df[mask]
        
        if not filtered_diet.empty:
            # Food type distribution
            all_foods = [food for foods_list in filtered_diet["foods"] for food in foods_list]
            food_counts = pd.Series(all_foods).value_counts()
            st.markdown("#### Food Type Distribution")
            st.bar_chart(food_counts)
            
            # Average water intake
            avg_water = filtered_diet["water_intake"].mean()
            st.metric("Average Daily Water Intake", f"{avg_water:.1f} glasses")

    # Export Data
    st.markdown("### Export Data")
    if st.button("Export All Data"):
        # Create Excel writer object
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Export diagnosis history
            if st.session_state.diagnosis_history:
                pd.DataFrame(st.session_state.diagnosis_history).to_excel(writer, sheet_name="Diagnoses", index=False)
            
            # Export pain history
            if st.session_state.pain_history:
                pd.DataFrame(st.session_state.pain_history).to_excel(writer, sheet_name="Pain_History", index=False)
            
            # Export exercise history
            if "exercise_history" in st.session_state:
                pd.DataFrame(st.session_state.exercise_history).to_excel(writer, sheet_name="Exercise", index=False)
            
            # Export diet history
            if "diet_history" in st.session_state:
                pd.DataFrame(st.session_state.diet_history).to_excel(writer, sheet_name="Diet", index=False)

        # Provide download button
        st.download_button(
            label="Download Excel Report",
            data=output.getvalue(),
            file_name="arthritis_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
