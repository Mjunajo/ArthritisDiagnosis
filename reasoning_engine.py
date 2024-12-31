def forward_chaining(knowledge_base, symptoms):
    inferred = set(symptoms)
    for rule in knowledge_base:
        if set(rule["if"]).issubset(inferred):
            inferred.add(rule["then"])
    return [item for item in inferred if item not in symptoms]

def get_medications(diagnosis, medications):
    return medications.get(diagnosis, [])
