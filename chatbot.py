"""
Main chatbot logic using Groq's Llama-3.3-70B-Versatile
"""
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, REQUIRED_INFO
from prompts import (
    SYSTEM_PROMPT, 
    GREETING_PROMPT, 
    INFORMATION_GATHERING_PROMPTS,
    TECHNICAL_QUESTION_PROMPT,
    FALLBACK_PROMPT,
    END_CONVERSATION_PROMPT
)
from utils import validate_email, validate_phone, check_conversation_end, extract_tech_stack_keywords

class TalentScoutChatbot:
    def __init__(self):
        """Initialize the chatbot with Groq client"""
        self.client = Groq(api_key=GROQ_API_KEY)
        self.conversation_history = []
        self.candidate_info = {}
        self.current_step = "greeting"
        self.info_collection_index = 0
        self.conversation_ended = False
        
    def get_chat_completion(self, messages, temperature=0.7):
        """Get completion from Groq's Llama model"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=MODEL_NAME,
                temperature=temperature,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"
    
    def add_to_history(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep conversation history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_greeting(self):
        """Get initial greeting message"""
        self.add_to_history("assistant", GREETING_PROMPT)
        self.current_step = "collecting_info"
        return GREETING_PROMPT
    
    def process_user_input(self, user_input):
        """Process user input and generate appropriate response"""
        if not user_input.strip():
            return "Please provide a response so I can assist you better."
        
        self.add_to_history("user", user_input)
        
        # Check for conversation end
        if check_conversation_end(user_input):
            self.conversation_ended = True
            response = END_CONVERSATION_PROMPT
            self.add_to_history("assistant", response)
            return response
        
        # Handle different conversation steps
        if self.current_step == "collecting_info":
            return self._handle_info_collection(user_input)
        elif self.current_step == "generating_questions":
            return self._generate_technical_questions()
        elif self.current_step == "questions_complete":
            return self._handle_follow_up(user_input)
        else:
            return self._handle_fallback(user_input)
    
    def _handle_info_collection(self, user_input):
        """Handle information collection phase"""
        info_keys = list(REQUIRED_INFO)
        
        if self.info_collection_index < len(info_keys):
            current_field = info_keys[self.info_collection_index]
            
            # Validate and store information
            if self._validate_and_store_info(current_field, user_input):
                self.info_collection_index += 1
                
                # Check if we have all required information
                if self.info_collection_index >= len(info_keys):
                    self.current_step = "generating_questions"
                    return self._generate_technical_questions()
                else:
                    # Ask for next piece of information
                    next_field = info_keys[self.info_collection_index]
                    response = INFORMATION_GATHERING_PROMPTS[next_field]
                    self.add_to_history("assistant", response)
                    return response
            else:
                # Invalid input, ask again
                response = f"I need valid information. {INFORMATION_GATHERING_PROMPTS[current_field]}"
                self.add_to_history("assistant", response)
                return response
        
        return self._handle_fallback(user_input)
    
    def _validate_and_store_info(self, field, value):
        """Validate and store candidate information"""
        value = value.strip()
        
        if field == "full_name":
            if len(value) >= 2:
                self.candidate_info[field] = value
                return True
        elif field == "email":
            if validate_email(value):
                self.candidate_info[field] = value
                return True
        elif field == "phone":
            if validate_phone(value):
                self.candidate_info[field] = value
                return True
        elif field == "experience_years":
            try:
                years = float(value)
                if 0 <= years <= 50:
                    self.candidate_info[field] = years
                    return True
            except:
                pass
        elif field in ["desired_position", "location", "tech_stack"]:
            if len(value) >= 2:
                self.candidate_info[field] = value
                return True
        
        return False
    
    def _generate_technical_questions(self):
        """Generate technical questions based on tech stack"""
        tech_stack = self.candidate_info.get("tech_stack", "")
        experience_years = self.candidate_info.get("experience_years", 0)
        
        # Create prompt for technical questions
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": TECHNICAL_QUESTION_PROMPT.format(
                tech_stack=tech_stack, 
                experience_years=experience_years
            )}
        ]
        
        response = self.get_chat_completion(messages)
        self.current_step = "questions_complete"
        self.add_to_history("assistant", response)
        
        return response
    
    def _handle_follow_up(self, user_input):
        """Handle follow-up questions and answers"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + self.conversation_history + [
            {"role": "user", "content": user_input}
        ]
        
        response = self.get_chat_completion(messages)
        self.add_to_history("assistant", response)
        return response
    
    def _handle_fallback(self, user_input):
        """Handle unexpected inputs"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User said: '{user_input}'. Respond with: {FALLBACK_PROMPT}"}
        ]
        
        response = self.get_chat_completion(messages)
        self.add_to_history("assistant", response)
        return response
    
    def get_candidate_info(self):
        """Return collected candidate information"""
        return self.candidate_info.copy()
    
    def is_conversation_complete(self):
        """Check if information collection is complete"""
        return len(self.candidate_info) == len(REQUIRED_INFO)
    
    def is_conversation_ended(self):
        """Check if conversation has ended"""
        return self.conversation_ended
