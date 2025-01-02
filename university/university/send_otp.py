import smtplib
import random

# Generate OTP
otp = random.randint(100000, 999999)

# Landlord's email details
landlord_email = "landlord_email@example.com"  # Replace with actual email
subject = "Your OTP for Verification"
message = f"Subject: {subject}\n\nYour OTP is: {otp}"

# Send OTP via Email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login("your_email@example.com", "your_password_or_app_password")  # Use App Password if Gmail
        server.sendmail("your_email@example.com", landlord_email, message)
    print("OTP sent successfully!")
except Exception as e:
    print(f"Error sending OTP: {e}")
