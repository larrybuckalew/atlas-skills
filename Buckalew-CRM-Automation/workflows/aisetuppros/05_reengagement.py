"""
AISetupPros - Re-engagement for Inactive Leads
===============================================
Win back leads who haven't engaged in 30+ days.

Flow:
1. Day 0: Send "what's new" email
2. Day 3: Send case study SMS
3. Day 7: Final offer email
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

def get_inactive_contacts(days_inactive=30):
    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    cutoff_iso = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"{GHL_BASE_URL}/contacts/?locationId={GHL_LOCATION_ID}&lastActivityBefore={cutoff_iso}&limit=100"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("contacts", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_sms(contact_id, message):
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({"type": "SMS", "contactId": contact_id, "message": message}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def send_email(contact_id, subject, body):
    url = f"{GHL_BASE_URL}/conversations/messages"
    data = json.dumps({"type": "Email", "contactId": contact_id, "subject": subject, "html": body}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def add_tag(contact_id, tag):
    url = f"{GHL_BASE_URL}/contacts/{contact_id}/tags"
    data = json.dumps({"tags": [tag]}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        return False

def get_tags(contact):
    tags = contact.get("tags", [])
    return tags if isinstance(tags, list) else []

def reengage_lead(contact, stage="initial"):
    contact_id = contact.get("id")
    first_name = contact.get("firstName", "there")
    email = contact.get("email")
    phone = contact.get("phone")
    company = contact.get("companyName", "your company")
    tags = get_tags(contact)
    
    if "re-engaged" in tags or "archived" in tags:
        return None
    
    print(f"Re-engaging: {first_name} at {company} (stage: {stage})")
    
    if stage == "initial":
        if email:
            subject = "🤖 New AI Features You're Missing Out On"
            body = f"""
            <h2>Hi {first_name},</h2>
            <p>It's been a while! A lot has changed at <strong>AISetupPros</strong>, and I wanted to share some exciting updates:</p>
            
            <h3>🆕 What's New:</h3>
            <ul>
                <li>🔥 <strong>AI Chatbots 2.0</strong> — Now handle 95% of customer inquiries automatically</li>
                <li>📊 <strong>Smart Lead Scoring</strong> — AI identifies your hottest prospects</li>
                <li>⚡ <strong>1-Click Integrations</strong> — Connect GoHighLevel, HubSpot, Zapier instantly</li>
                <li>💰 <strong>New ROI Dashboard</strong> — See exactly how much time and money you're saving</li>
            </ul>
            
            <h3>📈 Recent Client Results:</h3>
            <ul>
                <li>Insurance agency saved 15 hours/week with automated follow-ups</li>
                <li>Real estate team increased leads by 40% with AI chatbot</li>
                <li>Consulting firm automated their entire onboarding process</li>
            </ul>
            
            <p><strong>🎁 Special Offer:</strong> Reply to this email for a <strong>free automation audit</strong> (normally $500).</p>
            
            <p>Best,<br><strong>Larry Buckalew</strong><br>AISetupPros</p>
            """
            send_email(contact_id, subject, body)
            print(f"  ✓ Sent re-engagement email")
        
        add_tag(contact_id, "re-engagement-email-sent")
    
    elif stage == "followup":
        if phone:
            sms_msg = f"Hey {first_name}! Quick case study: We helped a business like {company} save 12hrs/week with AI automation. Interested in seeing how? Reply YES for a free demo! - Larry"
            send_sms(contact_id, sms_msg)
            print(f"  ✓ Sent case study SMS")
        
        add_tag(contact_id, "re-engagement-sms-sent")
    
    elif stage == "final":
        if email:
            subject = "🎁 Free AI Audit (Limited Time)"
            body = f"""
            <h2>Hi {first_name},</h2>
            <p>I've reached out a couple times — no worries if now isn't the right time!</p>
            <p>I just wanted to make sure you know about our <strong>limited-time offer</strong>:</p>
            
            <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 16px 0;">
                <h3 style="margin-top: 0;">🎁 FREE AI Automation Audit ($500 Value)</h3>
                <ul>
                    <li>✅ Complete workflow analysis</li>
                    <li>✅ Automation opportunity report</li>
                    <li>✅ ROI projection</li>
                    <li>✅ Custom implementation plan</li>
                </ul>
                <p><strong>No obligation. Just actionable insights.</strong></p>
            </div>
            
            <p>Simply reply to this email to claim your free audit.</p>
            
            <p>Talk soon,<br><strong>Larry Buckalew</strong><br>AISetupPros</p>
            """
            send_email(contact_id, subject, body)
            print(f"  ✓ Sent final offer email")
        
        add_tag(contact_id, "re-engagement-complete")
    
    return True

def process_reengagement():
    print(f"[{datetime.now()}] Processing AISetupPros re-engagement...\n")
    
    contacts_30d = get_inactive_contacts(30)
    contacts_90d = get_inactive_contacts(90)
    
    print(f"30+ days inactive: {len(contacts_30d)}")
    print(f"90+ days inactive: {len(contacts_90d)}\n")
    
    count = 0
    for contact in contacts_30d:
        tags = get_tags(contact)
        
        if "re-engagement-complete" in tags:
            continue
        elif "re-engagement-sms-sent" in tags:
            reengage_lead(contact, stage="final")
        elif "re-engagement-email-sent" in tags:
            reengage_lead(contact, stage="followup")
        else:
            reengage_lead(contact, stage="initial")
        
        count += 1
    
    print(f"\nDone! Re-engaged {count} contact(s)")

if __name__ == "__main__":
    process_reengagement()
