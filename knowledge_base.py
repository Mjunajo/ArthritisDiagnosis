knowledge_base = [
    {"if": ["joint_pain", "morning_stiffness", "swelling"], "then": "rheumatoid_arthritis"},
    {"if": ["joint_pain", "age_50+", "bone_spurs"], "then": "osteoarthritis"},
    {"if": ["joint_pain", "redness", "fever"], "then": "infectious_arthritis"},
    {"if": ["joint_pain", "skin_rashes", "eye_inflammation"], "then": "psoriatic_arthritis"},
    {"if": ["joint_pain", "back_pain", "stiff_spine"], "then": "ankylosing_spondylitis"},
    # Add more rules as needed
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
        },
        {
            "name": "Biologic Agents",
            "description": "Target specific parts of the immune system to reduce inflammation.",
            "usage": "Injected or infused at intervals specified by a doctor."
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
        },
        {
            "name": "Joint Injections",
            "description": "Injected steroids to reduce joint pain and swelling.",
            "usage": "Administered by a healthcare professional as needed."
        }
    ],
    "infectious_arthritis": [
        {
            "name": "Antibiotics",
            "description": "Treats bacterial infections causing arthritis.",
            "usage": "Taken as a complete course, strictly as prescribed."
        },
        {
            "name": "Drainage Procedures",
            "description": "Removes infected joint fluid to relieve pain and pressure.",
            "usage": "Performed in a medical setting when required."
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
        },
        {
            "name": "NSAIDs",
            "description": "Provides relief from pain and inflammation.",
            "usage": "Used as needed for symptom control."
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
            "usage": "Injected under the skin or through an IV, per doctor’s recommendation."
        },
        {
            "name": "Physical Therapy",
            "description": "Improves posture, flexibility, and spine health.",
            "usage": "Done regularly under the guidance of a therapist."
        }
    ],
    # Add similar entries for other conditions as needed.
}
