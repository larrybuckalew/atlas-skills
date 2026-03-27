"""
Workflow 1: New Lead Auto-Follow-Up
====================================
Automatically follows up with new leads when they enter GoHighLevel.

Flow:
1. Check for new leads created in the last hour
2. Send welcome SMS/email
3. Schedule follow-up task for 24 hours later
4. Tag lead as "nurturing"
"""

import urllib.request
import json
import os
from datetime import datetime, timedelta

# Load API key from environment
GHL_API_KEY = os.environ.get("GHL_API_KEY", "pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff")
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def get_new_leads(location_id, hours_ago=1):
    """Fetch contacts created in the last X hours."""
    since = datetime.utcnow() - timedelta(hours=hours_ago)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"{GHL_BASE_URL}/contacts/?locationId={location_id}&startAfter={since_iso}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contacts", [])
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return []

def send_sms(contact_id, message):
    """Send SMS to a contact via GoHighLevel."""
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({
        "type": "SMS",
        "contactId": contact_id,
        "message": message
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

def send_email(contact_id, subject, body):
    """Send email to a contact via GoHighLevel."""
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({
        "type": "Email",
        "contactId": contact_id,
        "subject": subject,
        "html": body
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

def add_tag(contact_id, tag):
    """Add a tag to a contact."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags"
    data = json.dumps({"tags": [tag]}).encode()
    
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        response = urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error adding tag: {e}")
        return False

def create_task(contact_id, title, due_date):
    """Create a follow-up task for a contact."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tasks"
    data = json.dumps({
        "title": title,
        "dueDate": due_date.isoformat(),
        "completed": False
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error creating task: {e}")
        return None

def process_new_leads(location_id):
    """Main workflow: Process all new leads."""
    print(f"[{datetime.now()}] Checking for new leads...")
    
    leads = get_new_leads(location_id, hours_ago=1)
    print(f"Found {len(leads)} new lead(s)")
    
    for lead in leads:
        contact_id = lead.get("id")
        first_name = lead.get("firstName", "there")
        email = lead.get("email")
        phone = lead.get("phone")
        
        print(f"Processing: {first_name} ({email or phone})")
        
        # Send welcome SMS if phone exists
        if phone:
            sms_msg = f"Hi {first_name}! Thanks for your interest in Buckalew Financial Services. We'll be in touch soon to help with your Medicare and insurance needs. - Larry"
            send_sms(contact_id, sms_msg)
            print(f"  ✓ Sent welcome SMS")
        
        # Send welcome email if email exists
        if email:
            email_subject = "Welcome to Buckalew Financial Services!"
            email_body = f"""
            <h2>Hi {first_name},</h2>
            <p>Thank you for reaching out to <strong>Buckalew Financial Services</strong>!</p>
            <p>We specialize in helping individuals and families navigate:</p>
            <ul>
                <li>Medicare plans and enrollment</li>
                <li>Health insurance options</li>
                <li>Life insurance planning</li>
            </ul>
            <p>I'll be reaching out personally to discuss how we can help.</p>
            <p>Best regards,<br><strong>Larry Buckalew</strong><br>Buckalew Financial Services</p>
            """
            send_email(contact_id, email_subject, email_body)
            print(f"  ✓ Sent welcome email")
        
        # Tag as "nurturing"
        add_tag(contact_id, "nurturing")
        print(f"  ✓ Tagged as 'nurturing'")
        
        # Create follow-up task for tomorrow
        follow_up_date = datetime.now() + timedelta(days=1)
        create_task(contact_id, f"Follow up with {first_name}", follow_up_date)
        print(f"  ✓ Created follow-up task")
    
    print(f"Done! Processed {len(leads)} lead(s)\n")

if __name__ == "__main__":
    # Replace with your actual GoHighLevel Location ID
    LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "GXAzp8lTmMJ93EPLDBmW")
    process_new_leads(LOCATION_ID)
