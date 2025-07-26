import streamlit as st
import random
from typing import List, Dict, Any
import time

# Import your existing modules (assuming they exist)
try:
    from nlp_engine import preprocess_text, detect_intents, detect_emotion, detect_possible_career, detect_fusion_domains
    from career_logic import get_all_detected_intents, get_careers_for_intent, get_career_info
    from intents_data_enhanced import intents
except ImportError:
    # Mock functions for demonstration if modules don't exist
    def preprocess_text(text): return text.lower().split()
    def detect_intents(tokens): return []
    def detect_emotion(text): return "neutral" if len(text) < 10 else "confused"
    def detect_possible_career(text): return []
    def detect_fusion_domains(domains): return []
    def get_all_detected_intents(intents): return ["tech", "arts", "healthcare"]
    def get_careers_for_intent(domain): return ["Software Developer", "Data Scientist", "Web Designer"]
    def get_career_info(career): 
        return {
            "skills": ["Programming", "Problem Solving", "Communication"],
            "roadmap": ["Learn basics", "Build projects", "Get experience", "Apply for jobs"],
            "resources": ["FreeCodeCamp", "Coursera", "YouTube tutorials"]
        }

# Domain emojis
DOMAIN_EMOJIS = {
    "tech": "🧑‍💻", "arts": "🎨", "media": "🎬", "healthcare": "🩺", "commerce": "💼",
    "psychology": "🧠", "public-administration": "🏛️", "aviation": "✈️", "design": "🖌️",
    "defence": "🪖", "education": "🏫", "hospitality": "🍽️", "sports": "🏅", "law": "⚖️",
    "linguistics": "📚", "dance": "💃", "music": "🎵", "gaming": "🎮", "fashion": "👗",
    "photography": "📸", "writing": "✍️", "environment": "🌿"
}

# Initialize session state
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 Hey! I'm your senior from the future 😁\n\nI'll help you figure out career paths that actually fit your vibe. Let's start by exploring your interests!",
                "timestamp": time.time()
            }
        ]
    if 'conversation_state' not in st.session_state:
        st.session_state.conversation_state = "initial"
    if 'detected_domains' not in st.session_state:
        st.session_state.detected_domains = []
    if 'selected_domain' not in st.session_state:
        st.session_state.selected_domain = ""
    if 'careers_list' not in st.session_state:
        st.session_state.careers_list = []
    if 'selected_career' not in st.session_state:
        st.session_state.selected_career = ""
    if 'user_input_key' not in st.session_state:
        st.session_state.user_input_key = 0

def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": time.time()
    })

def process_user_input(user_input: str):
    """Process user input based on current conversation state"""
    
    # Add user message
    add_message("user", user_input)
    
    if st.session_state.conversation_state == "initial":
        handle_initial_input(user_input)
    elif st.session_state.conversation_state == "domain_selection":
        handle_domain_selection(user_input)
    elif st.session_state.conversation_state == "career_selection":
        handle_career_selection(user_input)
    elif st.session_state.conversation_state == "restart_prompt":
        handle_restart_prompt(user_input)

def handle_initial_input(user_input: str):
    """Handle the initial user input about interests"""
    
    # Check for confused emotion
    if detect_emotion(user_input) == "confused":
        add_message("assistant", "🫂 That's okay! Everyone starts somewhere. Think of anything you've enjoyed — like music, tech, painting, or even chatting with people!")
        return
    
    # Step 1: Domain Detection
    tokens = preprocess_text(user_input)
    detected_domains = get_all_detected_intents(detect_intents(tokens))
    
    # Add fusion domains
    fusion_domains = detect_fusion_domains(detected_domains)
    for fusion in fusion_domains:
        if fusion not in detected_domains:
            detected_domains.append(fusion)
    
    if detected_domains:
        st.session_state.detected_domains = detected_domains
        st.session_state.conversation_state = "domain_selection"
        
        response = "✅ Based on what you said, I found these areas of interest:\n\n"
        for idx, domain in enumerate(detected_domains, 1):
            icon = "⚡" if "+" in domain else "🧠"
            response += f"{idx}. {icon} **{domain.title()}**\n"
        response += "\n👉 Pick one domain by typing its **name** or **number**:"
        add_message("assistant", response)
        
    else:
        # Step 2: Career Detection Fallback
        matched_careers = detect_possible_career(user_input)
        if matched_careers:
            response = "💭 Based on what you typed, here's what I found:\n\n"
            career_domains = []
            for domain, career in matched_careers:
                response += f"• Looks like **{career}** (under {domain.replace('-', ' ').title()})\n"
                if domain not in career_domains:
                    career_domains.append(domain)
            
            if career_domains:
                st.session_state.detected_domains = career_domains
                st.session_state.conversation_state = "domain_selection"
                response += "\n👉 Want to explore these paths? Type **yes** to continue or share another interest:"
            
            add_message("assistant", response)
        else:
            add_message("assistant", "🤔 Hmm, couldn't find a matching domain or career. Can you rephrase or share another interest?")

def handle_domain_selection(user_input: str):
    """Handle domain selection"""
    selected_domain = ""
    
    # Check if user typed a number
    if user_input.isdigit():
        try:
            index = int(user_input) - 1
            if 0 <= index < len(st.session_state.detected_domains):
                selected_domain = st.session_state.detected_domains[index]
        except (ValueError, IndexError):
            add_message("assistant", "⚠️ Invalid number. Please try again.")
            return
    else:
        # Check for name match
        matches = [d for d in st.session_state.detected_domains if user_input.lower() in d.lower()]
        if matches:
            selected_domain = matches[0]
        elif user_input.lower() in ["yes", "y"]:
            # If they said yes to explore careers, pick the first domain
            if st.session_state.detected_domains:
                selected_domain = st.session_state.detected_domains[0]
    
    if selected_domain:
        st.session_state.selected_domain = selected_domain
        careers = get_careers_for_intent(selected_domain)
        
        if careers:
            st.session_state.careers_list = careers
            st.session_state.conversation_state = "career_selection"
            
            # Get emoji for domain
            base = selected_domain.lower().split("+")[0]
            emoji = DOMAIN_EMOJIS.get(base, "💡")
            
            response = f"🎓 Career paths under **{selected_domain.title()}**:\n\n"
            for i, career in enumerate(careers, 1):
                response += f"{i}. {emoji} **{career}**\n"
            response += "\n👉 Choose one career you're most interested in (number, name, or say **'surprise me'**):"
            
            add_message("assistant", response)
        else:
            add_message("assistant", "⚠️ Sorry, couldn't find careers for that domain. Let's start again with a different interest!")
            reset_conversation()
    else:
        add_message("assistant", "⚠️ Couldn't match that to a domain. Please try again with the domain name or number.")

def handle_career_selection(user_input: str):
    """Handle career selection and show career info"""
    selected_career = ""
    
    if user_input.lower() == "surprise me":
        selected_career = random.choice(st.session_state.careers_list)
        add_message("assistant", f"🎁 Surprise career for you: **{selected_career}**!")
    elif user_input.isdigit():
        try:
            index = int(user_input) - 1
            if 0 <= index < len(st.session_state.careers_list):
                selected_career = st.session_state.careers_list[index]
        except (ValueError, IndexError):
            add_message("assistant", "⚠️ Invalid number. Please try again.")
            return
    else:
        # Check for name match
        matches = [c for c in st.session_state.careers_list if user_input.lower() in c.lower()]
        if matches:
            selected_career = matches[0]
    
    if selected_career:
        st.session_state.selected_career = selected_career
        show_career_info(selected_career)
        st.session_state.conversation_state = "restart_prompt"
    else:
        add_message("assistant", "⚠️ Couldn't find that career. Please try again with the career name or number.")

def show_career_info(career: str):
    """Display detailed career information"""
    info = get_career_info(career)
    
    response = f"🔍 **Info for {career}:**\n\n"
    
    # Skills section
    response += "🛠️ **Must-Know Skills:**\n"
    for skill in info.get("skills", []):
        response += f"• {skill}\n"
    
    # Roadmap section
    response += "\n📈 **Roadmap:**\n"
    for step in info.get("roadmap", []):
        response += f"• {step}\n"
    
    # Resources section
    if info.get("resources"):
        response += "\n📚 **Free Learning Resources:**\n"
        for res in info["resources"]:
            response += f"• {res}\n"
    else:
        response += "\n📚 **Free Learning Resources:** Coming soon...\n"
    
    response += "\n🔁 Want to explore another path? Type **'yes'** to continue or **'exit'** to finish:"
    
    add_message("assistant", response)

def handle_restart_prompt(user_input: str):
    """Handle restart or exit decision"""
    if user_input.lower() in ["yes", "y", "restart", "continue"]:
        add_message("assistant", "🔁 Great! Let's explore another career path. What are your interests or subjects you enjoy?")
        reset_conversation()
    elif user_input.lower() in ["exit", "quit", "bye", "no"]:
        add_message("assistant", "👋 Catch you later — you've got this! 🚀")
        st.session_state.conversation_state = "ended"
    else:
        add_message("assistant", "Please type **'yes'** to explore more careers or **'exit'** to finish.")

def reset_conversation():
    """Reset conversation to initial state"""
    st.session_state.conversation_state = "initial"
    st.session_state.detected_domains = []
    st.session_state.selected_domain = ""
    st.session_state.careers_list = []
    st.session_state.selected_career = ""

def main():
    # Page config
    st.set_page_config(
        page_title="Career Guidance Chatbot",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for modern chatbot UI
    st.markdown("""
    <style>
    .main > div {
        padding: 2rem 1rem;
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        margin-left: 20%;
        text-align: right;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-right: 20%;
    }
    
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Title
    st.markdown('<h1 class="title-gradient">🎯 Career Guidance Chatbot</h1>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-bottom: 2rem; color: #666; font-size: 1.1rem;'>Your AI senior helping you discover the perfect career path! 🚀</div>", unsafe_allow_html=True)
    
    # Chat interface
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Chat messages container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="stChatMessage user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stChatMessage assistant-message">
                        <strong>AI Career Guide:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input area
        if st.session_state.conversation_state != "ended":
            # Create a form for better UX
            with st.form(key=f"chat_form_{st.session_state.user_input_key}", clear_on_submit=True):
                user_input = st.text_input(
                    "Type your message here...", 
                    placeholder="Share your interests, pick a domain, or ask questions!",
                    key=f"user_input_{st.session_state.user_input_key}"
                )
                
                col_send, col_restart = st.columns([3, 1])
                
                with col_send:
                    send_button = st.form_submit_button("Send 📤", use_container_width=True)
                
                with col_restart:
                    restart_button = st.form_submit_button("Restart 🔄", use_container_width=True)
                
                if send_button and user_input.strip():
                    process_user_input(user_input.strip())
                    st.session_state.user_input_key += 1
                    st.rerun()
                
                if restart_button:
                    st.session_state.messages = [
                        {
                            "role": "assistant", 
                            "content": "👋 Hey! I'm your senior from the future 😁\n\nI'll help you figure out career paths that actually fit your vibe. Let's start fresh!",
                            "timestamp": time.time()
                        }
                    ]
                    reset_conversation()
                    st.session_state.user_input_key += 1
                    st.rerun()
        
        else:
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-top: 2rem;'>
                <h3>Thanks for using the Career Guidance Chatbot! 🎉</h3>
                <p>Click the Restart button above to explore more career paths.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Sidebar with helpful information
    with st.sidebar:
        st.markdown("### 💡 How to Use")
        st.markdown("""
        1. **Share your interests** (e.g., "I like coding and art")
        2. **Select a domain** from the suggestions
        3. **Pick a career** that interests you
        4. **Get detailed info** about skills, roadmap, and resources
        5. **Explore more** or restart anytime!
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 Example Inputs")
        st.markdown("""
        - "I love technology and problem solving"
        - "Art and design fascinate me"
        - "I want to help people with their health"
        - "Gaming and entertainment interest me"
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.markdown("""
        - **Smart domain detection**
        - **Fusion career paths**
        - **Personalized recommendations**
        - **Learning resources**
        - **Career roadmaps**
        """)

if __name__ == "__main__":
    main()