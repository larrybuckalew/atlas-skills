"""
AISetupPros - Demo Call Reminders
==================================
Automated reminders for scheduled demo/consultation calls.

Flow:
1. Send reminder 24 hours before
2. Send reminder 1 hour before
3. Follow up if no-show
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

def send_24h_reminder(appointment):
    """Send 24-hour demo reminder."""
    contact_id = appointment.get("contactId")
    contact_name = appointment.get("contactName", "there")
    apt_time = appointment.get("startTime")
    
    apt_dt = datetime.fromisoformat(apt_time.replace("Z", "+00:00"))
    formatted_time = apt_dt.strftime("%I:%M %p on %B %d, %Y")
    
    # SMS
    sms_msg = f"Hi {contact_name}! Reminder: Your free AI automation demo with AISetupPros is tomorrow at {formatted_time}. We'll show you exactly how to save 10-20hrs/week! See you then! - Larry"
    send_sms(contact_id, sms_msg)
    
    # Email
    email_subject = "🤖 Reminder: Your AI Automation Demo Tomorrow"
    email_body = f"""
    <h2>Demo Reminder</h2>
    <p>Hi {contact_name},</p>
    <p>Your <strong>free AI automation demo</strong> is scheduled for:</p>
    <p style="font-size: 18px; font-weight: bold;">{formatted_time}</p>
    
    <h3>What We'll Cover:</h3>
    <ul>
        <li>🔍 Audit your current workflows</li>
        <li>🤖 Identify automation opportunities</li>
        <li>💰 Calculate potential ROI</li>
        <li>📋 Create a custom implementation plan</li>
    </ul>
    
    <p><strong>Meeting Link:</strong> We'll send it before the call.</p>
    <p>See you there!</p>
    <p><strong>Larry Buckalew</strong><br>AISetupPros</p>
    """
    
    send_email(contact_id, email_subject, email_body)
    add_tag(contact_id, "reminder-24h-sent")
    print(f"  ✓ Sent 24h demo reminder to {contact_name}")

def send_1h_reminder(appointment):
    """Send 1-hour demo reminder."""
    contact_id = appointment.get("contactId")
    contact_name = appointment.get("contactName", "there")
    
    sms_msg = f"Hi {contact_name}! Your AISetupPros AI demo starts in 1 hour! We'll show you how to automate your business. See you soon! 🚀"
    send_sms(contact_id, sms_msg)
    add_tag(contact_id, "reminder-1h-sent")
    print(f"  ✓ Sent 1h demo reminder to {contact_name}")

if __name__ == "__main__":
    print("AISetupPros Demo Reminders Workflow")
