
import re

# Words related to our agricultural chatbot
TOPICS = [
    "farmer", "farming", "agriculture", "crop",
    "scheme", "subsidy", "benefit", "eligibility",
    "irrigation", "pm-kisan", "kisan", "kaviadp",
    "government", "document", "application",
    "soil", "seed", "fertilizer", "loan",
    "விவசாய", "உழவர்", "விவசாயி", "திட்ட",
    "மானிய", "பயன்", "தகுதி", "பாசன",
    "வேளாண்", "கிசான்", "ஆவண"
]

# Common prompt injection phrases
BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal your system prompt",
    "show your system prompt",
    "developer instructions",
    "bypass your rules",
    "disable guardrails",
    "forget your instructions"
]


def check_input(question, language):
    """Check a question before sending it to Neo4j."""

    tamil = language == "தமிழ்"
    text = question.strip()
    lower = text.lower()

    if not text:
        return False, "கேள்வியை உள்ளிடவும்." if tamil else "Please enter a question."

    if len(text) > 500:
        return False, (
            "கேள்வியை 500 எழுத்துகளுக்குள் எழுதவும்."
            if tamil else
            "Please keep your question under 500 characters."
        )

    # Aadhaar-like 12-digit numbers
    if re.search(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)", text):
        return False, (
            "ஆதார் எண்ணைப் பகிர வேண்டாம்."
            if tamil else
            "Please do not share Aadhaar numbers."
        )

    # Indian mobile numbers
    if re.search(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", text):
        return False, (
            "தொலைபேசி எண்ணைப் பகிர வேண்டாம்."
            if tamil else
            "Please do not share personal phone numbers."
        )

    # Email addresses
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        return False, (
            "தனிப்பட்ட மின்னஞ்சல் முகவரியைப் பகிர வேண்டாம்."
            if tamil else
            "Please do not share personal email addresses."
        )

    # Prompt injection
    if any(phrase in lower for phrase in BLOCKED_PHRASES):
        return False, (
            "இந்தக் கோரிக்கைக்கு பதிலளிக்க முடியாது."
            if tamil else
            "I cannot follow requests to override my instructions."
        )

    # Basic topic restriction
    if not any(word in lower for word in TOPICS):
        return False, (
            "விவசாயம் மற்றும் அரசுத் திட்டங்கள் பற்றிய கேள்விகளை கேளுங்கள்."
            if tamil else
            "Please ask about farming or government agricultural schemes."
        )

    return True, ""


def check_output(answer, language):
    """Check the answer before displaying it."""

    tamil = language == "தமிழ்"

    if not answer or not str(answer).strip():
        return (
            "இந்தக் கேள்விக்கான தகவல் தற்போது கிடைக்கவில்லை."
            if tamil else
            "Information is currently unavailable for this question."
        )

    return str(answer)
