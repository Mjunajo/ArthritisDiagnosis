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
    /* Enhanced text readability */
    p, li {
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        letter-spacing: 0.3px !important;
    }
    
    /* Headers styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        letter-spacing: 0.5px !important;
    }
    
    h2, h3 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        letter-spacing: 0.3px !important;
    }
    
    /* Improved multiselect styling */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        margin: 3px !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px -1px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* Enhanced boxes */
    .diagnosis-box, .medication-box {
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Warning text */
    .warning {
        color: #DC2626 !important;
        font-size: 0.95rem !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    knowledge_base = [
        {
            "if": ["joint_pain", "morning_stiffness", "swelling", "fatigue", "fever"],
            "then": "rheumatoid_arthritis",
            "confidence": 0.90
        },
        {
            "if": ["joint_pain", "age_50+", "bone_spurs", "joint_crackling", "morning_stiffness"],
            "then": "osteoarthritis",
            "confidence": 0.88
        },
        {
            "if": ["joint_pain", "redness", "fever", "chills", "joint_swelling"],
            "then": "infectious_arthritis",
            "confidence": 0.85
        },
        {
            "if": ["joint_pain", "skin_rashes", "eye_inflammation", "nail_pitting", "fatigue"],
            "then": "psoriatic_arthritis",
            "confidence": 0.87
        },
        {
            "if": ["joint_pain", "back_pain", "stiff_spine", "fatigue", "eye_inflammation"],
            "then": "ankylosing_spondylitis",
            "confidence": 0.86
        },
        {
            "if": ["joint_pain", "butterfly_rash", "fatigue", "fever", "kidney_problems"],
            "then": "lupus_arthritis",
            "confidence": 0.85
        },
        {
            "if": ["joint_pain", "muscle_weakness", "skin_rash", "fatigue", "weight_loss"],
            "then": "inflammatory_myopathy",
            "confidence": 0.82
        },
        {
            "if": ["joint_pain", "skin_tightness", "raynauds_phenomenon", "fatigue"],
            "then": "systemic_sclerosis",
            "confidence": 0.83
        },
        {
            "if": ["joint_pain", "dry_eyes", "dry_mouth", "fatigue", "joint_swelling"],
            "then": "sjogrens_syndrome",
            "confidence": 0.84
        },
        {
            "if": ["joint_pain", "uric_acid_crystals", "red_joints", "sudden_pain"],
            "then": "gout",
            "confidence": 0.89
        }
    ]
    
    medications = {
        "rheumatoid_arthritis": [
            {
                "name": "Methotrexate",
                "description": "A disease-modifying drug that reduces inflammation and prevents joint damage.",
                "usage": "Taken weekly, preferably at the same time each week."
            },
            {
                "name": "Biologics",
                "description": "Advanced medications that target specific parts of the immune system.",
                "usage": "Administered by injection or infusion as prescribed."
            }
        ],
        "osteoarthritis": [
            {
                "name": "Acetaminophen",
                "description": "Pain reliever that helps manage osteoarthritis pain.",
                "usage": "Taken as needed for pain relief."
            },
            {
                "name": "NSAIDs",
                "description": "Anti-inflammatory medications that reduce pain and swelling.",
                "usage": "Taken daily or as needed according to prescription."
            }
        ],
        "infectious_arthritis": [
            {
                "name": "Antibiotics",
                "description": "Treats the underlying infection causing the arthritis.",
                "usage": "Course prescribed by doctor, usually for several weeks."
            },
            {
                "name": "Anti-inflammatory medications",
                "description": "Helps reduce joint inflammation and pain.",
                "usage": "Taken as prescribed alongside antibiotics."
            }
        ],
        "psoriatic_arthritis": [
            {
                "name": "DMARDs",
                "description": "Disease-modifying drugs that slow joint damage.",
                "usage": "Regular dosing as prescribed by rheumatologist."
            },
            {
                "name": "TNF Inhibitors",
                "description": "Biologics that target specific inflammation pathways.",
                "usage": "Injections or infusions on a set schedule."
            }
        ],
        "ankylosing_spondylitis": [
            {
                "name": "NSAIDs",
                "description": "First-line treatment for pain and stiffness.",
                "usage": "Regular dosing to maintain anti-inflammatory effect."
            },
            {
                "name": "TNF Blockers",
                "description": "Biological medications for severe cases.",
                "usage": "Regular injections as prescribed."
            }
        ],
        "lupus_arthritis": [
            {
                "name": "Hydroxychloroquine",
                "description": "An antimalarial drug that helps control lupus symptoms.",
                "usage": "Taken daily as prescribed by your doctor."
            },
            {
                "name": "Belimumab",
                "description": "A biologic medication specifically for lupus.",
                "usage": "Administered through IV infusion or injection."
            }
        ],
        "inflammatory_myopathy": [
            {
                "name": "Corticosteroids",
                "description": "Reduces inflammation in muscles and joints.",
                "usage": "Taken daily, dose may be tapered over time."
            },
            {
                "name": "Immunosuppressants",
                "description": "Helps control the immune system response.",
                "usage": "Regular dosing as prescribed by specialist."
            }
        ],
        "systemic_sclerosis": [
            {
                "name": "Immunosuppressants",
                "description": "Helps manage autoimmune aspects of the condition.",
                "usage": "Taken regularly as prescribed."
            },
            {
                "name": "Vasodilators",
                "description": "Improves circulation and reduces Raynaud's symptoms.",
                "usage": "Taken daily or as needed for symptoms."
            }
        ],
        "sjogrens_syndrome": [
            {
                "name": "Hydroxychloroquine",
                "description": "Helps manage joint pain and fatigue.",
                "usage": "Daily oral medication as prescribed."
            },
            {
                "name": "Pilocarpine",
                "description": "Helps with dry mouth and eyes symptoms.",
                "usage": "Taken multiple times daily as needed."
            }
        ],
        "gout": [
            {
                "name": "Colchicine",
                "description": "Reduces gout pain and inflammation during attacks.",
                "usage": "Taken as needed during gout attacks."
            },
            {
                "name": "Allopurinol",
                "description": "Helps prevent gout attacks by lowering uric acid levels.",
                "usage": "Taken daily for prevention."
            }
        ]
    }
    
    return knowledge_base, medications

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
                    "total_symptoms": total_symptoms
                })
    
    return sorted(diagnoses, key=lambda x: x["confidence"], reverse=True)

# Ensure medications are shown only for the diagnosed condition
def get_medications(diagnosis, medications):
    if not diagnosis:
        return []  # Return an empty list if no diagnosis
    meds = medications.get(diagnosis, [])
    for med in meds:
        med["warning"] = "Please consult a healthcare professional before taking any medication."
    return meds

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

    selected_symptoms = joint_symptoms + systemic_symptoms + skin_symptoms + other_symptoms

    if st.button("Generate Diagnosis", help="Click to analyze your symptoms"):
        if not selected_symptoms:
            st.error("⚠️ Please select at least one symptom for diagnosis.")
        else:
            knowledge_base, medications = load_data()
            diagnoses = forward_chaining(knowledge_base, selected_symptoms)
            
            if diagnoses:
                # Only display the top diagnosis for medications
                top_diagnosis = diagnoses[0]
                confidence_color = "green" if top_diagnosis["confidence"] > 0.8 else "orange"
                st.markdown(f"""
                    <div class="diagnosis-box" style="border: 2px solid {confidence_color}">
                        <h3>{top_diagnosis["condition"].replace("_", " ").title()}</h3>
                        <p>Confidence: {top_diagnosis["confidence"]*100:.1f}%</p>
                        <p>Matching Symptoms: {top_diagnosis["matching_symptoms"]}/{top_diagnosis["total_symptoms"]}</p>
                    </div>
                """, unsafe_allow_html=True)

                meds = get_medications(top_diagnosis["condition"], medications)
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
                    st.warning("No medications available for this diagnosis.")
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
