# chat_engine.py

from nlp_engine import preprocess_text, detect_intents, detect_emotion, detect_possible_career, detect_fusion_domains
from career_logic import get_all_detected_intents, get_careers_for_intent, get_career_info
from intents_data_enhanced import intents

domain_emojis = {
    "tech": "🧑‍💻", "arts": "🎨", "media": "🎬", "healthcare": "🩺", "commerce": "💼",
    "psychology": "🧠", "public-administration": "🏛️", "aviation": "✈️", "design": "🖌️",
    "defence": "🪖", "education": "🏫", "hospitality": "🍽️", "sports": "🏅", "law": "⚖️",
    "linguistics": "📚", "dance": "💃", "music": "🎵", "gaming": "🎮", "fashion": "👗",
    "photography": "📸", "writing": "✍️", "environment": "🌿"
}

def get_bot_response(user_input):
    response = {
        "status": "ok",
        "emotion": None,
        "detected_domains": [],
        "selected_domain": None,
        "career_options": [],
        "selected_career": None,
        "career_info": None,
        "message": "",
    }

    emotion = detect_emotion(user_input)
    response["emotion"] = emotion
    if emotion == "confused":
        response["message"] = "You seem unsure. Think of anything you’ve enjoyed — music, tech, talking to people?"
        response["status"] = "confused"
        return response

    tokens = preprocess_text(user_input)
    detected_domains = get_all_detected_intents(detect_intents(tokens))
    fusion_domains = detect_fusion_domains(detected_domains)
    for fusion in fusion_domains:
        if fusion not in detected_domains:
            detected_domains.append(fusion)

    if detected_domains:
        response["detected_domains"] = detected_domains
        response["message"] = "Found relevant domains based on your interests."
        return response

    matched_careers = detect_possible_career(user_input)
    if matched_careers:
        career_domains = list(set(domain for domain, _ in matched_careers))
        response["detected_domains"] = career_domains
        response["message"] = "Matched your input to known careers."
        return response

    response["status"] = "not_found"
    response["message"] = "Couldn’t detect a relevant domain or career. Try something else."
    return response

def get_career_response(domain: str, career: str = None):
    response = {
        "selected_domain": domain,
        "career_options": [],
        "selected_career": career,
        "career_info": None,
        "status": "ok",
        "message": ""
    }

    careers = get_careers_for_intent(domain)
    if not careers:
        response["status"] = "no_careers"
        response["message"] = "No careers found under this domain."
        return response

    response["career_options"] = careers

    if career and career in careers:
        info = get_career_info(career)
        if info:
            response["career_info"] = info
            response["message"] = f"Details for {career}"
        else:
            response["message"] = "Career selected but info missing."
    else:
        response["message"] = f"Here are career options under {domain.title()}."

    return response
