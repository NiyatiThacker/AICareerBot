
from intents_data_enhanced import intents

def get_all_detected_intents(detected_intents):
    """
    Returns both individual and fusion domains if multiple interests are detected.
    Example: ['tech', 'arts'] → ['tech', 'arts', 'tech+arts']
    """
    all_combined = detected_intents.copy()

    # Add fusion combinations
    for i in range(len(detected_intents)):
        for j in range(i + 1, len(detected_intents)):
            combo = f"{detected_intents[i]}+{detected_intents[j]}"
            reverse_combo = f"{detected_intents[j]}+{detected_intents[i]}"
            if combo in intents:
                all_combined.append(combo)
            elif reverse_combo in intents:
                all_combined.append(reverse_combo)

    return all_combined


def get_careers_for_intent(intent):
    """
    Returns a list of careers for the selected domain/intent.
    """
    return intents.get(intent, {}).get("careers", [])


def get_career_info(career_name):
    """
    Looks through all intents to find a career match and return full info.
    """
    for data in intents.values():
        for career in data.get("careers", []):
            if career.lower() == career_name.lower():
                return {
                    "skills": data.get("skills", []),
                    "roadmap": data.get("roadmap", []),
                    "resources": data.get("resources", [])
                }
    return None


# Test if needed
if __name__ == "__main__":
    print(get_all_detected_intents(["tech", "arts"]))
    print(get_careers_for_intent("tech+arts"))
    print(get_career_info("Game Designer"))
