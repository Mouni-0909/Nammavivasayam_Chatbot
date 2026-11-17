
import streamlit as st
from pathlib import Path
import base64

from rag_engine import ask_graph
from guardrails import check_input, check_output


# 1. Page configuration
st.set_page_config(
    page_title="Namma Vivasayam",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# 2. Website styling
st.markdown("""
<style>
.stApp {
    background: #F8FAF6;
}

/* Keep content below Streamlit toolbar */
.block-container {
    max-width: 1100px;
    padding-top: 3.5rem !important;
    padding-bottom: 2rem !important;
}

/* Navigation title */
.site-name {
    color: #20583A;
    font-size: 1.2rem;
    font-weight: 750;
    line-height: 1.6;
    padding: 8px 0;
    margin: 0;
}

/* Compact language selector */
div[role="radiogroup"] {
    display: flex;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
}

/* Hero banner */
.hero {
    background: #174B32;
    border-radius: 18px;
    padding: 28px 35px;
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 25px;
    box-sizing: border-box;
}

.hero-text {
    flex: 1;
    min-width: 0;
}

.hero-title {
    color: white;
    font-size: 2rem;
    font-weight: 750;
    line-height: 1.4;
    margin: 0;
    padding: 4px 0;
}

.hero-tamil {
    color: #E7F5E9;
    font-size: 1.1rem;
    font-weight: 600;
    line-height: 1.5;
    margin-top: 8px;
}

.hero-description {
    color: #D1E8D7;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-top: 12px;
}

.hero-image {
    width: 35%;
    max-height: 180px;
    object-fit: contain;
    border-radius: 12px;
}

/* Assistant heading */
.assistant-title {
    color: #245B39;
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.5;
    padding: 6px 0;
}

/* Compact question form */
div[data-testid="stForm"] {
    border: none;
    padding: 0;
    background: transparent;
}

/* Question input */
div[data-testid="stTextInput"] input {
    border-radius: 10px;
    min-height: 42px;
    background: white;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #D6E5D8;
    background: white;
    color: #245B39;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #245B39;
    color: #245B39;
}

/* Ask button */
div[data-testid="stFormSubmitButton"] button {
    background: #246B45;
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 42px;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #174B32;
    color: white;
}

/* Conversation messages */
div[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #E1EAE1;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 8px;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding-top: 3.5rem !important;
    }

    .hero {
        flex-direction: column;
        align-items: stretch;
        padding: 20px;
        gap: 14px;
    }

    .hero-title {
        font-size: 1.5rem;
    }

    .hero-tamil {
        font-size: 0.95rem;
    }

    .hero-image {
        width: 100%;
        max-height: 160px;
    }

    .assistant-title {
        font-size: 1.2rem;
    }
}
</style>
""", unsafe_allow_html=True)


# 3. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# 4. Navigation and language selector
nav_left, nav_right = st.columns(
    [4, 2],
    vertical_alignment="center"
)

with nav_left:
    st.markdown(
        '<div class="site-name">🌾 Namma Vivasayam</div>',
        unsafe_allow_html=True
    )

with nav_right:
    language = st.radio(
        "Language / மொழி",
        ["English", "தமிழ்"],
        horizontal=True,
        key="language",
        label_visibility="collapsed"
    )

tamil = language == "தமிழ்"


# 5. Hero banner
banner = Path(__file__).parent / "assets" / "agri_banner.png"

image_html = ""

if banner.exists():
    image_data = base64.b64encode(
        banner.read_bytes()
    ).decode("utf-8")

    image_html = (
        f'<img class="hero-image" '
        f'src="data:image/png;base64,{image_data}" '
        f'alt="Tamil Nadu farmer">'
    )

description = (
    "தமிழக விவசாயத் திட்டங்கள், மானியங்கள் மற்றும் அரசு உதவிகள்"
    if tamil else
    "Your guide to Tamil Nadu agricultural schemes, subsidies and benefits"
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-text">
            <div class="hero-title">Namma Vivasayam</div>
            <div class="hero-tamil">
                நம்ம விவசாயம் – உழவர் நலத் திட்ட வழிகாட்டி
            </div>
            <div class="hero-description">
                {description}
            </div>
        </div>
        {image_html}
    </div>
    """,
    unsafe_allow_html=True
)


# 6. Assistant heading
st.markdown(
    '<div class="assistant-title">விவசாயத் திட்ட உதவியாளர்</div>'
    if tamil else
    '<div class="assistant-title">Agricultural Scheme Assistant</div>',
    unsafe_allow_html=True
)


# 7. Welcome message
if not st.session_state.messages:
    st.info(
        "வணக்கம்! விவசாயத் திட்டங்களைப் பற்றி உங்கள் கேள்வியை கேளுங்கள்."
        if tamil else
        "Welcome! Ask about agricultural schemes, subsidies and eligibility."
    )


# 8. Question input, Ask and Clear Chat
form_col, clear_col = st.columns(
    [6, 1.4],
    vertical_alignment="bottom"
)

with form_col:
    with st.form("question_form", clear_on_submit=True):

        input_col, ask_col = st.columns(
            [5, 1],
            vertical_alignment="bottom"
        )

        with input_col:
            question = st.text_input(
                "உங்கள் கேள்வி" if tamil else "Your Question",
                placeholder=(
                    "உங்கள் கேள்வியை இங்கே எழுதுங்கள்..."
                    if tamil else
                    "Ask about government schemes..."
                ),
                label_visibility="collapsed",
                max_chars=500
            )

        with ask_col:
            submitted = st.form_submit_button(
                "கேள்" if tamil else "Ask",
                use_container_width=True
            )

with clear_col:
    if st.button(
        "உரையாடலை அழி" if tamil else "Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# 9. Suggested questions
suggestions = (
    [
        "பிஎம் கிசான் பயன்கள்?",
        "பாசன மானியம்?",
        "திட்டத் தகுதிகள்?"
    ]
    if tamil else
    [
        "PM-KISAN benefits?",
        "Irrigation subsidy?",
        "Scheme eligibility?"
    ]
)

selected_question = None
columns = st.columns(3)

for i, suggestion in enumerate(suggestions):
    with columns[i]:
        if st.button(
            suggestion,
            key=f"suggestion_{language}_{i}",
            use_container_width=True
        ):
            selected_question = suggestion


# 10. Process question using Guardrails + Neo4j
user_question = (
    question.strip()
    if submitted else
    selected_question
)

if user_question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # First guardrail: validate user input
    allowed, message = check_input(
        user_question,
        language
    )

    if not allowed:
        # Block unsafe or unrelated questions
        answer = message

    else:
        try:
            with st.spinner(
                "தகவல்கள் தேடப்படுகின்றன..."
                if tamil else
                "Searching agricultural schemes..."
            ):

                # Retrieve answer from Neo4j GraphRAG
                answer, _ = ask_graph(
                    user_question,
                    language
                )

                # Second guardrail: validate output
                answer = check_output(
                    answer,
                    language
                )

        except Exception:
            answer = (
                "தகவலைப் பெற முடியவில்லை. மீண்டும் முயற்சிக்கவும்."
                if tamil else
                "Unable to retrieve information. Please try again."
            )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# 11. Display conversation
if st.session_state.messages:

    st.markdown(
        "#### உரையாடல்"
        if tamil else
        "#### Conversation"
    )

    messages = st.session_state.messages

    # Latest question and answer first
    for i in range(len(messages) - 2, -1, -2):

        with st.chat_message("user"):
            st.write(messages[i]["content"])

        with st.chat_message("assistant"):
            st.markdown(messages[i + 1]["content"])


# 12. Footer
st.caption(
    "திட்ட விவரங்களை அதிகாரப்பூர்வ அரசு இணையதளங்களில் சரிபார்க்கவும்."
    if tamil else
    "Please verify scheme details with official government sources."
)
