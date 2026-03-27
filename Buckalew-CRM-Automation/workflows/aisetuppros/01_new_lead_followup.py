"""
AISetupPros - New Lead Auto-Follow-Up
======================================
Automatically follows up with new leads interested in AI automation services.

Flow:
1. Check for new leads created in the last hour
2. Send welcome SMS/email
3. Schedule demo call task for 24 hours later
4. Tag lead as "ai-prospect"
"""

import urllib.request
import json
import os
from datetime import datetime, timedelta

GHL_API_KEY = os.environ.get("GHL_API_KEY", "pit-fcb5ac96-c1fb-489a-bbdc-a6bea29e23ff")
GHL_LOCATION_ID = "ZnF8KJSaKmiUTbmrpMHC"  # AISetupPros
GHL_BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}

def get_new_leads(hours_ago=1):
    """Fetch contacts created in the last X hours."""
    since = datetime.utcnow() - timedelta(hours=hours_ago)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"{GHL_BASE_URL}/contacts/?locationId={GHL_LOCATION_ID}&startAfter={since_iso}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contacts", [])
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return []

def send_sms(contact_id, message):
    """Send SMS via GoHighLevel."""
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({"type": "SMS", "contactId": contact_id, "message": message}).encode()
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
    data = json.dumps({"type": "Email", "contactId": contact_id, "subject": subject, "html": body}).encode()
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

def create_task(contact_id, title, due_date):
    """Create follow-up task."""
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tasks"
    data = json.dumps({"title": title, "dueDate": due_date.isoformat(), "completed": False}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Error creating task: {e}")
        return False

def process_new_leads():
    """Main workflow: Process all new leads."""
    print(f"[{datetime.now()}] Checking for new AISetupPros leads...")
    
    leads = get_new_leads(hours_ago=1)
    print(f"Found {len(leads)} new lead(s)")
    
    for lead in leads:
        contact_id = lead.get("id")
        first_name = lead.get("firstName", "there")
        email = lead.get("email")
        phone = lead.get("phone")
        company = lead.get("companyName", "")
        
        print(f"Processing: {first_name} from {company or 'Unknown'} ({email or phone})")
        
        # Send welcome SMS
        if phone:
            sms_msg = f"Hi {first_name}! Thanks for your interest in AISetupPros. We help businesses like yours automate workflows with AI. Let's schedule a free demo! - Larry"
            send_sms(contact_id, sms_msg)
            print(f"  ✓ Sent welcome SMS")
        
        # Send welcome email
        if email:
            email_subject = "Welcome to AISetupPros - Let's Automate Your Business!"
            email_body = f"""
            <h2>Hi {first_name},</h2>
            <p>Thank you for your interest in <strong>AISetupPros</strong>!</p>
            <p>We help businesses <strong>save 10-20 hours per week</strong> by automating repetitive tasks with AI:</p>
            <ul>
                <li>🤖 <strong>AI Chatbots</strong> — Handle customer inquiries 24/7</li>
                <li>📧 <strong>Email Automation</strong> — Nurture leads on autopilot</li>
                <li>📊 <strong>CRM Integration</strong> — Connect your tools seamlessly</li>
                <li>📈 <strong>Lead Generation</strong> — AI-powered prospect qualification</li>
            </ul>
            <p><strong>🎁 Free Offer:</strong> Book a <a href="https://aisetuppros.com/demo">free AI audit</a> and we'll show you exactly where you can save time and money.</p>
            <p>Best regards,<br><strong>Larry Buckalew</strong><br>Founder, AISetupPros</p>
            """
            send_email(contact_id, email_subject, email_body)
            print(f"  ✓ Sent welcome email")
        
        # Tag as prospect
        add_tag(contact_id, "ai-prospect")
        add_tag(contact_id, "new-lead")
        print(f"  ✓ Tagged as ai-prospect")
        
        # Create demo call task
        follow_up_date = datetime.now() + timedelta(days=1)
        create_task(contact_id, f"Schedule demo call with {first_name}", follow_up_date)
        print(f"  ✓ Created demo call task")
    
    print(f"Done! Processed {len(leads)} lead(s)\n")

if __name__ == "__main__":
    process_new_leads()
