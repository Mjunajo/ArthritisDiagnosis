knowledge_base = [
    {"if": ["joint_pain", "morning_stiffness", "swelling"], "then": "rheumatoid_arthritis"},
    {"if": ["joint_pain", "age_50+", "bone_spurs"], "then": "osteoarthritis"},
    {"if": ["joint_pain", "redness", "fever"], "then": "infectious_arthritis"},
    {"if": ["joint_pain", "skin_rashes", "eye_inflammation"], "then": "psoriatic_arthritis"},
    {"if": ["joint_pain", "back_pain", "stiff_spine"], "then": "ankylosing_spondylitis"},
    # Add more rules as needed
]

medications = {
    "rheumatoid_arthritis": ["Methotrexate", "Corticosteroids", "Biologic Agents"],
    "osteoarthritis": ["NSAIDs", "Acetaminophen", "Joint Injections"],
    "infectious_arthritis": ["Antibiotics", "Drainage Procedures"],
    "psoriatic_arthritis": ["DMARDs", "Biologics", "NSAIDs"],
    "ankylosing_spondylitis": ["NSAIDs", "TNF Blockers", "Physical Therapy"]
}
