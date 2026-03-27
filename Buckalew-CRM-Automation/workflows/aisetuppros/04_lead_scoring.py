"""
AISetupPros - Lead Scoring & Tagging
=====================================
Score leads based on engagement and business fit.

Scoring:
- +20: Has phone
- +10: Has email
- +15: Company name provided
- +10: Email opened
- +20: Link clicked
- +25: Replied
- +30: Visited pricing page
- +50: Booked demo
- +25: 10+ employees (higher budget potential)

Tags:
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
GHL_LOCATION_ID = "ZnF8KJSaKmiUTbmrpMHC"
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def get_contact(contact_id):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contact", {})
    except Exception as e:
        print(f"Error: {e}")
        return {}

def get_contact_activities(contact_id):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/activities"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("activities", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def add_tag(contact_id, tag):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags"
    data = json.dumps({"tags": [tag]}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def remove_tag(contact_id, tag):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags/{tag}"
    req = urllib.request.Request(url, headers=HEADERS, method="DELETE")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def update_score(contact_id, score):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    data = json.dumps({"customFields": [{"id": "lead_score", "value": str(score)}]}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="PUT")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def calculate_score(contact, activities):
    score = 0
    reasons = []
    
    # Contact info
    if contact.get("phone"):
        score += 20; reasons.append("+20 phone")
    if contact.get("email"):
        score += 10; reasons.append("+10 email")
    if contact.get("companyName"):
        score += 15; reasons.append("+15 company")
    
    # Employee count (budget potential)
    employees = contact.get("employeeCount", 0)
    if employees and int(employees) >= 10:
        score += 25; reasons.append("+25 10+ employees")
    
    # Engagement
    for activity in activities:
        atype = activity.get("type", "").lower()
        if "open" in atype:
            score += 10; reasons.append("+10 email opened")
        elif "click" in atype:
            score += 20; reasons.append("+20 link clicked")
        elif "repl" in atype:
            score += 25; reasons.append("+25 replied")
        elif "pricing" in atype or "page_view" in atype:
            score += 30; reasons.append("+30 page visit")
        elif "appointment" in atype or "booking" in atype:
            score += 50; reasons.append("+50 demo booked")
    
    return score, reasons

def apply_tags(contact_id, score):
    for tag in ["cold-lead", "warm-lead", "hot-lead", "priority"]:
        remove_tag(contact_id, tag)
    
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
    contact = get_contact(contact_id)
    if not contact:
        return None
    
    first_name = contact.get("firstName", "Unknown")
    activities = get_contact_activities(contact_id)
    score, reasons = calculate_score(contact, activities)
    
    update_score(contact_id, score)
    tag = apply_tags(contact_id, score)
    
    print(f"  {first_name}: Score={score}, Tag={tag}")
    return {"contact_id": contact_id, "name": first_name, "score": score, "tag": tag}

def score_all_leads(limit=100):
    url = f"{GHL_BASE_URL}/contacts/?locationId={GHL_LOCATION_ID}&limit={limit}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        contacts = data.get("contacts", [])
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print(f"Scoring {len(contacts)} AISetupPros leads...\n")
    results = [score_lead(c.get("id")) for c in contacts if score_lead(c.get("id"))]
    
    hot = len([r for r in results if r["tag"] in ["hot-lead", "priority"]])
    warm = len([r for r in results if r["tag"] == "warm-lead"])
    cold = len([r for r in results if r["tag"] == "cold-lead"])
    
    print(f"\n🔥 Hot: {hot} | 🌡️ Warm: {warm} | ❄️ Cold: {cold}")

if __name__ == "__main__":
    score_all_leads()
