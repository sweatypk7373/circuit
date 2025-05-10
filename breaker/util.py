"""
Utility module for the Circuit Breakers Team Hub application.
Provides functions for data management, access control, and file operations.
"""

import os
import json
import hashlib
import uuid
from datetime import datetime
import streamlit as st

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Define paths for data files
USERS_FILE = "data/users.json"
TASKS_FILE = "data/tasks.json"
BUILD_LOGS_FILE = "data/build_logs.json"
RESOURCES_FILE = "data/resources.json"
MEDIA_ITEMS_FILE = "data/media_items.json"
MESSAGES_FILE = "data/messages.json"
EVENTS_FILE = "data/events.json"
SPONSORS_FILE = "data/sponsors.json"
SETTINGS_FILE = "data/settings.json"

# Initialize data directories
def initialize_data_directories():
    """Create all necessary directories for data storage."""
    os.makedirs("data", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/resources", exist_ok=True)
    os.makedirs("uploads/media", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

# Role-based access control
def check_role_access(required_roles):
    """Check if the current user has one of the required roles."""
    if not st.session_state.get("authenticated", False):
        st.warning("You must be logged in to access this page")
        return False
    
    user_role = st.session_state.get("role", None)
    if user_role not in required_roles:
        st.warning("You don't have permission to access this page")
        return False
    
    return True

# Utility functions to read/write JSON files
def read_json_file(file_path, default=None):
    """Read and return data from a JSON file."""
    if default is None:
        default = [] if not file_path.endswith(('settings.json', 'users.json')) else {}
        
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return default

def write_json_file(file_path, data):
    """Write data to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {str(e)}")
        return False

# Task management functions
def load_tasks():
    """Load tasks from JSON file."""
    return read_json_file(TASKS_FILE)

def save_tasks(tasks):
    """Save tasks to JSON file."""
    return write_json_file(TASKS_FILE, tasks)

# Build logs functions
def load_logs():
    """Load build logs from JSON file."""
    return read_json_file(BUILD_LOGS_FILE)

def save_logs(logs):
    """Save build logs to JSON file."""
    return write_json_file(BUILD_LOGS_FILE, logs)

# Resource management functions
def load_resources():
    """Load resources from JSON file."""
    return read_json_file(RESOURCES_FILE)

def save_resources(resources):
    """Save resources to JSON file."""
    return write_json_file(RESOURCES_FILE, resources)

# Media management functions
def load_media():
    """Load media items from JSON file."""
    return read_json_file(MEDIA_ITEMS_FILE)

def save_media(media_items):
    """Save media items to JSON file."""
    return write_json_file(MEDIA_ITEMS_FILE, media_items)

# Sponsor management functions
def load_sponsors():
    """Load sponsors from JSON file."""
    return read_json_file(SPONSORS_FILE)

def save_sponsors(sponsors):
    """Save sponsors to JSON file."""
    return write_json_file(SPONSORS_FILE, sponsors)

# Event management functions
def load_events():
    """Load events from JSON file."""
    return read_json_file(EVENTS_FILE)

def save_events(events):
    """Save events to JSON file."""
    return write_json_file(EVENTS_FILE, events)

# Team member management functions
def load_team_members():
    """Load team members from users JSON file."""
    users = read_json_file(USERS_FILE)
    team_members = []
    
    for username, user_data in users.items():
        team_members.append({
            "username": username,
            "name": user_data.get("name", ""),
            "role": user_data.get("role", "member"),
            "email": user_data.get("email", ""),
            "department": user_data.get("department", ""),
            "created_at": user_data.get("created_at", datetime.now().isoformat())
        })
    
    return team_members

# Message management functions
def load_messages():
    """Load messages from JSON file."""
    return read_json_file(MESSAGES_FILE)

def save_messages(messages):
    """Save messages to JSON file."""
    return write_json_file(MESSAGES_FILE, messages)

# Helper functions
def format_date(iso_date):
    """Format ISO date string to a more readable format."""
    try:
        date_obj = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return date_obj.strftime("%b %d, %Y")
    except:
        return iso_date

def generate_id():
    """Generate a unique ID for database records."""
    return str(uuid.uuid4())

def load_svg(svg_path):
    """Load an SVG file as a string."""
    try:
        if os.path.exists(svg_path):
            with open(svg_path, 'r') as f:
                return f.read()
        return """<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#f1f1f1" stroke="#0084D8" stroke-width="5"/>
            <text x="100" y="90" font-family="Arial" font-size="18" fill="#0084D8" text-anchor="middle">CIRCUIT</text>
            <text x="100" y="115" font-family="Arial" font-size="18" fill="#0084D8" text-anchor="middle">BREAKERS</text>
            <path d="M80,130 L95,150 L110,130 L125,150" stroke="#C0C0C0" stroke-width="4" fill="none"/>
            <path d="M60,120 L140,120" stroke="#0084D8" stroke-width="3" fill="none"/>
            <path d="M70,60 L130,60" stroke="#0084D8" stroke-width="3" fill="none"/>
            <path d="M90,60 L90,120" stroke="#0084D8" stroke-width="3" fill="none"/>
            <path d="M110,60 L110,120" stroke="#0084D8" stroke-width="3" fill="none"/>
        </svg>"""
    except Exception as e:
        print(f"Error loading SVG: {str(e)}")
        return """<svg width="150" height="50" xmlns="http://www.w3.org/2000/svg">
            <rect width="150" height="50" fill="#0084D8"/>
            <text x="75" y="30" font-family="Arial" font-size="16" fill="white" text-anchor="middle">Circuit Breakers</text>
        </svg>"""
