knowledge_base = [
    {"if": ["joint_pain", "morning_stiffness", "swelling"], "then": "rheumatoid_arthritis"},
    {"if": ["joint_pain", "age_50+", "bone_spurs", "joint_crackling"], "then": "osteoarthritis"},
    {"if": ["joint_pain", "redness", "fever", "chills"], "then": "infectious_arthritis"},
    {"if": ["joint_pain", "skin_rashes", "eye_inflammation", "nail_pitting"], "then": "psoriatic_arthritis"},
    {"if": ["joint_pain", "back_pain", "stiff_spine", "fatigue"], "then": "ankylosing_spondylitis"},
    {"if": ["joint_pain", "weight_loss", "fever", "night_sweats"], "then": "tubercular_arthritis"},
    {"if": ["joint_pain", "abdominal_pain", "diarrhea"], "then": "enteropathic_arthritis"},
    # Add more rules as needed
]

medications = {
    "rheumatoid_arthritis": ["Methotrexate", "Corticosteroids", "Biologic Agents"],
    "osteoarthritis": ["NSAIDs", "Acetaminophen", "Joint Injections"],
    "infectious_arthritis": ["Antibiotics", "Drainage Procedures"],
    "psoriatic_arthritis": ["DMARDs", "Biologics", "NSAIDs"],
    "ankylosing_spondylitis": ["NSAIDs", "TNF Blockers", "Physical Therapy"],
    "tubercular_arthritis": ["Anti-Tubercular Drugs (Rifampicin, Isoniazid)", "Pain Relievers"],
    "enteropathic_arthritis": ["Corticosteroids", "Immunosuppressants"],
}
