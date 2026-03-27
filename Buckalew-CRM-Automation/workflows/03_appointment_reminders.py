"""
Workflow 3: Appointment Reminders
==================================
Automated SMS and email reminders before scheduled appointments.

Flow:
1. Check for appointments scheduled in the next 24-48 hours
2. Send reminder 24 hours before
3. Send reminder 2 hours before
4. Follow up after appointment if no-show
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

def get_appointments(location_id, hours_ahead=48):
    """Fetch appointments scheduled in the next X hours."""
    start = datetime.utcnow()
    end = start + timedelta(hours=hours_ahead)
    
    url = f"{GHL_BASE_URL}/appointments/?locationId={location_id}&startTime={start.isoformat()}Z&endTime={end.isoformat()}Z"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        return data.get("events", [])
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        return []

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

def send_24h_reminder(appointment):
    """Send 24-hour appointment reminder."""
    contact_id = appointment.get("contactId")
    contact_name = appointment.get("contactName", "there")
    apt_time = appointment.get("startTime")
    apt_title = appointment.get("title", "Consultation")
    
    # Parse appointment time
    apt_dt = datetime.fromisoformat(apt_time.replace("Z", "+00:00"))
    formatted_time = apt_dt.strftime("%I:%M %p on %B %d, %Y")
    
    # SMS reminder
    sms_msg = f"Hi {contact_name}! Reminder: You have a {apt_title} scheduled for {formatted_time} with Buckalew Financial. Reply CONFIRM to confirm or call us to reschedule. - Larry"
    send_sms(contact_id, sms_msg)
    
    # Email reminder
    email_subject = f"Reminder: Appointment Tomorrow at {apt_dt.strftime('%I:%M %p')}"
    email_body = f"""
    <h2>Appointment Reminder</h2>
    <p>Hi {contact_name},</p>
    <p>This is a friendly reminder about your upcoming appointment:</p>
    <table style="border-collapse: collapse; margin: 16px 0;">
        <tr><td style="padding: 8px; font-weight: bold;">Service:</td><td style="padding: 8px;">{apt_title}</td></tr>
        <tr><td style="padding: 8px; font-weight: bold;">Date:</td><td style="padding: 8px;">{apt_dt.strftime('%B %d, %Y')}</td></tr>
        <tr><td style="padding: 8px; font-weight: bold;">Time:</td><td style="padding: 8px;">{apt_dt.strftime('%I:%M %p')}</td></tr>
    </table>
    <p><strong>Please bring:</strong></p>
    <ul>
        <li>Your Medicare card (if applicable)</li>
        <li>Current insurance information</li>
        <li>List of medications</li>
        <li>Any questions you have</li>
    </ul>
    <p>Need to reschedule? Reply to this email or call us.</p>
    <p>See you soon!</p>
    <p><strong>Larry Buckalew</strong><br>Buckalew Financial Services</p>
    """
    
    send_email(contact_id, email_subject, email_body)
    add_tag(contact_id, "reminder-24h-sent")
    print(f"  ✓ Sent 24h reminder to {contact_name}")

def send_2h_reminder(appointment):
    """Send 2-hour appointment reminder."""
    contact_id = appointment.get("contactId")
    contact_name = appointment.get("contactName", "there")
    apt_time = appointment.get("startTime")
    apt_title = appointment.get("title", "Consultation")
    
    apt_dt = datetime.fromisoformat(apt_time.replace("Z", "+00:00"))
    formatted_time = apt_dt.strftime("%I:%M %p")
    
    sms_msg = f"Hi {contact_name}! Your {apt_title} with Buckalew Financial is in 2 hours at {formatted_time}. See you soon! - Larry"
    send_sms(contact_id, sms_msg)
    add_tag(contact_id, "reminder-2h-sent")
    print(f"  ✓ Sent 2h reminder to {contact_name}")

def process_appointment_reminders(location_id):
    """Main workflow: Process appointment reminders."""
    print(f"[{datetime.now()}] Checking for upcoming appointments...")
    
    appointments = get_appointments(location_id, hours_ahead=48)
    print(f"Found {len(appointments)} upcoming appointment(s)")
    
    now = datetime.utcnow()
    
    for apt in appointments:
        apt_time = apt.get("startTime")
        contact_id = apt.get("contactId")
        apt_dt = datetime.fromisoformat(apt_time.replace("Z", "+00:00"))
        
        hours_until = (apt_dt - now).total_seconds() / 3600
        
        # Check if we've already sent reminders
        tags = apt.get("tags", [])
        
        # 24-hour reminder (between 23-25 hours before)
        if 23 <= hours_until <= 25 and "reminder-24h-sent" not in tags:
            send_24h_reminder(apt)
        
        # 2-hour reminder (between 1.5-2.5 hours before)
        elif 1.5 <= hours_until <= 2.5 and "reminder-2h-sent" not in tags:
            send_2h_reminder(apt)
    
    print(f"Done!\n")

if __name__ == "__main__":
    LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "GXAzp8lTmMJ93EPLDBmW")
    process_appointment_reminders(LOCATION_ID)
