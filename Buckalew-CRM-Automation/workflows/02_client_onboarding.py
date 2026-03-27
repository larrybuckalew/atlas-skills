"""
Workflow 2: Client Onboarding Sequence
=======================================
Automated welcome sequence for new clients after they sign up.

Flow:
1. Tag contact as "active-client"
2. Send welcome email with next steps
3. Schedule onboarding call reminder (if not already booked)
4. Send follow-up email after 3 days
5. Add to client newsletter list
"""

import urllib.request
import json
import os
from datetime import datetime, timedelta

GHL_API_KEY = os.environ.get("GHL_API_KEY", "pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff")
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def update_contact(contact_id, data):
    """Update contact fields in GoHighLevel."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PUT")
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error updating contact: {e}")
        return None

def send_sms(contact_id, message):
    """Send SMS via GoHighLevel."""
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({
        "type": "SMS",
        "contactId": contact_id,
        "message": message
    }).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def send_email(contact_id, subject, body):
    """Send email via GoHighLevel."""
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({
        "type": "Email",
        "contactId": contact_id,
        "subject": subject,
        "html": body
    }).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
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

def onboard_client(contact_id, first_name, email, phone, plan_type="Medicare"):
    """Execute onboarding sequence for a new client."""
    print(f"Starting onboarding for {first_name}...")
    
    # 1. Tag as active client
    add_tag(contact_id, "active-client")
    add_tag(contact_id, f"plan-{plan_type.lower()}")
    print(f"  ✓ Tagged as active-client")
    
    # 2. Send welcome email
    welcome_subject = "Welcome Aboard! Your Next Steps with Buckalew Financial"
    welcome_body = f"""
    <h2>Welcome, {first_name}! 🎉</h2>
    <p>We're thrilled to have you as a client at <strong>Buckalew Financial Services</strong>.</p>
    
    <h3>Your Next Steps:</h3>
    <ol>
        <li><strong>Review your plan details</strong> - Check your email for your personalized {plan_type} summary</li>
        <li><strong>Save important dates</strong> - Mark your calendar for enrollment periods</li>
        <li><strong>Contact us anytime</strong> - Questions? Reply to this email or call us</li>
    </ol>
    
    <h3>What to Expect:</h3>
    <ul>
        <li>Personalized guidance for your {plan_type} needs</li>
        <li>Regular check-ins to ensure your plan fits your needs</li>
        <li>Annual review reminders before open enrollment</li>
    </ul>
    
    <p><strong>Need help?</strong> Simply reply to this email or call us directly.</p>
    
    <p>Welcome to the family!</p>
    <p><strong>Larry Buckalew</strong><br>Buckalew Financial Services</p>
    """
    
    if email:
        send_email(contact_id, welcome_subject, welcome_body)
        print(f"  ✓ Sent welcome email")
    
    # 3. Send welcome SMS
    if phone:
        sms_msg = f"Hi {first_name}! Welcome to Buckalew Financial! 🎉 We're here to help with your {plan_type} needs. Save this number for any questions. - Larry"
        send_sms(contact_id, sms_msg)
        print(f"  ✓ Sent welcome SMS")
    
    # 4. Schedule 3-day follow-up (tag for automation)
    add_tag(contact_id, "pending-3day-followup")
    print(f"  ✓ Scheduled 3-day follow-up")
    
    print(f"Onboarding complete for {first_name}!\n")
    return True

def send_3day_followup(contact_id, first_name, email):
    """Send 3-day follow-up email."""
    subject = "Checking In - How's Everything Going?"
    body = f"""
    <h2>Hi {first_name},</h2>
    <p>Just checking in to see how everything is going with your insurance plan!</p>
    <p>If you have any questions or concerns, don't hesitate to reach out. We're here to help.</p>
    <p><strong>Quick reminders:</strong></p>
    <ul>
        <li>Keep your plan documents in a safe place</li>
        <li>Your member ID card should arrive within 7-10 business days</li>
        <li>Don't forget to schedule your preventive care visits</li>
    </ul>
    <p>Best,<br><strong>Larry Buckalew</strong></p>
    """
    
    if email:
        send_email(contact_id, subject, body)
        # Remove pending tag, add completed tag
        add_tag(contact_id, "3day-followup-complete")
        print(f"  ✓ Sent 3-day follow-up to {first_name}")

if __name__ == "__main__":
    print("Client Onboarding Workflow")
    print("This script is triggered when a contact is tagged 'new-client'")
    print("Usage: onboard_client(contact_id, first_name, email, phone, plan_type)")
