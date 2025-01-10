import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Configure Streamlit page settings
st.set_page_config(
    page_title="Arthritis Diagnosis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load knowledge base and medications from JSON files
@st.cache_data
def load_data():
    knowledge_base = [
        {"if": ["joint_pain", "morning_stiffness", "swelling"], "then": "rheumatoid_arthritis", "confidence": 0.85},
        {"if": ["joint_pain", "age_50+", "bone_spurs"], "then": "osteoarthritis", "confidence": 0.80},
        {"if": ["joint_pain", "redness", "fever"], "then": "infectious_arthritis", "confidence": 0.75},
        {"if": ["joint_pain", "skin_rashes", "eye_inflammation"], "then": "psoriatic_arthritis", "confidence": 0.82},
        {"if": ["joint_pain", "back_pain", "stiff_spine"], "then": "ankylosing_spondylitis", "confidence": 0.78},
    ]
    
    medications = {
        "rheumatoid_arthritis": [
            {
                "name": "Methotrexate",
                "description": "A disease-modifying drug that reduces inflammation and prevents joint damage.",
                "usage": "Taken weekly, preferably at the same time each week."
            },
            {
                "name": "Corticosteroids",
                "description": "Helps reduce severe inflammation quickly.",
                "usage": "Used for short-term relief or during flare-ups, as prescribed by a doctor."
            }
        ],
        "osteoarthritis": [
            {
                "name": "NSAIDs",
                "description": "Non-steroidal anti-inflammatory drugs to relieve pain and reduce inflammation.",
                "usage": "Taken as needed for pain relief, usually after meals."
            },
            {
                "name": "Acetaminophen",
                "description": "Helps manage mild to moderate pain.",
                "usage": "Taken up to 4 times a day, but not exceeding the maximum daily dose."
            }
        ],
        "infectious_arthritis": [
            {
                "name": "Antibiotics",
                "description": "Treats bacterial infections causing arthritis.",
                "usage": "Taken as a complete course, strictly as prescribed."
            }
        ],
        "psoriatic_arthritis": [
            {
                "name": "DMARDs",
                "description": "Slow disease progression and prevent joint damage.",
                "usage": "Taken daily or weekly, depending on the prescription."
            },
            {
                "name": "Biologics",
                "description": "Target immune pathways involved in psoriatic arthritis.",
                "usage": "Injected or infused as prescribed by a specialist."
            }
        ],
        "ankylosing_spondylitis": [
            {
                "name": "NSAIDs",
                "description": "Reduce stiffness and inflammation in the spine.",
                "usage": "Taken daily or as needed for symptom relief."
            },
            {
                "name": "TNF Blockers",
                "description": "Target specific immune pathways to reduce inflammation.",
                "usage": "Injected under the skin or through an IV, per doctor's recommendation."
            }
        ]
    }
    
    return knowledge_base, medications

# Enhanced reasoning engine with confidence scoring
def forward_chaining(knowledge_base, symptoms):
    inferred = set(symptoms)
    diagnoses = []
    
    for rule in knowledge_base:
        matching_symptoms = len(set(rule["if"]).intersection(inferred))
        total_symptoms = len(rule["if"])
        if matching_symptoms > 0:
            confidence = (matching_symptoms / total_symptoms) * rule["confidence"]
            if confidence >= 0.5:  # Minimum confidence threshold
                diagnoses.append({
                    "condition": rule["then"],
                    "confidence": confidence,
                    "matching_symptoms": matching_symptoms,
                    "total_symptoms": total_symptoms
                })
    
    return sorted(diagnoses, key=lambda x: x["confidence"], reverse=True)

# Get medications with enhanced information
def get_medications(diagnosis, medications):
    meds = medications.get(diagnosis, [])
    for med in meds:
        med["warning"] = "Please consult a healthcare professional before taking any medication."
    return meds

# Custom CSS with improved styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .diagnosis-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .medication-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .warning {
        color: #ff4b4b;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Project information
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Arthritis Diagnosis System")
    st.markdown("### Project Team")
    st.markdown("- Muhammad Junaid\n- Hamid Shehzad\n- Aneeqa Sabir")
    st.markdown("---")

# Main application
st.title("🏥 Arthritis Diagnosis System")
st.markdown("### Smart Diagnosis Assistant")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Diagnosis", "Information", "History"])

with tab1:
    # Symptom selection with categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Primary Symptoms")
        joint_symptoms = st.multiselect(
            "Joint Symptoms",
            ["joint_pain", "joint_crackling", "morning_stiffness", "swelling"],
            help="Select all applicable joint symptoms"
        )
        
        systemic_symptoms = st.multiselect(
            "Systemic Symptoms",
            ["fever", "chills", "fatigue", "weight_loss", "night_sweats"],
            help="Select any systemic symptoms you're experiencing"
        )
    
    with col2:
        st.subheader("Additional Symptoms")
        skin_symptoms = st.multiselect(
            "Skin Symptoms",
            ["skin_rashes", "nail_pitting", "redness"],
            help="Select any skin-related symptoms"
        )
        
        other_symptoms = st.multiselect(
            "Other Symptoms",
            ["age_50+", "bone_spurs", "back_pain", "stiff_spine", "eye_inflammation"],
            help="Select any other symptoms you're experiencing"
        )

    # Collect all symptoms
    selected_symptoms = joint_symptoms + systemic_symptoms + skin_symptoms + other_symptoms

    # Diagnosis button
    if st.button("Generate Diagnosis", help="Click to analyze your symptoms"):
        if not selected_symptoms:
            st.error("⚠️ Please select at least one symptom for diagnosis.")
        else:
            knowledge_base, medications = load_data()
            diagnoses = forward_chaining(knowledge_base, selected_symptoms)
            
            if diagnoses:
                for diagnosis in diagnoses:
                    confidence_color = "green" if diagnosis["confidence"] > 0.8 else "orange"
                    st.markdown(f"""
                        <div class="diagnosis-box" style="border: 2px solid {confidence_color}">
                            <h3>{diagnosis["condition"].replace("_", " ").title()}</h3>
                            <p>Confidence: {diagnosis["confidence"]*100:.1f}%</p>
                            <p>Matching Symptoms: {diagnosis["matching_symptoms"]}/{diagnosis["total_symptoms"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    meds = get_medications(diagnosis["condition"], medications)
                    if meds:
                        st.markdown("#### Recommended Medications:")
                        for med in meds:
                            st.markdown(f"""
                                <div class="medication-box">
                                    <h4>{med["name"]}</h4>
                                    <p><em>{med["description"]}</em></p>
                                    <p><strong>Usage:</strong> {med["usage"]}</p>
                                    <p class="warning">{med["warning"]}</p>
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning("No definitive diagnosis found. Please consult a healthcare professional.")

with tab2:
    st.markdown("""
        ### About Arthritis
        Arthritis is a term for joint inflammation that can affect people of all ages. Early diagnosis and treatment are crucial for managing symptoms and preventing joint damage.
        
        ### Types of Arthritis
        - **Rheumatoid Arthritis**: An autoimmune condition
        - **Osteoarthritis**: Age-related joint deterioration
        - **Psoriatic Arthritis**: Associated with psoriasis
        - **Ankylosing Spondylitis**: Affects the spine
        
        ### Disclaimer
        This system is for educational purposes only. Always consult a healthcare professional for medical advice.
    """)

with tab3:
    if "diagnosis_history" not in st.session_state:
        st.session_state.diagnosis_history = []
    
    st.markdown("### Previous Diagnoses")
    if st.session_state.diagnosis_history:
        history_df = pd.DataFrame(st.session_state.diagnosis_history)
        st.dataframe(history_df)
    else:
        st.info("No previous diagnoses recorded in this session.")
