# GoHighLevel Pipeline Setup

## Overview
This document outlines the step-by-step process for setting up a **GoHighLevel CRM pipeline** to serve as the foundation for your automation system. This pipeline will track leads from initial contact to appointment booking and beyond.

---

## Step 1: Create the Pipeline

### **Pipeline Name:** `Lead to Client Conversion`

### **Stages and Descriptions:**
1. **New Lead**
   - **Description:** Newly captured leads from website forms or chat interactions.
   - **Action:** Automatically assigned when a lead is created.

2. **AI Qualified**
   - **Description:** Leads who have been qualified by the AI chat assistant.
   - **Action:** Move leads here after they complete the AI chat qualification process.

3. **Needs Follow-Up**
   - **Description:** Leads who require additional follow-up before scheduling an appointment.
   - **Action:** Trigger automated follow-up sequences (SMS/email).

4. **Appointment Scheduled**
   - **Description:** Leads who have booked an appointment.
   - **Action:** Confirm appointment details and prepare for the consultation.

5. **Closed Client**
   - **Description:** Leads who have become paying clients.
   - **Action:** Move leads here upon successful conversion.

---

## Step 2: Build the Lead Capture Form

### **Form Name:** `Lead Qualification Form`

### **Fields to Include:**
- **Name** (First Name, Last Name)
- **Phone Number**
- **Email Address**
- **Interests** (Dropdown Menu with Options):
  - Medicare Help
  - Health Insurance
  - Life Insurance
  - AI Automation for Business

### **Form Integration:**
- Embed the form on your website (Buckalew Financial Services and AISetupPros).
- Ensure the form is connected to the **New Lead** stage in your pipeline.

---

## Step 3: Add an AI Chat Assistant

### **Recommended Tools:**
- **GoHighLevel Chat Widget** (for simplicity and direct CRM integration)

### **Chat Widget Setup:**
1. **Go to GoHighLevel Dashboard** → **Chat Widgets** → **Create New Widget**.
2. **Configure the Chat Widget:**
   - **Greeting Message:** "Hi! What can I help you with today?"
   - **Options:**
     - Medicare Questions
     - Health Insurance
     - Life Insurance
     - AI Automation for Business

3. **Qualification Questions:**
   - **Question 1:** "Are you looking for help now or just information?"
     - Options: Now, Later, Information Only
   - **Question 2:** "What’s the best phone number to reach you?"

4. **Automated Actions:**
   - Once the lead completes the chat, automatically create a lead in the **New Lead** stage.
   - Use the answers to populate fields in the CRM (e.g., interest area, phone number).

---

## Step 4: Automated Follow-Up Sequence

### **Automation Workflow:**
1. **Immediately After Lead Creation:**
   - **SMS:** "Hi, this is Larry with Buckalew Financial Services. I received your request. When is a good time to talk?"

2. **10 Minutes Later:**
   - **Email:** Include a booking link and detailed information about services.
   - **Subject:** "Learn how we can help you with [Interested Area]"

3. **1 Day Later:**
   - **Reminder Message:** "Reminder: We’d love to discuss your needs. Book a call here: [Link]"

4. **3 Days Later:**
   - **Follow-Up Text:** "Still interested in learning more? Let’s schedule a call today!"

### **How to Set Up:**
- Go to **GoHighLevel Dashboard** → **Automations** → **Create New Automation**.
- Use the **Lead Created** trigger to set up the sequence.

---

## Step 5: Appointment Booking

### **Integration:**
- Use the **GoHighLevel Calendar** feature to allow leads to book appointments directly.
- Ensure the calendar is linked to the **Appointment Scheduled** stage in your pipeline.

### **Steps:**
1. **Go to GoHighLevel Dashboard** → **Calendar** → **Create New Calendar**.
2. **Configure Appointment Types:**
   - Medicare Consultation
   - Insurance Review
   - AI Automation Consultation
3. **Link to CRM:** Ensure appointments are automatically logged in the **Appointment Scheduled** stage.

---

## Step 6: AI Qualification (Advanced)

### **Future Enhancement:**
- Implement a more advanced AI qualification system to route leads based on specific criteria.
- Example questions:
  - Are you turning 65 soon?
  - Do you currently have Medicare?
  - What state do you live in?
  - Do you have a business needing automation?

### **Automated Routing:**
- **Insurance Leads:** Route to Buckalew Financial Services.
- **Business Automation Leads:** Route to AISetupPros.

---

## Next Steps
1. **Set Up the Pipeline:** Create the stages in GoHighLevel.
2. **Build the Lead Capture Form:** Add the form to your website.
3. **Configure the Chat Widget:** Set up the GoHighLevel chat widget.
4. **Automate Follow-Ups:** Create the SMS/email sequence.
5. **Integrate Calendar:** Set up appointment booking.

---

## Tools and Resources
- **GoHighLevel Dashboard:** [https://app.gohighlevel.com](https://app.gohighlevel.com)
- **Chat Widget Guide:** [GoHighLevel Chat Widget Documentation](https://support.gohighlevel.com/hc/en-us)
- **Automation Guide:** [GoHighLevel Automations Documentation](https://support.gohighlevel.com/hc/en-us)

---

## Notes
- **Proactive:** Atlas will assist in setting up these steps and troubleshooting any issues.
- **Scalable:** This pipeline can be expanded to include more services and automation as needed.
- **Measurable:** Track conversion rates at each stage to optimize performance.

---

## References
- **USER.md:** Larry’s goals for automation and scaling.
- **SOUL.md:** Atlas’s focus on efficiency and actionable systems.