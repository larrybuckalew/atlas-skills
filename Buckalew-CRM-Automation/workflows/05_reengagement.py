"""
Workflow 5: Re-engagement for Inactive Leads
=============================================
Automatically reach out to leads who haven't engaged in 30+ days.

Flow:
1. Find leads with no activity in 30+ days
2. Send "checking in" email
3. Send SMS after 2 days if no response
4. Tag as "re-engaged" or "unresponsive"
5. Archive leads unresponsive after 90 days
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

def get_inactive_contacts(location_id, days_inactive=30):
    """Fetch contacts with no activity in X days."""
    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    cutoff_iso = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"{GHL_BASE_URL}/contacts/?locationId={location_id}&lastActivityBefore={cutoff_iso}&limit=100"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contacts", [])
    except Exception as e:
        print(f"Error fetching inactive contacts: {e}")
        return []

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

def get_tags(contact):
    """Get tags from contact."""
    tags = contact.get("tags", [])
    if isinstance(tags, list):
        return tags
    return []

def reengage_lead(contact, stage="initial"):
    """Execute re-engagement sequence for a lead."""
    contact_id = contact.get("id")
    first_name = contact.get("firstName", "there")
    email = contact.get("email")
    phone = contact.get("phone")
    tags = get_tags(contact)
    
    # Skip if already re-engaged or archived
    if "re-engaged" in tags or "archived" in tags:
        return None
    
    print(f"Re-engaging: {first_name} (inactive {stage})")
    
    if stage == "initial":
        # Day 0: Send re-engagement email
        if email:
            subject = "We Miss You! Here's What's New at Buckalew Financial"
            body = f"""
            <h2>Hi {first_name},</h2>
            <p>It's been a while since we've heard from you, and I wanted to check in!</p>
            <p>A lot has changed in the Medicare and insurance landscape, and I'd love to help you:</p>
            <ul>
                <li>🔍 Review your current coverage</li>
                <li>💰 Find potential savings</li>
                <li>📋 Explore new plan options</li>
                <li>❓ Answer any questions you have</li>
            </ul>
            <p><strong>Open enrollment is right around the corner</strong> — now is the perfect time to make sure you have the best plan for your needs.</p>
            <p>Simply reply to this email or give me a call. I'm here to help!</p>
            <p>Best regards,<br><strong>Larry Buckalew</strong><br>Buckalew Financial Services</p>
            <p style="color: #666; font-size: 12px;">If you no longer wish to hear from us, just let me know and I'll update your preferences.</p>
            """
            send_email(contact_id, subject, body)
            print(f"  ✓ Sent re-engagement email")
        
        add_tag(contact_id, "re-engagement-email-sent")
        
    elif stage == "followup":
        # Day 3: Send SMS if no response
        if phone:
            sms_msg = f"Hi {first_name}! Larry from Buckalew Financial here. Just checking in — have you reviewed your insurance lately? I have some updates that might save you money. Quick call when you're free? Reply YES if interested!"
            send_sms(contact_id, sms_msg)
            print(f"  ✓ Sent follow-up SMS")
        
        add_tag(contact_id, "re-engagement-sms-sent")
        
    elif stage == "final":
        # Day 7: Final attempt
        if email:
            subject = "One Last Check-In + A Special Offer"
            body = f"""
            <h2>Hi {first_name},</h2>
            <p>I've reached out a couple of times and haven't heard back — no worries!</p>
            <p>I just wanted to make sure you know that <strong>I'm here whenever you need help</strong> with:</p>
            <ul>
                <li>Medicare plans and enrollment</li>
                <li>Health insurance options</li>
                <li>Life insurance planning</li>
            </ul>
            <p><strong>🎁 Special Offer:</strong> Reply to this email for a <strong>free plan review</strong> — no obligation, just helpful advice.</p>
            <p>If now isn't a good time, I understand. Just save my info for when you need us!</p>
            <p>All the best,<br><strong>Larry Buckalew</strong><br>Buckalew Financial Services</p>
            """
            send_email(contact_id, subject, body)
            print(f"  ✓ Sent final re-engagement email")
        
        add_tag(contact_id, "re-engagement-complete")
    
    return True

def process_reengagement(location_id):
    """Main workflow: Process all re-engagement stages."""
    print(f"[{datetime.now()}] Processing re-engagement workflow...\n")
    
    # Get inactive contacts
    contacts_30d = get_inactive_contacts(location_id, days_inactive=30)
    contacts_90d = get_inactive_contacts(location_id, days_inactive=90)
    
    print(f"Found {len(contacts_30d)} contacts inactive 30+ days")
    print(f"Found {len(contacts_90d)} contacts inactive 90+ days\n")
    
    reengaged = 0
    
    for contact in contacts_30d:
        tags = get_tags(contact)
        
        # Determine stage
        if "re-engagement-complete" in tags:
            continue
        elif "re-engagement-sms-sent" in tags:
            reengage_lead(contact, stage="final")
        elif "re-engagement-email-sent" in tags:
            reengage_lead(contact, stage="followup")
        else:
            reengage_lead(contact, stage="initial")
        
        reengaged += 1
    
    print(f"\nDone! Re-engaged {reengaged} contact(s)")

if __name__ == "__main__":
    LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "GXAzp8lTmMJ93EPLDBmW")
    process_reengagement(LOCATION_ID)
