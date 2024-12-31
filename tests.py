from reasoning_engine import forward_chaining

def test_forward_chaining():
    knowledge_base = [
        {"if": ["joint_pain", "morning_stiffness"], "then": "rheumatoid_arthritis"}
    ]
    symptoms = ["joint_pain", "morning_stiffness"]
    assert forward_chaining(knowledge_base, symptoms) == ["rheumatoid_arthritis"]
