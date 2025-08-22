"""
Data handling functions for candidate information
"""
import json
import os
from datetime import datetime
from utils import anonymize_data

CANDIDATE_DATA_FILE = "candidate_data.json"

def save_candidate_data(candidate_info):
    """Save candidate data to JSON file (anonymized)"""
    try:
        # Load existing data
        if os.path.exists(CANDIDATE_DATA_FILE):
            with open(CANDIDATE_DATA_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        # Anonymize and add new candidate
        anonymized_data = anonymize_data(candidate_info)
        data.append(anonymized_data)
        
        # Save back to file
        with open(CANDIDATE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving candidate data: {e}")
        return False

def load_candidate_data():
    """Load all candidate data from JSON file"""
    try:
        if os.path.exists(CANDIDATE_DATA_FILE):
            with open(CANDIDATE_DATA_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading candidate data: {e}")
        return []

def initialize_data_file():
    """Initialize empty candidate data file if it doesn't exist"""
    if not os.path.exists(CANDIDATE_DATA_FILE):
        with open(CANDIDATE_DATA_FILE, 'w') as f:
            json.dump([], f)
