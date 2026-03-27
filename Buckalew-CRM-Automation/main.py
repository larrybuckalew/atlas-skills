#!/usr/bin/env python3
"""
Main script for Buckalew CRM Automation.
Handles client onboarding, follow-ups, and GoHighLevel integrations.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_gh_api_key():
    """Retrieve GoHighLevel API key from environment variables."""
    return os.getenv("GH_API_KEY")

def create_client(client_data):
    """Create a new client in GoHighLevel."""
    api_key = get_gh_api_key()
    url = "https://app.gohighlevel.com/api/v1/clients"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=client_data, headers=headers)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response.json()

def schedule_followup(client_id, followup_data):
    """Schedule a follow-up for a client in GoHighLevel."""
    api_key = get_gh_api_key()
    url = f"https://app.gohighlevel.com/api/v1/clients/{client_id}/followups"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=followup_data, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Example usage
    client_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890"
    }
    
    # Create a new client
    new_client = create_client(client_data)
    print(f"Created client: {new_client}")
    
    # Schedule a follow-up
    followup_data = {
        "message": "Welcome to Buckalew CRM Automation!",
        "timezone": "America/New_York",
        "date": "2026-03-15",
        "time": "10:00:00"
    }
    
    if "id" in new_client:
        scheduled_followup = schedule_followup(new_client["id"], followup_data)
        print(f"Scheduled follow-up: {scheduled_followup}")