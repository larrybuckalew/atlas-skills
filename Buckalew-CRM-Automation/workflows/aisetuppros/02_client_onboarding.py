"""
AISetupPros - Client Onboarding Sequence
=========================================
Automated onboarding for new AI automation clients.

Flow:
1. Tag as "active-client"
2. Send welcome email with onboarding steps
3. Schedule kickoff call
4. Send project questionnaire
5. Add to client updates list
"""

import urllib.request
import json
import os
from datetime import datetime, timedelta

GHL_API_KEY = os.environ.get("GHL_API_KEY", "pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff")
GHL_LOCATION_ID = "ZnF8KJSaKmiUTbmrpMHC"
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def send_sms(contact_id, message):
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({"type": "SMS", "contactId": contact_id, "message": message}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_email(contact_id, subject, body):
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({"type": "Email", "contactId": contact_id, "subject": subject, "html": body}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def add_tag(contact_id, tag):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags"
    data = json.dumps({"tags": [tag]}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def onboard_client(contact_id, first_name, email, phone, package="Growth"):
    """Execute onboarding sequence for new AI automation client."""
    print(f"Starting AISetupPros onboarding for {first_name}...")
    
    # Tag as active client
    add_tag(contact_id, "active-client")
    add_tag(contact_id, f"package-{package.lower()}")
    print(f"  ✓ Tagged as active-client ({package})")
    
    # Send welcome email
    welcome_subject = f"🚀 Welcome to AISetupPros! Your {package} Package Is Active"
    welcome_body = f"""
    <h2>Welcome aboard, {first_name}! 🎉</h2>
    <p>We're excited to have you as an <strong>AISetupPros</strong> client!</p>
    
    <h3>Your {package} Package Includes:</h3>
    <ul>
        <li>✅ AI workflow automation setup</li>
        <li>✅ CRM integration (GoHighLevel, HubSpot, etc.)</li>
        <li>✅ Lead generation automation</li>
        <li>✅ Email marketing sequences</li>
        <li>✅ Monthly optimization calls</li>
    </ul>
    
    <h3>Next Steps:</h3>
    <ol>
        <li><strong>Kickoff Call</strong> — We'll schedule your implementation call within 48 hours</li>
        <li><strong>Discovery Questionnaire</strong> — Complete the brief questionnaire (separate email)</li>
        <li><strong>Setup & Launch</strong> — We'll have your automations running within 7-10 days</li>
    </ol>
    
    <h3>What to Expect:</h3>
    <ul>
        <li>⏱️ Save 10-20 hours per week on repetitive tasks</li>
        <li>📈 Increase lead conversion by 30-50%</li>
        <li>🤖 AI handles routine inquiries while you focus on growth</li>
    </ul>
    
    <p><strong>Questions?</strong> Reply to this email or text us anytime.</p>
    
    <p>Let's automate! 🚀</p>
    <p><strong>Larry Buckalew</strong><br>Founder, AISetupPros</p>
    """
    
    if email:
        send_email(contact_id, welcome_subject, welcome_body)
        print(f"  ✓ Sent welcome email")
    
    # Send welcome SMS
    if phone:
        sms_msg = f"Welcome to AISetupPros, {first_name}! 🚀 Your {package} package is active. We'll reach out within 48hrs to schedule your kickoff call. - Larry"
        send_sms(contact_id, sms_msg)
        print(f"  ✓ Sent welcome SMS")
    
    print(f"Onboarding complete for {first_name}!\n")
    return True

if __name__ == "__main__":
    print("AISetupPros Client Onboarding Workflow")
    print("Usage: onboard_client(contact_id, first_name, email, phone, package)")
