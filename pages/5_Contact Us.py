import streamlit as st
import smtplib
from util import logo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit page config
st.set_page_config(page_title="Contact Us", page_icon="📩")

st.title("Contact Us")

# Sidebar for assessment info
with st.sidebar:
    logo()

# Form to collect user input
with st.form(key="contact_form"):
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    subject = st.text_input("Subject", placeholder="Enter subject")
    message = st.text_area("Message", placeholder="Enter your message here...")

    submit_button = st.form_submit_button("Send Message")

# Function to send email
def send_email(name, email, subject, message):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_app_password"  # Replace with an App Password (not your main password)
    receiver_email = "your_email@gmail.com"  # Replace with the email where you want to receive messages

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"New Contact Form Submission: {subject}"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Handle form submission
if submit_button:
    if name and email and subject and message:
        success = send_email(name, email, subject, message)
        if success:
            st.success("✅ Your message has been sent successfully!")
        else:
            st.error("❌ Failed to send message. Please try again later.")
    else:
        st.warning("⚠️ Please fill out all fields before submitting.")
