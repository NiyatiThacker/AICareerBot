import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')

from nltk.data import find

def ensure_nltk_resources():
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger")
    ]
    for path, name in resources:
        try:
            find(path)
        except LookupError:
            nltk.download(name)

ensure_nltk_resources()


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from difflib import get_close_matches
from intents_data_enhanced import intents

# 📦 Download NLTK resources (only once)
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

# 🔧 POS tag mapping
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# ✨ Clean user input
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos))
        for word, pos in tagged
        if word.isalpha() and word not in stopwords.words('english')
    ]

# 🧠 Empathy detector
def detect_emotion(user_input):
    sad_keywords = [
        "confused", "don’t know", "don’t have idea", "no idea", "not sure",
        "not interested", "stuck", "nothing", "hopeless", "fail", "idk", "i don't know"
    ]
    lowered = user_input.lower()
    for word in sad_keywords:
        if word in lowered:
            return "confused"
    return "okay"

# 🧠 Detect intents with fuzzy keyword matching


def detect_intents(tokens):
    detected = set()

    for intent, data in intents.items():
        keywords = [k.lower() for k in data.get("keywords", [])]

        for token in tokens:
            # Prefer exact match first
            if token in keywords:
                detected.add(intent)
                if "inherits_from" in data:
                    detected.add(data["inherits_from"])
                break  # No need to check further if matched exactly

            # Fallback: allow fuzzy match only if intent allows it
            if data.get("allow_fuzzy", True):  # Add this flag to control per intent
                matches = get_close_matches(token, keywords, n=1, cutoff=0.85)
                if matches:
                    detected.add(intent)
                    if "inherits_from" in data:
                        detected.add(data["inherits_from"])
                    break

    return sorted(detected)


# 🧩 Detect fusion domains
def detect_fusion_domains(intents_list):
    combos = []
    for i in range(len(intents_list)):
        for j in range(i + 1, len(intents_list)):
            a, b = intents_list[i], intents_list[j]
            fusion_key = f"{a}+{b}"
            alt_key = f"{b}+{a}"
            if fusion_key in intents or alt_key in intents:
                combos.append(fusion_key if fusion_key in intents else alt_key)
    return combos

# 🧠 Detect if user typed a career name instead of domain

def detect_possible_career(user_input):
    user_input = user_input.lower().strip()
    user_tokens = set(user_input.split())

    matched_domains = set()

    for domain, data in intents.items():
        for career in data.get("careers", []):
            career_lower = career.lower()
            career_tokens = set(career_lower.split())

            # Exact or partial match
            if user_input in career_lower or user_tokens & career_tokens:
                matched_domains.add((domain, career))

            # Acronym match (e.g. ias = IAS Officer)
            initials = ''.join(word[0] for word in career_tokens if word)
            if user_input == initials.lower():
                matched_domains.add((domain, career))

            # Fuzzy match
            matches = get_close_matches(user_input, [career_lower], n=1, cutoff=0.75)
            if matches:
                matched_domains.add((domain, career))

    return list(matched_domains)
