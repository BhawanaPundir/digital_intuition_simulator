"""
Simple file-based progress tracker for the Digital Intuition Simulator.
In production, replace with a proper database (PostgreSQL, MongoDB, etc).
"""

import json
import os
from datetime import datetime


PROGRESS_DIR = os.path.join(os.path.dirname(__file__), '.data')


def ensure_data_dir():
    """Create .data directory if it doesn't exist"""
    if not os.path.exists(PROGRESS_DIR):
        os.makedirs(PROGRESS_DIR)


def get_user_progress_file(user_id):
    """Get the path to a user's progress file"""
    ensure_data_dir()
    return os.path.join(PROGRESS_DIR, f'progress_{user_id}.json')


def load_progress(user_id):
    """Load user progress from file"""
    path = get_user_progress_file(user_id)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'Error loading progress: {e}')
    return {}


def save_progress(user_id, progress_data):
    """Save user progress to file"""
    try:
        ensure_data_dir()
        path = get_user_progress_file(user_id)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'Error saving progress: {e}')
        return False


def add_scenario_result(user_id, scenario_id, score, completed=False):
    """Record a scenario result for a user"""
    progress = load_progress(user_id)
    if 'scenarios' not in progress:
        progress['scenarios'] = {}
    
    progress['scenarios'][str(scenario_id)] = {
        'score': score,
        'completed': completed,
        'timestamp': datetime.now().isoformat()
    }
    
    save_progress(user_id, progress)
    return progress
