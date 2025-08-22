"""
Utility functions for TalentScout Hiring Assistant
"""
import re
import hashlib
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Check if it has 10-15 digits (international format)
    return 10 <= len(digits) <= 15

def anonymize_data(data):
    """Anonymize sensitive candidate data for storage"""
    anonymized = data.copy()
    
    # Hash email and phone for privacy
    if 'email' in anonymized:
        anonymized['email_hash'] = hashlib.sha256(anonymized['email'].encode()).hexdigest()
        del anonymized['email']
    
    if 'phone' in anonymized:
        anonymized['phone_hash'] = hashlib.sha256(anonymized['phone'].encode()).hexdigest()
        del anonymized['phone']
    
    # Add timestamp
    anonymized['submission_time'] = datetime.now().isoformat()
    
    return anonymized

def check_conversation_end(message):
    """Check if message contains conversation-ending keywords"""
    from config import END_KEYWORDS
    message_lower = message.lower().strip()
    return any(keyword in message_lower for keyword in END_KEYWORDS)

def extract_tech_stack_keywords(tech_stack_text):
    """Extract and categorize tech stack components"""
    text_lower = tech_stack_text.lower()
    
    # Common technology categories
    languages = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin']
    frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel', 'rails', 'fastapi']
    databases = ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra', 'dynamodb']
    tools = ['docker', 'kubernetes', 'git', 'jenkins', 'aws', 'azure', 'gcp', 'terraform', 'ansible']
    
    found_techs = {
        'languages': [lang for lang in languages if lang in text_lower],
        'frameworks': [fw for fw in frameworks if fw in text_lower],
        'databases': [db for db in databases if db in text_lower],
        'tools': [tool for tool in tools if tool in text_lower]
    }
    
    return found_techs
