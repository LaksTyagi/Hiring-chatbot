"""
Streamlit app for TalentScout Hiring Assistant
"""
import streamlit as st
from chatbot import TalentScoutChatbot
from data_handler import save_candidate_data, initialize_data_file
from config import PAGE_TITLE, PAGE_ICON

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = TalentScoutChatbot()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

def display_chat_interface():
    """Display the main chat interface"""
    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("*Your AI-powered recruitment screening assistant*")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Start conversation if not started
    if not st.session_state.conversation_started:
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state.conversation_started = True
        st.rerun()
    
    # Chat input
    if not st.session_state.chatbot.is_conversation_ended():
        if prompt := st.chat_input("Type your response here..."):
            # Display user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.process_user_input(prompt)
                    st.write(response)
            
            # Add response to message history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save candidate data if conversation is complete
            if st.session_state.chatbot.is_conversation_complete():
                candidate_info = st.session_state.chatbot.get_candidate_info()
                save_candidate_data(candidate_info)
                st.success("✅ Your information has been recorded successfully!")
            
            st.rerun()
    else:
        st.info("🎯 Conversation ended. Thank you for your time!")
        
        # Save final candidate data
        if st.session_state.chatbot.is_conversation_complete():
            candidate_info = st.session_state.chatbot.get_candidate_info()
            save_candidate_data(candidate_info)

def display_sidebar():
    """Display sidebar with additional information"""
    with st.sidebar:
        st.header("📋 About TalentScout")
        st.write("""
        This AI assistant helps with initial candidate screening for technology positions.
        
        **What we collect:**
        - Full Name
        - Email Address  
        - Phone Number
        - Years of Experience
        - Desired Position(s)
        - Current Location
        - Tech Stack
        
        **What happens next:**
        - Technical questions based on your skills
        - Initial screening assessment
        - Follow-up from our recruitment team
        """)
        
        st.header("🔒 Privacy & Data")
        st.write("""
        - Your data is handled securely
        - Personal information is anonymized for storage
        - We comply with data privacy standards
        - Information used only for recruitment purposes
        """)
        
        st.header("💡 Tips")
        st.write("""
        - Be specific about your tech stack
        - Include programming languages, frameworks, databases, and tools
        - Answer questions honestly for best matching
        - Type 'exit' or 'quit' to end conversation anytime
        """)
        
        # Reset button
        if st.button("🔄 Start New Conversation", type="secondary"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def main():
    """Main application function"""
    # Initialize data file and session state
    initialize_data_file()
    initialize_session_state()
    
    # Display main interface
    display_sidebar()
    display_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "TalentScout Hiring Assistant • Powered by Groq Llama-3.3-70B-Versatile • "
        "Built with ❤️ using Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
