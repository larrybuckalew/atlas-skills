"""
Workflow 4: Lead Scoring & Tagging
===================================
Automatically score and tag leads based on engagement and demographics.

Scoring Criteria:
- +10 points: Opened email
- +20 points: Clicked link in email
- +25 points: Replied to message
- +30 points: Visited website
- +50 points: Booked appointment
- +15 points: Age 64-66 (Medicare eligibility window)
- +20 points: Has phone number
- +10 points: Has email

Tags Applied:
- "hot-lead": Score >= 75
- "warm-lead": Score 40-74
- "cold-lead": Score < 40
- "priority": Score >= 100
"""

import urllib.request
import json
import os
from datetime import datetime

GHL_API_KEY = os.environ.get("GHL_API_KEY", "pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff")
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def get_contact(contact_id):
    """Fetch contact details."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contact", {})
    except Exception as e:
        print(f"Error fetching contact: {e}")
        return {}

def get_contact_activities(contact_id):
    """Fetch contact activity/engagement history."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/activities"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("activities", [])
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return []

def update_contact_score(contact_id, score, custom_field_id=None):
    """Update lead score custom field."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    data = json.dumps({
        "customFields": [
            {"id": custom_field_id or "lead_score", "value": str(score)}
        ]
    }).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="PUT")
    
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error updating score: {e}")
        return False

def add_tag(contact_id, tag):
    """Add tag to contact."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags"
    data = json.dumps({"tags": [tag]}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error adding tag: {e}")
        return False

def remove_tag(contact_id, tag):
    """Remove tag from contact."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags/{tag}"
    req = urllib.request.Request(url, headers=HEADERS, method="DELETE")
    
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error removing tag: {e}")
        return False

def calculate_lead_score(contact, activities):
    """Calculate lead score based on contact info and activities."""
    score = 0
    reasons = []
    
    # Demographics scoring
    phone = contact.get("phone")
    email = contact.get("email")
    
    if phone:
        score += 20
        reasons.append("+20 has phone")
    if email:
        score += 10
        reasons.append("+10 has email")
    
    # Age-based scoring (Medicare eligibility window)
    dob = contact.get("dateOfBirth")
    if dob:
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.now() - birth_date).days / 365.25
            if 64 <= age <= 66:
                score += 15
                reasons.append("+15 Medicare eligibility window")
        except:
            pass
    
    # Engagement scoring from activities
    for activity in activities:
        activity_type = activity.get("type", "").lower()
        
        if "email_opened" in activity_type or "open" in activity_type:
            score += 10
            reasons.append("+10 email opened")
        elif "email_clicked" in activity_type or "click" in activity_type:
            score += 20
            reasons.append("+20 link clicked")
        elif "replied" in activity_type or "reply" in activity_type:
            score += 25
            reasons.append("+25 replied")
        elif "website" in activity_type or "page_visit" in activity_type:
            score += 30
            reasons.append("+30 website visit")
        elif "appointment" in activity_type or "booking" in activity_type:
            score += 50
            reasons.append("+50 booked appointment")
    
    return score, reasons

def apply_score_tags(contact_id, score):
    """Apply tags based on lead score."""
    # Remove old score tags
    for tag in ["cold-lead", "warm-lead", "hot-lead", "priority"]:
        remove_tag(contact_id, tag)
    
    # Apply new score tag
    if score >= 100:
        add_tag(contact_id, "priority")
        add_tag(contact_id, "hot-lead")
        return "priority"
    elif score >= 75:
        add_tag(contact_id, "hot-lead")
        return "hot-lead"
    elif score >= 40:
        add_tag(contact_id, "warm-lead")
        return "warm-lead"
    else:
        add_tag(contact_id, "cold-lead")
        return "cold-lead"

def score_lead(contact_id):
    """Main function: Score a single lead."""
    print(f"Scoring lead: {contact_id}")
    
    # Get contact details
    contact = get_contact(contact_id)
    if not contact:
        print("  ✗ Contact not found")
        return None
    
    first_name = contact.get("firstName", "Unknown")
    
    # Get activities
    activities = get_contact_activities(contact_id)
    
    # Calculate score
    score, reasons = calculate_lead_score(contact, activities)
    
    # Update score
    update_contact_score(contact_id, score)
    
    # Apply tags
    tag_applied = apply_score_tags(contact_id, score)
    
    print(f"  Name: {first_name}")
    print(f"  Score: {score}")
    print(f"  Tag: {tag_applied}")
    print(f"  Reasons: {', '.join(reasons)}")
    print()
    
    return {"contact_id": contact_id, "name": first_name, "score": score, "tag": tag_applied}

def score_all_leads(location_id, limit=100):
    """Score all active leads."""
    url = f"{GHL_BASE_URL}/contacts/?locationId={location_id}&limit={limit}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        contacts = data.get("contacts", [])
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return
    
    print(f"Scoring {len(contacts)} leads...\n")
    
    results = []
    for contact in contacts:
        contact_id = contact.get("id")
        result = score_lead(contact_id)
        if result:
            results.append(result)
    
    # Summary
    hot = len([r for r in results if r["tag"] in ["hot-lead", "priority"]])
    warm = len([r for r in results if r["tag"] == "warm-lead"])
    cold = len([r for r in results if r["tag"] == "cold-lead"])
    
    print(f"Summary:")
    print(f"  🔥 Hot leads: {hot}")
    print(f"  🌡️ Warm leads: {warm}")
    print(f"  ❄️ Cold leads: {cold}")
    
    return results

if __name__ == "__main__":
    LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "GXAzp8lTmMJ93EPLDBmW")
    score_all_leads(LOCATION_ID)
